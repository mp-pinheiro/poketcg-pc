#include "runtime.h"

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

#include <pthread.h>
#include <setjmp.h>
#include <stdint.h>
#include <string.h>
#define AUDIO_SAMPLES_PER_FRAME 1470u


static RuntimeStateDumpCb g_state_dump_callback;
static const uint32_t *g_state_dump_frames;
static size_t g_state_dump_frame_count;

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

static void *run_game(void *context)
{
	RuntimeState *state = context;

	runtime_events_reset();
	runtime_mark_event(RUNTIME_EVENT_BOOT_STARTED);
	poketcg_request_boot_restart = boot_restart_trampoline;
	if (setjmp(g_boot_restart_env) == 0) {
		Start(0x11u);
	} else {
		/* Soft reset: WRAM survives, boot re-enters with the original A. */
		runtime_mark_event(RUNTIME_EVENT_BOOT_STARTED);
		Start(wInitialA);
	}
	GameLoop();
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
	if (pthread_mutex_init(&state.lock, NULL) != 0)
		return -1;
	if (pthread_cond_init(&state.condition, NULL) != 0) {
		pthread_mutex_destroy(&state.lock);
		return -1;
	}
	ppu_init_offsets(&state.ppu);
	frame_boundary_install(boundary, &state);
	pthread_t worker;
	if (pthread_create(&worker, NULL, run_game, &state) != 0) {
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
		if (state.button_count)
			input.buttons = state.buttons[state.frames % state.button_count];
		g_keys = shell_hkeys_from_input(input.buttons);
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
		shell_present(shell, state.framebuffer);
		shell_queue_audio(shell, state.audio, pcm_count);
		if (g_state_dump_callback) {
			for (size_t i = 0; i < g_state_dump_frame_count; i++) {
				if (state.frames != g_state_dump_frames[i])
					continue;
				RuntimeResult dump;
				dump.frame_limit = frame_limit;
				dump.frames = state.frames;
				dump.event_mask = runtime_event_mask();
				dump.event_count = runtime_event_count();
				dump.terminal_event = runtime_terminal_event();
				dump.stopped_by_user = state.stopped_by_user;
				memcpy(dump.framebuffer, state.framebuffer,
				       sizeof dump.framebuffer);
				g_state_dump_callback(state.frames, &dump);
				break;
			}
		}

		pthread_mutex_lock(&state.lock);
		if (state.frame_limit && state.frames >= state.frame_limit)
			state.stop = 1;
		state.resume = 1;
		pthread_cond_broadcast(&state.condition);
		pthread_mutex_unlock(&state.lock);
	}
	pthread_join(worker, NULL);
	frame_boundary_install(NULL, NULL);
	if (result) {
		result->frame_limit = frame_limit;
		result->frames = state.frames;
		result->event_mask = runtime_event_mask();
		result->event_count = runtime_event_count();
		result->terminal_event = runtime_terminal_event();
		result->stopped_by_user = state.stopped_by_user;
		memcpy(result->framebuffer, state.framebuffer, sizeof state.framebuffer);
	}
	pthread_cond_destroy(&state.condition);
	pthread_mutex_destroy(&state.lock);
	return 0;
}

int runtime_run(Shell *shell, uint32_t frame_limit, RuntimeResult *result)
{
	return runtime_run_with_input(shell, frame_limit, NULL, 0, result);
}
