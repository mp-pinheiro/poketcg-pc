#include "home/sound.h"

#include "home/frames.h"
#include "home/music.h"
#include "generated/constants.h"
#include "generated/hram.h"
#include "home/switch_rom.h"
#include "mem.h"

#define BANK_CARD_GRAPHICS 0x31u
#define MUSIC_BANK 0x42u

/* >>> factory Func_37c5 */
/* sound.asm:56-113 */
TileConvertResult Func_37c5(uint16_t hl, uint16_t de, uint8_t a, uint8_t carry_in)
{
	uint8_t carry = carry_in;
	for (uint8_t outer = 0u; outer < 8u; outer++) {
		for (uint8_t mid = 0u; mid < 6u; mid++) {
			for (uint8_t inner = 0u; inner < 8u; inner++) {
				for (uint8_t lo = 0u; lo < 2u; lo++) {
					uint8_t c = gb_read8(hl);
					for (uint8_t i = 0u; i < 4u; i++) {
						uint8_t next = c & 1u;
						c = (uint8_t)((c >> 1u) | (uint8_t)(carry << 7u));
						carry = next;
						next = a & 1u;
						a = (uint8_t)((a >> 1u) | (uint8_t)(carry << 7u));
						carry = next;
						next = a & 1u;
						a = (uint8_t)((a >> 1u) | (a & 0x80u));
						carry = next;
					}
					gb_write8((uint16_t)(de + 0xC0u), a);
					gb_write8((uint16_t)(de + 0xC2u), a);
					for (uint8_t i = 0u; i < 4u; i++) {
						uint8_t next = c & 1u;
						c = (uint8_t)((c >> 1u) | (uint8_t)(carry << 7u));
						carry = next;
						next = a & 1u;
						a = (uint8_t)((a >> 1u) | (uint8_t)(carry << 7u));
						carry = next;
						next = a & 1u;
						a = (uint8_t)((a >> 1u) | (a & 0x80u));
						carry = next;
					}
					gb_write8(de, a);
					gb_write8((uint16_t)(de + 2u), a);
					hl = (uint16_t)(hl + 1u);
					de = (uint16_t)(de + 1u);
				}
				de = (uint16_t)(de + 2u);
			}
		}
		de = (uint16_t)(de + 0xC0u);
		a = (uint8_t)(de >> 8u);
	}
	return (TileConvertResult){hl, de, a, carry};
}
/* <<< factory Func_37c5 */

/* >>> factory Func_37a5 */
/* sound.asm:35-54 */
TileConvertWrapResult Func_37a5(uint16_t hl, uint16_t de)
{
	uint8_t saved_bank = hBankROM;
	uint8_t bank = (uint8_t)(BANK_CARD_GRAPHICS + (uint8_t)((uint8_t)(hl >> 8u) >> 3u));
	BankswitchROM(bank);
	uint16_t shifted = hl;
	uint8_t carry = 0u;
	for (uint8_t i = 0u; i < 3u; i++) {
		carry = (uint8_t)((shifted >> 15u) & 1u);
		shifted = (uint16_t)(shifted << 1u);
	}
	shifted = (uint16_t)((shifted & (uint16_t)~0x8000u) | 0x4000u);
	TileConvertResult result = Func_37c5(shifted, de, bank, carry);
	BankswitchROM(saved_bank);
	return (TileConvertWrapResult){result.hl, result.de, saved_bank};
}
/* <<< factory Func_37a5 */

static uint8_t enter_music_bank(void)
{
	uint8_t saved_bank = hBankROM;
	frame_boundary_timer_sync();
	BankswitchROM(MUSIC_BANK);
	return saved_bank;
}

/* >>> factory SetupSound */
/* sound.asm:1-3 */
void SetupSound(void)
{
	uint8_t saved_bank = enter_music_bank();
	_SetupSound();
	BankswitchROM(saved_bank);
}
/* <<< factory SetupSound */

/* >>> factory StopMusic */
/* sound.asm:5-9 */
void StopMusic(void)
{
	PlaySong(0u);
}
/* <<< factory StopMusic */

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
