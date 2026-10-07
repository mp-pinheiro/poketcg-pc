/* >>> part includes */
#include "home/sound.h"

#include "home/frames.h"
#include "home/music.h"
#include "generated/constants.h"
#include "generated/hram.h"
#include "home/switch_rom.h"
#include "mem.h"
/* <<< part includes */
/* --- factory Func_37c5 */
/* --- factory Func_37a5 */
/* --- part BANK_AUDIO_1 */
/* --- part enter_audio_bank */
/* === part BANK_CARD_GRAPHICS */
/* >>> part MUSIC_BANK */
#define MUSIC_BANK 0x42u
/* <<< part MUSIC_BANK */
/* >>> part enter_music_bank */
static uint8_t enter_music_bank(void)
{
	uint8_t saved_bank = hBankROM;
	frame_boundary_timer_sync();
	BankswitchROM(MUSIC_BANK);
	return saved_bank;
}
/* <<< part enter_music_bank */
/* >>> factory SetupSound */
/* sound.asm:1-3 */
void SetupSound(void)
{
	uint8_t saved_bank = enter_music_bank();
	_SetupSound();
	BankswitchROM(saved_bank);
}
/* <<< factory SetupSound */
/* --- part StopMusic */
/* >>> factory PlaySong */
/* sound.asm:5-7 */
void PlaySong(uint8_t a)
{
	uint8_t saved_bank = enter_music_bank();
	_PlaySong(a);
	BankswitchROM(saved_bank);
}
/* <<< factory PlaySong */
/* >>> factory AssertSongFinished */
/* sound.asm:10-12 */
uint8_t AssertSongFinished(void)
{
	uint8_t saved_bank = enter_music_bank();
	uint8_t result = _AssertSongFinished();
	BankswitchROM(saved_bank);
	return result;
}
/* <<< factory AssertSongFinished */
/* >>> factory AssertSFXFinished */
/* sound.asm:13-17 */
uint8_t AssertSFXFinished(void)
{
	uint8_t saved_bank = enter_music_bank();
	uint8_t result = _AssertSFXFinished();
	BankswitchROM(saved_bank);
	return result;
}
/* <<< factory AssertSFXFinished */
/* >>> factory PlaySFX_InvalidChoice */
/* sound.asm:19-23 */
void PlaySFX_InvalidChoice(void)
{
	PlaySFX(SFX_DENIED);
}
/* <<< factory PlaySFX_InvalidChoice */
/* >>> factory PlaySFX */
/* sound.asm:21-23 */
void PlaySFX(uint8_t a)
{
	uint8_t saved_bank = enter_music_bank();
	_PlaySFX(a);
	BankswitchROM(saved_bank);
}
/* <<< factory PlaySFX */
/* >>> factory PauseSong */
/* sound.asm:25-27 */
void PauseSong(void)
{
	uint8_t saved_bank = enter_music_bank();
	_PauseSong();
	BankswitchROM(saved_bank);
}
/* <<< factory PauseSong */
/* >>> factory ResumeSong */
/* sound.asm:29-31 */
void ResumeSong(void)
{
	uint8_t saved_bank = enter_music_bank();
	_ResumeSong();
	BankswitchROM(saved_bank);
}
/* <<< factory ResumeSong */
/* === factory StopMusic */
