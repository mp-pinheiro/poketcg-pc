#define _GNU_SOURCE
#include <SDL2/SDL.h>
#include <stdint.h>

#ifndef PATH_MAX
#define PATH_MAX 4096
#endif

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#include <direct.h>
#include <process.h>
#include <windows.h>
#else
#include <limits.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <unistd.h>
#endif

static const char *const PROFILE_VANILLA = "vanilla";
static const char *const PROFILE_EXTENDED = "extended";

static void draw_text(SDL_Renderer *renderer, const char *text, int x, int y)
{
	static const uint8_t glyphs[26][5] = {
		{0x1E, 0x05, 0x1F, 0x11, 0x1F}, {0x1E, 0x11, 0x1E, 0x11, 0x1E},
		{0x0F, 0x10, 0x10, 0x10, 0x0F}, {0x1E, 0x11, 0x11, 0x11, 0x1E},
		{0x1F, 0x10, 0x1E, 0x10, 0x1F}, {0x1F, 0x10, 0x1E, 0x10, 0x10},
		{0x0F, 0x10, 0x17, 0x11, 0x0F}, {0x11, 0x11, 0x1F, 0x11, 0x11},
		{0x1F, 0x04, 0x04, 0x04, 0x1F}, {0x01, 0x01, 0x01, 0x11, 0x0E},
		{0x11, 0x12, 0x1C, 0x12, 0x11}, {0x10, 0x10, 0x10, 0x10, 0x1F},
		{0x11, 0x1B, 0x15, 0x11, 0x11}, {0x11, 0x19, 0x15, 0x13, 0x11},
		{0x0E, 0x11, 0x11, 0x11, 0x0E}, {0x1E, 0x11, 0x1E, 0x10, 0x10},
		{0x0E, 0x11, 0x15, 0x12, 0x0D}, {0x1E, 0x11, 0x1E, 0x12, 0x11},
		{0x0F, 0x10, 0x0E, 0x01, 0x1E}, {0x1F, 0x04, 0x04, 0x04, 0x04},
		{0x11, 0x11, 0x11, 0x11, 0x0E}, {0x11, 0x11, 0x11, 0x0A, 0x04},
		{0x11, 0x11, 0x15, 0x15, 0x0A}, {0x11, 0x0A, 0x04, 0x0A, 0x11},
		{0x11, 0x0A, 0x04, 0x04, 0x04}, {0x1F, 0x02, 0x04, 0x08, 0x1F},
	};
	for (size_t index = 0u; text[index] != '\0'; index++) {
		unsigned char c = (unsigned char)text[index];
		if (c >= 'a' && c <= 'z')
			c = (unsigned char)(c - 'a' + 'A');
		if (c >= 'A' && c <= 'Z') {
			SDL_Rect glyph = {x, y, 2, 2};
			for (int row = 0; row < 5; row++)
				for (int column = 0; column < 5; column++)
					if ((glyphs[c - 'A'][row] & (1u << (4 - column))) != 0u) {
						glyph.x = x + column * 2;
						glyph.y = y + row * 2;
						SDL_RenderFillRect(renderer, &glyph);
					}
			x += 12;
		} else {
			x += 8;
		}
	}
}

static int choose_profile(void)
{
	if (SDL_Init(SDL_INIT_VIDEO) != 0)
		return -1;
	SDL_Window *window = SDL_CreateWindow("poketcg-pc", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
	                                      320, 288, SDL_WINDOW_SHOWN);
	SDL_Renderer *renderer = window ? SDL_CreateRenderer(window, -1, SDL_RENDERER_SOFTWARE) : NULL;
	if (!window || !renderer) {
		if (renderer)
			SDL_DestroyRenderer(renderer);
		if (window)
			SDL_DestroyWindow(window);
		SDL_Quit();
		return -1;
	}
	int selected = 0;
	int running = 1;
	while (running) {
		SDL_Event event;
		while (SDL_PollEvent(&event)) {
			if (event.type == SDL_QUIT)
				running = 0;
			if (event.type == SDL_KEYDOWN) {
				if (event.key.keysym.sym == SDLK_UP || event.key.keysym.sym == SDLK_DOWN)
					selected = 1 - selected;
				if (event.key.keysym.sym == SDLK_z || event.key.keysym.sym == SDLK_RETURN)
					running = 0;
			}
		}
		SDL_SetRenderDrawColor(renderer, 10, 16, 32, 255);
		SDL_RenderClear(renderer);
		for (int index = 0; index < 2; index++) {
			SDL_Rect row = {16, 96 + index * 56, 288, 40};
			SDL_SetRenderDrawColor(renderer, index == selected ? 55 : 25, index == selected ? 95 : 45,
			                     index == selected ? 150 : 75, 255);
			SDL_RenderFillRect(renderer, &row);
			SDL_SetRenderDrawColor(renderer, 230, 240, 255, 255);
			draw_text(renderer, index == 0 ? "Pokemon TCG" : "Pokemon TCG Extended", 32, 111 + index * 56);
		}
		SDL_RenderPresent(renderer);
		SDL_Delay(16);
	}
	SDL_DestroyRenderer(renderer);
	SDL_DestroyWindow(window);
	SDL_Quit();
	return selected;
}

