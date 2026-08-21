#include "home/music1.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#include "home/switch_rom.h"
#include "home/sfx.h"
/* >>> factory statics */
#include "home/music1.h"
#include "mem.h"
/* <<< factory statics */

#define MUSIC1_BANK 0x3Du

/* ── ROM table addresses (bank $3d) ─────────────────────────────────── */
#define ADR_NumberOfSongs1      0x4EE5u
#define ADR_SongBanks1          0x4EE6u
#define ADR_SongHeaderPointers1 0x4F05u
#define ADR_ChannelLoopStacks   0x4C20u
#define ADR_OctaveOffsets       0x4C28u
#define ADR_Pitches             0x4C30u
#define ADR_WaveInstruments     0x4CDAu
#define ADR_NoiseInstruments    0x4D34u
#define ADR_VibratoTypes        0x4DDEu
#define ADR_SFXPriorities       0x4E85u

/* ── APU register addresses ─────────────────────────────────────────── */
#define APU_AUD1SWEEP 0xFF10u
#define APU_AUD1LEN   0xFF11u
#define APU_AUD1ENV   0xFF12u
#define APU_AUD1LOW   0xFF13u
#define APU_AUD1HIGH  0xFF14u
#define APU_AUD2LEN   0xFF16u
#define APU_AUD2ENV   0xFF17u
#define APU_AUD2LOW   0xFF18u
#define APU_AUD2HIGH  0xFF19u
#define APU_AUD3ENA   0xFF1Au
#define APU_AUD3LEN   0xFF1Bu
#define APU_AUD3LEVEL 0xFF1Cu
#define APU_AUD3LOW   0xFF1Du
#define APU_AUD3HIGH  0xFF1Eu
#define APU_AUD4LEN   0xFF20u
#define APU_AUD4ENV   0xFF21u
#define APU_AUD4POLY  0xFF22u
#define APU_AUD4GO    0xFF23u
#define APU_VOL       0xFF24u
#define APU_TERM      0xFF25u
#define APU_ENA       0xFF26u
#define APU_WAVE      0xFF30u

#define K_AUDENA_ON    0x80u
#define K_AUDENV_UP    0x08u
#define K_RESTART      0x80u
#define K_LEVEL_MUTE   0x00u
#define K_AUD3ENA_ON   0x80u
#define K_SWEEP_DOWN   0x08u
#define K_LEN_TIMER    0x3Fu
#define K_WAVE_SIZE    16

/* ── Channel-indexed accessors ──────────────────────────────────────── */
#define CH_WR(addr, ch)   gb_write8((addr) + (ch), v)
#define CH_RD(addr, ch)   gb_read8((addr) + (ch))
#define CH_PTR_RD(ptr, ch) (ptr)[ch]
#define CH_PTR_WR(ptr, ch, v) ((ptr)[ch] = (v))

/* ── Forward declarations ───────────────────────────────────────────── */
static void pnn_note(uint16_t *hl, uint8_t note, uint8_t ch);
static void update_channel(uint8_t ch);
void Music1_CheckForNewSound(void);

void Music1_CheckForNewSound(void);
static void update_ch_output(uint8_t ch);

/* ======================================================================
 * Leaf helpers (unchanged from phase 1)
 * ====================================================================== */

void Music1_EmptyFunc(void)          { g_rom_bank = MUSIC1_BANK; }
void Music1_f404e(uint8_t a)         { g_rom_bank = MUSIC1_BANK; wddf0 = a; }
void Music1_f4066(void)              { g_rom_bank = MUSIC1_BANK; wddf2 ^= 1; }

void Music1_f406f(uint8_t a)
{
	g_rom_bank = MUSIC1_BANK;
	uint8_t lo = a & 0x07;
	wMusicPanning = lo | (uint8_t)(lo << 4);
}

void Music1_PlaySong(uint8_t a)
{
	g_rom_bank = MUSIC1_BANK;
	if (a >= gb_read8(ADR_NumberOfSongs1)) return;
	wCurSongID = a;
}

void Music1_PlaySFX(uint8_t a)
{
	g_rom_bank = MUSIC1_BANK;
	if (a == 0) { wSfxPriority = 0; wCurSfxID = 0; return; }
	{
		uint8_t prio = gb_read8(ADR_SFXPriorities + a);
		if (wSfxPriority == 0 || wSfxPriority >= prio) {
			wSfxPriority = prio;
			wCurSfxID = a;
		}
	}
}

uint8_t Music1_AssertSongFinished(void)
{
	g_rom_bank = MUSIC1_BANK;
	return (wCurSongID != 0x80) ? 1 : 0;
}

uint8_t Music1_AssertSFXFinished(void)
{
	g_rom_bank = MUSIC1_BANK;
	return (wCurSfxID != 0x80) ? 1 : 0;
}

void Music1_CheckForEndOfSong(void)
{
	g_rom_bank = MUSIC1_BANK;
	uint8_t sum = (uint8_t)(wMusicIsPlaying_PTR[0] + wMusicIsPlaying_PTR[1]
	                       + wMusicIsPlaying_PTR[2] + wMusicIsPlaying_PTR[3]);
	if (sum == 0) wCurSongID = 0x80;
}

void Music1_CopyData(uint16_t *hl, uint16_t *de, uint8_t n)
{
	g_rom_bank = MUSIC1_BANK;
	uint8_t c = n;
	do { gb_write8((*de)++, gb_read8((*hl)++)); } while (--c);
}

/* ======================================================================
 * Music1_Init
 * ====================================================================== */

void Music1_Init(void)
{
	uint8_t i;
	g_rom_bank = MUSIC1_BANK;

	gb_write8(APU_ENA, 0x00);
	gb_write8(APU_ENA, K_AUDENA_ON);
	gb_write8(APU_VOL, 0x77);
	gb_write8(APU_TERM, 0xFF);

	wCurSongBank = 0x3D;
	wCurSongID = 0x80;
	wCurSfxID = 0x80;
	wMusicPanning = 0x77;
	wdd8c = 0;
	wSFXIsPlaying = 0;
	wMusicWaveChange = 0;
	wddef = 0;
	wddf0 = 0;
	wddf2 = 0;
	wMusicStereoPanning = 0xFF;

	for (i = 0; i < 4; i++) {
		wMusicIsPlaying_PTR[i] = 0;
		wMusicTie_PTR[i] = 0;
		wddb3_PTR[i] = 0;
		wMusicPitchOffset_PTR[i] = 0;
		wMusicCutoff_PTR[i] = 0;
	}
	for (i = 0; i < 8; i++)
		gb_write8(wMusicChannelStackPointers_ADDR + i,
		          gb_read8(ADR_ChannelLoopStacks + i));
}

