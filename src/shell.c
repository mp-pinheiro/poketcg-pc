#define _POSIX_C_SOURCE 200809L
#include "shell.h"

#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifdef POKETCG_HAVE_SDL
#include <SDL2/SDL.h>
#endif

/* One PPU frame: 1e9 * 70224 / 4194304 ns (59.7275 Hz), the same cadence the
 * runtime ages the hardware clock by (mem_advance_hardware_clock(70224)). */
#define POKETCG_FRAME_NS 16742706ull

struct Shell {
	int headless;
	/* Held buttons across host passes. SDL delivers press/release edges, so the
	 * pump has to keep the level itself or a held key lasts one pass. */
	uint8_t buttons;
	uint64_t next_ns;
#ifdef POKETCG_HAVE_SDL
	int have_audio;
	SDL_AudioDeviceID audio_device;
	SDL_Window *window;
	SDL_Renderer *renderer;
	SDL_Texture *texture;
#endif
};

uint8_t shell_hkeys_from_input(uint8_t buttons)
{
	return (uint8_t)((buttons << 4) | (buttons >> 4));
}

Shell *shell_create(const ShellConfig *config)
{
	Shell *shell = calloc(1, sizeof *shell);
	if (!shell)
		return NULL;
	shell->headless = config && config->headless;
#ifdef POKETCG_HAVE_SDL
	/* Video alone gates the window. Audio is a separate subsystem on purpose: a host
	 * with no audio device (CI, WSL without a dsp node) must still get a window, and
	 * initialising both in one SDL_Init would sink the video backend with it. */
	if (!shell->headless && SDL_Init(SDL_INIT_VIDEO) == 0) {
		shell->have_audio = SDL_InitSubSystem(SDL_INIT_AUDIO) == 0;
		if (shell->have_audio) {
			SDL_AudioSpec desired = {0};
			desired.freq = 44100;
			desired.format = AUDIO_S16SYS;
			desired.channels = 2;
			desired.samples = 1024;
			shell->audio_device = SDL_OpenAudioDevice(NULL, 0, &desired, NULL, 0);
			if (!shell->audio_device)
				shell->have_audio = 0;
			else
				SDL_PauseAudioDevice(shell->audio_device, 0);
		}
		shell->window = SDL_CreateWindow("poketcg", SDL_WINDOWPOS_UNDEFINED,
			SDL_WINDOWPOS_UNDEFINED, SCREEN_W * 3, SCREEN_H * 3, 0);
		shell->renderer = shell->window ? SDL_CreateRenderer(shell->window, -1,
			SDL_RENDERER_ACCELERATED) : NULL;
		shell->texture = shell->renderer ? SDL_CreateTexture(shell->renderer,
			SDL_PIXELFORMAT_BGR555, SDL_TEXTUREACCESS_STREAMING, SCREEN_W, SCREEN_H) : NULL;
		if (!shell->texture) {
			if (shell->renderer)
				SDL_DestroyRenderer(shell->renderer);
			if (shell->window)
				SDL_DestroyWindow(shell->window);
			shell->renderer = NULL;
			shell->window = NULL;
			shell->headless = 1;
		}
	} else {
		shell->headless = 1;
	}
#else
	shell->headless = 1;
#endif
	return shell;
}

void shell_destroy(Shell *shell)
{
	if (!shell)
		return;
#ifdef POKETCG_HAVE_SDL
	if (shell->audio_device)
		SDL_CloseAudioDevice(shell->audio_device);
	if (shell->texture)
		SDL_DestroyTexture(shell->texture);
	if (shell->renderer)
		SDL_DestroyRenderer(shell->renderer);
	if (shell->window)
		SDL_DestroyWindow(shell->window);
	SDL_Quit();
#endif
	free(shell);
}

const char *shell_backend_name(const Shell *shell)
{
	return shell && !shell->headless ? "sdl" : "headless";
}

int shell_has_window(const Shell *shell)
{
	return shell && !shell->headless;
}

