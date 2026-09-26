#define _POSIX_C_SOURCE 200809L
#include "shell.h"
#include "runtime.h"
#include "mem.h"

#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdio.h>

#ifdef POKETCG_HAVE_SDL
#include <SDL2/SDL.h>
#endif
#ifdef POKETCG_HAVE_PULSE
#include <pulse/error.h>
#include <pulse/simple.h>
#endif

/* One PPU frame: 1e9 * 70224 / 4194304 ns (59.7275 Hz), the same cadence the
 * runtime ages the hardware clock by (mem_advance_hardware_clock(70224)). */
#define POKETCG_FRAME_NS 16742706ull
#define SHELL_AUDIO_BUFFER_SAMPLES 4096u
#define SHELL_PULSE_GAIN 4

struct Shell {
	int headless;
	int width;
	int game_width;
	int scale;
	PcOptions *options;
	uint8_t buttons;
	uint64_t next_ns;
	int height;
	PresentationMode presentation;
	unsigned speed;
	int sgb_border;
#ifdef POKETCG_HAVE_SDL
	int have_audio;
	SDL_AudioDeviceID audio_device;
#ifdef POKETCG_HAVE_PULSE
	int have_pulse;
	pa_simple *pulse_audio;
#endif
	SDL_Window *window;
	SDL_Renderer *renderer;
	SDL_Texture *texture;
	uint16_t *presentation_frame;
	int audio_filter_ready;
	int32_t audio_dc[2];
	int16_t audio_buffer[SHELL_AUDIO_BUFFER_SAMPLES];
#endif
};

uint8_t shell_hkeys_from_input(uint8_t buttons)
{
	return (uint8_t)((buttons << 4) | (buttons >> 4));
}

#ifdef POKETCG_HAVE_PULSE
static int shell_open_pulse_audio(Shell *shell)
{
	pa_sample_spec spec = {
		.format = PA_SAMPLE_S16NE,
		.rate = 44100,
		.channels = 2
	};
	int error = 0;
	shell->pulse_audio = pa_simple_new(
		NULL, "poketcg", PA_STREAM_PLAYBACK, NULL, "Game audio",
		&spec, NULL, NULL, &error);
	if (!shell->pulse_audio) {
		fprintf(stderr, "audio: PulseAudio unavailable: %s\n", pa_strerror(error));
		return 0;
	}
	shell->have_pulse = 1;
	fprintf(stderr, "audio: PulseAudio\n");
	return 1;
}
#endif

static int clamp_int(int value, int low, int high)
{
	if (value < low)
		return low;
	if (value > high)
		return high;
	return value;
}


#ifdef POKETCG_HAVE_SDL
static void destroy_video(Shell *shell)
{
	if (shell->texture)
		SDL_DestroyTexture(shell->texture);
	if (shell->renderer)
		SDL_DestroyRenderer(shell->renderer);
	if (shell->window)
		SDL_DestroyWindow(shell->window);
	free(shell->presentation_frame);
	shell->texture = NULL;
	shell->renderer = NULL;
	shell->window = NULL;
	shell->presentation_frame = NULL;
}

static int create_video(Shell *shell)
{
	if (shell->presentation == PRESENTATION_SGB_FRAME) {
		shell->width = PRESENTATION_SGB_WIDTH;
		shell->height = PRESENTATION_SGB_HEIGHT;
		shell->presentation_frame = calloc(
			(size_t)PRESENTATION_SGB_WIDTH * PRESENTATION_SGB_HEIGHT,
			sizeof *shell->presentation_frame);
	} else {
		shell->width = shell->game_width;
		shell->height = SCREEN_H;
	}
	if (shell->presentation == PRESENTATION_SGB_FRAME && !shell->presentation_frame)
		return -1;
	shell->window = SDL_CreateWindow("poketcg", SDL_WINDOWPOS_UNDEFINED,
		SDL_WINDOWPOS_UNDEFINED, shell->width * shell->scale,
		shell->height * shell->scale, 0);
	shell->renderer = shell->window ? SDL_CreateRenderer(shell->window, -1,
		SDL_RENDERER_ACCELERATED) : NULL;
	shell->texture = shell->renderer ? SDL_CreateTexture(shell->renderer,
		SDL_PIXELFORMAT_BGR555, SDL_TEXTUREACCESS_STREAMING,
		shell->width, shell->height) : NULL;
	if (!shell->texture)
		return -1;
	SDL_RenderSetLogicalSize(shell->renderer, shell->width, shell->height);
	return 0;
}