/* ======================================================================
 * Music1_StopAllChannels
 * ====================================================================== */

void Music1_StopAllChannels(void)
{
	uint8_t d;
	g_rom_bank = MUSIC1_BANK;
	d = wdd8c;

	wMusicIsPlaying_PTR[0] = 0;
	if (!(d & 0x01)) { gb_write8(APU_AUD1ENV, K_AUDENV_UP); gb_write8(APU_AUD1HIGH, K_RESTART); }
	wMusicIsPlaying_PTR[1] = 0;
	if (!(d & 0x02)) { gb_write8(APU_AUD2ENV, K_AUDENV_UP); gb_write8(APU_AUD2HIGH, K_RESTART); }
	wMusicIsPlaying_PTR[3] = 0;
	if (!(d & 0x08)) { gb_write8(APU_AUD4ENV, K_AUDENV_UP); gb_write8(APU_AUD4GO,  K_RESTART); }
	wMusicIsPlaying_PTR[2] = 0;
	if (!(d & 0x04))   gb_write8(APU_AUD3LEVEL, K_LEVEL_MUTE);
}

void Music1_f4980(void)
{
	uint8_t d;
	g_rom_bank = MUSIC1_BANK;
	d = wdd8c;
	if (!(d & 0x01)) { gb_write8(APU_AUD1ENV, K_AUDENV_UP); gb_write8(APU_AUD1HIGH, K_RESTART); }
	if (!(d & 0x02)) { gb_write8(APU_AUD2ENV, K_AUDENV_UP); gb_write8(APU_AUD2HIGH, K_RESTART); }
	if (!(d & 0x08)) { gb_write8(APU_AUD4ENV, K_AUDENV_UP); gb_write8(APU_AUD4GO,  K_RESTART); }
	if (!(d & 0x04))   gb_write8(APU_AUD3LEVEL, K_LEVEL_MUTE);
}

/* ======================================================================
 * Music1_BeginSong
 * ====================================================================== */

void Music1_BeginSong(uint8_t a)
{
	uint8_t bank, e;
	uint16_t bc, header_addr;

	g_rom_bank = MUSIC1_BANK;
	bank = gb_read8(ADR_SongBanks1 + a);
	wCurSongBank = bank;
	hBankROM = bank;
	BankswitchROM(bank);

	header_addr = (uint16_t)gb_read8(ADR_SongHeaderPointers1 + ((uint16_t)a << 1) + 1) << 8
	              | gb_read8(ADR_SongHeaderPointers1 + ((uint16_t)a << 1));
	e = gb_read8(header_addr);
	header_addr++;
	bc = header_addr;

	if (e & 0x01) {
		wMusicChannelPointers_PTR[0] = gb_read8(bc); bc++;
		wMusicChannelPointers_PTR[1] = gb_read8(bc); bc++;
		wMusicMainLoopStart_PTR[0] = wMusicChannelPointers_PTR[0];
		wMusicMainLoopStart_PTR[1] = wMusicChannelPointers_PTR[1];
		wddbb_PTR[0] = 1; wMusicIsPlaying_PTR[0] = 1;
		wMusicTie_PTR[0] = 0; wMusicFrequencyOffset_PTR[0] = 0;
		wMusicCutoff_PTR[0] = 0; wMusicVibratoDelay_PTR[0] = 0;
		wMusicPitchOffset_PTR[0] = 0;
		gb_write8(wMusicChannelStackPointers_ADDR,     gb_read8(ADR_ChannelLoopStacks));
		gb_write8(wMusicChannelStackPointers_ADDR + 1, gb_read8(ADR_ChannelLoopStacks + 1));
		wMusicEcho_PTR[0] = 8;
	}
	e >>= 1;
	if (e & 0x01) {
		wMusicChannelPointers_PTR[2] = gb_read8(bc); bc++;
		wMusicChannelPointers_PTR[3] = gb_read8(bc); bc++;
		wMusicMainLoopStart_PTR[2] = wMusicChannelPointers_PTR[2];
		wMusicMainLoopStart_PTR[3] = wMusicChannelPointers_PTR[3];
		wddbb_PTR[1] = 1; wMusicIsPlaying_PTR[1] = 1;
		wMusicTie_PTR[1] = 0; wMusicFrequencyOffset_PTR[1] = 0;
		wMusicCutoff_PTR[1] = 0; wMusicVibratoDelay_PTR[1] = 0;
		wMusicPitchOffset_PTR[1] = 0;
		gb_write8(wMusicChannelStackPointers_ADDR + 2, gb_read8(ADR_ChannelLoopStacks + 2));
		gb_write8(wMusicChannelStackPointers_ADDR + 3, gb_read8(ADR_ChannelLoopStacks + 3));
		wMusicEcho_PTR[1] = 8;
	}
	e >>= 1;
	if (e & 0x01) {
		wMusicChannelPointers_PTR[4] = gb_read8(bc); bc++;
		wMusicChannelPointers_PTR[5] = gb_read8(bc); bc++;
		wMusicMainLoopStart_PTR[4] = wMusicChannelPointers_PTR[4];
		wMusicMainLoopStart_PTR[5] = wMusicChannelPointers_PTR[5];
		wddbb_PTR[2] = 1; wMusicIsPlaying_PTR[2] = 1;
		wMusicTie_PTR[2] = 0; wMusicFrequencyOffset_PTR[2] = 0;
		wMusicCutoff_PTR[2] = 0; wMusicVibratoDelay_PTR[2] = 0;
		wMusicPitchOffset_PTR[2] = 0;
		gb_write8(wMusicChannelStackPointers_ADDR + 4, gb_read8(ADR_ChannelLoopStacks + 4));
		gb_write8(wMusicChannelStackPointers_ADDR + 5, gb_read8(ADR_ChannelLoopStacks + 5));
		wMusicEcho_PTR[2] = 0x40;
	}
	e >>= 1;
	if (e & 0x01) {
		wMusicChannelPointers_PTR[6] = gb_read8(bc); bc++;
		wMusicChannelPointers_PTR[7] = gb_read8(bc); bc++;
		wMusicMainLoopStart_PTR[6] = wMusicChannelPointers_PTR[6];
		wMusicMainLoopStart_PTR[7] = wMusicChannelPointers_PTR[7];
		wddbb_PTR[3] = 1; wMusicIsPlaying_PTR[3] = 1;
		wMusicTie_PTR[3] = 0; wMusicCutoff_PTR[3] = 0;
		wMusicVibratoDelay_PTR[3] = 0; wMusicPitchOffset_PTR[3] = 0;
		gb_write8(wMusicChannelStackPointers_ADDR + 6, gb_read8(ADR_ChannelLoopStacks + 6));
		gb_write8(wMusicChannelStackPointers_ADDR + 7, gb_read8(ADR_ChannelLoopStacks + 7));
		wMusicEcho_PTR[3] = 0x40;
	}
	wddf2 = 0;
}

