#include "home/sfx.h"

#include <stdbool.h>
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
/* rAUD1ENV is NR12 ($ff12); AUD1ENV_UP is the envelope-direction bit of NRx2.
 * wdd8c has no generated symbol in this port's header set, so its address is
 * defined locally. */
#define RAUD1ENV     0xff12u
#define AUD1ENV_UP   0x08u
#define WDD8C        0xdd8cu

#include "generated/wram.h"
#include "mem.h"
#define rAUD1ENV 0xFF12u

#include "home/sfx.h"
#include "generated/wram.h"
#include "mem.h"
#define rAUD1LEN 0xFF11u

#include "home/sfx.h"
#include "generated/wram.h"
#include "mem.h"

#include "generated/wram.h"
#include "mem.h"
#include "home/sfx.h"
/* <<< factory statics */

#define SFX_BANK 0x3Fu

#define SFX_NumberOfSFX_ADDR     0x4290u
#define SFX_HeaderPointers_ADDR  0x4291u
#define SFX_WaveInstruments_ADDR 0x4485u

#define rAUD1LEN   0xFF11u
#define rAUD1ENV   0xFF12u
#define rAUD1LOW   0xFF13u
#define rAUD1HIGH  0xFF14u
#define rAUD4LEN   0xFF20u
#define rAUD4GO    0xFF23u

#define AUD3WAVERAM   0xFF30u
#define AUD3ENA_ON    0x80u
#define AUD3WAVE_SIZE 16u

#define AUD1ENV_UP 0x08u

/* >>> factory Func_fc279 */
/* sfx.asm:485-497. The asm is a documented ROM bug: it loads $8/$80 into `a`
 * and then does `ldh a, [rAUDxENV/HIGH]`, reading the registers instead of
 * writing them, so those loads are dead and the only surviving effect is
 * clearing wdd8c. The reads are kept because they are observable bus traffic. */
void Func_fc279(void)
{
	gb_read8(rAUD1ENV);
	gb_read8(0xFF17u);
	gb_read8(0xFF1Cu);
	gb_read8(0xFF21u);
	gb_read8(rAUD1HIGH);
	gb_read8(0xFF19u);
	gb_read8(rAUD4GO);
	wdd8c = 0;
}

/* <<< factory Func_fc279 */

/* >>> factory Func_fc26c */
/* sfx.asm:475-481. */
void Func_fc26c(void)
{
	wSFXIsPlaying = 0;
	wSfxPriority = 0;
	wCurSfxID = 0x80;
}
/* <<< factory Func_fc26c */

static void StoreCmdPtr(uint8_t c, uint16_t ptr)
{
	uint16_t addr = (uint16_t)(wSFXCommandPointers_ADDR + (uint16_t)c * 2u);
	gb_write8(addr, (uint8_t)ptr);
	gb_write8((uint16_t)(addr + 1u), (uint8_t)(ptr >> 8));
}

static uint8_t read_wde2b(uint8_t c)
{
	if (c == 3u)
		return gb_read8(wde2e_ADDR);
	return gb_read8((uint16_t)(wde2b_ADDR + c));
}

static void write_wde2b(uint8_t c, uint8_t v)
{
	if (c == 3u)
		gb_write8(wde2e_ADDR, v);
	else
		gb_write8((uint16_t)(wde2b_ADDR + c), v);
}

static uint16_t read_wde37(uint8_t c)
{
	if (c == 3u)
		return (uint16_t)gb_read8(wde3d_ADDR) | (uint16_t)(gb_read8((uint16_t)(wde3d_ADDR + 1u)) << 8);
	uint16_t addr = (uint16_t)(wde37_ADDR + (uint16_t)c * 2u);
	return (uint16_t)gb_read8(addr) | (uint16_t)(gb_read8((uint16_t)(addr + 1u)) << 8);
}

static void write_wde37(uint8_t c, uint16_t freq)
{
	if (c == 3u) {
		gb_write8(wde3d_ADDR, (uint8_t)freq);
		gb_write8((uint16_t)(wde3d_ADDR + 1u), (uint8_t)(freq >> 8));
		return;
	}
	uint16_t addr = (uint16_t)(wde37_ADDR + (uint16_t)c * 2u);
	gb_write8(addr, (uint8_t)freq);
	gb_write8((uint16_t)(addr + 1u), (uint8_t)(freq >> 8));
}

