#include "runtime.h"
#include "isr.h"
#include "serial_track.h"
#include "widescreen.h"
#include "link.h"

#include "bank_guard.h"
#include "digest.h"
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
#include "apu.h"
#include "trace.h"
#ifdef POKETCG_DEBUG_MENU
#include "persistence.h"
#include "state_dump.h"
#include "generated/hram.h"
#include "generated/sram.h"
#include "home/duel.h"
#include "home/scripting.h"
#include "home/switch_sram.h"
#include "debug_cheats.h"
#endif

#include <pthread.h>
#include <setjmp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
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
static const RuntimePoke *g_pokes;
static size_t g_poke_count;
static size_t g_poke_next;
static const LagTrack *g_lag;
/* Timer-ISR schedule progress within the current DoFrame interval. */
static struct {
	uint32_t ordinal;
	uint32_t call;
	uint16_t delivered;
} g_schedule;
static uint32_t g_schedule_mismatches;
static uint32_t g_first_mismatch = UINT32_MAX;

void runtime_set_lag_track(const LagTrack *track)
{
	g_lag = track && track->count ? track : NULL;
	runtime_serial_track(g_lag ? g_lag->serial : NULL, g_lag ? g_lag->count : 0);
	runtime_stack_track(g_lag ? g_lag->stack_start : NULL, g_lag ? g_lag->stack_address : NULL,
	                    g_lag ? g_lag->count : 0);
	memset(&g_schedule, 0, sizeof g_schedule);
	if (g_lag) {
		g_schedule_mismatches = 0;
		g_first_mismatch = UINT32_MAX;
	}
	frame_boundary_services_from_track(g_lag != NULL);
}

uint32_t runtime_lag_schedule_mismatches(void)
{
	return g_schedule_mismatches;
}

uint32_t runtime_lag_first_mismatch(void)
{
	return g_first_mismatch;
}

static void schedule_mismatch(void)
{
	if (g_first_mismatch == UINT32_MAX)
		g_first_mismatch = frame_boundary_doframe_ordinal();
	g_schedule_mismatches++;
}

/* One VBlank ISR: the halt-return work (vblank.asm:2-46) and the counter it
 * keeps (vblank.asm:35). Every increment of wVBlankCounter under a host goes
 * through here, so the count per ordinal is exactly the services delivered. */
static unsigned stat_count(uint32_t interval, unsigned index)
{
	unsigned segment = index < 7u ? index : 7u;
	if (!g_lag || interval >= g_lag->count)
		return 1u;
	if (!((g_lag->stat_masks[interval] >> segment) & 1u))
		return 0u;
	size_t lo = 0, hi = g_lag->repeats;
	while (lo < hi) {
		size_t mid = lo + (hi - lo) / 2u;
		if (g_lag->repeat_interval[mid] < interval)
			lo = mid + 1u;
		else
			hi = mid;
	}
	for (; lo < g_lag->repeats && g_lag->repeat_interval[lo] == interval; lo++)
		if (g_lag->repeat_segment[lo] == segment)
			return g_lag->repeat_count[lo];
	return 1u;
}

static struct {
	uint32_t interval;
	unsigned delivered;
} g_stats = {UINT32_MAX, 0};

static void stat_deliver_to(uint32_t interval, unsigned target)
{
	if (g_stats.interval != interval) {
		g_stats.interval = interval;
		g_stats.delivered = 0;
	}
	while (g_stats.delivered < target) {
		isr_context_enter();
		RuntimeLCDCHandlerOnce();
		isr_context_leave();
		g_stats.delivered++;
	}
}

static void stat_service(uint32_t interval, unsigned index)
{
	if (g_lag && g_lag->exact_stats) {
		unsigned last = index < 7u ? index : 7u;
		unsigned target = 0;
		for (unsigned segment = 0; segment <= last; segment++)
			target += stat_count(interval, segment);
		stat_deliver_to(interval, target);
	} else if (stat_count(interval, index)) {
		isr_context_enter();
		RuntimeLCDCHandler();
		isr_context_leave();
	}
}

static void vblank_service(uint32_t interval, unsigned index)
{
	isr_context_enter();
	stat_service(interval, index);
	RuntimeVBlankHandler();
	gb_write8(wVBlankCounter_ADDR, (uint8_t)(gb_read8(wVBlankCounter_ADDR) + 1u));
	isr_context_leave();
}