static int executable_directory(char *buffer, size_t size)
{
#ifdef _WIN32
	DWORD length = GetModuleFileNameA(NULL, buffer, (DWORD)size);
	if (length == 0u || length >= size)
		return -1;
#else
	ssize_t length = readlink("/proc/self/exe", buffer, size - 1u);
	if (length <= 0 || (size_t)length >= size)
		return -1;
	buffer[length] = '\0';
#endif
	char *slash = strrchr(buffer, '/');
#ifdef _WIN32
	char *backslash = strrchr(buffer, '\\');
	if (backslash > slash)
		slash = backslash;
#endif
	if (!slash)
		return -1;
	*slash = '\0';
	return 0;
}

static int ensure_directory(const char *path)
{
#ifdef _WIN32
	if (_mkdir(path) == 0 || errno == EEXIST)
		return 0;
#else
	if (mkdir(path, 0755) == 0 || errno == EEXIST)
		return 0;
#endif
	return -1;
}

static int save_directory(char *buffer, size_t size)
{
#ifdef _WIN32
	const char *base = getenv("APPDATA");
	if (!base)
		base = ".";
#else
	const char *base = getenv("XDG_DATA_HOME");
	if (!base || !*base) {
		const char *home = getenv("HOME");
		if (!home)
			return -1;
		if (snprintf(buffer, size, "%s/.local/share/poketcg", home) >= (int)size)
			return -1;
		if (ensure_directory(buffer) != 0)
			return -1;
		goto profile_dir;
	}
#endif
	if (snprintf(buffer, size, "%s/poketcg", base) >= (int)size)
		return -1;
	if (ensure_directory(buffer) != 0)
		return -1;
profile_dir:
	return 0;
}

static int file_exists(const char *path)
{
	FILE *stream = fopen(path, "rb");
	if (!stream)
		return 0;
	fclose(stream);
	return 1;
}

static int has_option(int argc, char **argv, const char *name)
{
	for (int index = 1; index < argc; index++)
		if (strcmp(argv[index], name) == 0)
			return 1;
	return 0;
}

static int run_child(const char *path, char **argv)
{
#ifdef _WIN32
	int result = _spawnv(_P_WAIT, path, (const char *const *)argv);
	return result < 0 ? 127 : result;
#else
	pid_t child = fork();
	if (child < 0)
		return 127;
	if (child == 0) {
		execv(path, argv);
		_exit(127);
	}
	int status = 0;
	if (waitpid(child, &status, 0) < 0)
		return 127;
	if (WIFEXITED(status))
		return WEXITSTATUS(status);
	return 128 + WTERMSIG(status);
#endif
}

int main(int argc, char **argv)
{
	const char *override = NULL;
	char **forwarded = calloc((size_t)argc + 8u, sizeof(*forwarded));
	if (!forwarded)
		return 2;
	int forwarded_count = 1;
	for (int index = 1; index < argc; index++) {
		if (strcmp(argv[index], "--profile") == 0) {
			if (++index >= argc || (strcmp(argv[index], PROFILE_VANILLA) != 0 && strcmp(argv[index], PROFILE_EXTENDED) != 0)) {
				fprintf(stderr, "unknown profile\n");
				free(forwarded);
				return 2;
			}
			override = argv[index];
			continue;
		}
		forwarded[forwarded_count++] = argv[index];
	}
	const char *profile = override;
	if (!profile) {
		int selected = choose_profile();
		if (selected < 0) {
			fprintf(stderr, "profile chooser requires SDL; pass --profile vanilla or extended\n");
			free(forwarded);
			return 2;
		}
		profile = selected == 0 ? PROFILE_VANILLA : PROFILE_EXTENDED;
	}
	char directory[PATH_MAX];
	if (executable_directory(directory, sizeof directory) != 0) {
		free(forwarded);
		return 2;
	}
	char child[PATH_MAX];
	char pack[PATH_MAX];
	const char *pack_name = strcmp(profile, PROFILE_EXTENDED) == 0 ? "data-pack-extended.bin" : "data-pack.bin";
	if (snprintf(child, sizeof child, "%s/%s", directory,
	             strcmp(profile, PROFILE_EXTENDED) == 0 ? "poketcg-extended" : "poketcg") >= (int)sizeof child ||
	    snprintf(pack, sizeof pack, "%s/%s", directory, pack_name) >= (int)sizeof pack ||
	    (!file_exists(pack) &&
	     snprintf(pack, sizeof pack, "%s/completion/%s", directory, pack_name) >= (int)sizeof pack)) {
		free(forwarded);
		return 2;
	}
	char data_dir[PATH_MAX];
	char save[PATH_MAX];
	if (save_directory(data_dir, sizeof data_dir) != 0 ||
	    snprintf(save, sizeof save, "%s/%s", data_dir,
	             strcmp(profile, PROFILE_EXTENDED) == 0 ? "poketcg-extended.sav" : "poketcg.sav") >= (int)sizeof save) {
		free(forwarded);
		return 2;
	}
	forwarded[0] = child;
	if (!has_option(forwarded_count, forwarded, "--data-pack")) {
		forwarded[forwarded_count++] = "--data-pack";
		forwarded[forwarded_count++] = pack;
	}
	if (!has_option(forwarded_count, forwarded, "--save")) {
		forwarded[forwarded_count++] = "--save";
		forwarded[forwarded_count++] = save;
	}
	if (!has_option(forwarded_count, forwarded, "--load-save")) {
		FILE *stream = fopen(save, "rb");
		if (stream) {
			fclose(stream);
			forwarded[forwarded_count++] = "--load-save";
			forwarded[forwarded_count++] = save;
		}
	}
	forwarded[forwarded_count] = NULL;
	int result = run_child(child, forwarded);
	free(forwarded);
	return result;
}
