#include "home/sound.h"

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

/* home/sound.asm audio wrappers — farcall trampolines dissolved to direct calls */
#define SFX_DENIED 0x04u

void SetupSound(void)       { Music1_Init(); }
void StopMusic(void)        { Music1_PlaySong(0); }
void PlaySong(uint8_t a)    { Music1_PlaySong(a); }
uint8_t AssertSongFinished(void)  { return Music1_AssertSongFinished(); }
uint8_t AssertSFXFinished(void)   { return Music1_AssertSFXFinished(); }
void PlaySFX_InvalidChoice(void)  { Music1_PlaySFX(SFX_DENIED); }
void PlaySFX(uint8_t a)     { Music1_PlaySFX(a); }
void PauseSong(void)        { Music1_PauseSong(); }
void ResumeSong(void)       { Music1_ResumeSong(); }
