#ifndef POKETCG_ISR_H
#define POKETCG_ISR_H

#include <stddef.h>
#include <stdint.h>

#define ISR_KIND_VBLANK 0u
#define ISR_KIND_STAT 1u
#define ISR_KIND_SERIAL 2u
#define ISR_KIND_TIMER 3u

typedef struct {
	uint32_t *start;
	uint16_t *site;
	uint16_t *nth;
	uint8_t *kind;
	uint16_t *ordinal;
	uint8_t *value;
	const void **site_fn;
	int16_t *site_event;
	size_t sites;
	size_t records;
	size_t count;
} IsrTrack;

typedef void (*IsrDeliver)(uint32_t interval, unsigned kind, unsigned ordinal, uint8_t value);

void isr_set_track(const IsrTrack *track, IsrDeliver deliver);
void isr_begin_interval(uint32_t interval);
void isr_on_entry(const void *fn);
void isr_on_site(unsigned site);
void isr_close_interval(void);
void isr_context_enter(void);
void isr_context_leave(void);
int isr_in_context(void);
uint32_t isr_placed(void);
uint32_t isr_unplaced(void);

#endif
