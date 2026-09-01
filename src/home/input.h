#ifndef POKETCG_HOME_INPUT_H
#define POKETCG_HOME_INPUT_H

#include <stdint.h>

void ReadJoypad(void);
void SaveButtonsHeld(uint8_t c);
void ClearJoypad(uint16_t *hl);

/* Boot-restart hook for the A+B+Start+Select soft reset (input.asm Reset).
 * The host loop (src/runtime.c run_game) installs a setjmp-guarded restart
 * that re-runs Start(wInitialA); GameLoop();. NULL default: Reset() falls
 * through to its bounded probe behavior. */
extern void (*poketcg_request_boot_restart)(void);

/* >>> factory Reset */
uint8_t Reset(void);
/* <<< factory Reset */
#endif
