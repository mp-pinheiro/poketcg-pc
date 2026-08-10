#ifndef POKETCG_HOME_DUEL_CORE_STATUS_H
#define POKETCG_HOME_DUEL_CORE_STATUS_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint16_t hl;
	uint8_t f;
} DuelCoreStatusResult;

typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
	uint8_t f;
} DuelCoreStatusDiscardResult;

DuelCoreStatusResult IsArenaPokemonAsleepOrPoisoned(void);
DuelCoreStatusDiscardResult DiscardAttachedPlusPowers(void);
DuelCoreStatusDiscardResult DiscardAttachedDefenders(void);

#endif
