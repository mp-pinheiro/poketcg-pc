#include "runtime.h"
#include "mem.h"
#include "pc_options.h"

#include "home/frames.h"
#include "generated/wram.h"

#include <limits.h>

#define PC_FONT_COUNT 4
#define PC_OPTION_PLAYER_CHARACTER 10u
#define PC_OPTION_CHARACTER_SELECT 11u
#define EVENT_PLAYER_GENDER_OFFSET 0x1du

static RuntimeEvent g_terminal_event;
static uint32_t g_event_mask;
static uint32_t g_event_count;
static int g_player_gender_dirty;

void runtime_events_reset(void)
{
	g_terminal_event = RUNTIME_EVENT_NONE;
	g_event_mask = 0u;
	g_event_count = 0u;
	g_player_gender_dirty = 0;
}

static void record_event(RuntimeEvent event)
{
	if (event == RUNTIME_EVENT_NONE)
		return;
	uint32_t bit = 1u << (unsigned)event;
	if ((g_event_mask & bit) == 0u) {
		g_event_mask |= bit;
		g_event_count++;
	}
}

void runtime_mark_event(RuntimeEvent event)
{
	record_event(event);
	if (event != RUNTIME_EVENT_NONE)
		g_terminal_event = event;
}

void runtime_record_event(RuntimeEvent event)
{
	record_event(event);
}

RuntimeEvent runtime_terminal_event(void)
{
	return g_terminal_event;
}

uint32_t runtime_event_mask(void)
{
	return g_event_mask;
}

uint32_t runtime_event_count(void)
{
	return g_event_count;
}
static int g_pc_options_enabled;
static PcOptions *g_pc_options;

void runtime_bind_pc_options(struct PcOptions *options)
{
	g_pc_options = options;
}

int runtime_player_gender(void)
{
	return g_pc_options_enabled &&
		(gb_read8((uint16_t)(wEventVars_ADDR + EVENT_PLAYER_GENDER_OFFSET)) & 1u);
}

void runtime_set_player_gender(int female)
{
	if (!g_pc_options_enabled)
		return;
	uint16_t address = (uint16_t)(wEventVars_ADDR + EVENT_PLAYER_GENDER_OFFSET);
	uint8_t old = gb_read8(address);
	uint8_t next = female ? (uint8_t)(old | 1u) : (uint8_t)(old & (uint8_t)~1u);
	if (old != next)
		g_player_gender_dirty = 1;
	gb_write8(address, next);
}

int runtime_player_gender_dirty(void)
{
	return g_player_gender_dirty;
}

void runtime_clear_player_gender_dirty(void)
{
	g_player_gender_dirty = 0;
}

int runtime_character_selection_enabled(void)
{
	return g_pc_options_enabled && g_pc_options && g_pc_options->character_select;
}

int runtime_pc_option_value(unsigned option)
{
	if (!g_pc_options)
		return 0;
	switch (option) {
	case 0u: return g_pc_options->scale;
	case 2u: return g_pc_options->sgb;
	case 3u: return g_pc_options->master_volume;
	case 4u: return g_pc_options->music_volume;
	case 5u: return g_pc_options->big_font;
	case 6u: return g_pc_options->sgb_border;
	case 7u: return g_pc_options->text_case;
	case 8u: return g_pc_options->sfx_volume;
	case 9u: return g_pc_options->small_font;
	case PC_OPTION_PLAYER_CHARACTER: return runtime_player_gender();
	case PC_OPTION_CHARACTER_SELECT: return g_pc_options->character_select;
	default: return 0;
	}
}

static void adjust_volume(int *volume, int direction)
{
	*volume += direction * 10;
	if (*volume < 0)
		*volume = 0;
	if (*volume > 100)
		*volume = 100;
}

static void apply_font_override(void)
{
	if (g_pc_options_enabled && g_pc_options)
		mem_set_font_override(g_pc_options->big_font, g_pc_options->small_font);
	else
		mem_set_font_override(0, 0);
}

