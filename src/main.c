#include "mem.h"
#include "persistence.h"
#include "state_dump.h"
#include "runtime.h"
#include "shell.h"
#include "checkpoint.h"
#include "digest.h"
#include "trace.h"

#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int parse_frame_limit(const char *text, uint32_t *value)
{
	char *end = NULL;
	unsigned long long parsed;
	errno = 0;
	parsed = strtoull(text, &end, 10);
	if (errno || !text[0] || !end || *end != '\0' || parsed > UINT32_MAX)
		return -1;
	*value = (uint32_t)parsed;
	return 0;
}

static int parse_bank_address(
	const char *text, uint8_t *bank, uint16_t *address)
{
	char *end = NULL;
	unsigned long parsed_bank = strtoul(text, &end, 16);
	if (!text[0] || !end || *end != ':' || parsed_bank > UINT8_MAX)
		return -1;
	const char *address_text = end + 1;
	unsigned long parsed_address = strtoul(address_text, &end, 16);
	if (!address_text[0] || !end || *end != '\0' || parsed_address > UINT16_MAX)
		return -1;
	*bank = (uint8_t)parsed_bank;
	*address = (uint16_t)parsed_address;
	return 0;
}

static int load_input_timeline(
	const char *path, uint8_t **buttons_out, size_t *count_out)
{
	FILE *file = fopen(path, "rb");
	if (!file)
		return -1;
	if (fseek(file, 0, SEEK_END) != 0) {
		fclose(file);
		return -1;
	}
	long raw_size = ftell(file);
	if (raw_size < 1) {
		fclose(file);
		return -1;
	}
	rewind(file);
	size_t size = (size_t)raw_size;
	char *text = malloc(size + 1u);
	if (!text) {
		fclose(file);
		return -1;
	}
	if (fread(text, 1, size, file) != size) {
		free(text);
		fclose(file);
		return -1;
	}
	fclose(file);
	text[size] = '\0';
	uint8_t *buttons = NULL;
	size_t count = 0;
	size_t capacity = 0;
	char *cursor = text;
	while (*cursor) {
		while (*cursor == ',' || *cursor == ' ' || *cursor == '\t' ||
		       *cursor == '\r' || *cursor == '\n')
			cursor++;
		if (!*cursor)
			break;
		char *end = NULL;
		errno = 0;
		unsigned long value = strtoul(cursor, &end, 0);
		if (errno || end == cursor || value > UINT8_MAX) {
			free(buttons);
			free(text);
			return -1;
		}
		if (count == capacity) {
			size_t next = capacity ? capacity * 2u : 16u;
			uint8_t *grown = realloc(buttons, next);
			if (!grown) {
				free(buttons);
				free(text);
				return -1;
			}
			buttons = grown;
			capacity = next;
		}
		buttons[count++] = (uint8_t)value;
		cursor = end;
		if (*cursor && *cursor != ',' && *cursor != ' ' && *cursor != '\t' &&
		    *cursor != '\r' && *cursor != '\n') {
			free(buttons);
			free(text);
			return -1;
		}
	}
	free(text);
	if (!count) {
		free(buttons);
		return -1;
	}
	*buttons_out = buttons;
	*count_out = count;
	return 0;
}
/* Lag track: one line per DoFrame, `<cycles> <ticks> <vblanks>`. */
/* One line per DoFrame interval: `<cycles> <timer ISRs> <VBlank ISRs>`
 * followed by, per sound-driver wrapper call in that interval, the number of
 * its timer ISRs that had fired before the call (tools/completion/session.py
 * lag_track). */
static void lag_track_free(LagTrack *track)
{
	free(track->cycles);
	free(track->ticks);
	free(track->vblanks);
	free(track->call_start);
	free(track->call_ticks);
	memset(track, 0, sizeof *track);
}

static int grow(void **block, size_t capacity, size_t size)
{
	void *grown = realloc(*block, capacity * size);
	if (!grown)
		return -1;
	*block = grown;
	return 0;
}

