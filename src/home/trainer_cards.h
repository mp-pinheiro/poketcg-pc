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
/* >>> factory AIDecide_Recycle */
AIDecideResult AIDecide_Recycle(void);
/* <<< factory AIDecide_Recycle */
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
/* >>> factory AIDecide_Gambler */
AIDecideResult AIDecide_Gambler(void);
/* <<< factory AIDecide_Gambler */
/* >>> factory AIDecide_Revive */
typedef struct { uint8_t a, f; } AIDecideReviveResult;
AIDecideReviveResult AIDecide_Revive(void);
/* <<< factory AIDecide_Revive */
/* >>> factory AIDecide_ImposterProfessorOak */
AIDecideResult AIDecide_ImposterProfessorOak(void);
/* <<< factory AIDecide_ImposterProfessorOak */
/* >>> factory PickPokedexCards_Unreferenced */
PickPokedexResult PickPokedexCards_Unreferenced(void);
/* <<< factory PickPokedexCards_Unreferenced */
/* >>> factory AIDecide_Pokedex */
typedef struct { uint8_t a; uint8_t f; } AIDecidePokedexResult;
AIDecidePokedexResult AIDecide_Pokedex(void);
/* <<< factory AIDecide_Pokedex */
/* >>> factory AIDecide_ItemFinder */
typedef struct { uint8_t a; uint8_t f; } AIDecide_ItemFinderResult;
AIDecide_ItemFinderResult AIDecide_ItemFinder(void);
/* <<< factory AIDecide_ItemFinder */
/* >>> factory AIDecide_EnergyRetrieval */
typedef struct { uint8_t a; uint8_t f; } AIDecideEnergyRetrievalResult;
AIDecideEnergyRetrievalResult AIDecide_EnergyRetrieval(uint8_t a);
/* <<< factory AIDecide_EnergyRetrieval */
/* >>> factory AIDecide_SuperEnergyRetrieval */
typedef struct { uint8_t a; uint8_t f; } AIDecideSuperEnergyRetrievalResult;
AIDecideSuperEnergyRetrievalResult AIDecide_SuperEnergyRetrieval(uint8_t a);
/* <<< factory AIDecide_SuperEnergyRetrieval */
#endif /* POKETCG_HOME_TRAINER_CARDS_H */
