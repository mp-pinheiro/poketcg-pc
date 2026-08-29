#include "home/main_menu.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/common.h"
#include "home/lcd_enable_frame.h"
#include "home/overworld.h"
#include "home/sound.h"
#include "generated/wram.h"
#define MUSIC_CARD_POP 0x08u
#define MUSIC_STOP 0x00u
/* <<< factory statics */

/* >>> factory MainMenu_CardPop */
uint8_t MainMenu_CardPop(void)
{
	PlaySong(MUSIC_CARD_POP);
	DoCardPop();
	WhiteOutDMGPals();
	DoFrameIfLCDEnabled();
	PlaySong(MUSIC_STOP);
	return 0x10u;
}
/* <<< factory MainMenu_CardPop */
