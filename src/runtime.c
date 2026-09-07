#include "runtime.h"

#include "bank_guard.h"
#include "generated/wram.h"
#include "home/frames.h"
#include "home/game_loop.h"
#include "home/input.h"
#include "home/time.h"
#include "home/vblank.h"
#include "home/start.h"
#include "mem.h"
#include "ppu.h"
#include "shell.h"
#include "trace.h"

#include <pthread.h>
#include <setjmp.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#define AUDIO_SAMPLES_PER_FRAME 1470u


static RuntimeStateDumpCb g_state_dump_callback;
static const uint32_t *g_state_dump_frames;
static size_t g_state_dump_frame_count;

static const uint8_t *g_ordinal_buttons;
static size_t g_ordinal_count;
static FILE *g_record_sink;
static RuntimeStateDumpCb g_ordinal_dump_callback;
static const uint32_t *g_ordinal_dump_list;
static size_t g_ordinal_dump_count;
static uint32_t g_stop_ordinal;

void runtime_set_ordinal_input(const uint8_t *buttons, size_t count)
{
	g_ordinal_buttons = buttons;
	g_ordinal_count = count;
}

void runtime_set_record_input(FILE *sink)
{
	g_record_sink = sink;
}

void runtime_set_state_dump_ordinals(
	RuntimeStateDumpCb callback, const uint32_t *ordinals, size_t count)
{
	g_ordinal_dump_callback = callback;
	g_ordinal_dump_list = ordinals;
	g_ordinal_dump_count = count;
}

void runtime_set_stop_ordinal(uint32_t ordinal)
{
	g_stop_ordinal = ordinal;
}

typedef struct {
	pthread_mutex_t lock;
	pthread_cond_t condition;
	Shell *shell;
	Ppu ppu;
	uint16_t framebuffer[SCREEN_W * SCREEN_H];
	int16_t audio[AUDIO_SAMPLES_PER_FRAME];
	const uint8_t *buttons;
	size_t button_count;
	uint32_t frame_limit;
	uint32_t frames;
	uint32_t timer_cycles;
	int frame_ready;
	int resume;
	int stop;
	int stopped_by_user;
	int worker_done;
} RuntimeState;

static void boundary(void *context)
{
	RuntimeState *state = context;
	int stop;
	pthread_mutex_lock(&state->lock);
	state->frame_ready = 1;
	pthread_cond_broadcast(&state->condition);
	while (!state->resume && !state->stop)
		pthread_cond_wait(&state->condition, &state->lock);
	stop = state->stop;
	state->resume = 0;
	if (stop) {
		state->worker_done = 1;
		pthread_cond_broadcast(&state->condition);
	}
	pthread_mutex_unlock(&state->lock);
	if (stop)
		pthread_exit(NULL);
}

static int stopped(RuntimeState *state)
{
	int stop;
	pthread_mutex_lock(&state->lock);
	stop = state->stop;
	pthread_mutex_unlock(&state->lock);
	return stop;
}

static jmp_buf g_boot_restart_env;

static void boot_restart_trampoline(void)
{
	longjmp(g_boot_restart_env, 1);
}

static int g_skip_boot;

void runtime_skip_boot(int enable)
{
	g_skip_boot = enable;
}

static void *run_game(void *context)
{
	RuntimeState *state = context;

	runtime_events_reset();
	if (!g_skip_boot) {
		runtime_mark_event(RUNTIME_EVENT_BOOT_STARTED);
		poketcg_request_boot_restart = boot_restart_trampoline;
		if (setjmp(g_boot_restart_env) == 0) {
			Start(0x11u);
		} else {
			/* Soft reset: WRAM survives, boot re-enters with the original A.
			 * The longjmp skipped every pending exit hook. */
			bank_guard_reset();
			runtime_mark_event(RUNTIME_EVENT_BOOT_STARTED);
			Start(wInitialA);
		}
		GameLoop();
	}
	for (;;) {
		DoFrame();
		if (stopped(state))
			break;
	}
	pthread_mutex_lock(&state->lock);
	state->worker_done = 1;
	pthread_cond_broadcast(&state->condition);
	pthread_mutex_unlock(&state->lock);
	return NULL;
}