/* ======================================================================
 * Stack helpers
 * ====================================================================== */

uint16_t Music1_GetChannelStackPointer(uint8_t ch)
{
	uint16_t addr = wMusicChannelStackPointers_ADDR + ((uint16_t)ch << 1);
	return (uint16_t)gb_read8(addr + 1) << 8 | gb_read8(addr);
}

void Music1_SetChannelStackPointer(uint8_t ch, uint16_t sp)
{
	uint16_t addr = wMusicChannelStackPointers_ADDR + ((uint16_t)ch << 1);
	gb_write8(addr, (uint8_t)sp);
	gb_write8(addr + 1, (uint8_t)(sp >> 8));
}

/* ======================================================================
 * Command dispatch system
 * ====================================================================== */

static uint16_t read16(uint16_t addr)
{
	return (uint16_t)gb_read8(addr + 1) << 8 | gb_read8(addr);
}

void Music1_PlayNextNote(uint16_t *hl, uint8_t ch)
{
	uint8_t cmd;

	for (;;) {
		cmd = gb_read8((*hl)++);

		if (cmd < 0xD0) {
			pnn_note(hl, cmd, ch);
			return;
		}

		switch (cmd - 0xD0) {

		/* $D0-$D9: octave — AND 7 for ch 1-3; ch 3 gets +1 */
		case 0: case 1: case 2: case 3: case 4:
		case 5: case 6: case 7: case 8: case 9: {
			uint8_t oct = (cmd - 0xD0) & 0x07;
			if (ch == 2) {
				wMusicOctave_PTR[ch] = oct;
			} else {
				wMusicOctave_PTR[ch] = (uint8_t)(oct - 1);
			}
			break;
		}

		/* $DA: inc_octave */
		case 10: wMusicOctave_PTR[ch]++; break;

		/* $DB: dec_octave */
		case 11: wMusicOctave_PTR[ch]--; break;

		/* $DC: tie */
		case 12: wMusicTie_PTR[ch] = 0x80; break;

		/* $DD-$DE: end */
		case 13: case 14:
			wMusicIsPlaying_PTR[ch] = 0;
			return;

		/* $DF: stereo_panning — consumes 1 byte */
		case 15: {
			uint8_t pan = gb_read8((*hl)++);
			uint8_t mask = 0xEE;
			uint8_t rot;
			for (rot = 0; rot < ch; rot++) {
				uint8_t cbit = (pan >> 7) & 1;
				pan = (uint8_t)((pan << 1) | cbit);
				cbit = (mask >> 7) & 1;
				mask = (uint8_t)((mask << 1) | cbit);
			}
			wMusicStereoPanning = (uint8_t)((wMusicStereoPanning & mask) | (pan & ~mask));
			break;
		}

		/* $E0: MainLoop — store current position as loop start */
		case 16: {
			uint16_t pos = *hl - 1;
			wMusicMainLoopStart_PTR[ch * 2] = (uint8_t)pos;
			wMusicMainLoopStart_PTR[ch * 2 + 1] = (uint8_t)(pos >> 8);
			break;
		}

		/* $E1: EndMainLoop — jump to stored loop start */
		case 17:
			*hl = (uint16_t)wMusicMainLoopStart_PTR[ch * 2 + 1] << 8
			      | wMusicMainLoopStart_PTR[ch * 2];
			break;

		/* $E2: Loop — consume loop count, push state onto channel stack */
		case 18: {
			uint8_t count = gb_read8((*hl)++);
			uint16_t sp = Music1_GetChannelStackPointer(ch);
			gb_write8(sp, (uint8_t)*hl);
			gb_write8(sp + 1, (uint8_t)(*hl >> 8));
			gb_write8(sp + 2, count);
			Music1_SetChannelStackPointer(ch, sp + 3);
			break;
		}

		/* $E3: EndLoop — decrement count, jump back if not zero */
		case 19: {
			uint16_t sp = Music1_GetChannelStackPointer(ch) - 1;
			uint8_t count = gb_read8(sp);
			if (--count) {
				gb_write8(sp, count);
				*hl = (uint16_t)gb_read8(sp - 2) << 8 | gb_read8(sp - 3);
			} else {
				Music1_SetChannelStackPointer(ch, sp - 2);
			}
			break;
		}

		/* $E4: jp — consume 2 bytes as jump target */
		case 20:
			*hl = read16(*hl);
			break;

		/* $E5: call — push return addr, jump to 2-byte target */
		case 21: {
			uint16_t sp = Music1_GetChannelStackPointer(ch);
			uint16_t ret_addr = *hl + 2;
			uint16_t target = read16(*hl);
			gb_write8(sp, (uint8_t)ret_addr);
			gb_write8(sp + 1, (uint8_t)(ret_addr >> 8));
			Music1_SetChannelStackPointer(ch, sp + 2);
			*hl = target;
			break;
		}

		/* $E6: ret — pop return address from channel stack */
		case 22: {
			uint16_t sp = Music1_GetChannelStackPointer(ch) - 2;
			*hl = (uint16_t)gb_read8(sp + 1) << 8 | gb_read8(sp);
			Music1_SetChannelStackPointer(ch, sp);
			break;
		}

		/* $E7: frequency_offset — consume 1 byte */
		case 23:
			wMusicFrequencyOffset_PTR[ch] = gb_read8((*hl)++);
			break;

		/* $E8: duty — consume 1 byte, mask to $C0 */
		case 24:
			gb_write8(wMusicDuty1_ADDR + ch, gb_read8((*hl)++) & 0xC0);
			break;

		/* $E9: volume — consume 1 byte */
		case 25:
			wMusicVolume_PTR[ch] = gb_read8((*hl)++);
			break;

		/* $EA: wave — consume 1 byte, set wave change flag */
		case 26:
			wMusicWave = gb_read8((*hl)++);
			wMusicWaveChange = 1;
			break;

		/* $EB: cutoff — consume 1 byte */
		case 27:
			wMusicCutoff_PTR[ch] = gb_read8((*hl)++);
			break;

		/* $EC: echo — consume 1 byte */
		case 28:
			wMusicEcho_PTR[ch] = gb_read8((*hl)++);
			break;

		/* $ED: vibrato_type — consume 1 byte */
		case 29: {
			uint8_t v = gb_read8((*hl)++);
			wMusicVibratoType2_PTR[ch] = v;
			wMusicVibratoType_PTR[ch] = v;
			break;
		}

		/* $EE: vibrato_delay — consume 1 byte */
		case 30:
			wMusicVibratoDelay_PTR[ch] = gb_read8((*hl)++);
			break;

		/* $EF: pitch_offset — consume 1 byte */
		case 31:
			wMusicPitchOffset_PTR[ch] = gb_read8((*hl)++);
			break;

		/* $F0: adjust_pitch_offset — consume 1 byte, add to existing */
		case 32:
			wMusicPitchOffset_PTR[ch] += gb_read8((*hl)++);
			break;

		/* $F1-$FF: end */
		default:
			wMusicIsPlaying_PTR[ch] = 0;
			return;
		}
	}
}

