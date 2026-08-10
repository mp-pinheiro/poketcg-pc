#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "gbrt.h"
uint8_t g_joypad_buttons = 0xff;
uint8_t g_joypad_dpad = 0xff;


#define REQUEST_LIMIT (1u << 20)
#define DEFAULT_INSTRUCTION_BUDGET 1000000u
#define DEFAULT_CYCLE_BUDGET 4000000u

static void fail(const char *stage, const char *detail) {
    printf("{\"status\":\"%s\",\"detail\":\"%s\"}\n", stage, detail);
    exit(strcmp(stage, "ARTIFACT") == 0 ? 2 : 3);
}

static char *read_request(void) {
    size_t cap = 4096;
    size_t len = 0;
    char *data = malloc(cap);
    if (!data) fail("ARTIFACT", "request allocation failed");
    for (;;) {
        if (len + 1 == cap) {
            if (cap >= REQUEST_LIMIT) fail("SCHEMA", "request exceeds 1 MiB");
            cap *= 2;
            char *grown = realloc(data, cap);
            if (!grown) fail("ARTIFACT", "request allocation failed");
            data = grown;
        }
        size_t n = fread(data + len, 1, cap - len - 1, stdin);
        len += n;
        if (n == 0) break;
    }
    data[len] = '\0';
    return data;
}

static int json_number(const char *json, const char *key, uint64_t *out) {
    char needle[64];
    int n = snprintf(needle, sizeof needle, "\"%s\"", key);
    if (n < 0 || (size_t)n >= sizeof needle) return 0;
    const char *p = strstr(json, needle);
    if (!p) return 0;
    p += n;
    while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') p++;
    if (*p++ != ':') return -1;
    while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') p++;
    if (*p == '-' || *p < '0' || *p > '9') return -1;
    errno = 0;
    char *end = NULL;
    unsigned long long value = strtoull(p, &end, 10);
    if (errno != 0 || end == p) return -1;
    *out = (uint64_t)value;
    return 1;
}

static int json_string(const char *json, const char *key, char *out, size_t cap) {
    char needle[64];
    int n = snprintf(needle, sizeof needle, "\"%s\"", key);
    if (n < 0 || (size_t)n >= sizeof needle) return 0;
    const char *p = strstr(json, needle);
    if (!p) return 0;
    p += n;
    while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') p++;
    if (*p++ != ':') return -1;
    while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') p++;
    if (*p++ != '"') return -1;
    size_t len = 0;
    while (*p && *p != '"') {
        if (*p == '\\' || len + 1 >= cap) return -1;
        out[len++] = *p++;
    }
    if (*p != '"') return -1;
    out[len] = '\0';
    return 1;
}

static uint8_t *read_file(const char *path, size_t *size) {
    FILE *file = fopen(path, "rb");
    if (!file) return NULL;
    if (fseek(file, 0, SEEK_END) != 0) { fclose(file); return NULL; }
    long end = ftell(file);
    if (end <= 0) { fclose(file); return NULL; }
    if (fseek(file, 0, SEEK_SET) != 0) { fclose(file); return NULL; }
    uint8_t *data = malloc((size_t)end);
    if (!data) { fclose(file); return NULL; }
    size_t got = fread(data, 1, (size_t)end, file);
    fclose(file);
    if (got != (size_t)end) { free(data); return NULL; }
    *size = got;
    return data;
}

static void print_hex(const uint8_t *data, size_t size) {
    static const char digits[] = "0123456789abcdef";
    for (size_t i = 0; i < size; i++) {
        putchar(digits[data[i] >> 4]);
        putchar(digits[data[i] & 0x0f]);
    }
}

static void print_result(const GBContext *ctx, const char *completion,
                         uint64_t steps, uint64_t cycles) {
    printf("{\"status\":\"REFERENCE_OK\",\"completion\":\"%s\","
           "\"pc\":%" PRIu16 ",\"sp\":%" PRIu16 ","
           "\"af\":%" PRIu16 ",\"bc\":%" PRIu16 ","
           "\"de\":%" PRIu16 ",\"hl\":%" PRIu16 ","
           "\"rom_bank\":%" PRIu16 ",\"ram_bank\":%" PRIu8 ","
           "\"wram\":\"",
           completion, ctx->pc, ctx->sp, ctx->af, ctx->bc, ctx->de, ctx->hl,
           ctx->rom_bank, ctx->ram_bank);
    print_hex(ctx->wram, 0x2000);
    printf("\",\"hram\":\"");
    print_hex(ctx->hram, 0x7f);
    printf("\",\"vram\":\"");
    print_hex(ctx->vram, 0x4000);
    printf("\",\"oam\":\"");
    print_hex(ctx->oam, 0xa0);
    printf("\",\"sram\":\"");
    print_hex(ctx->eram, ctx->eram_size);
    printf("\",\"instructions\":%" PRIu64 ",\"cycles\":%" PRIu64 "}\n",
           steps, cycles);
}

