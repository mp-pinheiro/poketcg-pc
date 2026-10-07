#ifndef POKETCG_HOME_DUEL_CORE_STATUS_H
#define POKETCG_HOME_DUEL_CORE_STATUS_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part DuelCoreStatusResult */
typedef struct {
	uint8_t a;
	uint16_t hl;
	uint8_t f;
} DuelCoreStatusResult;
/* <<< part DuelCoreStatusResult */

/* >>> part DuelCoreStatusDiscardResult */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
	uint8_t f;
} DuelCoreStatusDiscardResult;
/* <<< part DuelCoreStatusDiscardResult */

/* >>> factory IsArenaPokemonAsleepOrPoisoned */
DuelCoreStatusResult IsArenaPokemonAsleepOrPoisoned(void);
/* <<< factory IsArenaPokemonAsleepOrPoisoned */
/* >>> factory DiscardAttachedPlusPowers */
DuelCoreStatusDiscardResult DiscardAttachedPlusPowers(void);
/* <<< factory DiscardAttachedPlusPowers */
/* >>> factory DiscardAttachedDefenders */
DuelCoreStatusDiscardResult DiscardAttachedDefenders(void);
/* <<< factory DiscardAttachedDefenders */

#endif
