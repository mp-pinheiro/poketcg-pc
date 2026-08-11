#include "home/ir_functions.h"

#include "home/music1.h"

#define MUSIC_CARD_POP 0x08u

void PlayCardPopSong(void)
{
	Music1_PlaySong(MUSIC_CARD_POP);
}