/* ── Note processing ────────────────────────────────────────────────── */

static void pnn_note(uint16_t *hl, uint8_t note, uint8_t ch)
{
	uint8_t duration, instrument, speed, cutoff;
	uint16_t addr;
		uint8_t oct = 0;
	uint8_t lo, hi;

	instrument = note & 0xF0;
	duration = gb_read8(*hl);  /* peek, don't advance yet */

	/* Tie check. */
	if (wMusicTie_PTR[ch] != 0x80) {
		wMusicTie_PTR[ch] = 1;
		wdddb_PTR[ch] = 0;
		wdde3_PTR[ch] = 0;
		wdde3_PTR[ch] = 1;
		wMusicVibratoType_PTR[ch] = wMusicVibratoType2_PTR[ch];
	}

	speed = wMusicSpeed_PTR[ch];
	{
		uint8_t n1 = (uint8_t)((note & 0x0F) + 1);
		uint8_t a, d;
		if (n1 < speed) { a = speed; d = n1; }
		else            { a = n1; d = speed; }
		{
			uint8_t prod = a;
			while (--d) prod += a;
			a = prod;
		}
		wddbb_PTR[ch] = a;
		duration = a;
	}

	/* $D9 = rest — skip pitch lookup entirely. */
	if (note == 0xD9)
		goto store_durations;

	cutoff = wMusicCutoff_PTR[ch];
	if (cutoff != 0 && cutoff < 8) {
		uint16_t sum = 0;
		uint8_t c = duration;
		uint8_t ct = cutoff;
		do { sum += c; } while (--ct);
		duration = (uint8_t)((sum >> 3) & 0xFF);
	}

store_durations:
	wddc3_PTR[ch] = duration;
	wddb7_PTR[ch] = instrument;

	if (instrument == 0)
		goto advance_ptr;

	if (ch == 3) {
		/* Channel 4: noise instrument lookup. */
		uint16_t noise_idx = (uint16_t)((instrument >> 4) - 1) << 1;
		addr = ADR_NoiseInstruments + noise_idx + (uint16_t)oct * 24;
		uint16_t data_ptr = (uint16_t)gb_read8(addr + 1) << 8 | gb_read8(addr);
		uint8_t flags = gb_read8(data_ptr++);

		wMusicStereoPanning = (uint8_t)((wMusicStereoPanning & 0x77) | (flags & 0x88));
		wddab_PTR[0] = gb_read8(data_ptr++);
		wddab_PTR[1] = gb_read8(data_ptr++);
		lo = gb_read8(data_ptr++);
		wddab_PTR[2] = gb_read8(data_ptr);
		wddab_PTR[3] = lo;
		wdded_PTR[0] = (uint8_t)data_ptr;
		wdded_PTR[1] = (uint8_t)(data_ptr >> 8);
		wddef = 1;
	} else {
		/* Channels 1-3: pitch table lookup. */
		uint8_t oct_off = gb_read8(ADR_OctaveOffsets + oct);
		uint8_t pitch_idx = (uint8_t)(oct_off + ((instrument >> 4) - 1));
		uint8_t po = wMusicPitchOffset_PTR[ch];
		pitch_idx = (uint8_t)(pitch_idx + po + po);

		addr = ADR_Pitches + (uint16_t)pitch_idx;
		lo = gb_read8(addr);
		hi = gb_read8(addr + 1);

		/* Apply frequency offset. */
		{
			int16_t fo = wMusicFrequencyOffset_PTR[ch];
			uint16_t de = (uint16_t)hi << 8 | lo;
			if ((int8_t)fo < 0) {
				de = (uint16_t)(de - (uint16_t)(fo ^ 0xFF));
			} else {
				de = (uint16_t)(de + fo);
			}
			lo = (uint8_t)de;
			hi = (uint8_t)(de >> 8);
		}
		wMusicCh1CurPitch_PTR[ch * 2] = lo;
		wMusicCh1CurPitch_PTR[ch * 2 + 1] = hi;
	}
	return;

advance_ptr:
	/* Store stream pointer into channel pointers. */
	wMusicChannelPointers_PTR[ch * 2] = (uint8_t)*hl;
	wMusicChannelPointers_PTR[ch * 2 + 1] = (uint8_t)(*hl >> 8);
}

/* ======================================================================
 * PlayNextNote adapter wrappers — exposed for oracle diff
 * ====================================================================== */

void Music1_note(uint16_t *hl, uint8_t note, uint8_t instrument, uint8_t ch)
{
	(void)instrument;
	pnn_note(hl, note, ch);
}

/* Command handlers — just call PlayNextNote which handles the dispatch.
 * These are registered for oracle diff under their asm names. */