static void schedule_sync(uint32_t ordinal)
{
	if (g_schedule.ordinal == ordinal)
		return;
	g_schedule.ordinal = ordinal;
	g_schedule.call = g_lag->call_start[ordinal];
	g_schedule.delivered = 0;
}

static void schedule_deliver(uint32_t ordinal, uint16_t target)
{
	if (target > g_lag->ticks[ordinal])
		target = g_lag->ticks[ordinal];
	while (g_schedule.delivered < target) {
		apu_trace_note_timer_tick();
		isr_context_enter();
		TimerHandler();
		isr_context_leave();
		g_schedule.delivered++;
	}
}

/* Game-thread hook at every timer sync point (home/frames.h): the interval's
 * timer ISRs that preceded this call on the ROM run now. */
static void timer_sync(void *context)
{
	(void)context;
	uint32_t ordinal = frame_boundary_doframe_ordinal();
	if (!g_lag || ordinal >= g_lag->count)
		return;
	schedule_sync(ordinal);
	if (g_schedule.call < g_lag->call_start[ordinal + 1])
		schedule_deliver(ordinal, g_lag->call_ticks[g_schedule.call++]);
	else
		schedule_mismatch();
}

/* Game-thread hook for a ROM loop that polls the sound driver without a
 * DoFrame (promotional_card.asm .loop): the ROM's ISRs keep running while it
 * spins. Replaying a track, the recorded timer schedule is those ISRs and the
 * loop's own sync points deliver them; once the interval's recorded polls are
 * spent, its remaining ticks run so a diverged replay still ends the wait.
 * Live, one pass lets a frame of hardware time go by. */
static void busy_wait(void *context)
{
	(void)context;
	uint32_t ordinal = frame_boundary_doframe_ordinal();
	if (g_lag && ordinal < g_lag->count) {
		schedule_sync(ordinal);
		if (g_schedule.call < g_lag->call_start[ordinal + 1])
			return;
		if (g_schedule.delivered < g_lag->ticks[ordinal]) {
			schedule_deliver(ordinal, g_lag->ticks[ordinal]);
			return;
		}
		schedule_mismatch();
		apu_trace_note_timer_tick();
		isr_context_enter();
		TimerHandler();
		isr_context_leave();
		return;
	}
	frame_boundary_reach();
}

/* The interval just ended at this anchor: its remaining timer ISRs run
 * before the state is digested. */
static void schedule_close(uint32_t ordinal)
{
	if (!g_lag || ordinal >= g_lag->count)
		return;
	schedule_sync(ordinal);
	schedule_deliver(ordinal, g_lag->ticks[ordinal]);
	if (g_schedule.call != g_lag->call_start[ordinal + 1])
		schedule_mismatch();
}

static void age_cycles(uint32_t *timer_cycles, uint32_t cycles)
{
	/* CGB hardware clock aging (Lane D model in mem.c): DIV free-runs at
	 * the double-speed rate; TIMA ticks every 256 fast cycles and reloads
	 * from TMA. Hardware timer cadence: SetupTimer programs TAC=$07
	 * (TAC_16KHZ: 16384 Hz, a 256-cycle tick) with TMA=-68 ($BC), so
	 * TimerHandler fires every 256*68 = 17408 cycles -- 240.93 Hz,
	 * 70224/17408 ~ 4.03 per frame. The interrupt layer is batched at the
	 * frame boundary in this port. */
	mem_advance_hardware_clock(cycles);
	*timer_cycles += cycles;
	while (*timer_cycles >= 17408u) {
		apu_trace_note_timer_tick();
		isr_context_enter();
		TimerHandler();
		isr_context_leave();
		*timer_cycles -= 17408u;
	}
}

void runtime_set_ordinal_input(const uint8_t *buttons, size_t count)
{
	g_ordinal_buttons = buttons;
	g_ordinal_count = count;
}

void runtime_set_record_input(FILE *sink)
{
	g_record_sink = sink;
}

static FILE *g_pcm_sink;

