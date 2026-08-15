#ifndef POKETCG_HOME_CONFIG_H
#define POKETCG_HOME_CONFIG_H

#include <stdint.h>

void DrawConfigMenuCursor(uint8_t a, uint8_t c);

/* >>> factory GetConfigCursorPositions */
void GetConfigCursorPositions(void);
/* <<< factory GetConfigCursorPositions */
/* >>> factory SaveConfigSettings */
void SaveConfigSettings(void);
/* <<< factory SaveConfigSettings */
#endif /* POKETCG_HOME_CONFIG_H */
