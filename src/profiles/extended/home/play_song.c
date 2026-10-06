#include "home/play_song.h"

#include "home/lcd_enable_frame.h"
#include "home/sound.h"

void ScriptPlaySong(uint8_t a)
{
	PlaySong(a);
}


void WaitForSongToFinish(void)
{
	do {
		DoFrameIfLCDEnabled();
	} while (AssertSongFinished());
}