static int load_lag_track(const char *path, LagTrack *track)
{
	FILE *file = fopen(path, "r");
	char line[4096];
	size_t capacity = 0, call_capacity = 0, calls = 0;
	memset(track, 0, sizeof *track);
	if (!file)
		return -1;
	while (fgets(line, sizeof line, file)) {
		char *cursor = line, *end;
		unsigned long f, t, v;
		if (!strchr(line, '\n') && !feof(file))
			goto fail;
		f = strtoul(cursor, &end, 10);
		if (end == cursor)
			goto fail;
		cursor = end;
		t = strtoul(cursor, &end, 10);
		if (end == cursor)
			goto fail;
		cursor = end;
		v = strtoul(cursor, &end, 10);
		if (end == cursor || f < 1 || f > 0xFFFFFFFFul || t > 65535 || v > 65535)
			goto fail;
		cursor = end;
		if (track->count == capacity) {
			capacity = capacity ? capacity * 2 : 1024;
			if (grow((void **)&track->cycles, capacity, sizeof *track->cycles) != 0 ||
			    grow((void **)&track->ticks, capacity, sizeof *track->ticks) != 0 ||
			    grow((void **)&track->vblanks, capacity, sizeof *track->vblanks) != 0 ||
			    grow((void **)&track->call_start, capacity + 1, sizeof *track->call_start) != 0)
				goto fail;
		}
		track->cycles[track->count] = (uint32_t)f;
		track->ticks[track->count] = (uint16_t)t;
		track->vblanks[track->count] = (uint16_t)v;
		track->call_start[track->count] = (uint32_t)calls;
		for (;;) {
			unsigned long o = strtoul(cursor, &end, 10);
			if (end == cursor)
				break;
			if (o > 65535)
				goto fail;
			cursor = end;
			if (calls == call_capacity) {
				call_capacity = call_capacity ? call_capacity * 2 : 1024;
				if (grow((void **)&track->call_ticks, call_capacity, sizeof *track->call_ticks) != 0)
					goto fail;
			}
			track->call_ticks[calls++] = (uint16_t)o;
		}
		track->count++;
	}
	fclose(file);
	if (!track->count)
		goto fail_closed;
	track->call_start[track->count] = (uint32_t)calls;
	return 0;
fail:
	fclose(file);
fail_closed:
	lag_track_free(track);
	return -1;
}

static const char *g_dump_state_path;
static uint32_t *g_dump_frames;
static size_t g_dump_frame_count;
static int g_dump_frames_failed;

static int compare_u32(const void *left, const void *right)
{
	uint32_t a = *(const uint32_t *)left, b = *(const uint32_t *)right;
	return a < b ? -1 : a > b ? 1 : 0;
}

static int parse_frame_list(const char *text, uint32_t **frames_out, size_t *count_out)
{
	uint32_t *frames = NULL;
	size_t count = 0;
	size_t capacity = 0;
	const char *cursor = text;
	if (!*text)
		return -1;
	while (*cursor) {
		char *end = NULL;
		errno = 0;
		unsigned long long parsed = strtoull(cursor, &end, 10);
		if (errno || end == cursor || parsed > UINT32_MAX)
			goto fail;
		if (count == capacity) {
			size_t next = capacity ? capacity * 2 : 8;
			uint32_t *grown = realloc(frames, next * sizeof *grown);
			if (!grown)
				goto fail;
			frames = grown;
			capacity = next;
		}
		frames[count++] = (uint32_t)parsed;
		cursor = end;
		if (*cursor == ',') {
			cursor++;
			if (!*cursor)
				goto fail;
		} else if (*cursor) {
			goto fail;
		}
	}
	qsort(frames, count, sizeof *frames, compare_u32);
	size_t unique = 0;
	for (size_t i = 0; i < count; i++)
		if (!i || frames[i] != frames[unique - 1])
			frames[unique++] = frames[i];
	*frames_out = frames;
	*count_out = unique;
	return 0;
fail:
	free(frames);
	return -1;
}

static void state_dump_frames_callback(uint32_t frame, const RuntimeResult *result)
{
	char path[512];
	const char *dump = g_dump_state_path;
	int written;
	if (dump && *dump) {
		const char *slash = strrchr(dump, '/');
		const char *dot = strrchr(dump, '.');
		size_t base = dot && (!slash || dot > slash) ? (size_t)(dot - dump) : strlen(dump);
		if (base >= sizeof path)
			base = sizeof path - 1;
		written = snprintf(path, sizeof path, "%.*s-f%u.json", (int)base, dump, frame);
	} else {
		written = snprintf(path, sizeof path, "state-%u.json", frame);
	}
	if (written < 0 || (size_t)written >= sizeof path ||
	    runtime_write_state(path, result) != 0) {
		fprintf(stderr, "cannot write per-frame native state for frame %u\n", frame);
		g_dump_frames_failed = 1;
	}
}