void runtime_set_state_dump_frames(
	RuntimeStateDumpCb callback, const uint32_t *frames, size_t frame_count)
{
	g_state_dump_callback = callback;
	g_state_dump_frames = frames;
	g_state_dump_frame_count = frame_count;
}

static void fill_result(const RuntimeState *state, uint32_t frame_limit,
                        RuntimeResult *out)
{
	out->frame_limit = frame_limit;
	out->frames = state->frames;
	out->event_mask = runtime_event_mask();
	out->event_count = runtime_event_count();
	out->terminal_event = runtime_terminal_event();
	out->stopped_by_user = state->stopped_by_user;
	memcpy(out->framebuffer, state->framebuffer, sizeof out->framebuffer);
}

/* Game-thread hook at the DoFrame anchor (frames.c, the $0552 analogue). The
 * host set resume as the last act of its pass and is parked on frame_ready, so
 * g_keys and the framebuffer are stable here. */
static void anchor(void *context)
{
	RuntimeState *state = context;
	uint32_t ordinal = frame_boundary_doframe_ordinal();

	if (g_record_sink) {
		/* g_keys is hKeysHeld order; the timeline file is InputFrame order. */
		fprintf(g_record_sink, "%u\n",
		        (unsigned)shell_hkeys_from_input(g_keys));
		if ((ordinal & 0xFFu) == 0u)
			fflush(g_record_sink);
	}
	if (!g_ordinal_dump_callback)
		return;
	for (size_t i = 0; i < g_ordinal_dump_count; i++) {
		if (ordinal != g_ordinal_dump_list[i])
			continue;
		RuntimeResult dump;
		fill_result(state, state->frame_limit, &dump);
		g_ordinal_dump_callback(ordinal, &dump);
		break;
	}
}