static int switch_presentation(Shell *shell)
{
	int width = shell->game_width;
	int height = SCREEN_H;
	uint16_t *frame = NULL;
	if (shell->presentation == PRESENTATION_SGB_FRAME) {
		width = PRESENTATION_SGB_WIDTH;
		height = PRESENTATION_SGB_HEIGHT;
		frame = calloc((size_t)width * height, sizeof *frame);
		if (!frame)
			return -1;
	}
	SDL_Texture *texture = SDL_CreateTexture(shell->renderer,
		SDL_PIXELFORMAT_BGR555, SDL_TEXTUREACCESS_STREAMING, width, height);
	if (!texture) {
		free(frame);
		return -1;
	}
	SDL_DestroyTexture(shell->texture);
	free(shell->presentation_frame);
	shell->texture = texture;
	shell->presentation_frame = frame;
	shell->width = width;
	shell->height = height;
	SDL_RenderSetLogicalSize(shell->renderer, width, height);
	SDL_SetWindowSize(shell->window, width * shell->scale, height * shell->scale);
	return 0;
}

static void set_scale(Shell *shell, int scale)
{
	shell->scale = clamp_int(scale, 1, 6);
	if (shell->window)
		SDL_SetWindowSize(shell->window, shell->width * shell->scale,
		                  shell->height * shell->scale);
}

#endif