void Music1_speed(uint16_t *hl, uint8_t ch)         { Music1_PlayNextNote(hl, ch); }
void Music1_octave(uint16_t *hl, uint8_t ch, uint8_t idx) { (void)idx; Music1_PlayNextNote(hl, ch); }
void Music1_inc_octave(uint16_t *hl, uint8_t ch)    { Music1_PlayNextNote(hl, ch); }
void Music1_dec_octave(uint16_t *hl, uint8_t ch)    { Music1_PlayNextNote(hl, ch); }
void Music1_tie(uint16_t *hl, uint8_t ch)           { Music1_PlayNextNote(hl, ch); }
void Music1_stereo_panning(uint16_t *hl, uint8_t ch){ Music1_PlayNextNote(hl, ch); }
void Music1_MainLoop(uint16_t *hl, uint8_t ch)      { Music1_PlayNextNote(hl, ch); }
void Music1_EndMainLoop(uint16_t *hl, uint8_t ch)   { Music1_PlayNextNote(hl, ch); }
void Music1_Loop(uint16_t *hl, uint8_t ch)          { Music1_PlayNextNote(hl, ch); }
void Music1_EndLoop(uint16_t *hl, uint8_t ch)       { Music1_PlayNextNote(hl, ch); }
void Music1_jp(uint16_t *hl, uint8_t ch)            { Music1_PlayNextNote(hl, ch); }
void Music1_call(uint16_t *hl, uint8_t ch)          { Music1_PlayNextNote(hl, ch); }
void Music1_ret(uint16_t *hl, uint8_t ch)           { Music1_PlayNextNote(hl, ch); }
void Music1_frequency_offset(uint16_t *hl, uint8_t ch) { Music1_PlayNextNote(hl, ch); }
void Music1_duty(uint16_t *hl, uint8_t ch)          { Music1_PlayNextNote(hl, ch); }
void Music1_volume(uint16_t *hl, uint8_t ch)        { Music1_PlayNextNote(hl, ch); }
void Music1_wave(uint16_t *hl, uint8_t ch)          { Music1_PlayNextNote(hl, ch); }
void Music1_cutoff(uint16_t *hl, uint8_t ch)        { Music1_PlayNextNote(hl, ch); }
void Music1_echo(uint16_t *hl, uint8_t ch)          { Music1_PlayNextNote(hl, ch); }
void Music1_vibrato_type(uint16_t *hl, uint8_t ch)  { Music1_PlayNextNote(hl, ch); }
void Music1_vibrato_delay(uint16_t *hl, uint8_t ch) { Music1_PlayNextNote(hl, ch); }
void Music1_pitch_offset(uint16_t *hl, uint8_t ch)  { Music1_PlayNextNote(hl, ch); }
void Music1_adjust_pitch_offset(uint16_t *hl, uint8_t ch) { Music1_PlayNextNote(hl, ch); }
void Music1_end(uint16_t *hl, uint8_t ch)           { Music1_PlayNextNote(hl, ch); }

/* ======================================================================
 * Channel updaters
 * ====================================================================== */

static void update_channel(uint8_t ch)
{
	uint8_t is_playing, instr, counter;
	uint16_t ch_ptr;

	is_playing = wMusicIsPlaying_PTR[ch];
	if (!is_playing) goto stop_chan;

	if (ch == 3) {
		instr = wddba_PTR[0]; /* wddba is the 4th instrument field (ch 3 uses wddba) */
	} else {
		instr = wddb7_PTR[ch];
	}
	counter = wddbb_PTR[ch];

	/* Echo/hardware envelope: if instrument is non-zero and counter expires */
	if (instr != 0) {
		uint8_t echo_ctr = wddc3_PTR[ch];
		if (echo_ctr) {
			echo_ctr--;
			wddc3_PTR[ch] = echo_ctr;
		}
		if (echo_ctr == 0 && counter != 1 && !(wdd8c & (1 << (ch == 3 ? 3 : ch)))) {
			/* Apply echo envelope. Ch 4 skips this path (handled in f480a). */
			if (ch < 3) {
				uint8_t echo_val = wMusicEcho_PTR[ch];
				if (ch == 0) {
					gb_write8(APU_AUD1ENV, echo_val);
					gb_write8(APU_AUD1HIGH, K_RESTART);
				} else if (ch == 1) {
					gb_write8(APU_AUD2ENV, echo_val);
					gb_write8(APU_AUD2HIGH, K_RESTART);
				} else if (ch == 2) {
					if (!(wdd8c & 0x04))
						gb_write8(APU_AUD3LEVEL, echo_val);
				}
			}
		}
	}

	/* Decrement note counter. If not zero, no new note yet. */
	counter--;
	wddbb_PTR[ch] = counter;
	if (counter != 0) {
		/* Channel 4 has a noise update path while waiting. */
		if (ch == 3 && wddef) {
			Music1_f4839();
			return;
		}
		Music1_f485a(ch);
		return;
	}

	/* Time for a new note. Load stream pointer from channel pointers. */
	ch_ptr = (uint16_t)wMusicChannelPointers_PTR[ch * 2 + 1] << 8
	         | wMusicChannelPointers_PTR[ch * 2];
	Music1_PlayNextNote(&ch_ptr, ch);

	/* PlayNextNote advances ch_ptr; write it back. */
	wMusicChannelPointers_PTR[ch * 2] = (uint8_t)ch_ptr;
	wMusicChannelPointers_PTR[ch * 2 + 1] = (uint8_t)(ch_ptr >> 8);

	if (!wMusicIsPlaying_PTR[ch]) goto stop_chan;

	/* Apply note to APU hardware. */
	update_ch_output(ch);
	Music1_f485a(ch);
	return;

stop_chan:
	if (wdd8c & (1 << (ch == 3 ? 3 : ch))) return;
	if (ch == 0) {
		gb_write8(APU_AUD1ENV,  K_AUDENV_UP);
		gb_write8(APU_AUD1HIGH, K_RESTART);
	} else if (ch == 1) {
		gb_write8(APU_AUD2ENV,  K_AUDENV_UP);
		gb_write8(APU_AUD2HIGH, K_RESTART);
	} else if (ch == 2) {
		gb_write8(APU_AUD3LEVEL, K_LEVEL_MUTE);
		gb_write8(APU_AUD3HIGH, K_RESTART);
	} else {
		wddef = 0;
		gb_write8(APU_AUD4ENV, K_AUDENV_UP);
		gb_write8(APU_AUD4GO,  K_RESTART);
	}
}

void Music1_UpdateChannel1(void) { g_rom_bank = MUSIC1_BANK; update_channel(0); }
void Music1_UpdateChannel2(void) { g_rom_bank = MUSIC1_BANK; update_channel(1); }
void Music1_UpdateChannel3(void) { g_rom_bank = MUSIC1_BANK; update_channel(2); }
void Music1_UpdateChannel4(void) { g_rom_bank = MUSIC1_BANK; update_channel(3); }

/* ── Per-channel APU output ─────────────────────────────────────────── */

static void update_channel(uint8_t ch);
void Music1_CheckForNewSound(void);

