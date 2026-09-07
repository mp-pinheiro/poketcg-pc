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

/* DoFrame ordinal: the count of DoFrame iterations whose tail (WaitForVBlank,
 * ReadJoypad, HandleDPadRepeat) has completed. Advanced at the analogue of the
 * reference anchor $0552 (frames.asm: the instruction after `call
 * HandleDPadRepeat`), so service passes, DisableLCD's rLY poll and the debug
 * pause spin add nothing -- the two lanes count the same thing. The anchor hook
 * runs on the game thread right after the increment; the host is parked
 * waiting for the next boundary by then, so it may read any state. */
uint32_t frame_boundary_doframe_ordinal(void);
void frame_boundary_reset_ordinal(void);
void frame_boundary_install_anchor(FrameBoundaryHook hook, void *context);
/* True while the boundary pass a DoFrame's own halt reached is running, as
 * opposed to DisableLCD's rLY poll (src/home/lcd.c): only the former is the
 * VBlank the ROM's DoFrame waits for. */
int frame_boundary_pass_is_doframe(void);
/* Timer sync points: every routine through which game code observes
 * timer-ISR state -- the home/sound.asm wrappers (src/home/sound.c) and the
 * play-time counter's readers and writers (CopyGeneralSaveDataToSRAM,
 * PrintPlayTime, Func_c1b1, ExecuteGameEvent) -- calls this at entry, and the
 * host delivers the timer ISRs the ROM had fired by that point of the DoFrame
 * interval (src/runtime.c timer_sync; the same set is hooked on the
 * reference in tools/completion/session.py TIMER_SYNC). */
void frame_boundary_install_timer_sync(FrameBoundaryHook hook, void *context);
void frame_boundary_timer_sync(void);
/* The game's own writes to wVBlankCounter (core.asm:291, :6255): under a
 * lag track the host delivers the VBlank services the ROM saw before the
 * write here, so a counter the game resets mid-interval reads the same. */
void frame_boundary_install_vblank_sync(FrameBoundaryHook hook, void *context);
void frame_boundary_vblank_sync(void);
/* When the host replays a session with the ROM's own servicing schedule (the
 * lag track), the hand-placed frame_boundary_consume_services sites stand
 * down: the track already carries every VBlank they model. */
void frame_boundary_services_from_track(int enable);

void DoAFrames(uint8_t a);
void DoFrame(void);
/* Returns hl: the asm leaves it on hDPadRepeat whenever a direction is held. */
uint16_t HandleDPadRepeat(uint16_t hl);
#endif
