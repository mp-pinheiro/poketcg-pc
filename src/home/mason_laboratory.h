#ifndef POKETCG_HOME_MASON_LABORATORY_H
#define POKETCG_HOME_MASON_LABORATORY_H

#include <stdint.h>

/* >>> factory Preload_DrMason */
typedef struct { uint8_t a; uint8_t f; } PreloadDrMasonResult;
PreloadDrMasonResult Preload_DrMason(void);
/* <<< factory Preload_DrMason */
/* >>> factory MasonLaboratoryAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } MasonLaboratoryAfterDuelResult;
MasonLaboratoryAfterDuelResult MasonLaboratoryAfterDuel(void);
/* <<< factory MasonLaboratoryAfterDuel */
/* >>> factory MasonLabCloseTextBox */
void MasonLabCloseTextBox(void);
/* <<< factory MasonLabCloseTextBox */
#endif /* POKETCG_HOME_MASON_LABORATORY_H */