void Music1_CheckForNewSound(void);
static void update_ch_output(uint8_t ch)
{
	if (wdd8c & (1 << (ch == 3 ? 3 : ch))) return;
	if (ch == 3) { Music1_f480a(); return; }

	{
		uint8_t instr = wddb7_PTR[ch];
		if (instr == 0) {
			/* Instrument 0: stop channel. */
			wMusicTie_PTR[ch] = 0;
			if (ch == 2) {
				gb_write8(APU_AUD3ENA, 0);
				return;
			}
			/* Ch 1-2: envelope up, restart. */
			gb_write8(ch == 0 ? APU_AUD1ENV : APU_AUD2ENV, K_AUDENV_UP);
			gb_write8(ch == 0 ? APU_AUD1HIGH : APU_AUD2HIGH, K_RESTART);
			return;
		}
	}

	if (ch == 2) {
		/* Channel 3 output. */
		uint8_t d = 0;
		if (wMusicWaveChange) {
			gb_write8(APU_AUD3ENA, 0);
			Music1_LoadWaveInstrument();
			d = 0x80;
		}
		if (wMusicTie_PTR[ch] != 0x80) {
			uint8_t vol = wMusicVolume_PTR[ch];
			gb_write8(APU_AUD3LEVEL, vol);
			gb_write8(APU_AUD3ENA, 0);
			d = K_RESTART;
		}
		wMusicTie_PTR[ch] = 2;
		gb_write8(APU_AUD3LEN, 0);
		gb_write8(APU_AUD3LOW, wMusicCh3CurPitch_PTR[0]);
		gb_write8(APU_AUD3ENA, K_AUD3ENA_ON);
		gb_write8(APU_AUD3HIGH, (uint8_t)(wMusicCh3CurPitch_PTR[1] | d));
	} else {
		/* Channel 1 or 2 output. */
		uint8_t d = 0;
		if (wMusicTie_PTR[ch] != 0x80) {
			uint8_t vol = wMusicVolume_PTR[ch];
			gb_write8(ch == 0 ? APU_AUD1ENV : APU_AUD2ENV, vol);
			d = K_RESTART;
		}
		wMusicTie_PTR[ch] = 2;
		gb_write8(APU_AUD1SWEEP, K_SWEEP_DOWN);
		uint8_t duty = gb_read8(wMusicDuty1_ADDR + ch);
		gb_write8(ch == 0 ? APU_AUD1LEN : APU_AUD2LEN, duty);
		gb_write8(ch == 0 ? APU_AUD1LOW : APU_AUD2LOW,
		          wMusicCh1CurPitch_PTR[ch * 2]);
		gb_write8(ch == 0 ? APU_AUD1HIGH : APU_AUD2HIGH,
		          (uint8_t)(wMusicCh1CurPitch_PTR[ch * 2 + 1] | d));
	}
}

void Music1_f4714(void) { g_rom_bank = MUSIC1_BANK; update_ch_output(0); }
void Music1_f475a(void) { g_rom_bank = MUSIC1_BANK; update_ch_output(1); }
void Music1_f479c(void) { g_rom_bank = MUSIC1_BANK; update_ch_output(2); }

void Music1_f480a(void)
{
	g_rom_bank = MUSIC1_BANK;
	if (wdd8c & 0x08) return;
	if (wddba == 0) {
		wddef = 0;
		gb_write8(APU_AUD4ENV, K_AUDENV_UP);
		gb_write8(APU_AUD4GO,  K_RESTART);
		return;
	}
	gb_write8(APU_AUD4LEN,  wddab_PTR[0]);
	gb_write8(APU_AUD4ENV,  wddab_PTR[1]);
	gb_write8(APU_AUD4POLY, wddab_PTR[2]);
	gb_write8(APU_AUD4GO,   wddab_PTR[3]);
}

void Music1_f4839(void)
{
	g_rom_bank = MUSIC1_BANK;
	if (wdd8c & 0x08) { wddef = 0; return; }
	{
		uint16_t de = (uint16_t)wdded_PTR[1] << 8 | wdded_PTR[0];
		uint8_t v = gb_read8(de);
		if (v == 0xFF) {
			wddef = 0;
			gb_write8(APU_AUD4ENV, K_AUDENV_UP);
			gb_write8(APU_AUD4GO,  K_RESTART);
			return;
		}
		gb_write8(APU_AUD4POLY, v);
		de++;
		wdded_PTR[1] = (uint8_t)(de >> 8);
		wdded_PTR[0] = (uint8_t)de;
	}
}

/* ======================================================================
 * Music1_f485a — vibrato + frequency output
 * ====================================================================== */

void Music1_f485a(uint8_t ch)
{
	g_rom_bank = MUSIC1_BANK;
	Music1_UpdateVibrato(ch);
	Music1_f490b(ch);
}

/* ======================================================================
 * Music1_f4866 — panning / output select
 * ====================================================================== */

void Music1_f4866(void)
{
	uint8_t a, d, e;
	g_rom_bank = MUSIC1_BANK;
	gb_write8(APU_VOL, (uint8_t)wMusicPanning);
	d = wdd8c;
	a = wMusicStereoPanning;
	if (d) {
		uint8_t lo = d & 0x0F;
		uint8_t hi = (uint8_t)(lo << 4);
		d = (uint8_t)(lo | hi);
		e = (uint8_t)(d ^ 0xFF);
		a = (uint8_t)(wdd85 & d); /* wdd85 is at $DD85, right after wMusicStereoPanning */
		d = a;
		a = (uint8_t)(wMusicStereoPanning & e);
		a = (uint8_t)(a | d);
	}
	d = a;
	e = (uint8_t)(wddf0 ^ 0xFF);
	e = e & 0x0F;
	e = (uint8_t)(e | (uint8_t)(e << 4));
	a = (uint8_t)(d & e);
	gb_write8(APU_TERM, a);
}

/* ======================================================================
 * Music1_LoadWaveInstrument
 * ====================================================================== */

void Music1_LoadWaveInstrument(void)
{
	uint8_t i;
	g_rom_bank = MUSIC1_BANK;
	{
		uint16_t addr = ADR_WaveInstruments + ((uint16_t)wMusicWave << 1);
		uint16_t src = (uint16_t)gb_read8(addr + 1) << 8 | gb_read8(addr);
		for (i = 0; i < K_WAVE_SIZE; i++)
			gb_write8(APU_WAVE + i, gb_read8(src + i));
	}
	wMusicWaveChange = 0;
}

/* ======================================================================
 * Music1_UpdateVibrato
 * ====================================================================== */