int shell_pump(Shell *shell, InputFrame *frame)
{
	if (!shell || !frame)
		return 0;
#ifdef POKETCG_HAVE_SDL
	if (!shell->headless) {
		SDL_Event event;
		while (SDL_PollEvent(&event)) {
			if (event.type == SDL_QUIT)
				return 0;
			if (event.type != SDL_KEYDOWN && event.type != SDL_KEYUP)
				continue;
			/* OS key-repeat re-delivers KEYDOWN for a held key; the game reads
			 * edge-triggered hKeysPressed, so a repeat must not be a new edge. */
			if (event.key.repeat)
				continue;
			uint8_t bit = 0;
			switch (event.key.keysym.sym) {
			case SDLK_RIGHT: bit = BTN_RIGHT; break;
			case SDLK_LEFT: bit = BTN_LEFT; break;
			case SDLK_UP: bit = BTN_UP; break;
			case SDLK_DOWN: bit = BTN_DOWN; break;
			case SDLK_z: bit = BTN_A; break;
			case SDLK_x: bit = BTN_B; break;
			case SDLK_BACKSPACE: bit = BTN_SELECT; break;
			case SDLK_RETURN: bit = BTN_START; break;
			default: break;
			}
			if (!bit)
				continue;
			if (event.type == SDL_KEYDOWN)
				shell->buttons |= bit;
			else
				shell->buttons &= (uint8_t)~bit;
		}
	}
#endif
	frame->buttons = shell->buttons;
	return 1;
}

void shell_pace(Shell *shell)
{
	if (!shell_has_window(shell))
		return;
	struct timespec ts;
	clock_gettime(CLOCK_MONOTONIC, &ts);
	uint64_t now = (uint64_t)ts.tv_sec * 1000000000ull + (uint64_t)ts.tv_nsec;
	/* More than four frames behind: drop the debt rather than free-run to
	 * catch up, so a stall never turns into a burst. */
	if (shell->next_ns == 0 || now > shell->next_ns + 4u * POKETCG_FRAME_NS)
		shell->next_ns = now;
	if (now < shell->next_ns) {
		uint64_t wait = shell->next_ns - now;
		struct timespec req;
		req.tv_sec = (time_t)(wait / 1000000000ull);
		req.tv_nsec = (long)(wait % 1000000000ull);
		nanosleep(&req, NULL);
	}
	shell->next_ns += POKETCG_FRAME_NS;
}

void shell_set_title(Shell *shell, const char *title)
{
#ifdef POKETCG_HAVE_SDL
	if (shell_has_window(shell) && shell->window)
		SDL_SetWindowTitle(shell->window, title);
#else
	(void)shell;
	(void)title;
#endif
}

void shell_take_focus(Shell *shell)
{
#ifdef POKETCG_HAVE_SDL
	if (shell_has_window(shell) && shell->window) {
		SDL_RaiseWindow(shell->window);
		SDL_SetWindowInputFocus(shell->window);
	}
#else
	(void)shell;
#endif
}

void shell_present(Shell *shell, const uint16_t *framebuffer)
{
#ifdef POKETCG_HAVE_SDL
	if (!shell || shell->headless || !framebuffer)
		return;
	SDL_UpdateTexture(shell->texture, NULL, framebuffer, SCREEN_W * (int)sizeof *framebuffer);
	SDL_RenderClear(shell->renderer);
	SDL_RenderCopy(shell->renderer, shell->texture, NULL, NULL);
	SDL_RenderPresent(shell->renderer);
#else
	(void)shell;
	(void)framebuffer;
#endif
}

/* Queue interleaved signed 16-bit samples when SDL audio is available. */
void shell_queue_audio(Shell *shell, const int16_t *samples, size_t count)
{
#ifdef POKETCG_HAVE_SDL
	if (!shell || !shell->have_audio || !samples || !count)
		return;
	(void)SDL_QueueAudio(shell->audio_device, samples, count * sizeof *samples);
#else
	(void)shell;
	(void)samples;
	(void)count;
#endif
}
