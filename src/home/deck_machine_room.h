#ifndef POKETCG_HOME_DECK_MACHINE_ROOM_H
#define POKETCG_HOME_DECK_MACHINE_ROOM_H
#include <stdint.h>
typedef struct {uint8_t a;uint8_t b;uint8_t c;uint16_t hl;} FuncD96cResult;
FuncD96cResult Func_d96c(uint8_t a);
/* >>> factory Script_BeatAaron */
typedef struct { uint8_t a; uint8_t c; } ScriptBeatAaronResult;
ScriptBeatAaronResult Script_BeatAaron(void);
/* <<< factory Script_BeatAaron */
/* >>> factory Script_d93f */
FuncD96cResult Script_d93f(void);
/* <<< factory Script_d93f */
/* >>> factory Script_d995 */
FuncD96cResult Script_d995(void);
/* <<< factory Script_d995 */
/* >>> factory Script_da49 */
FuncD96cResult Script_da49(void);
/* <<< factory Script_da49 */
/* >>> factory Script_daa3 */
FuncD96cResult Script_daa3(void);
/* <<< factory Script_daa3 */
/* >>> factory DeckMachineRoomCloseTextBox */
void DeckMachineRoomCloseTextBox(void);
/* <<< factory DeckMachineRoomCloseTextBox */
/* >>> factory DeckMachineRoomAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } DeckMachineRoomAfterDuelResult;
DeckMachineRoomAfterDuelResult DeckMachineRoomAfterDuel(void);
/* <<< factory DeckMachineRoomAfterDuel */
/* >>> factory Script_da76 */
void Script_da76(void);
/* <<< factory Script_da76 */
/* >>> factory Script_da1c */
void Script_da1c(void);
/* <<< factory Script_da1c */
/* >>> factory Script_d9c2 */
void Script_d9c2(void);
/* <<< factory Script_d9c2 */
/* >>> factory Script_d9ef */
void Script_d9ef(void);
/* <<< factory Script_d9ef */
#define Script_BeatAaron_START_SCRIPT 0x590bu
#define Script_d93f_START_SCRIPT 0x5944u
#define Script_d995_START_SCRIPT 0x599au
#define Script_d9c2_START_SCRIPT 0x59c7u
#define Script_d9ef_START_SCRIPT 0x59f4u
#define Script_da1c_START_SCRIPT 0x5a21u
#define Script_da49_START_SCRIPT 0x5a4eu
#define Script_da76_START_SCRIPT 0x5a7bu
#define Script_daa3_START_SCRIPT 0x5aa8u
#endif
