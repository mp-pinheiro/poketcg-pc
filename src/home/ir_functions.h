#ifndef POKETCG_HOME_IR_FUNCTIONS_H
#define POKETCG_HOME_IR_FUNCTIONS_H

#include <stdint.h>

void PlayCardPopSong(void);

/* >>> factory InitIRCommunications */
void InitIRCommunications(uint8_t a);
/* <<< factory InitIRCommunications */
/* >>> factory LoadLinkConnectingScene */
void LoadLinkConnectingScene(uint16_t hl);
/* <<< factory LoadLinkConnectingScene */
/* >>> factory ClearRPAndRestoreVBlankFunction */
void ClearRPAndRestoreVBlankFunction(void);
/* <<< factory ClearRPAndRestoreVBlankFunction */
#endif
