#ifndef POKETCG_HOME_TRAINER_CARDS_H
#define POKETCG_HOME_TRAINER_CARDS_H

#include <stdint.h>

/* >>> factory RemoveCardFromList */
void RemoveCardFromList(uint16_t *hl);
/* <<< factory RemoveCardFromList */
/* >>> factory FindDuplicateCards */
typedef struct { uint8_t a, f; uint16_t hl; } FindDupResult;
FindDupResult FindDuplicateCards(uint16_t hl);
/* <<< factory FindDuplicateCards */
/* >>> factory FindAndRemoveCardFromList */
void FindAndRemoveCardFromList(uint8_t a, uint16_t hl);
/* <<< factory FindAndRemoveCardFromList */
/* >>> factory PickPokedexCards */
typedef struct { uint8_t a, f; } PickPokedexResult;
PickPokedexResult PickPokedexCards(void);
/* <<< factory PickPokedexCards */
/* >>> factory AIDecide_Maintenance */
typedef struct { uint8_t a, f; } AIDecideMaintenanceResult;
AIDecideMaintenanceResult AIDecide_Maintenance(void);
/* <<< factory AIDecide_Maintenance */
/* >>> factory AIDecide_Lass */
typedef struct { uint8_t f; } AIDecideResult;
AIDecideResult AIDecide_Lass(void);
/* <<< factory AIDecide_Lass */
/* >>> factory AIDecide_Imakuni */
AIDecideResult AIDecide_Imakuni(void);
/* <<< factory AIDecide_Imakuni */
/* >>> factory AIDecide_Defender_Phase14 */
AIDecideResult AIDecide_Defender_Phase14(void);
/* <<< factory AIDecide_Defender_Phase14 */
/* >>> factory AIDecide_Bill */
AIDecideResult AIDecide_Bill(void);
/* <<< factory AIDecide_Bill */
/* >>> factory AIDecide_PokemonFlute */
typedef struct { uint8_t a, f; } AIDecidePokemonFluteResult;
AIDecidePokemonFluteResult AIDecide_PokemonFlute(uint8_t c);
/* <<< factory AIDecide_PokemonFlute */
/* >>> factory AIDecide_ClefairyDollOrMysteriousFossil */
AIDecidePokemonFluteResult AIDecide_ClefairyDollOrMysteriousFossil(void);
/* <<< factory AIDecide_ClefairyDollOrMysteriousFossil */
#endif /* POKETCG_HOME_TRAINER_CARDS_H */
