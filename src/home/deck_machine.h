#ifndef POKETCG_HOME_DECK_MACHINE_H
#define POKETCG_HOME_DECK_MACHINE_H

#include <stdint.h>

/* >>> factory CheckIfSelectedDeckMachineEntryIsEmpty */
uint8_t CheckIfSelectedDeckMachineEntryIsEmpty(void);
/* <<< factory CheckIfSelectedDeckMachineEntryIsEmpty */
/* >>> factory SafelySwitchToSRAM1 */
void SafelySwitchToSRAM1(void);
/* <<< factory SafelySwitchToSRAM1 */
/* >>> factory SafelySwitchToTempSRAMBank */
void SafelySwitchToTempSRAMBank(void);
/* <<< factory SafelySwitchToTempSRAMBank */
/* >>> factory CheckIfHasEnoughCardsToBuildDeck */
typedef struct {
	uint8_t a;
	uint8_t f;
} DeckBuildCheckResult;

DeckBuildCheckResult CheckIfHasEnoughCardsToBuildDeck(uint16_t *hl);
/* <<< factory CheckIfHasEnoughCardsToBuildDeck */
/* >>> factory GetSavedDeckPointers */
void GetSavedDeckPointers(uint16_t *hl, uint16_t *de);
/* <<< factory GetSavedDeckPointers */
/* >>> factory GetSavedDeckCount */
void GetSavedDeckCount(void);
/* <<< factory GetSavedDeckCount */
/* >>> factory GetSelectedSavedDeckPtr */
uint16_t GetSelectedSavedDeckPtr(void);
/* <<< factory GetSelectedSavedDeckPtr */
/* >>> factory SafelySwitchToSRAM0 */
void SafelySwitchToSRAM0(void);
/* <<< factory SafelySwitchToSRAM0 */
/* >>> factory DrawListScrollArrows */
void DrawListScrollArrows(void);
/* <<< factory DrawListScrollArrows */
/* >>> factory SetDeckMachineTitleText */
typedef struct { uint16_t hl; } SetDeckMachineTitleTextResult;
SetDeckMachineTitleTextResult SetDeckMachineTitleText(void);
/* <<< factory SetDeckMachineTitleText */
/* >>> factory FindFirstEmptyDeckSlot */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } FindFirstEmptyDeckSlotResult;
FindFirstEmptyDeckSlotResult FindFirstEmptyDeckSlot(void);
/* <<< factory FindFirstEmptyDeckSlot */
/* >>> factory EmptyScreenAndDrawTextBox */
void EmptyScreenAndDrawTextBox(void);
/* <<< factory EmptyScreenAndDrawTextBox */
/* >>> factory PrintCardToSendText */
void PrintCardToSendText(void);
/* <<< factory PrintCardToSendText */
/* >>> factory PrintReceivedTheseCardsText */
void PrintReceivedTheseCardsText(void);
/* <<< factory PrintReceivedTheseCardsText */
/* >>> factory PrintNumSavedDecks */
void PrintNumSavedDecks(void);
/* <<< factory PrintNumSavedDecks */
/* >>> factory Func_b568 */
void Func_b568(void);
/* <<< factory Func_b568 */
/* >>> factory CheckIfCanBuildSavedDeck */
DeckBuildCheckResult CheckIfCanBuildSavedDeck(uint8_t a, uint8_t b);
/* <<< factory CheckIfCanBuildSavedDeck */
/* >>> factory PrintDeckMachineEntry */
typedef struct { uint8_t a; uint8_t f; } PrintDeckMachineEntryResult;
PrintDeckMachineEntryResult PrintDeckMachineEntry(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory PrintDeckMachineEntry */
/* >>> factory ShowReceivedCardsList */
void ShowReceivedCardsList(void);
/* <<< factory ShowReceivedCardsList */
/* >>> factory Func_b088 */
typedef struct { uint8_t a; uint8_t f; } Func_b088Result;
Func_b088Result Func_b088(void);
/* <<< factory Func_b088 */
/* >>> factory TryDeleteSavedDeck */
typedef struct { uint8_t a; uint8_t f; } TryDeleteSavedDeckResult;
TryDeleteSavedDeckResult TryDeleteSavedDeck(void);
/* <<< factory TryDeleteSavedDeck */
#endif /* POKETCG_HOME_DECK_MACHINE_H */
