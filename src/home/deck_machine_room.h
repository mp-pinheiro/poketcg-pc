#ifndef POKETCG_HOME_DECK_MACHINE_ROOM_H
#define POKETCG_HOME_DECK_MACHINE_ROOM_H
#include <stdint.h>
typedef struct {uint8_t a;uint8_t b;uint8_t c;uint16_t hl;} FuncD96cResult;
FuncD96cResult Func_d96c(uint8_t a); void Script_BeatAaron(void);
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
#endif
