#ifndef POKETCG_HOME_LEGENDARY_ARTICUNO_H
#define POKETCG_HOME_LEGENDARY_ARTICUNO_H

#include <stdint.h>

/* >>> factory ScoreLegendaryArticunoCards */
void ScoreLegendaryArticunoCards(void);
/* <<< factory ScoreLegendaryArticunoCards */
/* >>> factory AIDoTurn_LegendaryArticuno */
typedef struct { uint8_t f; } AIDoTurn_LegendaryArticunoResult;
AIDoTurn_LegendaryArticunoResult AIDoTurn_LegendaryArticuno(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory AIDoTurn_LegendaryArticuno */
#endif /* POKETCG_HOME_LEGENDARY_ARTICUNO_H */
