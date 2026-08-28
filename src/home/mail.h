#ifndef POKETCG_HOME_MAIL_H
#define POKETCG_HOME_MAIL_H

#include <stdint.h>

typedef struct {
	uint8_t b;
	uint8_t c;
} PCPackCoordinates;

PCPackCoordinates GePCPackSelectionCoordinates(void);
void TryGivePCPack(uint8_t id);

/* >>> factory InitPCPacks */
void InitPCPacks(void);
/* <<< factory InitPCPacks */
/* >>> factory DrawMailMenuCursor */
void DrawMailMenuCursor(uint8_t symbol);
/* <<< factory DrawMailMenuCursor */
/* >>> factory GetPCPackCoordinates */
PCPackCoordinates GetPCPackCoordinates(uint8_t pack);
/* <<< factory GetPCPackCoordinates */
/* >>> factory ShowMailMenuCursor */
void ShowMailMenuCursor(void);
/* <<< factory ShowMailMenuCursor */
/* >>> factory HideMailMenuCursor */
void HideMailMenuCursor(void);
/* <<< factory HideMailMenuCursor */
/* >>> factory PrintEmptyPCPackName */
void PrintEmptyPCPackName(uint8_t pack);
/* <<< factory PrintEmptyPCPackName */
/* >>> factory UpdateMailMenuCursor */
void UpdateMailMenuCursor(void);
/* <<< factory UpdateMailMenuCursor */
/* >>> factory PCMailHandleDPadInput */
void PCMailHandleDPadInput(void);
/* <<< factory PCMailHandleDPadInput */
/* >>> factory GetPCPackNameTextID */
uint16_t GetPCPackNameTextID(uint8_t a);
/* <<< factory GetPCPackNameTextID */
/* >>> factory PrintPCPackName */
typedef struct {
	uint8_t a;
} PrintPCPackNameResult;
PrintPCPackNameResult PrintPCPackName(uint8_t a);
/* <<< factory PrintPCPackName */
/* >>> factory PrintObtainedPCPacks */
void PrintObtainedPCPacks(void);
/* <<< factory PrintObtainedPCPacks */
/* >>> factory BlinkUnopenedPCPacks */
/* >>> factory BlinkUnopenedPCPacks */
void BlinkUnopenedPCPacks(void);
/* <<< factory BlinkUnopenedPCPacks */
/* >>> factory TryOpenPCMailBoosterPack */
/* mail.asm:263. The tail is `call DisableLCD / ret`, and DisableLCD models no
 * register result, so nothing is returned. */
void TryOpenPCMailBoosterPack(void);
/* <<< factory TryOpenPCMailBoosterPack */
#endif
