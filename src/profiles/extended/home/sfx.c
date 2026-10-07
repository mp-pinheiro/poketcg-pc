/* >>> part includes */
#include "home/sfx.h"

#include "home/audio.h"

#include <stdbool.h>
#include "generated/rom.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> part SFX_BANK */
#define SFX_BANK NumberOfSFX_BANK
/* <<< part SFX_BANK */
/* === part rAUD1LEN */
/* >>> part rAUD1SWEEP */
#define rAUD1SWEEP 0xFF10u
/* <<< part rAUD1SWEEP */
/* >>> factory Func_fc26c */
/* sfx.asm:493-498. */
void Func_fc26c(void)
{
	wSFXIsPlaying = 0;
	wCurSfxID = 0x80;
}
/* <<< factory Func_fc26c */
/* >>> part SFX_Frequency */
static uint16_t SFX_Frequency(uint16_t cmd_ptr, uint8_t c, uint8_t high_nibble)
{
	uint8_t low = wAudioArg;
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
/* <<< part SFX_Frequency */
/* >>> part SFX_Envelope */
static uint16_t SFX_Envelope(uint16_t cmd_ptr, uint8_t c)
{
	write_wde2b(c, 0x80u);
	uint8_t env_val = wAudioArg;
	cmd_ptr = (uint16_t)(cmd_ptr + 1u);
	uint16_t reg = (uint16_t)(rAUD1ENV + (uint16_t)c * 5u);
	gb_write8(reg, env_val);
	return cmd_ptr;
}
/* <<< part SFX_Envelope */
/* >>> part SFX_Loop */
static uint16_t SFX_Loop(uint16_t cmd_ptr, uint8_t c)
{
	uint8_t count = wAudioArg;
	cmd_ptr = (uint16_t)(cmd_ptr + 1u);
	uint16_t store_addr = (uint16_t)(wde43_ADDR + (uint16_t)c * 2u);
	gb_write8(store_addr, (uint8_t)cmd_ptr);
	gb_write8((uint16_t)(store_addr + 1u), (uint8_t)(cmd_ptr >> 8));
	gb_write8((uint16_t)(wde3f_ADDR + c), count);
	return cmd_ptr;
}
/* <<< part SFX_Loop */
/* >>> part SFX_PitchOffset */
static uint16_t SFX_PitchOffset(uint16_t cmd_ptr, uint8_t c)
{
	uint8_t offset = wAudioArg;
	cmd_ptr = (uint16_t)(cmd_ptr + 1u);
	if (c == 3u)
		gb_write8(wde32_ADDR, offset);
	else
		gb_write8((uint16_t)(wSFXPitchOffsets_ADDR + c), offset);
	return cmd_ptr;
}
/* <<< part SFX_PitchOffset */
/* >>> part SFX_Wait */
static uint16_t SFX_Wait(uint16_t cmd_ptr, uint8_t c)
{
	if (c == 3u)
		Func_fc1cd();
	else
		SFX_ApplyPitchOffset(c);
	uint8_t wait_val = wAudioArg;
	cmd_ptr = (uint16_t)(cmd_ptr + 1u);
	gb_write8((uint16_t)(wde33_ADDR + c), wait_val);
	return cmd_ptr;
}
/* <<< part SFX_Wait */
/* >>> part SFX_Pan */
/* sfx.asm:423-445. `rlca` rotates pan_val (a) and `rlc e` (sfx.asm:434)
 * independently rotates e's own top bit into its bottom bit; e never reads
 * from a. */
static uint16_t SFX_Pan(uint16_t cmd_ptr, uint8_t c)
{
	uint8_t pan_val = wAudioArg;
	cmd_ptr = (uint16_t)(cmd_ptr + 1u);
	uint8_t ch = (uint8_t)(c + 1u);
	uint8_t e = 0xEEu;
	while (ch) {
		ch = (uint8_t)(ch - 1u);
		if (ch == 0u)
			break;
		pan_val = (uint8_t)((pan_val << 1u) | (pan_val >> 7u));
		e = (uint8_t)((e << 1u) | (e >> 7u));
	}
	wdd85 = (uint8_t)((wdd85 & e) | pan_val);
	return cmd_ptr;
}
/* <<< part SFX_Pan */
/* >>> factory ExecuteNextSFXCommand */
/* sfx.asm:103-138 */
void ExecuteNextSFXCommand(uint16_t hl, uint16_t bc)
{
	uint16_t cmd_ptr = hl;
	uint8_t c = (uint8_t)bc;
	for (;;) {
		uint8_t cmd = GetAudioCmdAndArgs(wSFXBank, cmd_ptr);
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
			cmd_ptr = SFX_EndLoop(cmd_ptr, c);
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
		case 9u:
			gb_write8(rAUD1SWEEP, gb_read8(cmd_ptr));
			cmd_ptr = (uint16_t)(cmd_ptr + 1u);
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
/* >>> factory SFX_Play */
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
	wSFXBank = gb_read8(ptr);
	ptr = (uint16_t)(ptr + 1u);

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
/* <<< factory SFX_Play */
/* >>> factory SFX_frequency */
void SFX_frequency(uint16_t bc, uint16_t caller_hl, uint8_t high)
{
	uint8_t d = high;
	uint8_t e = wAudioArg;
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
	uint8_t a = wAudioArg;
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
	uint8_t pan_val = wAudioArg;
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
/* >>> factory SFX_pitch_offset */
void SFX_pitch_offset(uint16_t bc, uint16_t caller_hl)
{
	gb_write8((uint16_t)(wSFXPitchOffsets_ADDR + bc), wAudioArg);
	caller_hl = (uint16_t)(caller_hl + 1u);
	ExecuteNextSFXCommand(caller_hl, bc);
}
/* <<< factory SFX_pitch_offset */
/* >>> factory SFX_envelope */
void SFX_envelope(uint16_t bc, uint16_t caller_hl)
{
	uint16_t store_addr = (uint16_t)(wde2b_ADDR + bc);
	gb_write8(store_addr, 0x80u);
	uint8_t e = wAudioArg;
	caller_hl = (uint16_t)(caller_hl + 1u);
	uint8_t c = (uint8_t)bc;
	uint16_t reg = (uint16_t)(rAUD1ENV + (uint16_t)c * 5u);
	gb_write8(reg, e);
	ExecuteNextSFXCommand(caller_hl, bc);
}
/* <<< factory SFX_envelope */
/* >>> factory SFX_wait */
uint16_t SFX_wait(uint16_t bc, uint16_t caller_hl)
{
	uint8_t c = (uint8_t)bc;
	if (c == 3u)
		Func_fc1cd();
	else
		SFX_ApplyPitchOffset(c);
	uint8_t wait_val = wAudioArg;
	caller_hl = (uint16_t)(caller_hl + 1u);
	gb_write8((uint16_t)(wde33_ADDR + bc), wait_val);
	return Func_fc105(bc, caller_hl);
}
/* <<< factory SFX_wait */
/* === factory GetSFXCommandAndArgs */
/* === factory SFX_sweep */
