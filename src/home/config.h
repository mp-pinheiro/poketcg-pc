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
/* >>> factory ShowConfigMenuCursor */
typedef struct { uint8_t b; uint8_t c; } ShowConfigMenuCursorResult;
ShowConfigMenuCursorResult ShowConfigMenuCursor(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory ShowConfigMenuCursor */
/* >>> factory HideConfigMenuCursor */
typedef struct { uint8_t b; uint8_t c; } HideConfigMenuCursorResult;
HideConfigMenuCursorResult HideConfigMenuCursor(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory HideConfigMenuCursor */
/* >>> factory ConfigScreenDPadLeft */
void ConfigScreenDPadLeft(void);
/* <<< factory ConfigScreenDPadLeft */
/* >>> factory ConfigScreenDPadRight */
void ConfigScreenDPadRight(void);
/* <<< factory ConfigScreenDPadRight */
/* >>> factory UpdateConfigMenuCursor */
typedef struct { uint8_t b; uint8_t c; } UpdateConfigMenuCursorResult;
UpdateConfigMenuCursorResult UpdateConfigMenuCursor(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory UpdateConfigMenuCursor */
#endif /* POKETCG_HOME_CONFIG_H */