void runtime_set_pcm_sink(FILE *sink)
{
	g_pcm_sink = sink;
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

void runtime_set_pokes(const RuntimePoke *pokes, size_t count)
{
	g_pokes = pokes;
	g_poke_count = count;
	g_poke_next = 0;
}

static const RuntimeOverread *g_overreads;
static size_t g_overread_count;
static size_t g_overread_next;
static uint32_t g_overread_mismatches;

void runtime_set_overreads(const RuntimeOverread *list, size_t count)
{
	g_overreads = list;
	g_overread_count = count;
	g_overread_next = 0;
	g_overread_mismatches = 0;
}

static int overread_hook(void *context, uint32_t interval, uint8_t *out, size_t length)
{
	(void)context;
	return runtime_overread_tail(interval, out, length);
}

int runtime_overread_tail(uint32_t interval, uint8_t *out, size_t length)
{
	if (!g_overreads || g_overread_next >= g_overread_count)
		return 0;
	const RuntimeOverread *entry = &g_overreads[g_overread_next++];
	if (entry->interval != interval || entry->length != length) {
		g_overread_mismatches++;
		return 0;
	}
	memcpy(out, entry->tail, length);
	return 1;
}

uint32_t runtime_overread_mismatches(void)
{
	return g_overread_mismatches;
}

typedef struct {
	pthread_mutex_t lock;
	pthread_cond_t condition;
	Shell *shell;
	Ppu ppu;
	uint16_t framebuffer[SCREEN_W * SCREEN_H];
	uint16_t present[(SCREEN_W + 2 * WIDE_EXTRA_MAX) * SCREEN_H];
	WidescreenRect present_rect;
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
	int handed_over;
	uint32_t aged_ordinal;
	uint16_t services; /* VBlank services delivered in the current ordinal */
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

static int g_present_extra;
static int g_present_limit = PPU_SPRITES_PER_LINE;

void runtime_set_presentation(int extra, int sprite_limit)
{
	g_present_extra = extra < 0 ? 0 : extra > WIDE_EXTRA_MAX ? WIDE_EXTRA_MAX : extra;
	g_present_limit = sprite_limit;
}

static int presentation_on(void)
{
	return g_present_extra > 0 || g_present_limit != PPU_SPRITES_PER_LINE;
}

static void present_frame(RuntimeState *state)
{
	ppu_render_span(&state->ppu, state->present, g_present_extra, g_present_extra, g_present_limit);
	state->present_rect = widescreen_apply_viewport(state->present, g_present_extra);
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
	out->present_width = presentation_on() ? SCREEN_W + 2 * g_present_extra : 0;
	if (out->present_width) {
		memcpy(out->present, state->present, sizeof out->present);
		out->present_x0 = state->present_rect.x0;
		out->present_x1 = state->present_rect.x1;
		out->present_room = state->present_rect.room;
	}
}
#ifdef POKETCG_DEBUG_MENU
typedef struct {
	int active;
	int page;
	int infinite_energy;
	int opponent_control;
	size_t selected;
	unsigned steps;
	unsigned speed;
	char save_path[512];
	char state_path[512];
} DebugMenu;

static const char *const debug_main_items[] = {
	"RESUME", "AUTO WIN", "STEP 1", "STEP 10",
	"STEP 60", "SPEED 1X", "SPEED 2X", "SPEED 4X",
	"SPEED MAX", "SAVE SRAM", "LOAD SRAM", "DUMP STATE", "CHEATS >"
};

static const char *const debug_cheat_items[] = {
	"BACK", "COIN HEADS", "COIN TAILS", "COIN RANDOM",
	"INF ENERGY", "RUN FULL HP", "RUN KO OPP", "RUN REFILL HAND",
	"RUN ALL CARDS", "RUN ALL MEDALS", "OPP CONTROL"
};

static void debug_menu_init(DebugMenu *menu)
{
	const char *dir = getenv("POKETCG_DEBUG_DIR");
	if (!dir || !*dir)
		dir = ".";
	menu->speed = 1u;
	menu->page = 0;
	menu->infinite_energy = 0;
	menu->opponent_control = 0;
	debug_cheats_set_coin_mode(DEBUG_COIN_RANDOM);
	snprintf(menu->save_path, sizeof menu->save_path, "%s/poketcg-debug.sav", dir);
	snprintf(menu->state_path, sizeof menu->state_path, "%s/poketcg-debug-state.json", dir);
}

static const char *debug_speed_name(unsigned speed)
{
	if (speed == 1u)
		return "1X";
	if (speed == 2u)
		return "2X";
	if (speed == 4u)
		return "4X";
	return "MAX";
}

#define DEBUG_DUELVARS_ARENA_CARD 0xBBu
#define DEBUG_DUELVARS_ARENA_CARD_HP 0xC8u
#define DEBUG_DUELVARS_HAND 0x42u
#define DEBUG_DUELVARS_HAND_COUNT 0xEEu
#define DEBUG_DUELVARS_NOT_IN_DECK 0xBAu
#define DEBUG_DUELVARS_DECK_CARDS 0x7Eu
#define DEBUG_DECK_SIZE 60u
#define DEBUG_CARD_LOCATION_DECK 0x00u
#define DEBUG_PLAYER_TURN ((uint8_t)(wPlayerDuelVariables_ADDR >> 8))
#define DEBUG_OPPONENT_TURN ((uint8_t)(wOpponentDuelVariables_ADDR >> 8))

static const char *const *debug_item_list(const DebugMenu *menu)
{
	return menu->page ? debug_cheat_items : debug_main_items;
}

static size_t debug_item_count(const DebugMenu *menu)
{
	return menu->page
		? sizeof debug_cheat_items / sizeof debug_cheat_items[0]
		: sizeof debug_main_items / sizeof debug_main_items[0];
}

static void debug_set_hp(uint8_t page, int zero)
{
	uint8_t saved_turn = hWhoseTurn;
	hWhoseTurn = page;
	for (uint8_t slot = 0; slot < 6u; slot++) {
		DuelistVarResult card = GetTurnDuelistVariable(
			(uint8_t)(DEBUG_DUELVARS_ARENA_CARD + slot));
		if (card.a == 0xFFu)
			continue;
		DuelistVarResult hp = GetTurnDuelistVariable(
			(uint8_t)(DEBUG_DUELVARS_ARENA_CARD_HP + slot));
		uint8_t value = zero ? 0u : GetCardDamageAndMaxHP(slot).c;
		gb_write8(hp.hl, value);
	}
	hWhoseTurn = saved_turn;
}

static void debug_refill_hand(void)
{
	uint8_t saved_turn = hWhoseTurn;
	hWhoseTurn = DEBUG_PLAYER_TURN;
	for (uint8_t guard = 0; guard < DEBUG_DECK_SIZE; guard++) {
		uint8_t count = GetTurnDuelistVariable(DEBUG_DUELVARS_HAND_COUNT).a;
		uint8_t not_in_deck = GetTurnDuelistVariable(
			DEBUG_DUELVARS_NOT_IN_DECK).a;
		if (count >= 7u || not_in_deck >= DEBUG_DECK_SIZE)
			break;
		DuelistVarResult deck = GetTurnDuelistVariable(DEBUG_DUELVARS_DECK_CARDS);
		uint8_t card = gb_read8((uint16_t)(deck.hl + not_in_deck));
		SearchCardInDeckAndAddToHand(card);
		AddCardToHand(card);
	}
	hWhoseTurn = saved_turn;
}

static void debug_unlock_cards(void)
{
	uint8_t saved_bank = hBankSRAM;
	BankswitchSRAM(0u);
	EnableSRAM();
	for (uint16_t card = 0; card < 0xE4u; card++)
		gb_write8((uint16_t)(sCardCollection_ADDR + card), 99u);
	DisableSRAM();
	BankswitchSRAM(saved_bank);
}

static void debug_unlock_medals(void)
{
	for (uint8_t event = 0x08u; event <= 0x0Fu; event++)
		(void)MaxOutEventValue(event, 0u, 0u, 0u);
	(void)MaxOutEventValue(0x2Eu, 0u, 0u, 0u);
	wMedalCount = 8u;
	uint8_t saved_bank = hBankSRAM;
	BankswitchSRAM(0u);
	EnableSRAM();
	gb_write8(sMedalCount_ADDR, 8u);
	DisableSRAM();
	BankswitchSRAM(saved_bank);
}

static void debug_menu_apply(const DebugMenu *menu)
{
	if (menu->infinite_energy)
		wAlreadyPlayedEnergy = 0u;
	if (menu->opponent_control)
		wOpponentDuelistType = 0u;
}
static int debug_cheat_active(const DebugMenu *menu, size_t index)
{
	if (!menu->page)
		return -1;
	switch (index) {
	case 1:
		return debug_cheats_coin_mode() == DEBUG_COIN_HEADS;
	case 2:
		return debug_cheats_coin_mode() == DEBUG_COIN_TAILS;
	case 3:
		return debug_cheats_coin_mode() == DEBUG_COIN_RANDOM;
	case 4:
		return menu->infinite_energy;
	case 10:
		return menu->opponent_control;
	default:
		return -1;
	}
}

static int debug_menu_loop(Shell *shell, RuntimeState *state, uint32_t frame_limit,
                           DebugMenu *menu)
{
	for (;;) {
		char status[96];
		char item_lines[13][32];
		const char *lines[14];
		const char *const *items = debug_item_list(menu);
		size_t item_count = debug_item_count(menu);
		snprintf(status, sizeof status, "ORD %u SPD %s",
		         (unsigned)frame_boundary_doframe_ordinal(),
		         debug_speed_name(menu->speed));
		lines[0] = status;
		for (size_t i = 0; i < item_count; i++) {
			int active = debug_cheat_active(menu, i);
			if (active >= 0) {
				snprintf(item_lines[i], sizeof item_lines[i], "%s %s",
				         active ? "[X]" : "[ ]", items[i]);
				lines[i + 1] = item_lines[i];
			} else {
				lines[i + 1] = items[i];
			}
		}
		ShellDebugView view = {
			.title = menu->page ? "DEBUG CHEATS" : "DEBUG MENU",
			.lines = lines,
			.line_count = item_count + 1u,
			.selected = menu->selected + 1u,
		};
		shell_present_debug(shell, state->framebuffer, &view);
		shell_pace(shell);
		ShellInput input = {0};
		if (!shell_pump(shell, &input))
			return -1;
		if (input.debug_toggle) {
			menu->active = 0;
			return 0;
		}
		if (input.pressed & BTN_B) {
			if (menu->page) {
				menu->page = 0;
				menu->selected = sizeof debug_main_items / sizeof debug_main_items[0] - 1u;
				continue;
			}
			menu->active = 0;
			return 0;
		}
		if (input.pressed & BTN_UP) {
			menu->selected = menu->selected == 0u
				? item_count - 1u
				: menu->selected - 1u;
			continue;
		}
		if (input.pressed & BTN_DOWN) {
			menu->selected = (menu->selected + 1u) % item_count;
			continue;
		}
		if (!(input.pressed & BTN_A))
			continue;
		if (!menu->page) {
			switch (menu->selected) {
			case 0:
				menu->active = 0;
				return 0;
			case 1:
				gb_write8(wDuelFinished_ADDR, 1u);
				break;
			case 2:
				menu->steps = 1u;
				return 1;
			case 3:
				menu->steps = 10u;
				return 1;
			case 4:
				menu->steps = 60u;
				return 1;
			case 5:
				menu->speed = 1u;
				shell_set_speed(shell, menu->speed);
				break;
			case 6:
				menu->speed = 2u;
				shell_set_speed(shell, menu->speed);
				break;
			case 7:
				menu->speed = 4u;
				shell_set_speed(shell, menu->speed);
				break;
			case 8:
				menu->speed = 0u;
				shell_set_speed(shell, menu->speed);
				break;
			case 9:
				(void)sram_save_atomic(menu->save_path);
				break;
			case 10:
				(void)sram_load(menu->save_path);
				break;
			case 11: {
				RuntimeResult result;
				fill_result(state, frame_limit, &result);
				(void)runtime_write_state(menu->state_path, &result);
				break;
			}
			case 12:
				menu->page = 1;
				menu->selected = 0u;
				break;
			}
			continue;
		}
		switch (menu->selected) {
		case 0:
			menu->page = 0;
			menu->selected = sizeof debug_main_items / sizeof debug_main_items[0] - 1u;
			break;
		case 1:
			debug_cheats_set_coin_mode(DEBUG_COIN_HEADS);
			break;
		case 2:
			debug_cheats_set_coin_mode(DEBUG_COIN_TAILS);
			break;
		case 3:
			debug_cheats_set_coin_mode(DEBUG_COIN_RANDOM);
			break;
		case 4:
			menu->infinite_energy = !menu->infinite_energy;
			break;
		case 5:
			debug_set_hp(DEBUG_PLAYER_TURN, 0);
			break;
		case 6:
			debug_set_hp(DEBUG_OPPONENT_TURN, 1);
			break;
		case 7:
			debug_refill_hand();
			break;
		case 8:
			debug_unlock_cards();
			break;
		case 9:
			debug_unlock_medals();
			break;
		case 10:
			menu->opponent_control = !menu->opponent_control;
			if (menu->opponent_control)
				wOpponentDuelistType = 0u;
			else
				wOpponentDuelistType = (uint8_t)(wOpponentDeckID | 0x80u);
			break;
		}
	}
}
#endif

/* VBlank ISRs the ROM saw before each of the game's own writes to
 * wVBlankCounter (runtime.h write_start/write_vblanks). Delivered on the game
 * thread at the same writes (frame_boundary_vblank_sync); the interval's
 * remainder runs at its end, before the DoFrame's own service. */
static struct {
	uint32_t ordinal;
	uint32_t write;
} g_vschedule = {UINT32_MAX, 0};

static void vschedule_sync(uint32_t ordinal)
{
	if (g_vschedule.ordinal == ordinal)
		return;
	g_vschedule.ordinal = ordinal;
	g_vschedule.write = g_lag->write_start[ordinal];
}

static RuntimeState *g_isr_state;

static void isr_deliver(uint32_t interval, unsigned kind, unsigned ordinal, uint8_t value)
{
	RuntimeState *state = g_isr_state;
	if (!state || interval != frame_boundary_doframe_ordinal())
		return;
	switch (kind) {
	case ISR_KIND_VBLANK:
		while (state->services < ordinal) {
			vblank_service(interval, state->services);
			state->services++;
		}
		break;
	case ISR_KIND_STAT:
		if (g_lag && g_lag->exact_stats)
			stat_deliver_to(interval, ordinal);
		break;
	case ISR_KIND_SERIAL:
		link_replay_serial(value);
		break;
	case ISR_KIND_TIMER:
		if (g_lag && interval < g_lag->count) {
			schedule_sync(interval);
			schedule_deliver(interval, (uint16_t)ordinal);
		}
		break;
	default:
		break;
	}
}

void runtime_set_isr_track(const IsrTrack *track)
{
	isr_set_track(track, isr_deliver);
}

static void vblank_sync(void *context)
{
	RuntimeState *state = context;
	uint32_t ordinal = frame_boundary_doframe_ordinal();

	if (!g_lag || ordinal >= g_lag->count)
		return;
	vschedule_sync(ordinal);
	if (g_vschedule.write >= g_lag->write_start[ordinal + 1]) {
		schedule_mismatch();
		return;
	}
	uint16_t target = g_lag->write_vblanks[g_vschedule.write++];
	while (state->services < target) {
		vblank_service(ordinal, state->services);
		state->services++;
	}
}

/* Game-thread hook at the DoFrame anchor (frames.c, the $0552 analogue). The
 * host set resume as the last act of its pass and is parked on frame_ready, so
 * g_keys and the framebuffer are stable here. */
static void anchor(void *context)
{
	RuntimeState *state = context;
	uint32_t ordinal = frame_boundary_doframe_ordinal();

	/* Ordinal k's anchor closes interval k-1 (frames.c increments first). */
	schedule_close(ordinal - 1u);
	if (ordinal >= 1u)
		isr_close_interval();
	if (g_lag && ordinal >= 1u && ordinal - 1u < g_lag->count) {
		/* The ROM's VBlank count for the interval, less what the
		 * boundary passes delivered: nonzero only when the closing
		 * DoFrame ran with the LCD off and had no service of its own. */
		while (state->services < g_lag->vblanks[ordinal - 1u]) {
			vblank_service(ordinal - 1u, state->services);
			state->services++;
		}
		stat_service(ordinal - 1u, state->services);
		if (g_vschedule.ordinal == ordinal - 1u &&
		    g_vschedule.write != g_lag->write_start[ordinal])
			schedule_mismatch();
	}
	/* Interval `ordinal` starts here; its services are counted from zero
	 * and delivered at the game's counter writes (vblank_sync) and at the
	 * interval's end (the host pass below). */
	state->services = 0;
	isr_begin_interval(ordinal);
	serial_track_begin_interval(ordinal);
	/* The reference's anchor digest includes its pokes (refstream.Core._exec
	 * writes before the user callback runs), so poke before the digest. */
	while (g_poke_next < g_poke_count && g_pokes[g_poke_next].ordinal <= ordinal) {
		const RuntimePoke *poke = &g_pokes[g_poke_next++];
		if (poke->ordinal == ordinal)
			gb_write8(poke->address, poke->value);
	}
	if (g_record_sink) {
		/* g_keys is hKeysHeld order; the timeline file is InputFrame order. */
		fprintf(g_record_sink, "%u\n",
		        (unsigned)shell_hkeys_from_input(g_keys));
		if ((ordinal & 0xFFu) == 0u)
			fflush(g_record_sink);
	}
	digest_anchor(ordinal);
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

static int frame_dump_pending(uint32_t frame)
{
	if (!g_state_dump_callback)
		return 0;
	for (size_t i = 0; i < g_state_dump_frame_count; i++)
		if (g_state_dump_frames[i] == frame)
			return 1;
	return 0;
}

static int ordinal_dump_pending(uint32_t ordinal)
{
	if (!g_ordinal_dump_callback)
		return 0;
	for (size_t i = 0; i < g_ordinal_dump_count; i++)
		if (g_ordinal_dump_list[i] == ordinal)
			return 1;
	return 0;
}

int runtime_run_with_input(
	Shell *shell, uint32_t frame_limit, const uint8_t *buttons,
	size_t button_count, RuntimeResult *result)
{
	RuntimeState state;
	memset(&state, 0, sizeof state);
	state.aged_ordinal = UINT32_MAX;
	state.shell = shell;
	state.buttons = buttons;
	state.button_count = button_count;
	state.frame_limit = frame_limit;
#ifdef POKETCG_DEBUG_MENU
	DebugMenu debug_menu = {0};
	debug_menu_init(&debug_menu);
#endif
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
	frame_boundary_install_timer_sync(timer_sync, &state);
	frame_boundary_install_busy_wait(busy_wait, &state);
	g_isr_state = &state;
	frame_boundary_install_vblank_sync(vblank_sync, &state);
	frame_boundary_install_overread(g_overreads ? overread_hook : NULL, NULL);
	pthread_t worker;
	if (pthread_create(&worker, NULL, run_game, &state) != 0) {
		frame_boundary_install_overread(NULL, NULL);
		frame_boundary_install_timer_sync(NULL, NULL);
	frame_boundary_install_busy_wait(NULL, NULL);
		frame_boundary_install_busy_wait(NULL, NULL);
		g_isr_state = NULL;
		frame_boundary_install_vblank_sync(NULL, NULL);
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

		ShellInput host_input = {0};
		if (!shell_pump(shell, &host_input)) {
			pthread_mutex_lock(&state.lock);
			state.stop = 1;
			state.stopped_by_user = 1;
			state.resume = 1;
			pthread_cond_broadcast(&state.condition);
			pthread_mutex_unlock(&state.lock);
			continue;
		}
		shell_sync_options(shell);
		InputFrame input = host_input.game;
#ifdef POKETCG_DEBUG_MENU
		if (host_input.debug_toggle || debug_menu.active) {
			if (host_input.debug_toggle)
				debug_menu.active = 1;
			if (debug_menu.active && debug_menu.steps == 0u) {
				int action = debug_menu_loop(shell, &state, frame_limit, &debug_menu);
				if (action < 0) {
					pthread_mutex_lock(&state.lock);
					state.stop = 1;
					state.stopped_by_user = 1;
					state.resume = 1;
					pthread_cond_broadcast(&state.condition);
					pthread_mutex_unlock(&state.lock);
					continue;
				}
				if (action == 0) {
					pthread_mutex_lock(&state.lock);
					state.resume = 1;
					pthread_cond_broadcast(&state.condition);
					pthread_mutex_unlock(&state.lock);
					continue;
				}
			}
			if (debug_menu.active && debug_menu.steps != 0u) {
				debug_menu.steps--;
				input.buttons = 0u;
			}
		}
#endif
#ifdef POKETCG_DEBUG_MENU
		debug_menu_apply(&debug_menu);
#endif
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
			 * aging, no render -- the game made no DoFrame progress. A
			 * track that counts STAT ISRs delivers them at the segment
			 * boundaries (stat_service), so only the chain model fires here. */
			isr_context_enter();
			if (!(g_lag && g_lag->exact_stats))
				RuntimeLCDCHandler();
			RuntimeVBlankHandler();
			isr_context_leave();
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
		trace_set_ordinal(ordinal);
		int timeline_live = g_ordinal_buttons && ordinal < g_ordinal_count;
		if (timeline_live) {
			input.buttons = g_ordinal_buttons[ordinal];
			g_keys = shell_hkeys_from_input(input.buttons);
			if ((ordinal & 0xFFu) == 0u) {
				char title[64];
				snprintf(title, sizeof title, "poketcg - replaying %u/%u",
				         (unsigned)ordinal, (unsigned)g_ordinal_count);
				shell_set_title(shell, title);
			}
		} else if (g_ordinal_buttons && !state.handed_over) {
			/* The replayed prefix just ended: from here the keyboard is
			 * the input, so take it. */
			state.handed_over = 1;
			shell_set_title(shell, "poketcg - your turn");
			shell_take_focus(shell);
		}
		if (g_lag && ordinal < g_lag->count) {
			/* The ROM's own schedule for this DoFrame: its real time ages
			 * the hardware clock and the extra VBlank services run the
			 * ISR work (vblank.asm:2-46); the timer ISRs are the game
			 * thread's (timer_sync, schedule_close). Once per ordinal:
			 * DisableLCD's rLY poll (src/home/lcd.c) reaches the boundary
			 * without completing a DoFrame and shares its ordinal with
			 * the DoFrame that follows. */
			if (state.aged_ordinal != ordinal) {
				state.aged_ordinal = ordinal;
				mem_advance_hardware_clock(g_lag->cycles[ordinal]);
			}
			/* All but the last service ran while game code was still
			 * working (DisableLCD's own poll included). Those the game
			 * observed before writing the counter were delivered at
			 * the write (vblank_sync); the rest run here, at the
			 * interval's end -- the DoFrame's pass, not DisableLCD's
			 * earlier poll pass. The last is the DoFrame's own below,
			 * or -- when the DoFrame finds the LCD off and waits for
			 * nothing -- the anchor's remainder. */
			if (frame_boundary_pass_is_doframe()) {
				while (state.services + 1u < g_lag->vblanks[ordinal]) {
					vblank_service(ordinal, state.services);
					state.services++;
				}
			}
		} else {
			age_cycles(&state.timer_cycles, 70224u);
		}
		/* The DoFrame's own VBlank: the halt-return work (OAM DMA,
		 * scroll/window/LCDC flush, VBlank function, palette flush) and
		 * the counter, so the PPU sample below and the next frame's game
		 * code see it, like the ROM's ISR -- which a disabled LCD never
		 * raises (lcd.asm:2-16: DoFrame then completes without waiting).
		 * Without a track DisableLCD's pass is a service as well. */
		if ((gb_read8(0xFF40u) & 0x80u) != 0u &&
		    (frame_boundary_pass_is_doframe() || !g_lag)) {
			vblank_service(ordinal, state.services);
			state.services++;
		}
		ShellAudioSettings audio_settings = shell_audio_settings(shell);
		apu_set_host_mix(audio_settings.master_volume,
		                 audio_settings.music_volume, audio_settings.sfx_volume,
		                 audio_settings.mono,
		                 (uint8_t)(gb_read8(wdd8c_ADDR) & 0x0Fu));
		apu_trace_set_tick(state.frames);
		size_t pcm_count = apu_trace_render_pcm(
			state.audio, AUDIO_SAMPLES_PER_FRAME);
		/* The framebuffer has two consumers: the window and a state dump
		 * (this frame's, or the anchor dump of the DoFrame that follows).
		 * A headless replay with neither skips the software PPU, which
		 * was half of a verify's native pass (gprof, rock-club). */
		if (shell_has_window(shell) || frame_dump_pending(state.frames) ||
		    ordinal_dump_pending(ordinal + 1u)) {
			ppu_render_frame(&state.ppu, state.framebuffer);
			if (presentation_on())
				present_frame(&state);
		}
		/* A recorded prefix replays at full speed; only live play is paced. */
		if (!timeline_live)
			shell_pace(shell);
		shell_present(shell, presentation_on() ? state.present : state.framebuffer);
		shell_queue_audio(shell, state.audio, pcm_count);
		if (g_pcm_sink) {
			uint32_t tag = ordinal ? ordinal - 1u : 0u;
			fwrite(&tag, sizeof tag, 1, g_pcm_sink);
			fwrite(state.audio, sizeof state.audio[0], pcm_count, g_pcm_sink);
		}
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
	frame_boundary_install_overread(NULL, NULL);
	frame_boundary_install_timer_sync(NULL, NULL);
	frame_boundary_install_busy_wait(NULL, NULL);
	g_isr_state = NULL;
	frame_boundary_install_vblank_sync(NULL, NULL);
	frame_boundary_install_anchor(NULL, NULL);
	frame_boundary_install(NULL, NULL);
	if (g_record_sink)
		fflush(g_record_sink);
	if (result) {
		ppu_render_frame(&state.ppu, state.framebuffer);
		if (presentation_on())
			present_frame(&state);
		fill_result(&state, frame_limit, result);
	}
	pthread_cond_destroy(&state.condition);
	pthread_mutex_destroy(&state.lock);
	return 0;
}

int runtime_run(Shell *shell, uint32_t frame_limit, RuntimeResult *result)
{
	return runtime_run_with_input(shell, frame_limit, NULL, 0, result);
}
