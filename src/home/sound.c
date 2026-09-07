#include "home/sound.h"
#include "home/frames.h"

#include "home/music1.h"
#include "generated/hram.h"
#include "home/switch_rom.h"
#include "mem.h"

#define BANK_CARD_GRAPHICS 0x31u

/* sound.asm:56-113. Bit-serial 2bpp -> shifted-tile-plane converter. Carry
 * threads continuously through every rotate triple with no reset anywhere in
 * the routine, so it is a genuine (if undocumented) entry/exit parameter --
 * whatever the caller's flags happened to be. 768 source bytes (8 outer x 6
 * mid x 8 inner x 2 innermost) are consumed; each contributes two nibble
 * groups of 4 bits into `a`, written to four offsets around the running `de`. */
TileConvertResult Func_37c5(uint16_t hl, uint16_t de, uint8_t a, uint8_t carry_in)
{
	uint8_t carry = carry_in;
	for (uint8_t outer = 0; outer < 8; outer++) {
		for (uint8_t mid = 0; mid < 6; mid++) {
			for (uint8_t inner = 0; inner < 8; inner++) {
				for (uint8_t lo = 0; lo < 2; lo++) {
					uint8_t c = gb_read8(hl);
					for (uint8_t i = 0; i < 4; i++) {
						uint8_t nc = (uint8_t)(c & 1u);
						c = (uint8_t)((c >> 1) | (uint8_t)(carry << 7));
						carry = nc;
						nc = (uint8_t)(a & 1u);
						a = (uint8_t)((a >> 1) | (uint8_t)(carry << 7));
						carry = nc;
						nc = (uint8_t)(a & 1u);
						a = (uint8_t)((a >> 1) | (a & 0x80u));
						carry = nc;
					}
					gb_write8((uint16_t)(de + 0xc0u), a);
					gb_write8((uint16_t)(de + 0xc2u), a);
					for (uint8_t i = 0; i < 4; i++) {
						uint8_t nc = (uint8_t)(c & 1u);
						c = (uint8_t)((c >> 1) | (uint8_t)(carry << 7));
						carry = nc;
						nc = (uint8_t)(a & 1u);
						a = (uint8_t)((a >> 1) | (uint8_t)(carry << 7));
						carry = nc;
						nc = (uint8_t)(a & 1u);
						a = (uint8_t)((a >> 1) | (a & 0x80u));
						carry = nc;
					}
					gb_write8(de, a);
					gb_write8((uint16_t)(de + 2u), a);
					hl = (uint16_t)(hl + 1u);
					de = (uint16_t)(de + 1u);
				}
				de = (uint16_t)(de + 2u);
			}
		}
		de = (uint16_t)(de + 0xc0u);
		a = (uint8_t)(de >> 8);
	}
	return (TileConvertResult){hl, de, a, carry};
}

/* sound.asm:35-54. Bank-switches to CardGraphics (offset by hl's top 3 bits),
 * normalizes hl into $4000-$7fff (hl <<= 3, forced into that window), and
 * hands off to Func_37c5. `f` is untouched by anything before the wrapper's
 * final `pop af`, so it is restored verbatim -- but that same `pop af` also
 * overwrites `a` with the ENTRY hBankROM value (pushed there at the top),
 * not the caller's original `a`; Func_37c5's own exit `a` never reaches
 * the caller. */
TileConvertWrapResult Func_37a5(uint16_t hl, uint16_t de)
{
	uint8_t bank = (uint8_t)(BANK_CARD_GRAPHICS + (uint8_t)((uint8_t)(hl >> 8) >> 3));

	uint8_t saved = hBankROM;
	BankswitchROM(bank);

	uint16_t shifted = hl;
	uint8_t carry = 0;
	for (int i = 0; i < 3; i++) {
		carry = (uint8_t)((shifted >> 15) & 1u);
		shifted = (uint16_t)(shifted << 1);
	}
	shifted = (uint16_t)((shifted & (uint16_t)~0x8000u) | 0x4000u);

	TileConvertResult r = Func_37c5(shifted, de, bank, carry);

	BankswitchROM(saved);
	return (TileConvertWrapResult){r.hl, r.de, saved};
}

/* home/sound.asm:19-33 reaches the driver by `farcall`, which selects the
 * driver's own bank and restores the caller's on return. The port calls the
 * bodies directly, and it renamed them (`_PlaySFX` -> `Music1_PlaySFX`), so
 * tools/gen_bank_guard.py cannot match them against the asm's farcall targets
 * and does not cover them. Without the restore the driver's internal switch
 * leaks: the overworld script interpreter then fetched its next opcode out of
 * bank $3D and ran a different command. */
#define SFX_DENIED 0x04u
#define BANK_AUDIO_1 0x3Du

static uint8_t enter_audio_bank(void)
{
	uint8_t saved = hBankROM;

	/* One entry per wrapper, StopMusic and PlaySFX_InvalidChoice included
	 * once through the wrapper they fall into (sound.asm:5-7, 21-23). */
	frame_boundary_timer_sync();
	BankswitchROM(BANK_AUDIO_1);
	return saved;
}

void SetupSound(void)
{
	uint8_t saved = enter_audio_bank();

	Music1_Init();
	BankswitchROM(saved);
}

void StopMusic(void)
{
	uint8_t saved = enter_audio_bank();

	Music1_PlaySong(0);
	BankswitchROM(saved);
}

void PlaySong(uint8_t a)
{
	uint8_t saved = enter_audio_bank();

	Music1_PlaySong(a);
	BankswitchROM(saved);
}

uint8_t AssertSongFinished(void)
{
	uint8_t saved = enter_audio_bank();
	uint8_t result = Music1_AssertSongFinished();

	BankswitchROM(saved);
	return result;
}

uint8_t AssertSFXFinished(void)
{
	uint8_t saved = enter_audio_bank();
	uint8_t result = Music1_AssertSFXFinished();

	BankswitchROM(saved);
	return result;
}

void PlaySFX_InvalidChoice(void)
{
	PlaySFX(SFX_DENIED);
}

void PlaySFX(uint8_t a)
{
	uint8_t saved = enter_audio_bank();

	Music1_PlaySFX(a);
	BankswitchROM(saved);
}

void PauseSong(void)
{
	uint8_t saved = enter_audio_bank();

	Music1_PauseSong();
	BankswitchROM(saved);
}

void ResumeSong(void)
{
	uint8_t saved = enter_audio_bank();

	Music1_ResumeSong();
	BankswitchROM(saved);
}
