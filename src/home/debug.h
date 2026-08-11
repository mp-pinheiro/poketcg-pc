#ifndef POKETCG_HOME_DEBUG_H
#define POKETCG_HOME_DEBUG_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
} DebugResult;

DebugResult DebugSGBFrame(void);
DebugResult DebugStandardBGCharacter(void);
DebugResult DebugQuit(uint8_t a);

#endif