static uint8_t read_pitch_offset(uint8_t c)
{
	if (c == 3u)
		return gb_read8(wde32_ADDR);
	return gb_read8((uint16_t)(wSFXPitchOffsets_ADDR + c));
}

static void apu_write_freq(uint8_t c, uint8_t low, uint8_t high)
{
	uint16_t reg = (uint16_t)(rAUD1LEN + (uint16_t)c * 5u);
	uint8_t len = gb_read8(reg);
	gb_write8(reg, (uint8_t)(len & 0xC0u));
	gb_write8((uint16_t)(reg + 2u), low);
	gb_write8((uint16_t)(reg + 3u), high);
}

/* >>> factory SFX_ApplyPitchOffset */
/* sfx.asm:297-350. Indexes wde37 by 2*c and wSFXPitchOffsets/wde2b by c; the
 * helpers' c==3 special cases are address aliasing, not a simplification
 * (0xDE37+6 == wde3d, 0xDE2F+3 == wde32, 0xDE2B+3 == wde2e). */
void SFX_ApplyPitchOffset(uint8_t c)
{
	uint8_t offset = read_pitch_offset(c);
	if (offset == 0u)
		return;
	uint16_t freq = read_wde37(c);
	uint16_t new_freq;
	if (offset & 0x80u) {
		uint8_t d = (uint8_t)((uint8_t)(offset ^ 0xFFu) + 1u);
		new_freq = (uint16_t)(freq - d);
	} else {
		new_freq = (uint16_t)(freq + offset);
	}
	write_wde37(c, new_freq);
	uint8_t env = read_wde2b(c);
	write_wde2b(c, 0u);
	apu_write_freq(c, (uint8_t)new_freq, (uint8_t)((new_freq >> 8) | env));
}
/* <<< factory SFX_ApplyPitchOffset */

/* >>> factory Func_fc1cd */
/* sfx.asm:352-392. The noise channel's pitch update: only the low byte is
 * tracked, and bit 3 of the delta is swapped into bit 7 of the high write. */
void Func_fc1cd(void)
{
	uint8_t offset = gb_read8(wde32_ADDR);
	if (offset == 0u)
		return;
	uint16_t freq_addr = wde3d_ADDR;
	uint8_t old_low = gb_read8(freq_addr);
	uint8_t new_low;
	if (offset & 0x80u) {
		uint8_t d = (uint8_t)((uint8_t)(offset ^ 0xFFu) + 1u);
		new_low = old_low - d;
	} else {
		new_low = old_low + offset;
	}
	gb_write8(freq_addr, new_low);
	uint8_t changed = new_low ^ old_low;
	uint8_t high = (uint8_t)((changed & 8u) << 4u);
	uint8_t env = gb_read8(wde2e_ADDR);
	gb_write8(wde2e_ADDR, 0u);
	high |= env;
	uint16_t reg = rAUD4LEN;
	gb_write8(reg, 0u);
	gb_write8((uint16_t)(reg + 2u), new_low);
	gb_write8((uint16_t)(reg + 3u), high);
}
/* <<< factory Func_fc1cd */

static uint16_t SFX_Frequency(uint16_t cmd_ptr, uint8_t c, uint8_t high_nibble)
{
	uint8_t low = gb_read8(cmd_ptr);
	cmd_ptr = (uint16_t)(cmd_ptr + 1u);
	uint8_t old_low = (uint8_t)read_wde37(c);
	write_wde37(c, (uint16_t)((uint16_t)high_nibble << 8 | low));
	uint8_t high_flags = high_nibble;
	if (c == 3u) {
		uint8_t changed = old_low ^ low;
		high_flags = (uint8_t)((changed & 8u) << 4u);
	}
	uint8_t env = read_wde2b(c);
	write_wde2b(c, 0u);
	apu_write_freq(c, low, (uint8_t)(high_flags | env));
	return cmd_ptr;
}

static uint16_t SFX_Envelope(uint16_t cmd_ptr, uint8_t c)
{
	write_wde2b(c, 0x80u);
	uint8_t env_val = gb_read8(cmd_ptr);
	cmd_ptr = (uint16_t)(cmd_ptr + 1u);
	uint16_t reg = (uint16_t)(rAUD1ENV + (uint16_t)c * 5u);
	gb_write8(reg, env_val);
	return cmd_ptr;
}

