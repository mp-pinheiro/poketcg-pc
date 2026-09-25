#ifndef POKETCG_SHELL_H
#define POKETCG_SHELL_H

#include <stddef.h>
#include <stdint.h>

#include "input.h"
#include "ppu.h"

typedef struct Shell Shell;

typedef struct {
	int headless;
	int width;
} ShellConfig;

typedef struct {
	InputFrame game;
	uint8_t debug_toggle;
	uint8_t pressed;
} ShellInput;

typedef struct {
	const char *title;
	const char *const *lines;
	size_t line_count;
	size_t selected;
} ShellDebugView;

Shell *shell_create(const ShellConfig *config);
void shell_destroy(Shell *shell);
int shell_pump(Shell *shell, ShellInput *input);
uint8_t shell_hkeys_from_input(uint8_t buttons);
void shell_present(Shell *shell, const uint16_t *framebuffer);
void shell_present_debug(Shell *shell, uint16_t *framebuffer, const ShellDebugView *view);
void shell_queue_audio(Shell *shell, const int16_t *samples, size_t count);
void shell_set_speed(Shell *shell, unsigned speed);

/* "sdl" or "headless" -- the backend actually in use, which is not simply the inverse
 * of ShellConfig.headless: shell_create falls back when SDL is absent or SDL_Init fails. */
const char *shell_backend_name(const Shell *shell);
int shell_has_window(const Shell *shell);

/* Sleep the host thread until the next PPU-frame slot (59.7275 Hz). No-op without a
 * window. The worker is parked at the frame boundary while this runs, so pacing
 * cannot change game state -- it only decides how fast a human sees it. */
void shell_pace(Shell *shell);

/* Window title, and raising the window with keyboard focus: a replayed prefix
 * ends with the human's hands still on the terminal, so the hand-over both
 * announces itself and grabs the keyboard. No-ops without a window. */
void shell_set_title(Shell *shell, const char *title);
void shell_take_focus(Shell *shell);

#endif
