/* >>> part includes */
#include "home/play_song.h"

#include "home/lcd_enable_frame.h"
#include "home/sound.h"
/* <<< part includes */

/* >>> factory ScriptPlaySong */
void ScriptPlaySong(uint8_t a)
{
	PlaySong(a);
}
/* <<< factory ScriptPlaySong */

/* >>> factory Func_3c87 */
void Func_3c87(uint8_t a)
{
	PauseSong();
	PlaySong(a);
	WaitForSongToFinish();
	ResumeSong();
}
/* <<< factory Func_3c87 */

/* >>> factory WaitForSongToFinish */
void WaitForSongToFinish(void)
{
	do {
		DoFrameIfLCDEnabled();
	} while (AssertSongFinished());
}
/* <<< factory WaitForSongToFinish */