void runtime_pc_option_adjust(unsigned option, int direction)
{
	if (!g_pc_options || !g_pc_options_enabled)
		return;
	switch (option) {
	case 0u:
		g_pc_options->scale = g_pc_options->scale + direction;
		if (g_pc_options->scale < 1) g_pc_options->scale = 1;
		if (g_pc_options->scale > 6) g_pc_options->scale = 6;
		break;
	case 2u:
		g_pc_options->sgb = !g_pc_options->sgb;
		break;
	case 3u:
		adjust_volume(&g_pc_options->master_volume, direction);
		break;
	case 4u:
		adjust_volume(&g_pc_options->music_volume, direction);
		break;
	case 5u:
		g_pc_options->big_font = (g_pc_options->big_font + direction % PC_FONT_COUNT + PC_FONT_COUNT)
			% PC_FONT_COUNT;
		apply_font_override();
		break;
	case 6u:
		g_pc_options->sgb_border = (g_pc_options->sgb_border + direction % 4 + 4) % 4;
		break;
	case 7u:
		g_pc_options->text_case = !g_pc_options->text_case;
		break;
	case 8u:
		adjust_volume(&g_pc_options->sfx_volume, direction);
		break;
	case 9u:
		g_pc_options->small_font = !g_pc_options->small_font;
		apply_font_override();
		break;
	case PC_OPTION_PLAYER_CHARACTER:
		runtime_set_player_gender(!runtime_player_gender());
		break;
	case PC_OPTION_CHARACTER_SELECT:
		g_pc_options->character_select = !g_pc_options->character_select;
		break;
	default:
		return;
	}
}
void runtime_set_pc_options_enabled(int enabled)
{
	g_pc_options_enabled = enabled != 0;
	apply_font_override();
}

int runtime_pc_options_enabled(void)
{
	return g_pc_options_enabled;
}

int runtime_text_mixed_case(void)
{
	return g_pc_options_enabled && g_pc_options && g_pc_options->text_case;
}

static struct {
	const uint16_t *counts;
	size_t count;
	uint32_t interval;
	unsigned used;
} g_serial = {NULL, 0, UINT32_MAX, 0};

void runtime_serial_track(const uint16_t *serial, size_t count)
{
	g_serial.counts = serial;
	g_serial.count = serial ? count : 0;
	g_serial.interval = UINT32_MAX;
	g_serial.used = 0;
}

unsigned runtime_serial_budget(void)
{
	if (!g_serial.counts)
		return UINT_MAX;
	uint32_t interval = frame_boundary_doframe_ordinal();
	if (interval >= g_serial.count)
		return 0;
	if (g_serial.interval != interval) {
		g_serial.interval = interval;
		g_serial.used = 0;
	}
	unsigned recorded = g_serial.counts[interval];
	return recorded > g_serial.used ? recorded - g_serial.used : 0;
}

void runtime_serial_consume(unsigned steps)
{
	if (g_serial.counts)
		g_serial.used += steps;
}

static struct {
	const uint32_t *start;
	const uint16_t *address;
	size_t count;
	uint32_t interval;
	uint32_t cursor;
} g_stack = {NULL, NULL, 0, UINT32_MAX, 0};

void runtime_stack_track(const uint32_t *start, const uint16_t *address, size_t count)
{
	g_stack.start = start;
	g_stack.address = address;
	g_stack.count = start ? count : 0;
	g_stack.interval = UINT32_MAX;
	g_stack.cursor = 0;
}

uint16_t runtime_instruction_address(uint16_t fallback)
{
	uint32_t interval = frame_boundary_doframe_ordinal();
	if (!g_stack.start || interval >= g_stack.count)
		return fallback;
	if (g_stack.interval != interval) {
		g_stack.interval = interval;
		g_stack.cursor = g_stack.start[interval];
	}
	if (g_stack.cursor >= g_stack.start[interval + 1u])
		return fallback;
	return g_stack.address[g_stack.cursor++];
}
