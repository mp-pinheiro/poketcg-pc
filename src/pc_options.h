#ifndef POKETCG_PC_OPTIONS_H
#define POKETCG_PC_OPTIONS_H

#include <stdint.h>

typedef struct PcOptions {
	int scale;
	int stereo;
	int sgb;
	int sound_volume;
	int music_volume;
	int font;
	int sgb_border;
	int text_case;
} PcOptions;
void pc_options_defaults(PcOptions *options);
int pc_options_load(PcOptions *options);
int pc_options_save(const PcOptions *options);

#endif
