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

#include "game_switch.h"

static const char *const PROFILE_VANILLA = "vanilla";
static const char *const PROFILE_EXTENDED = "extended";
static const char *const LAST_GAME_FILE = "last-game";

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

static int ensure_directories(const char *path)
{
	if (ensure_directory(path) == 0)
		return 0;
	if (errno != ENOENT)
		return -1;
	char parents[PATH_MAX];
	size_t length = strlen(path);
	if (length >= sizeof parents) {
		errno = ENAMETOOLONG;
		return -1;
	}
	memcpy(parents, path, length + 1u);
	size_t cursor = length;
	for (;;) {
		while (cursor) {
			if (parents[cursor] == '/')
				break;
#ifdef _WIN32
			if (parents[cursor] == '\\')
				break;
#endif
			cursor--;
		}
		if (!cursor)
			return -1;
		parents[cursor] = '\0';
		if (ensure_directory(parents) == 0)
			break;
		if (errno != ENOENT)
			return -1;
	}
	for (size_t index = cursor; index < length; index++) {
		if (parents[index] != '\0')
			continue;
		parents[index] = path[index];
		if (ensure_directory(parents) != 0)
			return -1;
	}
	return 0;
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
		if (ensure_directories(buffer) != 0)
			return -1;
		goto profile_dir;
	}
#endif
	if (snprintf(buffer, size, "%s/poketcg", base) >= (int)size)
		return -1;
	if (ensure_directories(buffer) != 0)
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

static int has_option(int count, char **items, const char *name)
{
	for (int index = 0; index < count; index++)
		if (strcmp(items[index], name) == 0)
			return 1;
	return 0;
}

static const char *other_profile(const char *profile)
{
	return strcmp(profile, PROFILE_EXTENDED) == 0 ? PROFILE_VANILLA : PROFILE_EXTENDED;
}

static const char *profile_binary(const char *profile)
{
	return strcmp(profile, PROFILE_EXTENDED) == 0 ? "poketcg-extended" : "poketcg";
}

static const char *profile_switch_label(const char *profile)
{
	return strcmp(profile, PROFILE_EXTENDED) == 0 ? "EXTENDED" : "ORIGINAL";
}

static int binary_exists(const char *directory, const char *profile)
{
	char path[PATH_MAX];
#ifdef _WIN32
	const char *suffix = ".exe";
#else
	const char *suffix = "";
#endif
	if (snprintf(path, sizeof path, "%s/%s%s", directory, profile_binary(profile), suffix) >= (int)sizeof path)
		return 0;
	return file_exists(path);
}

static const char *read_last_game(const char *data_dir)
{
	char path[PATH_MAX];
	if (snprintf(path, sizeof path, "%s/%s", data_dir, LAST_GAME_FILE) >= (int)sizeof path)
		return NULL;
	FILE *stream = fopen(path, "rb");
	if (!stream)
		return NULL;
	char text[16] = {0};
	size_t length = fread(text, 1u, sizeof text - 1u, stream);
	fclose(stream);
	while (length > 0u && (text[length - 1u] == '\n' || text[length - 1u] == '\r'))
		text[--length] = '\0';
	if (strcmp(text, PROFILE_VANILLA) == 0)
		return PROFILE_VANILLA;
	if (strcmp(text, PROFILE_EXTENDED) == 0)
		return PROFILE_EXTENDED;
	return NULL;
}