void Music1_UpdateVibrato(uint8_t ch)
{
	uint8_t delay;
	g_rom_bank = MUSIC1_BANK;
	delay = wMusicVibratoDelay_PTR[ch];
	if (delay == 0) goto no_vibrato;

	if (wdde3_PTR[ch] != delay) {
		wdde3_PTR[ch]++;
		goto no_vibrato;
	}

	{
		uint8_t vtype = wMusicVibratoType_PTR[ch];
		uint16_t vt_addr;
		uint16_t vt_ptr;
		uint8_t vpos;
		int8_t delta;

		vt_addr = ADR_VibratoTypes + ((uint16_t)vtype << 1);
		vt_ptr = (uint16_t)gb_read8(vt_addr + 1) << 8 | gb_read8(vt_addr);

		vpos = wdddb_PTR[ch];
		wdddb_PTR[ch]++;

		delta = (int8_t)gb_read8(vt_ptr + vpos);
		if (delta == (int8_t)0x80) {
			/* End of vibrato pattern: check for continuation. */
			vpos++;
			delta = (int8_t)gb_read8(vt_ptr + vpos);
			if (delta == (int8_t)0x80) {
				wdddb_PTR[ch] = 0;
				goto no_vibrato;
			}
			/* Chain to next vibrato type. */
			wMusicVibratoType_PTR[ch] = (uint8_t)delta;
			goto no_vibrato;
		}

		{
			uint16_t de = (uint16_t)wMusicCh1CurPitch_PTR[ch * 2 + 1] << 8
			              | wMusicCh1CurPitch_PTR[ch * 2];
			if (delta < 0) {
				de = (uint16_t)(de - (uint16_t)(delta ^ 0xFF));
			} else {
				de = (uint16_t)(de + (uint16_t)delta);
			}
			/* Store back. Note: the ASM returns de via d/e registers;
			 * f490b then reads them. We update wMusicCh*CurPitch inline. */
			wMusicCh1CurPitch_PTR[ch * 2] = (uint8_t)de;
			wMusicCh1CurPitch_PTR[ch * 2 + 1] = (uint8_t)(de >> 8);
		}
		return;
	}

no_vibrato:
	/* Return current pitch without modification. */
	;
}

/* ======================================================================
 * Music1_f490b — write frequency to APU
 * ====================================================================== */

void Music1_f490b(uint8_t ch)
{
	uint8_t lo, hi;
	g_rom_bank = MUSIC1_BANK;

	if (ch != 0) goto not_ch1;
	if (wMusicVibratoDelay_PTR[0] == 0) return;
	if (wdd8c & 0x01) return;
	lo = wMusicCh1CurPitch_PTR[0];
	hi = wMusicCh1CurPitch_PTR[1];
	gb_write8(APU_AUD1LOW, lo);
	gb_write8(APU_AUD1LEN, (uint8_t)(gb_read8(APU_AUD1LEN) & ~K_LEN_TIMER));
	gb_write8(APU_AUD1HIGH, (uint8_t)(hi & K_LEN_TIMER));
	return;

not_ch1:
	if (ch != 1) goto not_ch2;
	if (wMusicVibratoDelay_PTR[1] == 0) return;
	if (wdd8c & 0x02) return;
	lo = wMusicCh2CurPitch_PTR[0];
	hi = wMusicCh2CurPitch_PTR[1];
	gb_write8(APU_AUD2LOW, lo);
	gb_write8(APU_AUD2LEN, (uint8_t)(gb_read8(APU_AUD2LEN) & ~K_LEN_TIMER));
	gb_write8(APU_AUD2HIGH, hi);
	return;

not_ch2:
	if (ch != 2) return;
	if (wMusicVibratoDelay_PTR[2] == 0) return;
	if (wdd8c & 0x04) return;
	lo = wMusicCh3CurPitch_PTR[0];
	hi = wMusicCh3CurPitch_PTR[1];
	gb_write8(APU_AUD3LOW, lo);
	gb_write8(APU_AUD3LEN, 0);
	gb_write8(APU_AUD3HIGH, hi);
}

/* ======================================================================
 * Music1_f4967 — frequency offset
 * ====================================================================== */

void Music1_f4967(uint8_t ch)
{
	uint8_t fo;
	uint16_t de;
	g_rom_bank = MUSIC1_BANK;

	fo = wMusicFrequencyOffset_PTR[ch];
	de = (uint16_t)wMusicCh1CurPitch_PTR[ch * 2 + 1] << 8
	     | wMusicCh1CurPitch_PTR[ch * 2];

	if (fo & 0x80) {
		de = (uint16_t)(de - (uint16_t)(fo ^ 0xFF));
	} else {
		de = (uint16_t)(de + fo);
	}

	wMusicCh1CurPitch_PTR[ch * 2] = (uint8_t)de;
	wMusicCh1CurPitch_PTR[ch * 2 + 1] = (uint8_t)(de >> 8);
	/* In the ASM, de is returned via d/e registers and used inline.
	 * We store to WRAM for consistency. */
}

/* ======================================================================
 * Music1_Update — timer tick handler
 * ====================================================================== */

void Music1_Update(void)
{
	g_rom_bank = MUSIC1_BANK;
	Music1_EmptyFunc();
	Music1_CheckForNewSound();
	SFX_Update();
	{
		uint8_t bank = wCurSongBank;
		hBankROM = bank;
		BankswitchROM(bank);
	}
	if (wddf2 != 0) {
		Music1_f4980();
	} else {
		Music1_UpdateChannel1();
		Music1_UpdateChannel2();
		Music1_UpdateChannel3();
		Music1_UpdateChannel4();
	}
	Music1_f4866();
	Music1_CheckForEndOfSong();
}

/* ======================================================================
 * Music1_CheckForNewSound
 * ====================================================================== */

void Music1_CheckForNewSound(void);

void Music1_CheckForNewSound(void)
{
	uint8_t sid;
	g_rom_bank = MUSIC1_BANK;

	sid = wCurSongID;
	if (!(sid & 0x80)) {
		Music1_StopAllChannels();
		Music1_BeginSong(sid);
		wCurSongID = (uint8_t)(sid | 0x80);
	}

	sid = wCurSfxID;
	if (!(sid & 0x80)) {
		SFX_Play(sid);
		wCurSfxID = (uint8_t)(sid | 0x80);
	}
}

/* ======================================================================
 * Pause / Resume
 * ====================================================================== */

void Music1_PauseSong(void)
{
	g_rom_bank = MUSIC1_BANK;
	Music1_f4980();
	Music1_BackupSong();
	Music1_StopAllChannels();
}

void Music1_ResumeSong(void)
{
	g_rom_bank = MUSIC1_BANK;
	Music1_f4980();
	Music1_StopAllChannels();
	Music1_LoadBackup();
}