static void SFX_Duty(uint8_t c, uint8_t param)
{
	uint8_t duty = (uint8_t)((param << 4u) | (param >> 4u));
	uint16_t reg = (uint16_t)(rAUD1LEN + (uint16_t)c * 5u);
	gb_write8(reg, duty);
}

static uint16_t SFX_Loop(uint16_t cmd_ptr, uint8_t c)
{
	uint8_t count = gb_read8(cmd_ptr);
	cmd_ptr = (uint16_t)(cmd_ptr + 1u);
	uint16_t store_addr = (uint16_t)(wde43_ADDR + (uint16_t)c * 2u);
	gb_write8(store_addr, (uint8_t)cmd_ptr);
	gb_write8((uint16_t)(store_addr + 1u), (uint8_t)(cmd_ptr >> 8));
	gb_write8((uint16_t)(wde3f_ADDR + c), count);
	return cmd_ptr;
}

static bool SFX_EndLoop(uint16_t *cmd_ptr, uint8_t c)
{
	uint8_t count = gb_read8((uint16_t)(wde3f_ADDR + c));
	count = (uint8_t)(count - 1u);
	if (count == 0u)
		return false;
	gb_write8((uint16_t)(wde3f_ADDR + c), count);
	uint16_t store_addr = (uint16_t)(wde43_ADDR + (uint16_t)c * 2u);
	uint16_t loop_addr = (uint16_t)gb_read8(store_addr) | (uint16_t)(gb_read8((uint16_t)(store_addr + 1u)) << 8);
	*cmd_ptr = loop_addr;
	return true;
}

static uint16_t SFX_PitchOffset(uint16_t cmd_ptr, uint8_t c)
{
	uint8_t offset = gb_read8(cmd_ptr);
	cmd_ptr = (uint16_t)(cmd_ptr + 1u);
	if (c == 3u)
		gb_write8(wde32_ADDR, offset);
	else
		gb_write8((uint16_t)(wSFXPitchOffsets_ADDR + c), offset);
	return cmd_ptr;
}

static uint16_t SFX_Wait(uint16_t cmd_ptr, uint8_t c)
{
	if (c == 3u)
		Func_fc1cd();
	else
		SFX_ApplyPitchOffset(c);
	uint8_t wait_val = gb_read8(cmd_ptr);
	cmd_ptr = (uint16_t)(cmd_ptr + 1u);
	gb_write8((uint16_t)(wde33_ADDR + c), wait_val);
	return cmd_ptr;
}

static void SFX_Wave(uint8_t param)
{
	uint16_t table_addr = (uint16_t)(SFX_WaveInstruments_ADDR + (uint16_t)param * 2u);
	uint16_t wave_ptr = (uint16_t)gb_read8(table_addr) | (uint16_t)(gb_read8((uint16_t)(table_addr + 1u)) << 8);
	gb_write8(0xFF1Au, 0u);
	uint8_t b = 0u;
	uint16_t dst = AUD3WAVERAM;
	do {
		gb_write8(dst, gb_read8(wave_ptr));
		dst = (uint16_t)(dst + 1u);
		wave_ptr = (uint16_t)(wave_ptr + 1u);
		b = (uint8_t)(b + 1u);
	} while (b != AUD3WAVE_SIZE);
	wMusicWaveChange = 1u;
	gb_write8(0xFF1Au, AUD3ENA_ON);
}

static uint16_t SFX_Pan(uint16_t cmd_ptr, uint8_t c)
{
	uint8_t pan_val = gb_read8(cmd_ptr);
	cmd_ptr = (uint16_t)(cmd_ptr + 1u);
	uint8_t ch = (uint8_t)(c + 1u);
	uint8_t e = 0xEEu;
	while (ch) {
		ch = (uint8_t)(ch - 1u);
		if (ch == 0u)
			break;
		pan_val = (uint8_t)((pan_val << 1u) | (pan_val >> 7u));
		e = (uint8_t)((e << 1u) | (pan_val & 1u));
	}
	wdd85 = (uint8_t)((wdd85 & e) | pan_val);
	return cmd_ptr;
}

