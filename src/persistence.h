#ifndef POKETCG_PERSISTENCE_H
#define POKETCG_PERSISTENCE_H
#include "profile.h"

#include <stdint.h>

#define SAVE_PAYLOAD_SIZE 0x8000u

int sram_save_atomic(const char *path, ProfileId profile);
int sram_load(const char *path, ProfileId profile);
int sram_read_payload(const char *path, ProfileId profile, uint8_t *payload);
int file_replace(const char *from, const char *to);

#endif