Shell *shell_create(const ShellConfig *config)
{
	Shell *shell = calloc(1, sizeof *shell);
	if (!shell)
		return NULL;
	shell->headless = config && config->headless;
	shell->game_width = config && config->width >= SCREEN_W ? config->width : SCREEN_W;
	shell->scale = config ? clamp_int(config->scale, 1, 6) : 3;
	shell->presentation = config ? config->presentation : PRESENTATION_4X3;
	shell->options = config ? config->options : NULL;
	shell->width = shell->presentation == PRESENTATION_SGB_FRAME
		? PRESENTATION_SGB_WIDTH : shell->game_width;
	shell->height = shell->presentation == PRESENTATION_SGB_FRAME
		? PRESENTATION_SGB_HEIGHT : SCREEN_H;
	shell->speed = 1u;
	shell->sgb_border = -1;
#ifdef POKETCG_HAVE_SDL
	if (!shell->headless && SDL_Init(SDL_INIT_VIDEO) == 0) {
		int audio_initialized = SDL_InitSubSystem(SDL_INIT_AUDIO) == 0;
		if (audio_initialized) {
			SDL_AudioSpec desired = {0};
			desired.freq = 44100;
			desired.format = AUDIO_S16SYS;
			desired.channels = 2;
			desired.samples = 1024;
			shell->audio_device = SDL_OpenAudioDevice(NULL, 0, &desired, NULL, 0);
			if (shell->audio_device) {
				shell->have_audio = 1;
				SDL_PauseAudioDevice(shell->audio_device, 0);
				fprintf(stderr, "audio: SDL %s\n", SDL_GetCurrentAudioDriver());
			} else {
				SDL_AudioQuit();
			}
		}
#ifdef POKETCG_HAVE_PULSE
		if (!shell->have_audio)
			(void)shell_open_pulse_audio(shell);
#endif
		if (create_video(shell) != 0) {
			destroy_video(shell);
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
#ifdef POKETCG_HAVE_PULSE
	if (shell->pulse_audio) {
		int error = 0;
		(void)pa_simple_drain(shell->pulse_audio, &error);
		pa_simple_free(shell->pulse_audio);
	}
#endif
	if (shell->audio_device)
		SDL_CloseAudioDevice(shell->audio_device);
	destroy_video(shell);
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

ShellAudioSettings shell_audio_settings(const Shell *shell)
{
	ShellAudioSettings settings = {100u, 100u, 100u};
	if (shell && shell->options) {
		settings.master_volume = (uint8_t)clamp_int(shell->options->master_volume, 0, 100);
		settings.music_volume = (uint8_t)clamp_int(shell->options->music_volume, 0, 100);
		settings.sfx_volume = (uint8_t)clamp_int(shell->options->sfx_volume, 0, 100);
	}
	return settings;
}
void shell_sync_options(Shell *shell)
{
	if (!shell || !shell->options)
		return;
#ifdef POKETCG_HAVE_SDL
	if (shell->options->scale != shell->scale)
		set_scale(shell, shell->options->scale);
	PresentationMode desired = shell->options->sgb
		? PRESENTATION_SGB_FRAME : PRESENTATION_4X3;
	if (desired != shell->presentation && shell_has_window(shell)) {
		PresentationMode old = shell->presentation;
		shell->presentation = desired;
		if (switch_presentation(shell) != 0)
			shell->presentation = old;
	}
	if (shell->options->sgb_border != shell->sgb_border) {
		shell->sgb_border = shell->options->sgb_border;
		presentation_set_border(rom_sgb_border(shell->sgb_border));
	}
#endif
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
			} else {
				shell->buttons &= (uint8_t)~bit;
			}
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
static const uint8_t debug_font[39][7] = {
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
	{14,17,1,6,8,0,8},{0,4,0,0,0,4,0},
	{14,8,8,8,8,8,14},{14,2,2,2,2,2,14}
};

static int debug_font_index(char c)
{
	if (c >= 'A' && c <= 'Z')
		return c - 'A';
	if (c >= '0' && c <= '9')
		return 26 + c - '0';
	return c == ':' ? 36 : c == '[' ? 37 : c == ']' ? 38 : -1;
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
	int width = SCREEN_W;
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
	const uint16_t *output = framebuffer;
	if (shell->presentation == PRESENTATION_SGB_FRAME) {
		presentation_render(PRESENTATION_SGB_FRAME,
		                    shell->presentation_frame, framebuffer);
		output = shell->presentation_frame;
	}
	SDL_UpdateTexture(shell->texture, NULL, output,
	                  shell->width * (int)sizeof *output);
	SDL_RenderClear(shell->renderer);
	SDL_RenderCopy(shell->renderer, shell->texture, NULL, NULL);
	SDL_RenderPresent(shell->renderer);
#else
	(void)shell;
	(void)framebuffer;
#endif
}

#ifdef POKETCG_HAVE_SDL
static size_t shell_filter_audio(Shell *shell, const int16_t *samples, size_t count)
{
	if (count > SHELL_AUDIO_BUFFER_SAMPLES || count < 2u)
		return 0;
	if (!shell->audio_filter_ready) {
		shell->audio_dc[0] = samples[0];
		shell->audio_dc[1] = samples[1];
		shell->audio_filter_ready = 1;
	}
	for (size_t i = 0; i < count; i++) {
		unsigned channel = (unsigned)(i & 1u);
		int32_t sample = samples[i];
		int32_t delta = sample - shell->audio_dc[channel];
		shell->audio_dc[channel] += delta / 256;
		int32_t filtered = (sample - shell->audio_dc[channel]) * SHELL_PULSE_GAIN;
		if (filtered > 32767)
			filtered = 32767;
		else if (filtered < -32768)
			filtered = -32768;
		shell->audio_buffer[i] = (int16_t)filtered;
	}
	return count;
}
#endif
/* Queue interleaved signed 16-bit samples when SDL audio is available. */
void shell_queue_audio(Shell *shell, const int16_t *samples, size_t count)
{
	if (!shell || !samples || !count)
		return;
#ifdef POKETCG_HAVE_SDL
	if (shell->have_audio) {
		(void)SDL_QueueAudio(shell->audio_device,
		                     samples, count * sizeof *samples);
		return;
	}
#ifdef POKETCG_HAVE_PULSE
	if (shell->have_pulse) {
		size_t output_count = shell_filter_audio(shell, samples, count);
		if (!output_count)
			return;
		const int16_t *output = shell->audio_buffer;
		int error = 0;
		if (pa_simple_write(shell->pulse_audio, output,
		                    output_count * sizeof *output, &error) < 0) {
			fprintf(stderr, "audio: PulseAudio write failed: %s\n",
			        pa_strerror(error));
			pa_simple_free(shell->pulse_audio);
			shell->pulse_audio = NULL;
			shell->have_pulse = 0;
		}
	}
#endif
#endif
}