static void SFX_End(uint8_t c)
{
	uint8_t e = (uint8_t)(c + 1u);
	uint8_t a = 0x7Fu;
	do {
		a = (uint8_t)((a << 1u) | (a >> 7u));
		e = (uint8_t)(e - 1u);
	} while (e != 0u);
	wdd8c &= a;
	uint16_t reg = (uint16_t)(rAUD1ENV + (uint16_t)c * 5u);
	gb_write8(reg, AUD1ENV_UP);
	gb_write8((uint16_t)(reg + 2u), 0x80u);
}

/* >>> factory ExecuteNextSFXCommand */
/* sfx.asm:103-138 */
void ExecuteNextSFXCommand(uint16_t hl, uint16_t bc)
{
	uint16_t cmd_ptr = hl;
	uint8_t c = (uint8_t)bc;
	for (;;) {
		uint8_t cmd = gb_read8(cmd_ptr);
		cmd_ptr = (uint16_t)(cmd_ptr + 1u);
		uint8_t idx = (uint8_t)(cmd >> 4u);
		uint8_t param = (uint8_t)(cmd & 0xFu);

		switch (idx) {
		case 0u:
			StoreCmdPtr(c, SFX_Frequency(cmd_ptr, c, param));
			return;
		case 1u:
			cmd_ptr = SFX_Envelope(cmd_ptr, c);
			break;
		case 2u:
			SFX_Duty(c, param);
			break;
		case 3u:
			cmd_ptr = SFX_Loop(cmd_ptr, c);
			break;
		case 4u:
			if (!SFX_EndLoop(&cmd_ptr, c))
				return;
			break;
		case 5u:
			cmd_ptr = SFX_PitchOffset(cmd_ptr, c);
			break;
		case 6u:
			StoreCmdPtr(c, SFX_Wait(cmd_ptr, c));
			return;
		case 7u:
			SFX_Wave(param);
			break;
		case 8u:
			cmd_ptr = SFX_Pan(cmd_ptr, c);
			break;
		case 15u:
			SFX_End(c);
			return;
		default:
			break;
		}
	}
}
/* <<< factory ExecuteNextSFXCommand */

void SFX_Play(uint8_t sfx_id)
{
	g_rom_bank = SFX_BANK;
	uint8_t max_sfx = gb_read8(SFX_NumberOfSFX_ADDR);
	if (sfx_id >= max_sfx)
		return;

	uint16_t offset = (uint16_t)sfx_id * 2u;
	if (wSFXIsPlaying)
		Func_fc279();
	wSFXIsPlaying = 1u;

	uint16_t header_ptr = (uint16_t)(SFX_HeaderPointers_ADDR + offset);
	uint16_t ptr = (uint16_t)gb_read8(header_ptr) | (uint16_t)(gb_read8((uint16_t)(header_ptr + 1u)) << 8);

	uint8_t flags = gb_read8(ptr);
	ptr = (uint16_t)(ptr + 1u);
	wdd8c = flags;
	wde54 = flags;

	uint16_t de = wSFXCommandPointers_ADDR;
	uint8_t c = 0u;
	for (;;) {
		uint8_t mask = wde54;
		wde54 = (uint8_t)((mask >> 1) | ((mask << 7) & 0xFFu));
		if ((mask & 1u) == 0u) {
			de = (uint16_t)(de + 2u);
		} else {
			gb_write8(de, gb_read8(ptr));
			ptr = (uint16_t)(ptr + 1u);
			de = (uint16_t)(de + 1u);
			gb_write8(de, gb_read8(ptr));
			ptr = (uint16_t)(ptr + 1u);
			de = (uint16_t)(de + 1u);
			gb_write8((uint16_t)(wSFXPitchOffsets_ADDR + c), 0u);
			if (c == 3u)
				gb_write8(wde32_ADDR, 0u);
			gb_write8((uint16_t)(wde33_ADDR + c), 1u);
		}
		c = (uint8_t)(c + 1u);
		if (c == 4u)
			break;
	}
}

