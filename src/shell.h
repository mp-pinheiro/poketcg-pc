#ifndef POKETCG_SHELL_H
#define POKETCG_SHELL_H

#include <stddef.h>
#include <stdint.h>

#include "input.h"
#include "ppu.h"

typedef struct Shell Shell;

typedef struct {
	int headless;
} ShellConfig;

Shell *shell_create(const ShellConfig *config);
void shell_destroy(Shell *shell);
int shell_pump(Shell *shell, InputFrame *frame);
void shell_present(Shell *shell, const uint16_t *framebuffer);
void shell_queue_audio(Shell *shell, const int16_t *samples, size_t count);

/* "sdl" or "headless" -- the backend actually in use, which is not simply the inverse
 * of ShellConfig.headless: shell_create falls back when SDL is absent or SDL_Init fails. */
const char *shell_backend_name(const Shell *shell);

#endif
