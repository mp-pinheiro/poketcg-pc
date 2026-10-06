#ifndef POKETCG_PERSISTENCE_H
#define POKETCG_PERSISTENCE_H
#include "profile.h"

int sram_save_atomic(const char *path, ProfileId profile);
int sram_load(const char *path, ProfileId profile);
int file_replace(const char *from, const char *to);

#endif