void SFX_Update(void)
{
	g_rom_bank = SFX_BANK;
	if (wdd8c == 0u) {
		Func_fc26c();
		return;
	}
	wde54 = wdd8c;
	uint8_t c = 0u;
	for (;;) {
		uint8_t mask = wde54;
		wde54 = (uint8_t)((mask >> 1) | ((mask << 7) & 0xFFu));
		if ((mask & 1u) != 0u) {
			uint8_t wait = gb_read8((uint16_t)(wde33_ADDR + c));
			wait = (uint8_t)(wait - 1u);
			if (wait != 0u) {
				gb_write8((uint16_t)(wde33_ADDR + c), wait);
				SFX_ApplyPitchOffset(c);
			} else {
				uint16_t cmd_addr = (uint16_t)(wSFXCommandPointers_ADDR + (uint16_t)c * 2u);
				uint16_t cmd = (uint16_t)gb_read8(cmd_addr) | (uint16_t)(gb_read8((uint16_t)(cmd_addr + 1u)) << 8);
				ExecuteNextSFXCommand(cmd, c);
			}
		}
		c = (uint8_t)(c + 1u);
		if (c == 4u)
			break;
	}
}

/* >>> factory Func_fc105 */
/* sfx.asm:188-196 */
uint16_t Func_fc105(uint16_t bc, uint16_t de)
{
	uint16_t hl = (uint16_t)(wSFXCommandPointers_ADDR + bc + bc);
	gb_write8(hl, (uint8_t)de);
	hl = (uint16_t)(hl + 1u);
	gb_write8(hl, (uint8_t)(de >> 8));
	return hl;
}
/* <<< factory Func_fc105 */

/* >>> factory SFX_end */
SFX_endResult SFX_end(uint8_t b, uint8_t c, uint16_t caller_hl)
{
	uint8_t e = (uint8_t)(c + 1u);
	uint8_t mask = 0x7Fu;
	do {
		mask = (uint8_t)((mask << 1u) | (mask >> 7u));
		e = (uint8_t)(e - 1u);
	} while (e != 0u);
	wdd8c = (uint8_t)(wdd8c & mask);
	uint8_t rotated = (uint8_t)((c << 2u) | (c >> 6u));
	e = (uint8_t)(rotated + c);
	uint8_t d = b;
	return (SFX_endResult){0x80u, 0x00u, b, c, d, e, caller_hl};
}
/* <<< factory SFX_end */

/* >>> factory SFX_frequency */
void SFX_frequency(uint16_t bc, uint16_t caller_hl, uint8_t high)
{
	uint8_t d = high;
	uint8_t e = gb_read8(caller_hl);
	caller_hl = (uint16_t)(caller_hl + 1u);
	uint16_t freq_addr = (uint16_t)(wde37_ADDR + bc + bc);
	uint8_t old_low = gb_read8(freq_addr);
	gb_write8(freq_addr, e);
	gb_write8((uint16_t)(freq_addr + 1u), d);
	uint8_t c = (uint8_t)bc;
	if (c == 3u) {
		d = (uint8_t)((uint8_t)((old_low ^ e) & 0x08u) << 4u);
	}
	uint16_t env_addr = (uint16_t)(wde2b_ADDR + bc);
	uint8_t env = gb_read8(env_addr);
	gb_write8(env_addr, 0u);
	d = (uint8_t)(env | d);
	uint16_t reg = (uint16_t)(rAUD1LEN + (uint16_t)c * 5u);
	uint8_t length = gb_read8(reg);
	gb_write8(reg, (uint8_t)(length & 0xC0u));
	gb_write8((uint16_t)(reg + 2u), e);
	gb_write8((uint16_t)(reg + 3u), d);
	uint16_t de = caller_hl;
	Func_fc105(bc, de);
}
/* <<< factory SFX_frequency */

/* >>> factory SFX_loop */
void SFX_loop(uint16_t bc, uint16_t caller_de)
{
	uint16_t store_addr = (uint16_t)(wde43_ADDR + bc + bc);
	uint8_t a = gb_read8(caller_de);
	caller_de = (uint16_t)(caller_de + 1u);
	gb_write8(store_addr, (uint8_t)caller_de);
	gb_write8((uint16_t)(store_addr + 1u), (uint8_t)(caller_de >> 8));
	gb_write8((uint16_t)(wde3f_ADDR + bc), a);
	ExecuteNextSFXCommand(caller_de, bc);
}
/* <<< factory SFX_loop */

/* >>> factory SFX_pan */
void SFX_pan(uint16_t bc, uint16_t caller_hl)
{
	uint8_t pan_val = gb_read8(caller_hl);
	caller_hl = (uint16_t)(caller_hl + 1u);
	uint8_t rotate_count = (uint8_t)(bc + 1u);
	uint8_t mask = 0xEEu;
	for (;;) {
		rotate_count = (uint8_t)(rotate_count - 1u);
		if (rotate_count == 0u)
			break;
		pan_val = (uint8_t)((pan_val << 1u) | (pan_val >> 7u));
		mask = (uint8_t)((mask << 1u) | (mask >> 7u));
	}
	wdd85 = (uint8_t)((wdd85 & mask) | pan_val);
	ExecuteNextSFXCommand(caller_hl, bc);
}
/* <<< factory SFX_pan */

