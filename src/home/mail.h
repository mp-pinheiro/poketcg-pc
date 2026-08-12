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
#endif
