#ifndef POKETCG_HOME_FRAMES_H
#define POKETCG_HOME_FRAMES_H

#include <stdint.h>

typedef void (*FrameBoundaryHook)(void *context);
void frame_boundary_install(FrameBoundaryHook hook, void *context);

void frame_boundary_reach(void);
int frame_boundary_is_installed(void);

void DoAFrames(uint8_t a);
void DoFrame(void);
void HandleDPadRepeat(void);
#endif
