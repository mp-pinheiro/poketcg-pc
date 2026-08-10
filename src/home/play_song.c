#include "home/play_song.h"

#include "home/lcd_enable_frame.h"
#include "home/sound.h"

void ScriptPlaySong(uint8_t a)
{
	PlaySong(a);
}

void Func_3c87(uint8_t a)
{
	PauseSong();
	PlaySong(a);
	WaitForSongToFinish();
	ResumeSong();
}

void WaitForSongToFinish(void)
{
	do {
		DoFrameIfLCDEnabled();
	} while (AssertSongFinished());
}
