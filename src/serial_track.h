#ifndef POKETCG_SERIAL_TRACK_H
#define POKETCG_SERIAL_TRACK_H

#include <stdint.h>

#define SERIAL_TRACK_TRANSFER 0u
#define SERIAL_TRACK_TIMER 1u

extern uint8_t g_serial_track_watch[0x10000u >> 3];
extern int g_serial_track_on;

int serial_track_load(const char *path);
void serial_track_free(void);
void serial_track_begin_interval(uint32_t interval);
void serial_track_access(void);
void serial_track_anchor(void);
void serial_track_residue(uint8_t known, uint8_t bytes[8]);
uint32_t serial_track_mismatches(void);
uint32_t serial_track_first_mismatch(void);

static inline int serial_track_watches(uint16_t addr)
{
	return g_serial_track_on && (g_serial_track_watch[addr >> 3] >> (addr & 7u) & 1u);
}

#endif
