#define _POSIX_C_SOURCE 200809L
#include "pc_options.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

static int clamp(int value, int low, int high)
{
	if (value < low)
		return low;
	if (value > high)
		return high;
	return value;
}

static const char *options_path(void)
{
	const char *configured = getenv("POKETCG_CONFIG");
	if (configured && *configured)
		return configured;
	const char *home = getenv("HOME");
	const char *xdg = getenv("XDG_CONFIG_HOME");
	static char path[4096];
	if (xdg && *xdg)
		snprintf(path, sizeof path, "%s/poketcg/options.conf", xdg);
	else if (home && *home)
		snprintf(path, sizeof path, "%s/.config/poketcg/options.conf", home);
	else
		snprintf(path, sizeof path, "options.conf");
	return path;
}

static void normalize(PcOptions *options)
{
	options->scale = clamp(options->scale, 1, 6);
	options->stereo = options->stereo ? 1 : 0;
	options->sgb = options->sgb ? 1 : 0;
	options->sound_volume = clamp(options->sound_volume, 0, 100);
	options->music_volume = clamp(options->music_volume, 0, 100);
}

void pc_options_defaults(PcOptions *options)
{
	if (!options)
		return;
	options->scale = 3;
	options->stereo = 1;
	options->sgb = 0;
	options->sound_volume = 100;
	options->music_volume = 100;
}

int pc_options_load(PcOptions *options)
{
	if (!options)
		return -1;
	pc_options_defaults(options);
	FILE *file = fopen(options_path(), "r");
	if (!file) {
		if (errno == ENOENT)
			return 0;
		return -1;
	}
	char line[128];
	while (fgets(line, sizeof line, file)) {
		char key[64];
		int value;
		if (sscanf(line, " %63[^=]=%d", key, &value) != 2)
			continue;
		if (strcmp(key, "scale") == 0)
			options->scale = value;
		else if (strcmp(key, "stereo") == 0)
			options->stereo = value;
		else if (strcmp(key, "sgb") == 0)
			options->sgb = value;
		else if (strcmp(key, "sound_volume") == 0)
			options->sound_volume = value;
		else if (strcmp(key, "music_volume") == 0)
			options->music_volume = value;
	}
	int error = ferror(file) ? -1 : 0;
	fclose(file);
	normalize(options);
	return error;
}

int pc_options_save(const PcOptions *options)
{
	if (!options)
		return -1;
	PcOptions normalized = *options;
	normalize(&normalized);
	const char *path = options_path();
	char directory[4096];
	char temporary[4096];
	const char *slash = strrchr(path, '/');
	if (slash) {
		size_t length = (size_t)(slash - path);
		if (length == 0 || length >= sizeof directory)
			return -1;
		memcpy(directory, path, length);
		directory[length] = '\0';
		char *last = strrchr(directory, '/');
		if (last) {
			*last = '\0';
			if (*directory && mkdir(directory, 0755) != 0 && errno != EEXIST)
				return -1;
			*last = '/';
		}
		if (mkdir(directory, 0755) != 0 && errno != EEXIST)
			return -1;
	} else {
		strcpy(directory, ".");
	}
	if (snprintf(temporary, sizeof temporary, "%s.tmp.%ld", path, (long)getpid()) >= (int)sizeof temporary)
		return -1;
	FILE *file = fopen(temporary, "w");
	if (!file)
		return -1;
	int result = fprintf(file,
		"scale=%d\nstereo=%d\nsgb=%d\nsound_volume=%d\nmusic_volume=%d\n",
		normalized.scale, normalized.stereo, normalized.sgb,
		normalized.sound_volume, normalized.music_volume) < 0;
	if (fclose(file) != 0)
		result = 1;
	if (result || rename(temporary, path) != 0) {
		remove(temporary);
		return -1;
	}
	return 0;
}
