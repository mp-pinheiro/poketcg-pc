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
	int width;
	uint8_t buttons;
	uint64_t next_ns;
	unsigned speed;
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
	shell->width = config && config->width > SCREEN_W ? config->width : SCREEN_W;
	shell->speed = 1u;
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
			SDL_WINDOWPOS_UNDEFINED, shell->width * 3, SCREEN_H * 3, 0);
		shell->renderer = shell->window ? SDL_CreateRenderer(shell->window, -1,
			SDL_RENDERER_ACCELERATED) : NULL;
		shell->texture = shell->renderer ? SDL_CreateTexture(shell->renderer,
			SDL_PIXELFORMAT_BGR555, SDL_TEXTUREACCESS_STREAMING, shell->width, SCREEN_H) : NULL;
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

int shell_pump(Shell *shell, ShellInput *input)
{
	if (!shell || !input)
		return 0;
	input->game.buttons = shell->buttons;
	input->debug_toggle = 0u;
	input->pressed = 0u;
#ifdef POKETCG_HAVE_SDL
	if (!shell->headless) {
		SDL_Event event;
		while (SDL_PollEvent(&event)) {
			if (event.type == SDL_QUIT)
				return 0;
			if (event.type != SDL_KEYDOWN && event.type != SDL_KEYUP)
				continue;
			if (event.key.repeat)
				continue;
			if (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_F1) {
				input->debug_toggle = 1u;
				continue;
			}
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
			if (event.type == SDL_KEYDOWN) {
				shell->buttons |= bit;
				input->pressed |= bit;
			}
			else
				shell->buttons &= (uint8_t)~bit;
		}
	}
#endif
	input->game.buttons = shell->buttons;
	return 1;
}
void shell_pace(Shell *shell)
{
	if (!shell_has_window(shell) || shell->speed == 0u)
		return;
	struct timespec ts;
	clock_gettime(CLOCK_MONOTONIC, &ts);
	uint64_t now = (uint64_t)ts.tv_sec * 1000000000ull + (uint64_t)ts.tv_nsec;
	uint64_t frame_ns = POKETCG_FRAME_NS / shell->speed;
	if (shell->next_ns == 0 || now > shell->next_ns + 4u * frame_ns)
		shell->next_ns = now;
	if (now < shell->next_ns) {
		uint64_t wait = shell->next_ns - now;
		struct timespec req;
		req.tv_sec = (time_t)(wait / 1000000000ull);
		req.tv_nsec = (long)(wait % 1000000000ull);
		nanosleep(&req, NULL);
	}
	shell->next_ns += frame_ns;
}
void shell_set_speed(Shell *shell, unsigned speed)
{
	if (!shell)
		return;
	shell->speed = speed == 1u || speed == 2u || speed == 4u ? speed : 0u;
	shell->next_ns = 0;
}

#ifdef POKETCG_DEBUG_MENU
static const uint8_t debug_font[37][7] = {
	{14,17,17,31,17,17,17},{30,17,17,30,17,17,30},{14,17,16,16,16,17,14},
	{30,17,17,17,17,17,30},{31,16,16,30,16,16,31},{31,16,16,30,16,16,16},
	{14,17,16,23,17,17,15},{17,17,17,31,17,17,17},{14,4,4,4,4,4,14},
	{1,1,1,1,17,17,14},{17,18,20,24,20,18,17},{16,16,16,16,16,16,31},
	{17,27,21,21,17,17,17},{17,25,21,19,17,17,17},{14,17,17,17,17,17,14},
	{30,17,17,30,16,16,16},{14,17,17,17,21,18,13},{30,17,17,30,20,18,17},
	{15,16,16,14,1,1,30},{31,4,4,4,4,4,4},{17,17,17,17,17,17,14},
	{17,17,17,17,17,10,4},{17,17,17,21,21,21,10},{17,17,10,4,10,17,17},
	{17,17,10,4,4,4,4},{31,1,2,4,8,16,31},
	{14,17,19,21,25,17,14},{4,12,4,4,4,4,14},{14,17,1,2,4,8,31},
	{30,1,1,14,1,1,30},{2,6,10,18,31,2,2},{31,16,16,30,1,1,30},
	{14,16,16,30,17,17,14},{31,1,2,4,8,8,8},{14,17,17,14,17,17,14},
	{14,17,1,6,8,0,8},{0,4,0,0,0,4,0}
};

static int debug_font_index(char c)
{
	if (c >= 'A' && c <= 'Z')
		return c - 'A';
	if (c >= '0' && c <= '9')
		return 26 + c - '0';
	return c == ':' ? 36 : -1;
}

static void debug_draw_text(uint16_t *buffer, int stride, int x, int y,
                            const char *text, uint16_t color)
{
	for (; *text && x < stride - 5; text++, x += 6) {
		int index = debug_font_index(*text);
		if (index < 0)
			continue;
		for (int row = 0; row < 7; row++)
			for (int col = 0; col < 5; col++)
				if (debug_font[index][row] & (1u << (4 - col)))
					buffer[(y + row) * stride + x + col] = color;
	}
}
#endif

void shell_present_debug(Shell *shell, uint16_t *framebuffer, const ShellDebugView *view)
{
#ifdef POKETCG_DEBUG_MENU
	if (!shell || !framebuffer || !view || !shell_has_window(shell))
		return;
	int width = shell->width;
	int panel_width = width > 158 ? 156 : width - 4;
	for (int y = 2; y < SCREEN_H - 2; y++)
		for (int x = 2; x < panel_width + 2; x++)
			framebuffer[y * width + x] = 0;
	debug_draw_text(framebuffer, width, 6, 6, view->title, 0x7FFF);
	for (size_t i = 0; i < view->line_count; i++) {
		int y = 18 + (int)i * 9;
		if (i == view->selected)
			for (int x = 4; x < panel_width; x++)
				for (int row = 0; row < 8; row++)
					framebuffer[(y - 1 + row) * width + x] = 0x03E0;
		debug_draw_text(framebuffer, width, 7, y, view->lines[i],
		                i == view->selected ? 0x0000 : 0x7FFF);
	}
#else
	(void)view;
#endif
	shell_present(shell, framebuffer);
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
	SDL_UpdateTexture(shell->texture, NULL, framebuffer, shell->width * (int)sizeof *framebuffer);
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