int main(int argc, char **argv)
{
	ShellConfig config = {0};
	uint32_t frame_limit = 600;
	const char *pack_path = NULL;
	int require_data = 0;
	uint8_t required_bank = 0;
	uint16_t required_address = 0;
	const char *save_path = NULL;
	const char *load_save_path = NULL;
	const char *dump_state_path = NULL;
	const char *dump_state_frames_text = NULL;
	const char *input_path = NULL;
	const char *input_ordinal_path = NULL;
	const char *record_input_path = NULL;
	const char *digest_out_path = NULL;
	const char *lag_track_path = NULL;
	const char *digest_mask_path = NULL;
	const char *dump_state_ordinals_text = NULL;
	uint32_t *dump_ordinals = NULL;
	size_t dump_ordinal_count = 0;
	uint32_t stop_ordinal = 0;
	const char *trace_entries_path = NULL;
	const char *trace_calls_path = NULL;
	const char *checkpoint_path = NULL;
	for (int i = 1; i < argc; i++) {
		if (strcmp(argv[i], "--headless") == 0) {
			config.headless = 1;
		} else if (strcmp(argv[i], "--frames") == 0 && i + 1 < argc) {
			if (parse_frame_limit(argv[++i], &frame_limit) != 0) {
				fprintf(stderr, "invalid --frames value\n");
				return 2;
			}
		} else if (strcmp(argv[i], "--data-pack") == 0 && i + 1 < argc) {
			pack_path = argv[++i];
		} else if (strcmp(argv[i], "--require-data") == 0 && i + 1 < argc) {
			if (parse_bank_address(argv[++i], &required_bank, &required_address) != 0) {
				fprintf(stderr, "invalid --require-data value\n");
				return 2;
			}
			require_data = 1;
		} else if (strcmp(argv[i], "--save") == 0 && i + 1 < argc) {
			save_path = argv[++i];
		} else if (strcmp(argv[i], "--load-save") == 0 && i + 1 < argc) {
			load_save_path = argv[++i];
		} else if (strcmp(argv[i], "--dump-state") == 0 && i + 1 < argc) {
			dump_state_path = argv[++i];
		} else if (strcmp(argv[i], "--dump-state-frames") == 0 && i + 1 < argc) {
			dump_state_frames_text = argv[++i];
			if (parse_frame_list(dump_state_frames_text, &g_dump_frames,
			                    &g_dump_frame_count) != 0) {
				fprintf(stderr, "invalid --dump-state-frames value\n");
				return 2;
			}
		} else if (strcmp(argv[i], "--input") == 0 && i + 1 < argc) {
			input_path = argv[++i];
		} else if (strcmp(argv[i], "--input-ordinal") == 0 && i + 1 < argc) {
			input_ordinal_path = argv[++i];
		} else if (strcmp(argv[i], "--record-input") == 0 && i + 1 < argc) {
			record_input_path = argv[++i];
		} else if (strcmp(argv[i], "--digest-out") == 0 && i + 1 < argc) {
			digest_out_path = argv[++i];
		} else if (strcmp(argv[i], "--lag-track") == 0 && i + 1 < argc) {
			lag_track_path = argv[++i];
		} else if (strcmp(argv[i], "--digest-mask") == 0 && i + 1 < argc) {
			digest_mask_path = argv[++i];
		} else if (strcmp(argv[i], "--dump-state-ordinals") == 0 && i + 1 < argc) {
			dump_state_ordinals_text = argv[++i];
			if (parse_frame_list(dump_state_ordinals_text, &dump_ordinals,
			                    &dump_ordinal_count) != 0) {
				fprintf(stderr, "invalid --dump-state-ordinals value\n");
				return 2;
			}
		} else if (strcmp(argv[i], "--stop-ordinal") == 0 && i + 1 < argc) {
			if (parse_frame_limit(argv[++i], &stop_ordinal) != 0 || !stop_ordinal) {
				fprintf(stderr, "invalid --stop-ordinal value\n");
				return 2;
			}
		} else if (strcmp(argv[i], "--trace-entries") == 0 && i + 1 < argc) {
			trace_entries_path = argv[++i];
		} else if (strcmp(argv[i], "--trace-calls") == 0 && i + 1 < argc) {
			trace_calls_path = argv[++i];
			trace_flush_on_abort(trace_calls_path);
		} else if (strcmp(argv[i], "--load-checkpoint") == 0 && i + 1 < argc) {
			checkpoint_path = argv[++i];
		} else if (strcmp(argv[i], "--help") == 0) {
			printf("usage: poketcg [--headless] [--frames N] --data-pack PATH "
			       "[--require-data BANK:ADDR] [--load-save PATH] [--save PATH] "
			       "[--dump-state PATH] [--dump-state-frames N[,N...]] "
			       "[--input PATH] [--input-ordinal PATH] [--record-input PATH] "
			       "[--dump-state-ordinals N[,N...]] [--stop-ordinal N] "
			       "[--digest-out PATH [--digest-mask FILE]] [--lag-track PATH] "
			       "[--trace-entries PATH] [--trace-calls PATH] "
			       "[--load-checkpoint PATH]\n");
			printf("--frames 0 runs until the window closes\n");
			printf("--input is one byte per host frame (a movie axis); "
			       "--input-ordinal is one byte per DoFrame and never wraps: "
			       "past its end the keyboard takes over. They are exclusive\n");
			printf("--record-input writes one decimal byte per DoFrame, the "
			       "exact file --input-ordinal replays\n");
			printf("--dump-state-ordinals and --stop-ordinal count DoFrames, "
			       "not host frames\n");
			printf("--digest-out writes 16 bytes per DoFrame: CRC-32 of WRAM, HRAM, "
			       "OAM and VRAM with --digest-mask ranges zeroed\n");
			printf("--lag-track replays the reference's clock, timer and VBlank services "
			       "per DoFrame (session.py writes it); verification only\n");
			printf("--trace-calls needs a build configured with "
			       "-DPOKETCG_TRACE=ON; without it the dump is empty\n");
			printf("--load-checkpoint injects a reference state and skips boot; "
			       "it is a diagnostic fixture, not evidence the game works\n");
			printf("with --dump-state-frames and no --dump-state, per-frame dumps "
			       "are written to state-<N>.json in the current directory\n");
			return 0;
		} else {
			fprintf(stderr, "unknown argument: %s\n", argv[i]);
			return 2;
		}
	}
#ifdef POKETCG_DATA_PACK_PATH
	if (!pack_path)
		pack_path = POKETCG_DATA_PACK_PATH;
#endif
	if (!pack_path)
		pack_path = getenv("POKETCG_DATA_PACK");
	if (!pack_path || !*pack_path) {
		fprintf(stderr, "missing production data pack\n");
		return 2;
	}
	mem_reset();
	if (rom_pack_load(pack_path) != 0) {
		fprintf(stderr, "cannot load production data pack %s: %s\n",
		        pack_path, strerror(errno));
		return 2;
	}
	if (rom_use_product() != 0) {
		fprintf(stderr, "cannot activate production data pack: %s\n",
		        strerror(errno));
		rom_pack_free();
		return 2;
	}
	if (require_data)
		(void)rom_ptr_product(required_bank, required_address);
	if (load_save_path && sram_load(load_save_path) != 0) {
		fprintf(stderr, "cannot load save %s: %s\n",
		        load_save_path, strerror(errno));
		rom_pack_free();
		return 2;
	}
	if (input_path && input_ordinal_path) {
		fprintf(stderr, "--input and --input-ordinal are exclusive\n");
		rom_pack_free();
		return 2;
	}
	uint8_t *input_buttons = NULL;
	size_t input_count = 0;
	if (input_path && load_input_timeline(input_path, &input_buttons, &input_count) != 0) {
		fprintf(stderr, "cannot load input timeline %s\n", input_path);
		rom_pack_free();
		return 2;
	}
	uint8_t *ordinal_buttons = NULL;
	size_t ordinal_count = 0;
	if (input_ordinal_path &&
	    load_input_timeline(input_ordinal_path, &ordinal_buttons, &ordinal_count) != 0) {
		fprintf(stderr, "cannot load ordinal input timeline %s\n", input_ordinal_path);
		free(input_buttons);
		rom_pack_free();
		return 2;
	}
	LagTrack lag_track;
	memset(&lag_track, 0, sizeof lag_track);
	if (lag_track_path && load_lag_track(lag_track_path, &lag_track) != 0) {
		fprintf(stderr, "cannot load lag track %s\n", lag_track_path);
		free(ordinal_buttons);
		free(input_buttons);
		rom_pack_free();
		return 2;
	}
	runtime_set_lag_track(&lag_track);
	FILE *record_sink = NULL;
	if (record_input_path) {
		record_sink = fopen(record_input_path, "w");
		if (!record_sink) {
			fprintf(stderr, "cannot open --record-input %s: %s\n",
			        record_input_path, strerror(errno));
			free(ordinal_buttons);
			free(input_buttons);
			rom_pack_free();
			return 2;
		}
	}
	if (digest_out_path && digest_open(digest_out_path, digest_mask_path) != 0) {
		fprintf(stderr, "cannot open --digest-out %s: %s\n",
		        digest_out_path, strerror(errno));
		if (record_sink)
			fclose(record_sink);
		free(ordinal_buttons);
		free(input_buttons);
		rom_pack_free();
		return 2;
	}
	Shell *shell = shell_create(&config);
	if (!shell) {
		if (record_sink)
			fclose(record_sink);
		free(ordinal_buttons);
		free(input_buttons);
		rom_pack_free();
		return 1;
	}
	g_dump_state_path = dump_state_path;
	if (g_dump_frame_count)
		runtime_set_state_dump_frames(
			state_dump_frames_callback, g_dump_frames, g_dump_frame_count);
	if (dump_ordinal_count)
		runtime_set_state_dump_ordinals(
			state_dump_frames_callback, dump_ordinals, dump_ordinal_count);
	runtime_set_ordinal_input(ordinal_buttons, ordinal_count);
	runtime_set_record_input(record_sink);
	runtime_set_stop_ordinal(stop_ordinal);
	if (checkpoint_path) {
		if (checkpoint_load(checkpoint_path) != 0) {
			fprintf(stderr, "cannot load checkpoint %s\n", checkpoint_path);
			if (record_sink)
				fclose(record_sink);
			free(ordinal_buttons);
			free(input_buttons);
			shell_destroy(shell);
			rom_pack_free();
			return 2;
		}
		runtime_skip_boot(1);
	}
	RuntimeResult runtime = {0};
	int status = input_count
		? runtime_run_with_input(shell, frame_limit, input_buttons, input_count, &runtime)
		: runtime_run(shell, frame_limit, &runtime);
	if (digest_out_path && digest_close() != 0) {
		fprintf(stderr, "cannot finish --digest-out %s\n", digest_out_path);
		status = 1;
	}
	if (record_sink && fclose(record_sink) != 0) {
		fprintf(stderr, "cannot finish --record-input %s: %s\n",
		        record_input_path, strerror(errno));
		status = 1;
	}
	runtime_set_record_input(NULL);
	runtime_set_lag_track(NULL);
	lag_track_free(&lag_track);
	free(ordinal_buttons);
	free(input_buttons);
	if (g_dump_frames_failed)
		status = 1;
	free(dump_ordinals);
	free(g_dump_frames);
	if (status == 0 && save_path && sram_save_atomic(save_path) != 0) {
		fprintf(stderr, "cannot save %s: %s\n", save_path, strerror(errno));
		status = 1;
	}
	if (status == 0 && dump_state_path && runtime_write_state(dump_state_path, &runtime) != 0) {
		fprintf(stderr, "cannot write native state %s\n", dump_state_path);
		status = 1;
	}
	if (status == 0 && trace_entries_path && runtime_write_trace(trace_entries_path, &runtime) != 0) {
		fprintf(stderr, "cannot write native trace %s\n", trace_entries_path);
		status = 1;
	}
	if (status == 0 && trace_calls_path && trace_write_raw(trace_calls_path) != 0) {
		fprintf(stderr, "cannot write native call trace %s\n", trace_calls_path);
		status = 1;
	}
	if (status != 0)
		fprintf(stderr, "runtime rendezvous failed\n");
	else
		printf("%s frames: %u, P1=0x%02X\n",
		       shell_backend_name(shell), runtime.frames, g_io[0]);
	shell_destroy(shell);
	rom_pack_free();
	return status == 0 ? 0 : 1;
}
