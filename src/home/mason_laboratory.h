/* >>> part includes */
#include "generated/rom.h"
/* <<< part includes */
#ifndef POKETCG_HOME_MASON_LABORATORY_H
#define POKETCG_HOME_MASON_LABORATORY_H

/* >>> part includes_tail */
#include <stdint.h>
/* <<< part includes_tail */

/* >>> factory Func_d703 */
typedef struct { uint8_t a; uint8_t f; } FuncD703Result;
FuncD703Result Func_d703(void);
/* <<< factory Func_d703 */
/* >>> factory Preload_DrMason */
typedef struct { uint8_t a; uint8_t f; } PreloadDrMasonResult;
PreloadDrMasonResult Preload_DrMason(void);
/* <<< factory Preload_DrMason */
/* >>> factory Preload_Sam */
typedef struct { uint8_t a; uint8_t f; } PreloadSamResult;
PreloadSamResult Preload_Sam(void);
/* <<< factory Preload_Sam */
/* >>> factory Preload_Tech5 */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } PreloadTech5Result;
PreloadTech5Result Preload_Tech5(uint16_t hl);
/* <<< factory Preload_Tech5 */
/* >>> factory MasonLaboratoryAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } MasonLaboratoryAfterDuelResult;
MasonLaboratoryAfterDuelResult MasonLaboratoryAfterDuel(void);
/* <<< factory MasonLaboratoryAfterDuel */
/* >>> factory MasonLabCloseTextBox */
void MasonLabCloseTextBox(void);
/* <<< factory MasonLabCloseTextBox */
/* >>> factory MasonLabLoadMap */
void MasonLabLoadMap(void);
/* <<< factory MasonLabLoadMap */
/* >>> factory MasonLabPressedA */
typedef struct { uint16_t hl; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint8_t carry; } MasonLabPressedAResult;
MasonLabPressedAResult MasonLabPressedA(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory MasonLabPressedA */
/* >>> factory Script_Tech1 */
typedef struct { uint8_t a; uint8_t b; uint8_t c; uint16_t hl; } ScriptTech1Result;
ScriptTech1Result Script_Tech1(void);
/* <<< factory Script_Tech1 */
/* >>> part Script_Tech1_START_SCRIPT */
#define Script_Tech1_START_SCRIPT (Script_Tech1_ADDR + 0x14u)
/* <<< part Script_Tech1_START_SCRIPT */
#endif /* POKETCG_HOME_MASON_LABORATORY_H */
