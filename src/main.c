#include "mem.h"
#include "runtime.h"
#include "shell.h"

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

int main(int argc, char **argv)
{
	ShellConfig config = {0};
	uint32_t frame_limit = 600;
	const char *pack_path = NULL;
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
		} else if (strcmp(argv[i], "--help") == 0) {
			printf("usage: poketcg [--headless] [--frames N] --data-pack PATH\n");
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
	Shell *shell = shell_create(&config);
	if (!shell) {
		rom_pack_free();
		return 1;
	}
	RuntimeResult runtime = {0};
	int status = runtime_run(shell, frame_limit, &runtime);
	if (status != 0)
		fprintf(stderr, "runtime rendezvous failed\n");
	else
		printf("%s frames: %u, P1=0x%02X\n",
		       shell_backend_name(shell), runtime.frames, g_io[0]);
	shell_destroy(shell);
	rom_pack_free();
	return status == 0 ? 0 : 1;
}