int main(int argc, char **argv) {
    if (argc != 3 || strcmp(argv[1], "--rom") != 0) {
        fprintf(stderr, "usage: %s --rom ABSOLUTE_ROM_PATH\n", argv[0]);
        return 2;
    }
    if (argv[2][0] != '/') fail("SCHEMA", "--rom must be an absolute path");

    char *request = read_request();
    char completion[16];
    if (json_string(request, "completion", completion, sizeof completion) != 1 ||
        (strcmp(completion, "return") != 0 && strcmp(completion, "pre-ret") != 0 &&
         strcmp(completion, "event") != 0)) {
        free(request);
        fail("SCHEMA", "completion must be return, pre-ret, or event");
    }

    uint64_t entry = 0;
    int entry_state = json_number(request, "entry", &entry);
    uint64_t instruction_budget = DEFAULT_INSTRUCTION_BUDGET;
    uint64_t cycle_budget = DEFAULT_CYCLE_BUDGET;
    uint64_t stop_pc = 0;
    int stop_state = json_number(request, "stop_pc", &stop_pc);
    uint64_t event_addr = 0, event_value = 0, event_mask = 0xff;
    int event_addr_state = json_number(request, "event_addr", &event_addr);
    int event_value_state = json_number(request, "event_value", &event_value);
    int event_mask_state = json_number(request, "event_mask", &event_mask);
    int instruction_state = json_number(request, "instruction_budget", &instruction_budget);
    int cycle_state = json_number(request, "cycle_budget", &cycle_budget);
    uint64_t reg_a = 0, reg_f = 0, reg_b = 0, reg_c = 0;
    uint64_t reg_d = 0, reg_e = 0, reg_hl = 0;
    int reg_a_state = json_number(request, "a", &reg_a);
    int reg_f_state = json_number(request, "f", &reg_f);
    int reg_b_state = json_number(request, "b", &reg_b);
    int reg_c_state = json_number(request, "c", &reg_c);
    int reg_d_state = json_number(request, "d", &reg_d);
    int reg_e_state = json_number(request, "e", &reg_e);
    int reg_hl_state = json_number(request, "hl", &reg_hl);
    uint64_t mapper_rom_bank = 1, mapper_ram_bank = 0, mapper_ram_enable = 0;
    int mapper_rom_state = json_number(request, "rom_bank", &mapper_rom_bank);
    int mapper_ram_state = json_number(request, "ram_bank", &mapper_ram_bank);
    int mapper_enable_state = json_number(request, "ram_enable", &mapper_ram_enable);
    free(request);
    if (
        (strcmp(completion, "event") == 0 &&
         (event_addr_state != 1 || event_value_state != 1 || event_mask_state < 0 ||
          event_addr > 0xffff || event_value > 0xff || event_mask > 0xff)) ||
        entry > 0xffff || instruction_budget == 0 || cycle_budget == 0 ||
        instruction_budget > UINT32_MAX || cycle_budget > UINT32_MAX ||
        (strcmp(completion, "pre-ret") == 0 && (stop_state != 1 || stop_pc > 0xffff)) ||
        reg_a_state < 0 || reg_f_state < 0 || reg_b_state < 0 ||
        reg_c_state < 0 || reg_d_state < 0 || reg_e_state < 0 ||
        reg_hl_state < 0 || reg_a > 0xff || reg_f > 0xff ||
        reg_b > 0xff || reg_c > 0xff || reg_d > 0xff || reg_e > 0xff ||
        reg_hl > 0xffff || mapper_rom_state < 0 || mapper_ram_state < 0 ||
        mapper_enable_state < 0 || mapper_rom_bank > 0x1ff ||
        mapper_ram_bank > 0xff || mapper_ram_enable > 1) {
        fail("SCHEMA", "entry, registers, mapper, and finite budgets are required");
    }
    size_t rom_size = 0;
    uint8_t *rom = read_file(argv[2], &rom_size);
    if (!rom) fail("ARTIFACT", "ROM could not be read");

    GBConfig config = {0};
    config.model = GB_MODEL_DMG;
    config.speed_percent = 100;
    config.enable_audio = false;
    config.enable_serial = false;
    config.native_presentation_enabled = false;
    GBContext *ctx = gb_context_create(&config);
    if (!ctx) { free(rom); fail("BACKEND_UNHEALTHY", "gb_context_create failed"); }
    if (!gb_context_load_rom(ctx, rom, rom_size)) {
        gb_context_destroy(ctx);
        free(rom);
        fail("ARTIFACT", "runtime rejected ROM");
    }
    gb_context_reset(ctx, true);
    ctx->rom_bank = (uint16_t)mapper_rom_bank;
    ctx->ram_bank = (uint8_t)mapper_ram_bank;
    ctx->ram_enabled = (uint8_t)mapper_ram_enable;
    ctx->sp = 0xfffe;
    gb_push16(ctx, 0xfea0);
    ctx->pc = (uint16_t)entry;

    ctx->af = (uint16_t)((reg_a << 8) | reg_f);
    ctx->bc = (uint16_t)((reg_b << 8) | reg_c);
    ctx->de = (uint16_t)((reg_d << 8) | reg_e);
    ctx->hl = (uint16_t)reg_hl;
    uint64_t steps = 0;
    uint64_t cycles = 0;
    while (strcmp(completion, "event") == 0
               ? ((gb_read8(ctx, (uint16_t)event_addr) & (uint8_t)event_mask)
                  != (uint8_t)event_value)
               : ctx->pc != (strcmp(completion, "pre-ret") == 0 ? stop_pc : 0xfea0)) {
        if (steps >= instruction_budget || cycles >= cycle_budget) {
            fprintf(stdout, "{\"status\":\"BUDGET_EXHAUSTED\",\"pc\":%u,\"sp\":%u,"
                    "\"instructions\":%" PRIu64 ",\"cycles\":%" PRIu64 "}\n",
                    ctx->pc, ctx->sp, steps, cycles);
            gb_context_destroy(ctx);
            free(rom);
            return 4;
        }
        uint32_t delta = gb_debug_step(ctx, GB_EXECUTION_INTERPRETER);
        if (delta == 0) {
            gb_context_destroy(ctx);
            free(rom);
            fail("BACKEND_UNHEALTHY", "interpreter made no progress");
        }
        steps++;
        cycles += delta;
    }
    print_result(ctx, completion, steps, cycles);
    gb_context_destroy(ctx);
    free(rom);
    return 0;
}