/* >>> factory SFX_unused */
void SFX_unused(uint16_t hl, uint16_t bc)
{
	ExecuteNextSFXCommand(hl, bc);
}
/* <<< factory SFX_unused */

/* >>> factory SFX_pitch_offset */
void SFX_pitch_offset(uint16_t bc, uint16_t caller_hl)
{
	gb_write8((uint16_t)(wSFXPitchOffsets_ADDR + bc), gb_read8(caller_hl));
	caller_hl = (uint16_t)(caller_hl + 1u);
	ExecuteNextSFXCommand(caller_hl, bc);
}
/* <<< factory SFX_pitch_offset */

/* >>> factory SFX_wave */
void SFX_wave(uint8_t a, uint16_t bc, uint16_t caller_hl)
{
	uint16_t table_addr = (uint16_t)(SFX_WaveInstruments_ADDR + (uint16_t)a * 2u);
	const uint8_t *table = rom_ptr(SFX_BANK, table_addr);
	uint16_t wave_addr = (uint16_t)table[0] | (uint16_t)((uint16_t)table[1] << 8u);
	const uint8_t *wave = rom_ptr(SFX_BANK, wave_addr);
	gb_write8(0xFF1Au, 0u);
	for (uint8_t i = 0u; i < AUD3WAVE_SIZE; i++)
		gb_write8((uint16_t)(AUD3WAVERAM + i), wave[i]);
	wMusicWaveChange = 1u;
	gb_write8(0xFF1Au, AUD3ENA_ON);
	ExecuteNextSFXCommand(caller_hl, bc);
}
/* <<< factory SFX_wave */

/* >>> factory SFX_duty */
void SFX_duty(uint8_t a, uint16_t bc, uint16_t caller_hl)
{
	SFX_Duty((uint8_t)bc, a);
	ExecuteNextSFXCommand(caller_hl, bc);
}
/* <<< factory SFX_duty */

/* >>> factory SFX_envelope */
void SFX_envelope(uint16_t bc, uint16_t caller_hl)
{
	uint16_t store_addr = (uint16_t)(wde2b_ADDR + bc);
	gb_write8(store_addr, 0x80u);
	uint8_t e = gb_read8(caller_hl);
	caller_hl = (uint16_t)(caller_hl + 1u);
	uint8_t c = (uint8_t)bc;
	uint16_t reg = (uint16_t)(rAUD1ENV + (uint16_t)c * 5u);
	gb_write8(reg, e);
	ExecuteNextSFXCommand(caller_hl, bc);
}
/* <<< factory SFX_envelope */

/* >>> factory SFX_endloop */
void SFX_endloop(uint16_t bc, uint16_t caller_word)
{
	uint8_t count = gb_read8((uint16_t)(wde3f_ADDR + bc));
	count = (uint8_t)(count - 1u);
	if (count != 0u) {
		gb_write8((uint16_t)(wde3f_ADDR + bc), count);
		uint16_t store_addr = (uint16_t)(wde43_ADDR + bc + bc);
		uint16_t loop_addr = (uint16_t)gb_read8(store_addr) | (uint16_t)(gb_read8((uint16_t)(store_addr + 1u)) << 8u);
		ExecuteNextSFXCommand(loop_addr, bc);
		return;
	}
	ExecuteNextSFXCommand(caller_word, bc);
}
/* <<< factory SFX_endloop */

/* >>> factory SFX_wait */
uint16_t SFX_wait(uint16_t bc, uint16_t caller_hl)
{
	uint8_t c = (uint8_t)bc;
	if (c == 3u)
		Func_fc1cd();
	else
		SFX_ApplyPitchOffset(c);
	uint8_t wait_val = gb_read8(caller_hl);
	caller_hl = (uint16_t)(caller_hl + 1u);
	gb_write8((uint16_t)(wde33_ADDR + bc), wait_val);
	return Func_fc105(bc, caller_hl);
}
/* <<< factory SFX_wait */