/* ======================================================================
 * Backup / Restore — copy all music WRAM state to backup area
 * ====================================================================== */

void Music1_BackupSong(void)
{
	uint16_t hl, de;
	uint8_t i;
	g_rom_bank = MUSIC1_BANK;

	wCurSongIDBackup = wCurSongID;
	wCurSongBankBackup = wCurSongBank;
	wMusicStereoPanningBackup = wMusicStereoPanning;

	/* MusicDuty1[4] */
	hl = wMusicDuty1_ADDR; de = wMusicDuty1Backup_ADDR;
	Music1_CopyData(&hl, &de, 4);

	wMusicWaveBackup = wMusicWave;
	wMusicWaveChangeBackup = wMusicWaveChange;

	hl = wMusicIsPlaying_ADDR; de = wMusicIsPlayingBackup_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicTie_ADDR; de = wMusicTieBackup_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicChannelPointers_ADDR; de = wMusicChannelPointersBackup_ADDR;
	Music1_CopyData(&hl, &de, 8);

	hl = wMusicMainLoopStart_ADDR; de = wMusicMainLoopStartBackup_ADDR;
	Music1_CopyData(&hl, &de, 8);

	wde76 = wddab_PTR[0]; wde77 = wddab_PTR[1];

	hl = wMusicOctave_ADDR; de = wMusicOctaveBackup_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wddb3_ADDR; de = wde7c_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wddb7_ADDR; de = wde80_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wddbb_ADDR; de = wde84_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicCutoff_ADDR; de = wMusicCutoffBackup_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wddc3_ADDR; de = wde8c_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicEcho_ADDR; de = wMusicEchoBackup_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicPitchOffset_ADDR; de = wMusicPitchOffsetBackup_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicSpeed_ADDR; de = wMusicSpeedBackup_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicVibratoType2_ADDR; de = wMusicVibratoType2Backup_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicVibratoDelay_ADDR; de = wMusicVibratoDelayBackup_ADDR;
	Music1_CopyData(&hl, &de, 4);

	for (i = 0; i < 4; i++) wdddb_PTR[i] = 0;

	hl = wMusicVolume_ADDR; de = wMusicVolumeBackup_ADDR;
	Music1_CopyData(&hl, &de, 3);

	hl = wMusicFrequencyOffset_ADDR; de = wMusicFrequencyOffsetBackup_ADDR;
	Music1_CopyData(&hl, &de, 3);

	hl = wdded_ADDR; de = wdeaa_ADDR;
	Music1_CopyData(&hl, &de, 2);

	wdeac = 0;

	hl = wMusicChannelStackPointers_ADDR; de = wMusicChannelStackPointersBackup_ADDR;
	Music1_CopyData(&hl, &de, 8);

	hl = wMusicCh1Stack_ADDR; de = wMusicCh1StackBackup_ADDR;
	Music1_CopyData(&hl, &de, 48);
}

void Music1_LoadBackup(void)
{
	uint16_t hl, de;
	g_rom_bank = MUSIC1_BANK;

	wCurSongID = wCurSongIDBackup;
	wCurSongBank = wCurSongBankBackup;
	wMusicStereoPanning = wMusicStereoPanningBackup;

	hl = wMusicDuty1Backup_ADDR; de = wMusicDuty1_ADDR;
	Music1_CopyData(&hl, &de, 4);

	wMusicWave = wMusicWaveBackup;
	wMusicWaveChange = 1;

	hl = wMusicIsPlayingBackup_ADDR; de = wMusicIsPlaying_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicTieBackup_ADDR; de = wMusicTie_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicChannelPointersBackup_ADDR; de = wMusicChannelPointers_ADDR;
	Music1_CopyData(&hl, &de, 8);

	hl = wMusicMainLoopStartBackup_ADDR; de = wMusicMainLoopStart_ADDR;
	Music1_CopyData(&hl, &de, 8);

	wddab_PTR[0] = wde76; wddab_PTR[1] = wde77;

	hl = wMusicOctaveBackup_ADDR; de = wMusicOctave_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wde7c_ADDR; de = wddb3_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wde80_ADDR; de = wddb7_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wde84_ADDR; de = wddbb_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicCutoffBackup_ADDR; de = wMusicCutoff_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wde8c_ADDR; de = wddc3_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicEchoBackup_ADDR; de = wMusicEcho_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicPitchOffsetBackup_ADDR; de = wMusicPitchOffset_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicSpeedBackup_ADDR; de = wMusicSpeed_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicVibratoType2Backup_ADDR; de = wMusicVibratoType2_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicVibratoDelayBackup_ADDR; de = wMusicVibratoDelay_ADDR;
	Music1_CopyData(&hl, &de, 4);

	hl = wMusicVolumeBackup_ADDR; de = wMusicVolume_ADDR;
	Music1_CopyData(&hl, &de, 3);

	hl = wMusicFrequencyOffsetBackup_ADDR; de = wMusicFrequencyOffset_ADDR;
	Music1_CopyData(&hl, &de, 3);

	hl = wdeaa_ADDR; de = wdded_ADDR;
	Music1_CopyData(&hl, &de, 2);

	wddef = wdeac;

	hl = wMusicChannelStackPointersBackup_ADDR; de = wMusicChannelStackPointers_ADDR;
	Music1_CopyData(&hl, &de, 8);

	hl = wMusicCh1StackBackup_ADDR; de = wMusicCh1Stack_ADDR;
	Music1_CopyData(&hl, &de, 48);
}

/* >>> factory _PauseSong */
/* music1.asm:28-30 */
void _PauseSong(void)
{
	Music1_PauseSong();
}
/* <<< factory _PauseSong */

/* >>> factory _ResumeSong */
/* music1.asm:31-33 */
void _ResumeSong(void)
{
	Music1_ResumeSong();
}
/* <<< factory _ResumeSong */

/* >>> factory Music1_f400c */
void Music1_f400c(uint8_t a)
{
	Music1_f404e(a);
}
/* <<< factory Music1_f400c */

/* >>> factory Music1_f4018 */
void Music1_f4018(uint8_t a)
{
	Music1_f406f(a);
}
/* <<< factory Music1_f4018 */

/* >>> factory _AssertSFXFinished */
uint8_t _AssertSFXFinished(void)
{
	return Music1_AssertSFXFinished();
}
/* <<< factory _AssertSFXFinished */

/* >>> factory _AssertSongFinished */
uint8_t _AssertSongFinished(void)
{
	return Music1_AssertSongFinished();
}
/* <<< factory _AssertSongFinished */
