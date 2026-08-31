#ifndef POKETCG_PERSISTENCE_H
#define POKETCG_PERSISTENCE_H

int sram_save_atomic(const char *path);
int sram_load(const char *path);

#endif
