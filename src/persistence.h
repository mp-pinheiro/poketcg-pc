#ifndef POKETCG_PERSISTENCE_H
#define POKETCG_PERSISTENCE_H

int sram_save_atomic(const char *path);
int sram_load(const char *path);
int file_replace(const char *from, const char *to);

#endif
