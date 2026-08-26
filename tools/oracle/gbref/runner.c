#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "gbrt.h"
#include "ppu.h"
uint8_t g_joypad_buttons = 0xff;
uint8_t g_joypad_dpad = 0xff;

static void service_pending_interrupt(GBContext *ctx) {
    uint8_t pending = (uint8_t)(ctx->io[0x0f] & ctx->io[0x80] & 0x1f);
    if (ctx->ime && pending) gb_handle_interrupts(ctx);
    if (ctx->halted && pending) ctx->halted = 0;
    ctx->stopped = 0;
}
static void seed_call_environment(GBContext *ctx) {
    gb_write8(ctx, 0xcad0, 0xc3);
    gb_write8(ctx, 0xcad1, 0x48);
    gb_write8(ctx, 0xcad2, 0x03);
    gb_write8(ctx, 0xff40, 0);
    gb_write8(ctx, 0xff0f, 0);
}


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

static const char *skip_json_ws(const char *p) {
    while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') p++;
    return p;
}

static const char *skip_json_string(const char *p) {
    if (*p++ != '"') return NULL;
    while (*p) {
        if (*p == '"') return p + 1;
        if (*p == '\\') {
            if (!p[1]) return NULL;
            p += 2;
        } else {
            p++;
        }
    }
    return NULL;
}

static const char *skip_json_value(const char *p) {
    p = skip_json_ws(p);
    if (*p == '"') return skip_json_string(p);
    if (*p == '{' || *p == '[') {
        unsigned depth = 0;
        do {
            if (*p == '"') {
                p = skip_json_string(p);
                if (!p) return NULL;
                continue;
            }
            if (*p == '{' || *p == '[') depth++;
            if (*p == '}' || *p == ']') depth--;
            p++;
        } while (*p && depth != 0);
        return depth == 0 ? p : NULL;
    }
    const char *start = p;
    while (*p && *p != ',' && *p != '}' && *p != ']' &&
           *p != ' ' && *p != '\t' && *p != '\r' && *p != '\n') {
        p++;
    }
    return p == start ? NULL : p;
}

static int json_member(const char *json, const char *key, const char **out) {
    const char *p = skip_json_ws(json);
    if (*p++ != '{') return -1;
    for (;;) {
        p = skip_json_ws(p);
        if (*p == '}') return 0;
        if (*p != '"') return -1;
        const char *name = p + 1;
        const char *after_name = skip_json_string(p);
        if (!after_name) return -1;
        const char *name_end = after_name - 1;
        p = skip_json_ws(after_name);
        if (*p++ != ':') return -1;
        p = skip_json_ws(p);
        if ((size_t)(name_end - name) == strlen(key) &&
            memcmp(name, key, (size_t)(name_end - name)) == 0) {
            *out = p;
            return 1;
        }
        p = skip_json_value(p);
        if (!p) return -1;
        p = skip_json_ws(p);
        if (*p == ',') {
            p++;
        } else if (*p == '}') {
            return 0;
        } else {
            return -1;
        }
    }
}

static int json_number(const char *json, const char *key, uint64_t *out) {
    const char *p = NULL;
    int state = json_member(json, key, &p);
    if (state != 1) return state;
    if (*p == '-' || *p < '0' || *p > '9') return -1;
    errno = 0;
    char *end = NULL;
    unsigned long long value = strtoull(p, &end, 10);
    if (errno != 0 || end == p) return -1;
    *out = (uint64_t)value;
    return 1;
}

