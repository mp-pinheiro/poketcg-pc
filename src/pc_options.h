#ifndef POKETCG_PC_OPTIONS_H
#define POKETCG_PC_OPTIONS_H

#include <stddef.h>
#include <stdint.h>

typedef struct PcOptions {
	int scale;
	int stereo;
	int sgb;
	int master_volume;
	int music_volume;
	int sfx_volume;
	int big_font;
	int small_font;
	int sgb_border;
	int text_case;
} PcOptions;
void pc_options_defaults(PcOptions *options);
int pc_options_load(PcOptions *options);
int pc_options_save(const PcOptions *options);

#endif
