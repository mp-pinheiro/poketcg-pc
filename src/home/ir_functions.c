#include "home/ir_functions.h"

#include "home/sound.h"

#define MUSIC_CARD_POP 0x08u

void PlayCardPopSong(void)
{
	PlaySong(MUSIC_CARD_POP);
}
