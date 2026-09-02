#ifndef POKETCG_HOME_FRAMES_H
#define POKETCG_HOME_FRAMES_H

#include <stdint.h>

typedef void (*FrameBoundaryHook)(void *context);
void frame_boundary_install(FrameBoundaryHook hook, void *context);

/* Bounds a routine whose asm never returns (a scene loop such as LoadMap's
 * .overworld_loop) when it runs under the probe. Deliberately separate from the
 * host hook above: frame_boundary_is_installed() means "the runtime host is
 * driving frames" and is what main_menu/intro/start/game_loop branch on, and
 * frame_boundary_consume_services() must stay a no-op in the probe world. A
 * watchdog changes neither. */
void frame_boundary_install_watchdog(FrameBoundaryHook hook, void *context);

void frame_boundary_reach(void);
void frame_boundary_consume_services(uint8_t count);
uint8_t frame_boundary_take_service_pass(void);
int frame_boundary_is_installed(void);

void DoAFrames(uint8_t a);
void DoFrame(void);
void HandleDPadRepeat(void);
#endif
