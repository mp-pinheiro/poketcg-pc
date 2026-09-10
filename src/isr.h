#ifndef POKETCG_ISR_H
#define POKETCG_ISR_H

#include <stddef.h>
#include <stdint.h>

#define ISR_KIND_VBLANK 0u
#define ISR_KIND_STAT 1u

typedef struct {
	uint32_t *start;
	uint16_t *site;
	uint16_t *nth;
	uint8_t *kind;
	const void **site_fn;
	size_t sites;
	size_t records;
	size_t count;
} IsrTrack;

void isr_set_track(const IsrTrack *track);
void isr_begin_interval(uint32_t interval);
void isr_on_entry(const void *fn);
unsigned isr_close_interval(void);
uint32_t isr_placed(void);
uint32_t isr_unplaced(void);
int isr_active(void);

#endif /* POKETCG_ISR_H */