int runtime_run_with_input(
	Shell *shell, uint32_t frame_limit, const uint8_t *buttons,
	size_t button_count, RuntimeResult *result)
{
	RuntimeState state;
	memset(&state, 0, sizeof state);
	state.shell = shell;
	state.buttons = buttons;
	state.button_count = button_count;
	state.frame_limit = frame_limit;
	if (button_count)
		g_keys = shell_hkeys_from_input(buttons[0]);
	else if (g_ordinal_count)
		g_keys = shell_hkeys_from_input(g_ordinal_buttons[0]);
	if (pthread_mutex_init(&state.lock, NULL) != 0)
		return -1;
	if (pthread_cond_init(&state.condition, NULL) != 0) {
		pthread_mutex_destroy(&state.lock);
		return -1;
	}
	ppu_init_offsets(&state.ppu);
	/* The ordinal axis is monotone across a soft reset, exactly as the
	 * reference keeps counting $0552 hits through `jp Start`; it restarts
	 * only with the process. */
	frame_boundary_reset_ordinal();
	frame_boundary_install(boundary, &state);
	frame_boundary_install_anchor(anchor, &state);
	pthread_t worker;
	if (pthread_create(&worker, NULL, run_game, &state) != 0) {
		frame_boundary_install_anchor(NULL, NULL);
		frame_boundary_install(NULL, NULL);
		pthread_cond_destroy(&state.condition);
		pthread_mutex_destroy(&state.lock);
		return -1;
	}
	for (;;) {
		pthread_mutex_lock(&state.lock);
		while (!state.frame_ready && !state.worker_done)
			pthread_cond_wait(&state.condition, &state.lock);
		if (state.worker_done && !state.frame_ready) {
			pthread_mutex_unlock(&state.lock);
			break;
		}
		state.frame_ready = 0;
		pthread_mutex_unlock(&state.lock);

		InputFrame input = {0};
		if (!shell_pump(shell, &input)) {
			pthread_mutex_lock(&state.lock);
			state.stop = 1;
			state.stopped_by_user = 1;
			state.resume = 1;
			pthread_cond_broadcast(&state.condition);
			pthread_mutex_unlock(&state.lock);
			continue;
		}
		state.frames++;
		trace_set_frame(state.frames);
		if (state.button_count)
			/* gb-recompiled applies the scripted mask at scanout but
			 * the emulated joypad reads it back one scanout later
			 * (measured on the boot timeline: the reference sights
			 * every press edge exactly one game-loop iteration after
			 * the script frame -- title A@f1000 exits its loop at
			 * wvbc+2, not +1; the menu A@f1101 and the naming
			 * S@f1200/A@f1201 confirmations shift by the same one
			 * iteration). Index the previous entry so a press lands
			 * on the same loop iteration on both lanes. */
			input.buttons = state.buttons[(state.frames - 1u)
			                              % state.button_count];
		g_keys = shell_hkeys_from_input(input.buttons);
		if (frame_boundary_take_service_pass()) {
			/* Mid-processing VBlank service: ISR-equivalent work only.
			 * No input re-sample, no frame counter, no timer/clock
			 * aging, no render -- the game made no DoFrame progress. */
			RuntimeVBlankHandler();
			pthread_mutex_lock(&state.lock);
			state.resume = 1;
			pthread_cond_broadcast(&state.condition);
			pthread_mutex_unlock(&state.lock);
			continue;
		}
		/* DoFrame-ordinal timeline: the ordinal counter is the number of
		 * completed DoFrames, so entry [ordinal] is what the DoFrame this
		 * pass belongs to will read -- the same index refstream.Core
		 * serves at its anchor. Past the end, the shell's input stands. */
		uint32_t ordinal = frame_boundary_doframe_ordinal();
		int timeline_live = g_ordinal_buttons && ordinal < g_ordinal_count;
		if (timeline_live) {
			input.buttons = g_ordinal_buttons[ordinal];
			g_keys = shell_hkeys_from_input(input.buttons);
		}
		/* CGB hardware clock aging (Lane D model in mem.c): DIV free-runs
		 * at the double-speed rate; TIMA ticks every 256 fast cycles and
		 * reloads from TMA. One frame of slow cycles per host frame. */
		mem_advance_hardware_clock(70224u);
		/* Hardware timer cadence: SetupTimer programs TAC=$07
		 * (TAC_16KHZ: 16384 Hz, a 256-cycle tick) with TMA=-68
		 * ($BC), so TimerHandler fires every 256*68 = 17408 cycles
		 * — 240.93 Hz, 70224/17408 ≈ 4.03 per frame. The interrupt
		 * layer is batched at the frame boundary in this port. */
		state.timer_cycles += 70224u;
		while (state.timer_cycles >= 17408u) {
			TimerHandler();
			state.timer_cycles -= 17408u;
		}
		/* Halt-return VBlank work (OAM DMA, scroll/window/LCDC flush,
		 * VBlank function, palette flush), so the PPU sample below and
		 * the next frame's game code see it, like the ROM's ISR. */
		RuntimeVBlankHandler();
		apu_trace_set_tick(state.frames);
		size_t pcm_count = apu_trace_render_pcm(
			state.audio, AUDIO_SAMPLES_PER_FRAME);
		ppu_render_frame(&state.ppu, state.framebuffer);
		/* A recorded prefix replays at full speed; only live play is paced. */
		if (!timeline_live)
			shell_pace(shell);
		shell_present(shell, state.framebuffer);
		shell_queue_audio(shell, state.audio, pcm_count);
		if (g_state_dump_callback) {
			for (size_t i = 0; i < g_state_dump_frame_count; i++) {
				if (state.frames != g_state_dump_frames[i])
					continue;
				RuntimeResult dump;
				fill_result(&state, frame_limit, &dump);
				g_state_dump_callback(state.frames, &dump);
				break;
			}
		}

		pthread_mutex_lock(&state.lock);
		if (state.frame_limit && state.frames >= state.frame_limit)
			state.stop = 1;
		if (g_stop_ordinal && ordinal >= g_stop_ordinal)
			state.stop = 1;
		state.resume = 1;
		pthread_cond_broadcast(&state.condition);
		pthread_mutex_unlock(&state.lock);
	}
	pthread_join(worker, NULL);
	frame_boundary_install_anchor(NULL, NULL);
	frame_boundary_install(NULL, NULL);
	if (g_record_sink)
		fflush(g_record_sink);
	if (result)
		fill_result(&state, frame_limit, result);
	pthread_cond_destroy(&state.condition);
	pthread_mutex_destroy(&state.lock);
	return 0;
}

int runtime_run(Shell *shell, uint32_t frame_limit, RuntimeResult *result)
{
	return runtime_run_with_input(shell, frame_limit, NULL, 0, result);
}
