#include "shell.h"

#include "mem.h"

#include <stdlib.h>
#include <string.h>

#ifdef POKETCG_HAVE_SDL
#include <SDL2/SDL.h>
#endif

struct Shell {
	int headless;
#ifdef POKETCG_HAVE_SDL
	int have_audio;
	SDL_AudioDeviceID audio_device;
	SDL_Window *window;
	SDL_Renderer *renderer;
	SDL_Texture *texture;
#endif
};

static uint8_t row_value(uint8_t held, uint8_t mask)
{
	uint8_t value = 0x0F;
	for (unsigned i = 0; i < 4; i++) {
		if (held & (uint8_t)(mask << i))
			value &= (uint8_t)~(1u << i);
	}
	return value;
}

uint8_t joypad_p1(uint8_t held, uint8_t select_bits)
{
	uint8_t result = (uint8_t)(0xC0 | (select_bits & 0x30) | 0x0F);
	if (!(select_bits & 0x10))
		result = (uint8_t)((result & 0xF0) | row_value(held, BTN_RIGHT));
	if (!(select_bits & 0x20))
		result = (uint8_t)((result & 0x0F) | (uint8_t)(row_value(held, BTN_A) << 4));
	return result;
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
			if (event.type == SDL_KEYDOWN || event.type == SDL_KEYUP) {
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
				if (bit) {
					if (event.type == SDL_KEYDOWN)
						frame->buttons |= bit;
					else
						frame->buttons &= (uint8_t)~bit;
				}
			}
		}
	}
#else
	(void)shell;
#endif
	gb_write8(0xFF00, joypad_p1(frame->buttons, (uint8_t)(g_io[0] & 0x30)));
	g_keys = frame->buttons;
	return 1;
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
