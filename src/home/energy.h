#ifndef POKETCG_HOME_ENERGY_H
#define POKETCG_HOME_ENERGY_H

#include <stdint.h>

/* >>> factory RetrievePlayAreaAIScoreFromBackup1 */
typedef struct { uint16_t de, hl; } Backup1Result;
Backup1Result RetrievePlayAreaAIScoreFromBackup1(void);
/* <<< factory RetrievePlayAreaAIScoreFromBackup1 */
#endif /* POKETCG_HOME_ENERGY_H */