static void write_last_game(const char *data_dir, const char *profile)
{
	char path[PATH_MAX];
	if (snprintf(path, sizeof path, "%s/%s", data_dir, LAST_GAME_FILE) >= (int)sizeof path)
		return;
	FILE *stream = fopen(path, "wb");
	if (!stream)
		return;
	fprintf(stream, "%s\n", profile);
	fclose(stream);
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
	char **user = calloc((size_t)argc + 1u, sizeof(*user));
	char **child_argv = calloc((size_t)argc + 12u, sizeof(*child_argv));
	if (!user || !child_argv) {
		free(user);
		free(child_argv);
		return 2;
	}
	int user_count = 0;
	for (int index = 1; index < argc; index++) {
		if (strcmp(argv[index], "--profile") == 0) {
			if (++index >= argc || (strcmp(argv[index], PROFILE_VANILLA) != 0 && strcmp(argv[index], PROFILE_EXTENDED) != 0)) {
				fprintf(stderr, "unknown profile\n");
				free(user);
				free(child_argv);
				return 2;
			}
			override = argv[index];
			continue;
		}
		user[user_count++] = argv[index];
	}
	char directory[PATH_MAX];
	char data_dir[PATH_MAX];
	if (executable_directory(directory, sizeof directory) != 0 ||
	    save_directory(data_dir, sizeof data_dir) != 0) {
		free(user);
		free(child_argv);
		return 2;
	}
	const char *profile = override;
	if (!profile) {
		profile = read_last_game(data_dir);
		if (profile && !binary_exists(directory, profile))
			profile = NULL;
	}
	if (!profile) {
		int selected = choose_profile();
		if (selected < 0) {
			fprintf(stderr, "profile chooser requires SDL; pass --profile vanilla or extended\n");
			free(user);
			free(child_argv);
			return 2;
		}
		profile = selected == 0 ? PROFILE_VANILLA : PROFILE_EXTENDED;
	}
	int explicit_paths = has_option(user_count, user, "--data-pack") ||
		has_option(user_count, user, "--save") || has_option(user_count, user, "--load-save");
	int result = 2;
	for (;;) {
		char child[PATH_MAX];
		char pack[PATH_MAX];
		char save[PATH_MAX];
		const char *pack_name = strcmp(profile, PROFILE_EXTENDED) == 0 ? "data-pack-extended.bin" : "data-pack.bin";
		if (snprintf(child, sizeof child, "%s/%s", directory, profile_binary(profile)) >= (int)sizeof child ||
		    snprintf(pack, sizeof pack, "%s/%s", directory, pack_name) >= (int)sizeof pack ||
		    (!file_exists(pack) &&
		     snprintf(pack, sizeof pack, "%s/completion/%s", directory, pack_name) >= (int)sizeof pack) ||
		    snprintf(save, sizeof save, "%s/%s", data_dir,
		             strcmp(profile, PROFILE_EXTENDED) == 0 ? "poketcg-extended.sav" : "poketcg.sav") >= (int)sizeof save) {
			result = 2;
			break;
		}
		if (!explicit_paths && strcmp(profile, PROFILE_EXTENDED) == 0 && !file_exists(save)) {
			char vanilla_save[PATH_MAX];
			if (snprintf(vanilla_save, sizeof vanilla_save, "%s/poketcg.sav", data_dir) < (int)sizeof vanilla_save &&
			    file_exists(vanilla_save)) {
				char *import_argv[] = {child, "--data-pack", pack, "--convert-vanilla-save", vanilla_save, save, NULL};
				(void)run_child(child, import_argv);
			}
		}
		int count = 0;
		child_argv[count++] = child;
		for (int index = 0; index < user_count; index++)
			child_argv[count++] = user[index];
		if (!has_option(user_count, user, "--frames") && !has_option(user_count, user, "--headless")) {
			child_argv[count++] = "--frames";
			child_argv[count++] = "0";
		}
		if (!has_option(user_count, user, "--data-pack")) {
			child_argv[count++] = "--data-pack";
			child_argv[count++] = pack;
		}
		if (!has_option(user_count, user, "--save")) {
			child_argv[count++] = "--save";
			child_argv[count++] = save;
		}
		if (!has_option(user_count, user, "--load-save") && file_exists(save)) {
			child_argv[count++] = "--load-save";
			child_argv[count++] = save;
		}
		const char *other = other_profile(profile);
		int switchable = !explicit_paths && binary_exists(directory, other);
		if (switchable) {
			child_argv[count++] = "--switch-to";
			child_argv[count++] = (char *)profile_switch_label(other);
		}
		child_argv[count] = NULL;
		write_last_game(data_dir, profile);
		result = run_child(child, child_argv);
		if (!switchable || result != POKETCG_EXIT_SWITCH_GAME)
			break;
		profile = other;
	}
	free(user);
	free(child_argv);
	return result;
}
