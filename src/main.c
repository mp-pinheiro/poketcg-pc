#include "mem.h"
#include "persistence.h"
#include "state_dump.h"
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
		} else if (strcmp(argv[i], "--help") == 0) {
			printf("usage: poketcg [--headless] [--frames N] --data-pack PATH "
			       "[--require-data BANK:ADDR] [--load-save PATH] [--save PATH] "
			       "[--dump-state PATH]\n");
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
	Shell *shell = shell_create(&config);
	if (!shell) {
		rom_pack_free();
		return 1;
	}
	RuntimeResult runtime = {0};
	int status = runtime_run(shell, frame_limit, &runtime);
	if (status == 0 && save_path && sram_save_atomic(save_path) != 0) {
		fprintf(stderr, "cannot save %s: %s\n", save_path, strerror(errno));
		status = 1;
	}
	if (status == 0 && dump_state_path && runtime_write_state(dump_state_path, &runtime) != 0) {
		fprintf(stderr, "cannot write native state %s\n", dump_state_path);
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