static int json_string(const char *json, const char *key, char *out, size_t cap) {
    const char *p = NULL;
    int state = json_member(json, key, &p);
    if (state != 1) return state;
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
typedef struct {
    uint64_t entry;
    uint64_t rom_bank;
    uint64_t a, f, b, c, d, e, hl;
    int entry_state;
    int rom_bank_state;
    int reg_state[7];
} SetupCall;


static int json_array_start(const char *json, const char *key, const char **out) {
    const char *p = NULL;
    int state = json_member(json, key, &p);
    if (state != 1) return state;
    if (*p != '[') return -1;
    *out = p + 1;
    return 1;
}

static int parse_setup(const char *json, SetupCall *calls, size_t cap, size_t *count) {
    const char *p = NULL;
    int state = json_array_start(json, "setup", &p);
    if (state == 0) { *count = 0; return 1; }
    if (state < 0) return 0;
    size_t used = 0;
    for (;;) {
        p = skip_json_ws(p);
        if (*p == ']') { *count = used; return 1; }
        if (*p != '{' || used >= cap) return 0;
        const char *end = strchr(p, '}');
        if (!end) return 0;
        size_t length = (size_t)(end - p + 1);
        char object[1024];
        if (length >= sizeof object) return 0;
        memcpy(object, p, length);
        object[length] = '\0';
        SetupCall *call = &calls[used];
        memset(call, 0, sizeof *call);
        call->entry_state = json_number(object, "entry", &call->entry);
        call->rom_bank_state = json_number(object, "rom_bank", &call->rom_bank);
        const char *names[] = {"a", "f", "b", "c", "d", "e", "hl"};
        uint64_t *values[] = {&call->a, &call->f, &call->b, &call->c,
                              &call->d, &call->e, &call->hl};
        for (size_t i = 0; i < 7; i++) call->reg_state[i] = json_number(object, names[i], values[i]);
        if (call->entry_state != 1 || call->rom_bank_state != 1 ||
            call->entry > 0xffff || call->rom_bank > 0x1ff ||
            call->reg_state[0] < 0 || call->reg_state[1] < 0 ||
            call->reg_state[2] < 0 || call->reg_state[3] < 0 ||
            call->reg_state[4] < 0 || call->reg_state[5] < 0 ||
            call->reg_state[6] < 0 || call->a > 0xff || call->f > 0xff ||
            call->b > 0xff || call->c > 0xff || call->d > 0xff ||
            call->e > 0xff || call->hl > 0xffff) return 0;
        used++;
        p = skip_json_ws(end + 1);
        if (*p == ',') { p++; continue; }
        if (*p == ']') { *count = used; return 1; }
        return 0;
    }
}

#define MAX_STACK_WORDS 4

/* Words the caller pushed below this routine's return address, in push order.
 * A routine entered by `jp` from inside its own caller pops saves that caller
 * made, so a synthesized frame holding only a return address underflows into
 * whatever preceded it. Declaring them here reproduces the real frame. */
static int parse_stack_words(const char *json, uint16_t *words, size_t cap,
                             size_t *count) {
    const char *p = NULL;
    int state = json_array_start(json, "stack", &p);
    if (state == 0) { *count = 0; return 1; }
    if (state < 0) return 0;
    size_t used = 0;
    p = skip_json_ws(p);
    if (*p == ']') { *count = 0; return 1; }
    for (;;) {
        p = skip_json_ws(p);
        if (*p == '-' || *p < '0' || *p > '9') return 0;
        errno = 0;
        char *end = NULL;
        unsigned long long value = strtoull(p, &end, 10);
        if (errno != 0 || end == p || value > 0xffff || used >= cap) return 0;
        words[used++] = (uint16_t)value;
        p = skip_json_ws(end);
        if (*p == ',') { p++; continue; }
        if (*p == ']') { *count = used; return 1; }
        return 0;
    }
}

#define MAX_INPUT_EVENTS 16

/* One entry per rendered frame, cycled. The ROM's own key handling is edge
 * triggered: hKeysPressed holds what became newly pressed this frame, so a
 * button held from the first instruction is new exactly once, and a wait loop
 * that starts after that frame never sees it. Cycling a release/press pair
 * reproduces a human tapping the button, which lands an edge inside any wait
 * however many frames of text or animation precede it. A single-entry array
 * cycles onto itself and therefore still means held for the whole run. */
static int parse_input_keys(const char *json, uint8_t *buttons, uint8_t *dpad,
                            size_t cap, size_t *count) {
    const char *p = NULL;
    int state = json_array_start(json, "input_events", &p);
    if (state == 0) { *count = 0; return 1; }
    if (state < 0) return 0;
    size_t used = 0;
    for (;;) {
        p = skip_json_ws(p);
        if (*p == ']') { *count = used; return 1; }
        if (*p != '{' || used >= cap) return 0;
        const char *end = strchr(p, '}');
        if (!end) return 0;
        size_t length = (size_t)(end - p + 1);
        char object[128];
        if (length >= sizeof object) return 0;
        memcpy(object, p, length);
        object[length] = '\0';
        uint64_t keys = 0;
        if (json_number(object, "keys", &keys) != 1 || keys > 0xff) return 0;
        buttons[used] = (uint8_t)(~keys & 0x0f);
        dpad[used] = (uint8_t)(~(keys >> 4) & 0x0f);
        used++;
        p = skip_json_ws(end + 1);
        if (*p == ',') { p++; continue; }
        if (*p == ']') { *count = used; return 1; }
        return 0;
    }
}

static void seed_mapper_shadows(GBContext *ctx, uint64_t rom_bank,
                                uint64_t ram_bank, uint64_t ram_enable) {
    gb_write8(ctx, 0x2000, (uint8_t)rom_bank);
    gb_write8(ctx, 0x3000, (uint8_t)((rom_bank >> 8) & 1u));
    gb_write8(ctx, 0x4000, (uint8_t)ram_bank);
    gb_write8(ctx, 0x0000, ram_enable ? 0x0A : 0x00);
    gb_write8(ctx, 0xFF80, (uint8_t)rom_bank);
    gb_write8(ctx, 0xFF81, (uint8_t)ram_bank);
    gb_write8(ctx, 0xFF82, 0);
}

static void set_call_registers(GBContext *ctx, uint64_t a, uint64_t f,
                               uint64_t b, uint64_t c, uint64_t d, uint64_t e,
                               uint64_t hl) {
    ctx->a = (uint8_t)a;
    ctx->f_z = (uint8_t)((f >> 7) & 1u);
    ctx->f_n = (uint8_t)((f >> 6) & 1u);
    ctx->f_h = (uint8_t)((f >> 5) & 1u);
    ctx->f_c = (uint8_t)((f >> 4) & 1u);
    ctx->b = (uint8_t)b; ctx->c = (uint8_t)c;
    ctx->d = (uint8_t)d; ctx->e = (uint8_t)e;
    ctx->h = (uint8_t)(hl >> 8); ctx->l = (uint8_t)hl;
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
static int apply_seed_spans(GBContext *ctx, char *spec) {
    for (char *item = strtok(spec, ";"); item; item = strtok(NULL, ";")) {
        unsigned address = 0;
        char hex[65536];
        if (sscanf(item, "%x=%65535s", &address, hex) != 2 || address > 0xffffu) {
            return 0;
        }
        size_t length = strlen(hex);
        if ((length & 1u) != 0u || address + length / 2u > 0x10000u) {
            return 0;
        }
        for (size_t i = 0; i < length; i += 2) {
            unsigned byte = 0;
            if (sscanf(hex + i, "%2x", &byte) != 1) return 0;
            gb_write8(ctx, (uint16_t)(address + i / 2), (uint8_t)byte);
        }
    }
    return 1;
}
static int apply_banked_spans(GBContext *ctx, char *spec, uint8_t *region,
                               size_t region_size, unsigned base, unsigned banks) {
    for (char *item = strtok(spec, ";"); item; item = strtok(NULL, ";")) {
        unsigned bank = 0;
        unsigned address = 0;
        char hex[65536];
        if (sscanf(item, "%x:%x=%65535s", &bank, &address, hex) != 3 ||
            bank >= banks || address < base || address >= base + 0x2000u) return 0;
        size_t length = strlen(hex);
        if ((length & 1u) != 0u || address + length / 2u > base + 0x2000u) return 0;
        size_t offset = (size_t)bank * 0x2000u + address - base;
        if (offset + length / 2u > region_size) return 0;
        for (size_t i = 0; i < length; i += 2) {
            unsigned byte = 0;
            if (sscanf(hex + i, "%2x", &byte) != 1) return 0;
            region[offset + i / 2u] = (uint8_t)byte;
        }
    }
    return 1;
}

static void print_bus_spans(const GBContext *ctx, const uint16_t *bus_addresses,
                            const uint16_t *bus_sizes, size_t bus_count) {
    for (size_t i = 0; i < bus_count; i++) {
        for (uint32_t j = 0; j < bus_sizes[i]; j++) {
            uint8_t value = gb_read8((GBContext *)ctx,
                                     (uint16_t)(bus_addresses[i] + j));
            printf("%02x", value);
        }
    }
}

static void print_result(const GBContext *ctx, const char *completion,
                         uint64_t steps, uint64_t cycles,
                         const uint16_t *bus_addresses, const uint16_t *bus_sizes,
                         size_t bus_count) {
    uint8_t flags = (uint8_t)((ctx->f_z ? 0x80u : 0u) |
                              (ctx->f_n ? 0x40u : 0u) |
                              (ctx->f_h ? 0x20u : 0u) |
                              (ctx->f_c ? 0x10u : 0u));
    uint16_t af = (uint16_t)(((uint16_t)ctx->a << 8) | flags);
    uint16_t fixed_rom_bank = gb_resolve_rom_bank(ctx, 0x0000);
    uint16_t switch_rom_bank = gb_resolve_rom_bank(ctx, 0x4000);
    printf("{\"status\":\"REFERENCE_OK\",\"completion\":\"%s\","
           "\"pc\":%" PRIu16 ",\"sp\":%" PRIu16 ","
           "\"af\":%" PRIu16 ",\"bc\":%" PRIu16 ","
           "\"de\":%" PRIu16 ",\"hl\":%" PRIu16 ","
           "\"rom_bank\":%" PRIu16 ",\"ram_bank\":%" PRIu8 ","
           "\"ram_enable\":%" PRIu8 ",\"rom_bank_low\":%" PRIu8 ","
           "\"rom_bank_upper\":%" PRIu8 ",\"fixed_rom_bank\":%" PRIu16 ","
           "\"switch_rom_bank\":%" PRIu16 ",\"wram\":\"",
           completion, ctx->pc, ctx->sp, af, ctx->bc, ctx->de, ctx->hl,
           ctx->rom_bank, ctx->ram_bank, ctx->ram_enabled, ctx->rom_bank_low,
           ctx->rom_bank_upper, fixed_rom_bank, switch_rom_bank);
    print_hex(ctx->wram, 0x2000);
    printf("\",\"hram\":\"");
    print_hex(ctx->hram, 0x7f);
    printf("\",\"vram\":\"");
    print_hex(ctx->vram, 0x4000);
    printf("\",\"palette\":\"");
    const GBPPU *ppu = (const GBPPU *)ctx->ppu;
    print_hex(ppu->bg_palette_ram, 0x40);
    print_hex(ppu->obj_palette_ram, 0x40);
    printf("\",\"oam\":\"");
    print_hex(ctx->oam, 0xa0);
    printf("\",\"sram\":\"");
    print_hex(ctx->eram, ctx->eram_size);
    printf("\",\"bus\":\"");
    print_bus_spans(ctx, bus_addresses, bus_sizes, bus_count);
    printf("\",\"instructions\":%" PRIu64 ",\"cycles\":%" PRIu64 "}\n",
           steps, cycles);
}
static int parse_bus_spans(char *spec, uint16_t *addresses, uint16_t *sizes,
                           size_t *count, size_t cap) {
    size_t used = 0;
    for (char *item = strtok(spec, ";"); item; item = strtok(NULL, ";")) {
        unsigned address = 0, size = 0;
        if (used >= cap || sscanf(item, "%x:%x", &address, &size) != 2 ||
            address > 0xffffu || size == 0 || size > 0xffffu ||
            address + size > 0x10000u) return 0;
        addresses[used] = (uint16_t)address;
        sizes[used] = (uint16_t)size;
        used++;
    }
    *count = used;
    return 1;
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
    char hardware[4] = "dmg";
    int hardware_state = json_string(request, "hardware", hardware, sizeof hardware);

    uint64_t entry = 0;
    int entry_state = json_number(request, "entry", &entry);
    uint64_t instruction_budget = DEFAULT_INSTRUCTION_BUDGET;
    uint64_t cycle_budget = DEFAULT_CYCLE_BUDGET;
    uint64_t stop_pc = 0;
    int stop_state = json_number(request, "stop_pc", &stop_pc);
    char seed_wram[65536];
    char seed_sram[65536];
    char seed_vram[65536];
    int seed_wram_state = json_string(request, "seed_wram", seed_wram, sizeof seed_wram);
    int seed_sram_state = json_string(request, "seed_sram", seed_sram, sizeof seed_sram);
    int seed_vram_state = json_string(request, "seed_vram", seed_vram, sizeof seed_vram);
    char predicate[96];
    int predicate_state = json_string(request, "predicate", predicate, sizeof predicate);
    uint64_t event_addr = 0, event_value = 0, event_mask = 0xff;
    int event_addr_state = json_number(request, "event_addr", &event_addr);
    int event_value_state = json_number(request, "event_value", &event_value);
    int event_mask_state = json_number(request, "event_mask", &event_mask);
    if (predicate_state == 1 && sscanf(predicate, "mem:%" SCNx64 "==%" SCNx64 "&%" SCNx64,
                                        &event_addr, &event_value, &event_mask) == 3) {
        event_addr_state = event_value_state = event_mask_state = 1;
    } else if (predicate_state == 1 &&
               sscanf(predicate, "mem:%" SCNx64 "==%" SCNx64,
                      &event_addr, &event_value) == 2) {
        event_addr_state = event_value_state = event_mask_state = 1;
    }
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
    char mapper_mode[16] = "seeded";
    int mapper_mode_state = json_string(request, "mapper_mode", mapper_mode,
                                        sizeof mapper_mode);
    uint64_t mapper_rom_bank = 1, mapper_ram_bank = 0;
    uint64_t mapper_vram_bank = 0, mapper_ram_enable = 0;
    uint64_t mapper_hbank_rom = 0;
    int mapper_rom_state = json_number(request, "rom_bank", &mapper_rom_bank);
    int mapper_ram_state = json_number(request, "ram_bank", &mapper_ram_bank);
    int mapper_vram_state = json_number(request, "vram_bank", &mapper_vram_bank);
    int mapper_enable_state = json_number(request, "ram_enable", &mapper_ram_enable);
    int mapper_hbank_state = json_number(request, "hbank_rom", &mapper_hbank_rom);
    if (mapper_mode_state == 0) mapper_mode_state = 1;
    SetupCall setup_calls[256];
    size_t setup_count = 0;
    uint8_t input_buttons[MAX_INPUT_EVENTS], input_dpad[MAX_INPUT_EVENTS];
    size_t input_count = 0;
    uint16_t stack_words[MAX_STACK_WORDS];
    size_t stack_count = 0;
    int setup_state = parse_setup(request, setup_calls, 256, &setup_count);
    int input_state = parse_input_keys(request, input_buttons, input_dpad,
                                       MAX_INPUT_EVENTS, &input_count);
    int stack_state = parse_stack_words(request, stack_words, MAX_STACK_WORDS,
                                        &stack_count);
    if (!setup_state || !input_state) {
        free(request);
        fail("SCHEMA", "setup and input_events must be bounded arrays");
    }
    if (!stack_state) {
        free(request);
        fail("SCHEMA", "stack must be an array of at most 4 words below 0x10000");
    }
    char read_bus[65536];
    int read_bus_state = json_string(request, "read_bus", read_bus, sizeof read_bus);
    uint16_t bus_addresses[256], bus_sizes[256];
    size_t bus_count = 0;
    if (read_bus_state < 0 ||
        (read_bus_state == 1 &&
         !parse_bus_spans(read_bus, bus_addresses, bus_sizes, &bus_count, 256))) {
        free(request);
        fail("SCHEMA", "read_bus must contain address:size spans");
    }
    free(request);
    if (
        (strcmp(completion, "event") == 0 &&
         (predicate_state != 1 || event_addr_state != 1 || event_value_state != 1 ||
          event_mask_state != 1 || event_addr > 0xffff || event_value > 0xff ||
          event_mask > 0xff)) ||
        seed_wram_state < 0 || seed_sram_state < 0 || seed_vram_state < 0 ||
        entry_state != 1 || entry > 0xffff || instruction_budget == 0 || cycle_budget == 0 ||
        instruction_budget > UINT32_MAX || cycle_budget > UINT32_MAX ||
        instruction_state < 0 || cycle_state < 0 ||
        reg_a_state < 0 || reg_f_state < 0 || reg_b_state < 0 ||
        reg_c_state < 0 || reg_d_state < 0 || reg_e_state < 0 ||
        reg_hl_state < 0 || reg_a > 0xff || reg_f > 0xff ||
        reg_b > 0xff || reg_c > 0xff || reg_d > 0xff || reg_e > 0xff ||
        reg_hl > 0xffff || hardware_state < 0 ||
        (strcmp(hardware, "dmg") != 0 && strcmp(hardware, "cgb") != 0) ||
        mapper_mode_state < 0 ||
        (strcmp(mapper_mode, "reset") != 0 && strcmp(mapper_mode, "seeded") != 0) ||
        mapper_rom_state < 0 || mapper_ram_state < 0 || mapper_vram_state < 0 ||
        mapper_enable_state < 0 || mapper_rom_bank > 0x1ff ||
        mapper_hbank_state < 0 || mapper_hbank_rom > 0xff ||
        mapper_ram_bank > 0xff || mapper_vram_bank > 1 || mapper_ram_enable > 1) {
        fail("SCHEMA", "entry, registers, mapper, and finite budgets are required");
    }
    size_t rom_size = 0;
    uint8_t *rom = read_file(argv[2], &rom_size);
    if (!rom) fail("ARTIFACT", "ROM could not be read");

    GBConfig config = {0};
    config.model = strcmp(hardware, "cgb") == 0 ? GB_MODEL_CGB : GB_MODEL_DMG;
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
    seed_call_environment(ctx);
    if (strcmp(mapper_mode, "seeded") == 0) {
        seed_mapper_shadows(ctx, mapper_rom_bank, mapper_ram_bank, mapper_ram_enable);
    } else {
        gb_write8(ctx, 0xFF80, 0);
        gb_write8(ctx, 0xFF81, 0);
        gb_write8(ctx, 0xFF82, 0);
    }
    gb_write8(ctx, 0xFF4F, (uint8_t)mapper_vram_bank);
    ctx->sp = 0xfffe;
    gb_push16(ctx, 0xfea0);
    ctx->pc = (uint16_t)entry;
    set_call_registers(ctx, reg_a, reg_f, reg_b, reg_c, reg_d, reg_e, reg_hl);
    if (seed_wram_state == 1 && !apply_seed_spans(ctx, seed_wram)) {
        gb_context_destroy(ctx);
        free(rom);
        fail("SCHEMA", "seed_wram must contain address=hex spans");
    }
    if (seed_sram_state == 1 &&
        !apply_banked_spans(ctx, seed_sram, ctx->eram, ctx->eram_size, 0xa000, 4)) {
        gb_context_destroy(ctx);
        free(rom);
        fail("SCHEMA", "seed_sram must contain bank:address=hex spans");
    }
    if (seed_vram_state == 1 &&
        !apply_banked_spans(ctx, seed_vram, ctx->vram, 2u * 0x2000u, 0x8000, 2)) {
        gb_context_destroy(ctx);
        free(rom);
        fail("SCHEMA", "seed_vram must contain bank:address=hex spans");
    }
    uint64_t steps = 0;
    uint64_t cycles = 0;
    size_t input_index = 0;
    uint64_t frame_cycles = 0;
    uint64_t real_boundaries = 0, synth_vblanks = 0;
    g_joypad_buttons = input_count ? input_buttons[0] : 0xff;
    g_joypad_dpad = input_count ? input_dpad[0] : 0xff;
    for (size_t i = 0; i < setup_count; i++) {
        SetupCall *call = &setup_calls[i];
        seed_mapper_shadows(ctx, call->rom_bank, mapper_ram_bank, mapper_ram_enable);
        ctx->sp = 0xfffe;
        gb_push16(ctx, 0xfea0);
        ctx->pc = (uint16_t)call->entry;
        set_call_registers(ctx, call->a, call->f, call->b, call->c,
                           call->d, call->e, call->hl);
        uint64_t setup_steps = 0, setup_cycles = 0;
        while (ctx->pc != 0xfea0) {
            if (setup_steps >= instruction_budget || setup_cycles >= cycle_budget) {
                gb_context_destroy(ctx);
                free(rom);
                fail("SCHEMA", "setup exceeds execution budget");
            }
            uint32_t before = ctx->cycles;
            service_pending_interrupt(ctx);
            gb_debug_step(ctx, GB_EXECUTION_INTERPRETER);
            uint32_t delta = ctx->cycles - before;
            if (delta == 0) {
                gb_context_destroy(ctx);
                free(rom);
                fail("BACKEND_UNHEALTHY", "setup made no progress");
            }
            setup_steps++;
            setup_cycles += delta;
        }
    }
    if (strcmp(mapper_mode, "seeded") == 0)
        seed_mapper_shadows(ctx, mapper_rom_bank, mapper_ram_bank, mapper_ram_enable);
    /* seed_mapper_shadows ties hBankROM to rom_bank, which is right for paging
     * but wrong for a routine that re-reads hBankROM as data. An explicit
     * hbank_rom overrides it after the shadows are laid down. */
    if (mapper_hbank_state == 1)
        gb_write8(ctx, 0xFF80, (uint8_t)mapper_hbank_rom);
    int vblank_scheduler_armed = input_count > 0 || (gb_read8(ctx, 0xff40) & 0x80);
    if (vblank_scheduler_armed) {
        gb_write8(ctx, 0xffff, (uint8_t)(gb_read8(ctx, 0xffff) | 0x01));
        ctx->ime = 1;
    }
    ctx->sp = 0xfffe;
    gb_push16(ctx, 0xfea0);
    /* Sentinel first, so it stays the deepest word: the routine's final `ret`
     * must still land on it after popping every caller-pushed save below. */
    for (size_t i = 0; i < stack_count; i++)
        gb_push16(ctx, stack_words[i]);
    ctx->pc = (uint16_t)entry;
    set_call_registers(ctx, reg_a, reg_f, reg_b, reg_c, reg_d, reg_e, reg_hl);
    while (strcmp(completion, "event") == 0
               ? ((gb_read8(ctx, (uint16_t)event_addr) & (uint8_t)event_mask)
                  != (uint8_t)event_value)
               : ctx->pc != (strcmp(completion, "pre-ret") == 0 ? stop_pc : 0xfea0)) {
        if (steps >= instruction_budget || cycles >= cycle_budget) {
            /* A budget death parked in a halt is the common trap, and pc alone
             * cannot tell a spin apart from a wait for an interrupt that can
             * never arrive. Report the machine state that decides it: rLCDC
             * gates whether the PPU still publishes VBlank at all, and IF/IE
             * with halted say whether the wake condition is merely masked. */
            const GBPPU *view = (const GBPPU *)ctx->ppu;
            fprintf(stdout, "{\"status\":\"BUDGET_EXHAUSTED\",\"pc\":%u,\"sp\":%u,"
                    "\"instructions\":%" PRIu64 ",\"cycles\":%" PRIu64 ","
                    "\"lcdc\":%u,\"if\":%u,\"ie\":%u,\"ime\":%u,\"halted\":%u,"
                    "\"frame_cycles\":%" PRIu64 ",\"real_boundaries\":%" PRIu64 ","
                    "\"synth_vblanks\":%" PRIu64 ","
                    "\"ppu_lcdc\":%u,\"ppu_ly\":%u,\"ppu_mode\":%u,\"bus\":\"",
                    ctx->pc, ctx->sp, steps, cycles,
                    gb_read8(ctx, 0xff40), gb_read8(ctx, 0xff0f),
                    gb_read8(ctx, 0xffff), (unsigned)(ctx->ime ? 1 : 0),
                    (unsigned)(ctx->halted ? 1 : 0),
                    frame_cycles, real_boundaries, synth_vblanks,
                    view ? view->lcdc : 0u, view ? view->ly : 0u,
                    view ? (unsigned)view->mode : 0u);
            print_bus_spans(ctx, bus_addresses, bus_sizes, bus_count);
            fprintf(stdout, "\"}\n");
            gb_context_destroy(ctx);
            free(rom);
            return 4;
        }
        if (!vblank_scheduler_armed && (gb_read8(ctx, 0xff40) & 0x80)) {
            gb_write8(ctx, 0xffff, (uint8_t)(gb_read8(ctx, 0xffff) | 0x01));
            ctx->ime = 1;
            vblank_scheduler_armed = 1;
        }
        uint32_t before = ctx->cycles;
        service_pending_interrupt(ctx);
        gb_debug_step(ctx, GB_EXECUTION_INTERPRETER);
        uint32_t delta = ctx->cycles - before;
        if (delta == 0) {
            gb_context_destroy(ctx);
            free(rom);
            fail("BACKEND_UNHEALTHY", "interpreter made no progress");
        }
        steps++;
        cycles += delta;

        /*
         * gb_tick stops execution at the rendered-frame boundary so the
         * scheduler can publish VBlank and service the ROM's own ISR.  A
         * call-level runner has no outer frame scheduler, therefore retire
         * that boundary here after the instruction has completed.  IF/IE and
         * HALT state are intentionally left intact; the next debug step
         * observes the pending interrupt through the normal GBRT path.
         *
         * With the LCD disabled the PPU publishes no frames at all, so the
         * input timeline has to be driven by elapsed time instead. Without
         * that, a routine polling the joypad with the screen off - DoFrame's
         * game_paused_loop, say - never observes a second key state and spins
         * until its budget dies. One DMG frame is 70224 cycles.
         */
        frame_cycles += delta;
        int boundary = gb_frame_complete(ctx);
        if (boundary) {
            real_boundaries++;
            gb_reset_frame(ctx);
        } else if (frame_cycles >= 70224u &&
                   (!(gb_read8(ctx, 0xff40) & 0x80) || ctx->halted)) {
            boundary = 1;
            /* The runtime does not advance the PPU while the CPU is halted, so
             * gb_frame_complete never fires and a `halt` waiting on VBlank
             * (WaitForVBlank: halt / nop / cp [hl]) deadlocks with rLY frozen
             * mid-frame. Raise the request the PPU would have raised at line
             * 144; service_pending_interrupt then clears `halted` and dispatches
             * the ISR. Only the halted, LCD-on case is new -- LCD-off keeps its
             * existing synthetic boundary and running code is untouched. */
            if (ctx->halted && (gb_read8(ctx, 0xff40) & 0x80))
                gb_write8(ctx, 0xff0f,
                          (uint8_t)(gb_read8(ctx, 0xff0f) | 0x01));
            synth_vblanks++;
        }
        if (boundary) {
            frame_cycles = 0;
            if (input_count > 1) {
                input_index = (input_index + 1) % input_count;
                g_joypad_buttons = input_buttons[input_index];
                g_joypad_dpad = input_dpad[input_index];
            }
        }
    }
    print_result(ctx, completion, steps, cycles, bus_addresses, bus_sizes, bus_count);
    gb_context_destroy(ctx);
    free(rom);
    return 0;
}
