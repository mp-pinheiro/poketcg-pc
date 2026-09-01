#include "state_dump.h"

#include "mem.h"

#include <stdio.h>
#include <stdint.h>

static int write_bytes(FILE *file, const uint8_t *data, size_t count)
{
	if (fputc('[', file) == EOF)
		return -1;
	for (size_t i = 0; i < count; i++) {
		if (i && fputc(',', file) == EOF)
			return -1;
		if (fprintf(file, "%u", data[i]) < 0)
			return -1;
	}
	return fputc(']', file) == EOF ? -1 : 0;
}

static int write_words(FILE *file, const uint16_t *data, size_t count)
{
	if (fputc('[', file) == EOF)
		return -1;
	for (size_t i = 0; i < count; i++) {
		if (i && fputc(',', file) == EOF)
			return -1;
		if (fprintf(file, "%u", data[i]) < 0)
			return -1;
	}
	return fputc(']', file) == EOF ? -1 : 0;
}

static int write_region(FILE *file, const char *name, const uint8_t *data, size_t count)
{
	return fprintf(file, "\"%s\":", name) < 0 || write_bytes(file, data, count) != 0 ? -1 : 0;
}

static const char *runtime_event_name(RuntimeEvent event)
{
	switch (event) {
	case RUNTIME_EVENT_BOOT_STARTED:
		return "BOOT_STARTED";
	case RUNTIME_EVENT_TITLE_READY:
		return "TITLE_READY";
	case RUNTIME_EVENT_START_MENU_READY:
		return "START_MENU_READY";
	case RUNTIME_EVENT_NEW_GAME_ENTERED:
		return "NEW_GAME_ENTERED";
	default:
		return "NONE";
	}
}

int runtime_write_state(const char *path, const RuntimeResult *runtime)
{
	if (!path || !runtime)
		return -1;
	FILE *file = fopen(path, "wb");
	if (!file)
		return -1;
	int ok = fputc('{', file) != EOF;
	const char *terminal = runtime_event_name(runtime->terminal_event);
	ok = ok && fprintf(file,
	                   "\"runtime\":{\"frames\":%u,\"events\":%u,\"event_mask\":%u,\"terminal_event\":\"%s\"},",
	                   runtime->frames, runtime->event_count, runtime->event_mask, terminal) >= 0;
	ok = ok && write_region(file, "wram", g_wram, sizeof g_wram) == 0;
	ok = ok && fputc(',', file) != EOF;
	ok = ok && write_region(file, "hram", g_hram, sizeof g_hram) == 0;
	for (uint8_t bank = 0; ok && bank < 4; bank++) {
		if (fprintf(file, ",\"sram_bank_%u\":", bank) < 0 ||
		    write_bytes(file, g_sram + (size_t)bank * 0x2000u, 0x2000u) != 0)
			ok = 0;
	}
	for (uint8_t bank = 0; ok && bank < 2; bank++) {
		if (fprintf(file, ",\"vram_bank_%u\":", bank) < 0 ||
		    write_bytes(file, g_vram + (size_t)bank * 0x2000u, 0x2000u) != 0)
			ok = 0;
	}
	ok = ok && fputs(",\"oam\":", file) >= 0 && write_bytes(file, g_oam, sizeof g_oam) == 0;
	ok = ok && fputs(",\"io\":", file) >= 0 && write_bytes(file, g_io, sizeof g_io) == 0;
	ok = ok && fputs(",\"palette_ram\":", file) >= 0 && write_bytes(file, g_pal, sizeof g_pal) == 0;
	ok = ok && fprintf(file, ",\"mapper_state\":{\"rom_bank\":%u,\"sram_bank\":%u,\"vram_bank\":%u,\"sram_enabled\":%d}",
	                   g_rom_bank, g_sram_bank, g_vram_bank, g_sram_enabled) >= 0;
	ok = ok && fprintf(file, ",\"input_latch\":%u,\"timer_frame_counters\":{\"frames\":%u}",
	                   g_keys, runtime->frames) >= 0;
	ok = ok && fputs(",\"rng\":", file) >= 0;
	uint8_t rng[3] = {g_wram[0x0ACAu], g_wram[0x0ACBu], g_wram[0x0ACCu]};
	ok = ok && write_bytes(file, rng, sizeof rng) == 0;
	ok = ok && fprintf(file, ",\"apu_state\":{\"trace_count\":%zu},\"apu_trace\":[",
	                   apu_trace_count()) >= 0;
	const ApuWrite *trace = apu_trace_data();
	for (size_t i = 0; ok && i < apu_trace_count(); i++) {
		if ((i && fputc(',', file) == EOF) ||
		    fprintf(file, "{\"tick\":%u,\"address\":%u,\"value\":%u}",
	                    trace[i].tick, trace[i].address, trace[i].value) < 0)
			ok = 0;
	}
	ok = ok && fputs("]", file) >= 0;
	ok = ok && fputs(",\"framebuffer\":", file) >= 0 &&
	     write_words(file, runtime->framebuffer, SCREEN_W * SCREEN_H) == 0;
	ok = ok && fputs(",\"save\":", file) >= 0 && write_bytes(file, g_sram, sizeof g_sram) == 0;
	ok = ok && fputs(",\"transport\":[],\"printer\":[],\"scratch\":", file) >= 0 &&
	     write_bytes(file, g_scratch, sizeof g_scratch) == 0;
	ok = ok && fputc('}', file) != EOF;
	if (fclose(file) != 0)
		ok = 0;
	return ok ? 0 : -1;
}

int runtime_write_trace(const char *path, const RuntimeResult *runtime)
{
	if (!path || !runtime)
		return -1;
	FILE *file = fopen(path, "wb");
	if (!file)
		return -1;
	int ok = fprintf(file,
	                 "{\"schema\":1,\"frames\":%u,\"events\":%u,\"event_mask\":%u,"
	                 "\"terminal_event\":\"%s\","
	                 "\"symbols\":[\"Start\",\"GameLoop\",\"DoFrame\"],"
	                 "\"edges\":["
	                 "{\"source\":\"<host>\",\"target\":\"Start\",\"type\":\"direct-call\"},"
	                 "{\"source\":\"Start\",\"target\":\"GameLoop\",\"type\":\"direct-call\"},"
	                 "{\"source\":\"GameLoop\",\"target\":\"DoFrame\",\"type\":\"direct-call\"}"
	                 "]}",
	                 runtime->frames, runtime->event_count, runtime->event_mask,
	                 runtime_event_name(runtime->terminal_event)) >= 0;
	if (fclose(file) != 0)
		ok = 0;
	return ok ? 0 : -1;
}
