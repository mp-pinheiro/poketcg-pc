/* >>> part includes */
#include "home/music.h"

#include "home/frames.h"
#include "home/audio.h"
#include "home/sfx.h"
#include "generated/rom.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "home/switch_rom.h"
#include "mem.h"
/* <<< part includes */

/* >>> part MUSIC_BANK */
#define MUSIC_BANK 0x42u
/* <<< part MUSIC_BANK */
/* >>> part ADR_CHANNEL_LOOP_STACKS */
#define ADR_CHANNEL_LOOP_STACKS ChannelLoopStacks_ADDR
/* <<< part ADR_CHANNEL_LOOP_STACKS */
/* >>> part ADR_OCTAVE_OFFSETS */
#define ADR_OCTAVE_OFFSETS OctaveOffsets_ADDR
/* <<< part ADR_OCTAVE_OFFSETS */
/* >>> part ADR_PITCHES */
#define ADR_PITCHES Pitches_ADDR
/* <<< part ADR_PITCHES */
/* >>> part ADR_WAVE_INSTRUMENTS */
#define ADR_WAVE_INSTRUMENTS WaveInstruments_ADDR
/* <<< part ADR_WAVE_INSTRUMENTS */
/* >>> part ADR_NOISE_INSTRUMENTS */
#define ADR_NOISE_INSTRUMENTS NoiseInstruments_ADDR
/* <<< part ADR_NOISE_INSTRUMENTS */
/* >>> part ADR_VIBRATO_TYPES */
#define ADR_VIBRATO_TYPES VibratoTypes_ADDR
/* <<< part ADR_VIBRATO_TYPES */
/* >>> part ADR_NUMBER_OF_SONGS */
#define ADR_NUMBER_OF_SONGS NumberOfSongs_ADDR
/* <<< part ADR_NUMBER_OF_SONGS */
/* >>> part ADR_SONG_HEADER_POINTERS */
#define ADR_SONG_HEADER_POINTERS SongHeaderPointers_ADDR
/* <<< part ADR_SONG_HEADER_POINTERS */

/* >>> part APU_AUD1SWEEP */
#define APU_AUD1SWEEP 0xFF10u
/* <<< part APU_AUD1SWEEP */
/* >>> part APU_AUD1LEN */
#define APU_AUD1LEN 0xFF11u
/* <<< part APU_AUD1LEN */
/* >>> part APU_AUD1ENV */
#define APU_AUD1ENV 0xFF12u
/* <<< part APU_AUD1ENV */
/* >>> part APU_AUD1LOW */
#define APU_AUD1LOW 0xFF13u
/* <<< part APU_AUD1LOW */
/* >>> part APU_AUD1HIGH */
#define APU_AUD1HIGH 0xFF14u
/* <<< part APU_AUD1HIGH */
/* >>> part APU_AUD2LEN */
#define APU_AUD2LEN 0xFF16u
/* <<< part APU_AUD2LEN */
/* >>> part APU_AUD2ENV */
#define APU_AUD2ENV 0xFF17u
/* <<< part APU_AUD2ENV */
/* >>> part APU_AUD2LOW */
#define APU_AUD2LOW 0xFF18u
/* <<< part APU_AUD2LOW */
/* >>> part APU_AUD2HIGH */
#define APU_AUD2HIGH 0xFF19u
/* <<< part APU_AUD2HIGH */
/* >>> part APU_AUD3ENA */
#define APU_AUD3ENA 0xFF1Au
/* <<< part APU_AUD3ENA */
/* >>> part APU_AUD3LEN */
#define APU_AUD3LEN 0xFF1Bu
/* <<< part APU_AUD3LEN */
/* >>> part APU_AUD3LEVEL */
#define APU_AUD3LEVEL 0xFF1Cu
/* <<< part APU_AUD3LEVEL */
/* >>> part APU_AUD3LOW */
#define APU_AUD3LOW 0xFF1Du
/* <<< part APU_AUD3LOW */
/* >>> part APU_AUD3HIGH */
#define APU_AUD3HIGH 0xFF1Eu
/* <<< part APU_AUD3HIGH */
/* >>> part APU_AUD4LEN */
#define APU_AUD4LEN 0xFF20u
/* <<< part APU_AUD4LEN */
/* >>> part APU_AUD4ENV */
#define APU_AUD4ENV 0xFF21u
/* <<< part APU_AUD4ENV */
/* >>> part APU_AUD4POLY */
#define APU_AUD4POLY 0xFF22u
/* <<< part APU_AUD4POLY */
/* >>> part APU_AUD4GO */
#define APU_AUD4GO 0xFF23u
/* <<< part APU_AUD4GO */
/* >>> part APU_VOL */
#define APU_VOL 0xFF24u
/* <<< part APU_VOL */
/* >>> part APU_TERM */
#define APU_TERM 0xFF25u
/* <<< part APU_TERM */
/* >>> part APU_ENA */
#define APU_ENA 0xFF26u
/* <<< part APU_ENA */
/* >>> part APU_WAVE */
#define APU_WAVE 0xFF30u
/* <<< part APU_WAVE */

/* >>> part AUDENA_ON */
#define AUDENA_ON 0x80u
/* <<< part AUDENA_ON */
/* >>> part AUD1ENV_UP */
#define AUD1ENV_UP 0x08u
/* <<< part AUD1ENV_UP */
/* >>> part AUD2ENV_UP */
#define AUD2ENV_UP 0x08u
/* <<< part AUD2ENV_UP */
/* >>> part AUD4ENV_UP */
#define AUD4ENV_UP 0x08u
/* <<< part AUD4ENV_UP */
/* >>> part AUD1HIGH_RESTART */
#define AUD1HIGH_RESTART 0x80u
/* <<< part AUD1HIGH_RESTART */
/* >>> part AUD2HIGH_RESTART */
#define AUD2HIGH_RESTART 0x80u
/* <<< part AUD2HIGH_RESTART */
/* >>> part AUD3HIGH_RESTART */
#define AUD3HIGH_RESTART 0x80u
/* <<< part AUD3HIGH_RESTART */
/* >>> part AUD4GO_RESTART */
#define AUD4GO_RESTART 0x80u
/* <<< part AUD4GO_RESTART */
/* >>> part AUD3LEVEL_MUTE */
#define AUD3LEVEL_MUTE 0x00u
/* <<< part AUD3LEVEL_MUTE */
/* >>> part AUD3ENA_ON */
#define AUD3ENA_ON 0x80u
/* <<< part AUD3ENA_ON */
/* >>> part AUD1SWEEP_DOWN */
#define AUD1SWEEP_DOWN 0x08u
/* <<< part AUD1SWEEP_DOWN */
/* >>> part AUD1LEN_TIMER */
#define AUD1LEN_TIMER 0x3Fu
/* <<< part AUD1LEN_TIMER */
/* >>> part AUD2LEN_TIMER */
#define AUD2LEN_TIMER 0x3Fu
/* <<< part AUD2LEN_TIMER */
/* >>> part AUD3WAVE_SIZE */
#define AUD3WAVE_SIZE 16u
/* <<< part AUD3WAVE_SIZE */

/* >>> part rom_read8 */
static uint8_t rom_read8(uint16_t addr)
{
	return *rom_ptr(MUSIC_BANK, addr);
}
/* <<< part rom_read8 */

/* >>> part rom_read16 */
static uint16_t rom_read16(uint16_t addr)
{
	return (uint16_t)(rom_read8(addr) |
		((uint16_t)rom_read8((uint16_t)(addr + 1u)) << 8u));
}
/* <<< part rom_read16 */
/* >>> part read16 */
static uint16_t read16(uint16_t addr)
{
	return (uint16_t)(gb_read8(addr) |
		((uint16_t)gb_read8((uint16_t)(addr + 1u)) << 8u));
}
/* <<< part read16 */

/* >>> part write16 */
static void write16(uint16_t addr, uint16_t value)
{
	gb_write8(addr, (uint8_t)value);
	gb_write8((uint16_t)(addr + 1u), (uint8_t)(value >> 8u));
}
/* <<< part write16 */

/* >>> part channel_addr */
static uint16_t channel_addr(uint16_t base, uint8_t ch)
{
	return (uint16_t)(base + ch);
}
/* <<< part channel_addr */

/* >>> part channel_word_addr */
static uint16_t channel_word_addr(uint16_t base, uint8_t ch)
{
	return (uint16_t)(base + (uint16_t)ch * 2u);
}
/* <<< part channel_word_addr */

/* >>> part play_next_from */
static void play_next_from(uint16_t stream, uint8_t ch)
{
	PlayNextNote(&stream, ch);
}
/* <<< part play_next_from */

/* >>> factory _SetupSound */
/* music.asm:1-3 */
void _SetupSound(void)
{
	Music_SetupSound();
}
/* <<< factory _SetupSound */

/* >>> factory SoundTimerHandler */
/* music.asm:4-6 */
void SoundTimerHandler(void)
{
	MusicUpdate();
}
/* <<< factory SoundTimerHandler */

/* >>> factory _PlaySong */
/* music.asm:7-9 */
void _PlaySong(uint8_t a)
{
	SetCurSong(a);
}
/* <<< factory _PlaySong */

/* >>> factory _PlaySFX */
/* music.asm:10-12 */
void _PlaySFX(uint8_t a)
{
	SetCurSFX(a);
}
/* <<< factory _PlaySFX */

/* >>> factory _AssertSongFinished */
/* music.asm:13-15 */
uint8_t _AssertSongFinished(void)
{
	return Music_AssertSongFinished();
}
/* <<< factory _AssertSongFinished */

/* >>> factory _AssertSFXFinished */
/* music.asm:16-18 */
uint8_t _AssertSFXFinished(void)
{
	return Music_AssertSFXFinished();
}
/* <<< factory _AssertSFXFinished */

/* >>> factory _PauseSong */
/* music.asm:19-21 */
void _PauseSong(void)
{
	Music_PauseSong();
}
/* <<< factory _PauseSong */

/* >>> factory _ResumeSong */
/* music.asm:22-24 */
void _ResumeSong(void)
{
	Music_ResumeSong();
}
/* <<< factory _ResumeSong */

/* >>> factory SetCurSong */
/* music.asm:25-33 */
void SetCurSong(uint8_t a)
{
	g_rom_bank = MUSIC_BANK;
	if (a >= gb_read8(ADR_NUMBER_OF_SONGS))
		return;
	frame_boundary_timer_sync();
	wCurSongID = a;
}
/* <<< factory SetCurSong */

/* >>> factory SetCurSFX */
/* music.asm:35-37 */
void SetCurSFX(uint8_t a)
{
	g_rom_bank = MUSIC_BANK;
	frame_boundary_timer_sync();
	wCurSfxID = a;
}
/* <<< factory SetCurSFX */

/* >>> factory Music_AssertSongFinished */
/* music.asm:39-45 */
uint8_t Music_AssertSongFinished(void)
{
	g_rom_bank = MUSIC_BANK;
	return wCurSongID == 0x80u ? 0u : 1u;
}
/* <<< factory Music_AssertSongFinished */

/* >>> factory Music_AssertSFXFinished */
/* music.asm:47-53 */
uint8_t Music_AssertSFXFinished(void)
{
	g_rom_bank = MUSIC_BANK;
	return wCurSfxID == 0x80u ? 0u : 1u;
}
/* <<< factory Music_AssertSFXFinished */

/* >>> factory Music_SetupSound */
/* music.asm:55-111 */
void Music_SetupSound(void)
{
	g_rom_bank = MUSIC_BANK;
	gb_write8(APU_ENA, 0u);
	gb_write8(APU_ENA, AUDENA_ON);
	gb_write8(APU_VOL, 0x77u);
	gb_write8(APU_TERM, 0xFFu);
	wCurSongBank = MUSIC_BANK;
	wCurSongID = 0x80u;
	wCurSfxID = 0x80u;
	wMusicPanning = 0x77u;
	wdd8c = 0u;
	wSFXIsPlaying = 0u;
	wMusicWaveChange = 0u;
	wddef = 0u;
	wddf0 = 0u;
	wddf2 = 0u;
	wMusicStereoPanning = 0xFFu;
	for (uint8_t i = 0u; i < 4u; i++) {
		gb_write8(channel_addr(wMusicIsPlaying_ADDR, i), 0u);
		gb_write8(channel_addr(wMusicTie_ADDR, i), 0u);
		gb_write8(channel_addr(wddb3_ADDR, i), 0u);
		gb_write8(channel_addr(wMusicPitchOffset_ADDR, i), 0u);
		gb_write8(channel_addr(wMusicCutoff_ADDR, i), 0u);
	}
	for (uint8_t i = 0u; i < 8u; i++)
		gb_write8((uint16_t)(wMusicChannelStackPointers_ADDR + i),
		          gb_read8((uint16_t)(ADR_CHANNEL_LOOP_STACKS + i)));
}
/* <<< factory Music_SetupSound */

/* >>> factory MusicUpdate */
/* music.asm:113-129 */
void MusicUpdate(void)
{
	g_rom_bank = MUSIC_BANK;
	MusicEmptyFunc();
	CheckForNewSound();
	SFX_Update();
	g_rom_bank = MUSIC_BANK;
	if (wddf2 != 0u) {
		Music_f4980();
	} else {
		UpdateChannel1();
		UpdateChannel2();
		UpdateChannel3();
		UpdateChannel4();
	}
	Music_f4866();
	CheckForEndOfSong();
}
/* <<< factory MusicUpdate */

/* >>> factory CheckForNewSound */
/* music.asm:131-151 */
void CheckForNewSound(void)
{
	g_rom_bank = MUSIC_BANK;
	if ((wCurSongID & 0x80u) == 0u) {
		StopAllChannels();
		BeginSong(wCurSongID);
		wCurSongID = (uint8_t)(wCurSongID | 0x80u);
	}
	if ((wCurSfxID & 0x80u) == 0u) {
		SFX_Play(wCurSfxID);
		wCurSfxID = (uint8_t)(wCurSfxID | 0x80u);
	}
}
/* <<< factory CheckForNewSound */

/* >>> factory StopAllChannels */
/* music.asm:153-190 */
void StopAllChannels(void)
{
	g_rom_bank = MUSIC_BANK;
	uint8_t d = wdd8c;
	gb_write8(wMusicIsPlaying_ADDR, 0u);
	if ((d & 0x01u) == 0u) {
		gb_write8(APU_AUD1ENV, AUD1ENV_UP);
		gb_write8(APU_AUD1HIGH, AUD1HIGH_RESTART);
	}
	gb_write8((uint16_t)(wMusicIsPlaying_ADDR + 1u), 0u);
	if ((d & 0x02u) == 0u) {
		gb_write8(APU_AUD2ENV, AUD2ENV_UP);
		gb_write8(APU_AUD2HIGH, AUD2HIGH_RESTART);
	}
	gb_write8((uint16_t)(wMusicIsPlaying_ADDR + 3u), 0u);
	if ((d & 0x08u) == 0u) {
		gb_write8(APU_AUD4ENV, AUD4ENV_UP);
		gb_write8(APU_AUD4GO, AUD4GO_RESTART);
	}
	gb_write8((uint16_t)(wMusicIsPlaying_ADDR + 2u), 0u);
	if ((d & 0x04u) == 0u)
		gb_write8(APU_AUD3LEVEL, AUD3LEVEL_MUTE);
}
/* <<< factory StopAllChannels */

/* >>> factory BeginSong */
/* music.asm:193-314 */
void BeginSong(uint8_t a)
{
	g_rom_bank = MUSIC_BANK;
	uint16_t header = rom_read16((uint16_t)(ADR_SONG_HEADER_POINTERS + (uint8_t)(a + a)));
	uint8_t mask = rom_read8(header);
	header = (uint16_t)(header + 1u);
	uint8_t bank = rom_read8(header);
	header = (uint16_t)(header + 1u);
	wCurSongBank = bank;
	uint16_t bc = header;
	for (uint8_t ch = 0u; ch < 4u; ch++) {
		if ((mask & (uint8_t)(1u << ch)) == 0u)
			continue;
		uint16_t stream = rom_read16(bc);
		bc = (uint16_t)(bc + 2u);
		write16(channel_word_addr(wMusicChannelPointers_ADDR, ch), stream);
		write16(channel_word_addr(wMusicMainLoopStart_ADDR, ch), stream);
		gb_write8(channel_addr(wddbb_ADDR, ch), 1u);
		gb_write8(channel_addr(wMusicIsPlaying_ADDR, ch), 1u);
		gb_write8(channel_addr(wMusicTie_ADDR, ch), 0u);
		if (ch != 3u)
			gb_write8(channel_addr(wMusicFrequencyOffset_ADDR, ch), 0u);
		gb_write8(channel_addr(wMusicCutoff_ADDR, ch), 0u);
		gb_write8(channel_addr(wMusicVibratoDelay_ADDR, ch), 0u);
		gb_write8(channel_addr(wMusicPitchOffset_ADDR, ch), 0u);
		write16((uint16_t)(wMusicChannelStackPointers_ADDR + (uint16_t)ch * 2u),
		        rom_read16((uint16_t)(ADR_CHANNEL_LOOP_STACKS + (uint16_t)ch * 2u)));
		gb_write8(channel_addr(wMusicEcho_ADDR, ch), ch < 2u ? 0x08u : 0x40u);
	}
	wddf2 = 0u;
}
/* <<< factory BeginSong */

/* >>> factory MusicEmptyFunc */
/* music.asm:316-317 */
void MusicEmptyFunc(void)
{
	g_rom_bank = MUSIC_BANK;
}
/* <<< factory MusicEmptyFunc */

/* >>> part stop_channel */
static void stop_channel(uint8_t ch)
{
	uint8_t disabled_bit = ch == 3u ? 0x08u : (uint8_t)(1u << ch);
	if ((wdd8c & disabled_bit) != 0u)
		return;
	if (ch == 0u) {
		gb_write8(APU_AUD1ENV, AUD1ENV_UP);
		gb_write8(APU_AUD1HIGH, AUD1HIGH_RESTART);
	} else if (ch == 1u) {
		gb_write8(APU_AUD2ENV, AUD2ENV_UP);
		gb_write8(APU_AUD2HIGH, AUD2HIGH_RESTART);
	} else if (ch == 2u) {
		gb_write8(APU_AUD3LEVEL, AUD3LEVEL_MUTE);
		gb_write8(APU_AUD3HIGH, AUD3HIGH_RESTART);
	} else {
		wddef = 0u;
		gb_write8(APU_AUD4ENV, AUD4ENV_UP);
		gb_write8(APU_AUD4GO, AUD4GO_RESTART);
	}
}
/* <<< part stop_channel */

/* >>> part update_channel */
static void update_channel(uint8_t ch)
{
	uint8_t playing = gb_read8(channel_addr(wMusicIsPlaying_ADDR, ch));
	if (playing == 0u) {
		stop_channel(ch);
		return;
	}
	uint8_t counter = gb_read8(channel_addr(wddbb_ADDR, ch));
	if (ch != 3u) {
		uint8_t instrument = gb_read8(channel_addr(wddb7_ADDR, ch));
		if (instrument != 0u) {
			uint8_t echo_counter = (uint8_t)(gb_read8(channel_addr(wddc3_ADDR, ch)) - 1u);
			gb_write8(channel_addr(wddc3_ADDR, ch), echo_counter);
			if (echo_counter == 0u && counter != 1u &&
			    (wdd8c & (uint8_t)(1u << ch)) == 0u) {
				uint8_t echo = gb_read8(channel_addr(wMusicEcho_ADDR, ch));
				if (ch == 0u) {
					gb_write8(APU_AUD1ENV, echo);
					gb_write8(APU_AUD1HIGH, AUD1HIGH_RESTART);
				} else if (ch == 1u) {
					gb_write8(APU_AUD2ENV, echo);
					gb_write8(APU_AUD2HIGH, AUD2HIGH_RESTART);
				} else if ((wdd8c & 0x04u) == 0u) {
					gb_write8(APU_AUD3LEVEL, echo);
				}
			}
		}
	}
	counter = (uint8_t)(counter - 1u);
	gb_write8(channel_addr(wddbb_ADDR, ch), counter);
	if (counter != 0u) {
		if (ch == 3u) {
			if (wddef != 0u)
				Music_f4839();
		} else {
			Music_f485a(ch);
		}
		return;
	}
	uint16_t stream = read16(channel_word_addr(wMusicChannelPointers_ADDR, ch));
	PlayNextNote(&stream, ch);
	if (gb_read8(channel_addr(wMusicIsPlaying_ADDR, ch)) == 0u) {
		stop_channel(ch);
		return;
	}
	if (ch == 0u)
		Music_f4714();
	else if (ch == 1u)
		Music_f475a();
	else if (ch == 2u)
		Music_f479c();
	else
		Music_f480a();
	if (ch != 3u)
		Music_f485a(ch);
}
/* <<< part update_channel */

/* >>> factory UpdateChannel1 */
/* music.asm:319-369 */
void UpdateChannel1(void)
{
	g_rom_bank = MUSIC_BANK;
	update_channel(0u);
}
/* <<< factory UpdateChannel1 */

/* >>> factory UpdateChannel2 */
/* music.asm:371-421 */
void UpdateChannel2(void)
{
	g_rom_bank = MUSIC_BANK;
	update_channel(1u);
}
/* <<< factory UpdateChannel2 */

/* >>> factory UpdateChannel3 */
/* music.asm:423-469 */
void UpdateChannel3(void)
{
	g_rom_bank = MUSIC_BANK;
	update_channel(2u);
}
/* <<< factory UpdateChannel3 */

/* >>> factory UpdateChannel4 */
/* music.asm:471-506 */
void UpdateChannel4(void)
{
	g_rom_bank = MUSIC_BANK;
	update_channel(3u);
}
/* <<< factory UpdateChannel4 */

/* >>> factory GetMusicCommandAndArgs */
/* music.asm:510-514 */
uint8_t GetMusicCommandAndArgs(uint16_t *hl)
{
	uint8_t command = GetAudioCmdAndArgs(wCurSongBank, *hl);
	*hl = (uint16_t)(*hl + 1u);
	return command;
}
/* <<< factory GetMusicCommandAndArgs */

/* >>> part note_body */
static void note_body(uint16_t *hl, uint8_t note, uint8_t ch)
{
	g_rom_bank = MUSIC_BANK;
	uint8_t operand = wAudioArg;
	uint8_t instrument = (uint8_t)(note & 0xF0u);
	if (gb_read8(channel_addr(wMusicTie_ADDR, ch)) != 0x80u) {
		gb_write8(channel_addr(wMusicTie_ADDR, ch), 1u);
		gb_write8(channel_addr(wdddb_ADDR, ch), 0u);
		gb_write8(channel_addr(wdde3_ADDR, ch), 0u);
		gb_write8(channel_addr(wdde3_ADDR, ch), 1u);
		gb_write8(channel_addr(wMusicVibratoType_ADDR, ch),
		          gb_read8(channel_addr(wMusicVibratoType2_ADDR, ch)));
	}
	uint8_t speed = gb_read8(channel_addr(wMusicSpeed_ADDR, ch));
	uint8_t n1 = (uint8_t)((note & 0x0Fu) + 1u);
	uint8_t a = n1 < speed ? speed : n1;
	uint8_t d = n1 < speed ? n1 : speed;
	uint8_t duration = a;
	while (--d != 0u)
		duration = (uint8_t)(duration + a);
	gb_write8(channel_addr(wddbb_ADDR, ch), duration);
	if (operand != 0xD9u) {
		uint8_t cutoff = gb_read8(channel_addr(wMusicCutoff_ADDR, ch));
		if (cutoff != 8u) {
			uint16_t sum = 0u;
			uint8_t count = cutoff;
			do {
				sum = (uint16_t)(sum + duration);
			} while (--count != 0u);
			duration = (uint8_t)(sum >> 3u);
		}
	}
	gb_write8(channel_addr(wddc3_ADDR, ch), duration);
	gb_write8(channel_addr(wddb7_ADDR, ch), instrument);
	if (instrument != 0u) {
		uint8_t index = (uint8_t)((instrument >> 4u) - 1u);
		uint8_t octave = gb_read8(channel_addr(wMusicOctave_ADDR, ch));
		if (ch == 3u) {
			uint8_t stride = (uint8_t)(octave * 24u);
			uint16_t ptr = read16((uint16_t)(ADR_NOISE_INSTRUMENTS +
				(uint16_t)(uint8_t)(index * 2u) + stride));
			uint8_t flags = gb_read8(ptr);
			ptr = (uint16_t)(ptr + 1u);
			wMusicStereoPanning = (uint8_t)((wMusicStereoPanning & 0x77u) | flags);
			gb_write8(wddab_ADDR, gb_read8(ptr));
			ptr = (uint16_t)(ptr + 1u);
			gb_write8((uint16_t)(wddab_ADDR + 1u), gb_read8(ptr));
			ptr = (uint16_t)(ptr + 1u);
			uint8_t shared = gb_read8(ptr);
			ptr = (uint16_t)(ptr + 1u);
			gb_write8((uint16_t)(wddab_ADDR + 2u), gb_read8(ptr));
			gb_write8((uint16_t)(wddab_ADDR + 3u), shared);
			ptr = (uint16_t)(ptr + 1u);
			write16(wdded_ADDR, ptr);
			wddef = 1u;
		} else {
			uint8_t octave_offset = gb_read8((uint16_t)(ADR_OCTAVE_OFFSETS + octave));
			uint8_t pitch_offset = gb_read8(channel_addr(wMusicPitchOffset_ADDR, ch));
			uint8_t pitch_index = (uint8_t)((uint8_t)(index * 2u) + octave_offset +
				pitch_offset + pitch_offset);
			uint16_t frequency = read16((uint16_t)(ADR_PITCHES + pitch_index));
			uint8_t frequency_offset = gb_read8(channel_addr(wMusicFrequencyOffset_ADDR, ch));
			if ((frequency_offset & 0x80u) != 0u)
				frequency = (uint16_t)(frequency - (uint8_t)(frequency_offset ^ 0xFFu));
			else
				frequency = (uint16_t)(frequency + frequency_offset);
			write16(channel_word_addr(wMusicCh1CurPitch_ADDR, ch), frequency);
		}
	}
	write16(channel_word_addr(wMusicChannelPointers_ADDR, ch), *hl);
}
/* <<< part note_body */

/* >>> factory Music_note */
/* music.asm:586-778 */
void Music_note(uint16_t *hl, uint8_t note, uint8_t instrument, uint8_t ch)
{
	(void)instrument;
	note_body(hl, note, ch);
}
/* <<< factory Music_note */

/* >>> factory PlayNextNote */
/* music.asm:516-584 */
void PlayNextNote(uint16_t *hl, uint8_t ch)
{
	for (;;) {
		uint8_t command = GetMusicCommandAndArgs(hl);
		if (command < 0xD0u) {
			Music_note(hl, command, (uint8_t)(command & 0xF0u), ch);
			return;
		}
		switch ((uint8_t)(command - 0xD0u)) {
		case 0u:
			gb_write8(channel_addr(wMusicSpeed_ADDR, ch), wAudioArg);
			*hl = (uint16_t)(*hl + 1u);
			break;
		case 1u:
		case 2u:
		case 3u:
		case 4u:
		case 5u:
		case 6u: {
			uint8_t octave = (uint8_t)((command & 7u) - 1u);
			if (ch == 2u)
				octave = (uint8_t)(octave + 1u);
			gb_write8(channel_addr(wMusicOctave_ADDR, ch), octave);
			break;
		}
		case 7u:
			gb_write8(channel_addr(wMusicOctave_ADDR, ch),
			          (uint8_t)(gb_read8(channel_addr(wMusicOctave_ADDR, ch)) + 1u));
			break;
		case 8u:
			gb_write8(channel_addr(wMusicOctave_ADDR, ch),
			          (uint8_t)(gb_read8(channel_addr(wMusicOctave_ADDR, ch)) - 1u));
			break;
		case 9u:
			gb_write8(channel_addr(wMusicTie_ADDR, ch), 0x80u);
			break;
		case 10u:
		case 11u:
		default:
			gb_write8(channel_addr(wMusicIsPlaying_ADDR, ch), 0u);
			return;
		case 12u: {
			uint8_t value = wAudioArg;
			*hl = (uint16_t)(*hl + 1u);
			uint8_t mask = 0xEEu;
			for (uint8_t spin = 0u; spin < ch; spin++) {
				value = (uint8_t)((value << 1u) | (value >> 7u));
				mask = (uint8_t)((mask << 1u) | (mask >> 7u));
			}
			wMusicStereoPanning = (uint8_t)((wMusicStereoPanning & mask) | value);
			break;
		}
		case 13u:
			write16(channel_word_addr(wMusicMainLoopStart_ADDR, ch),
			        (uint16_t)(*hl - 1u));
			break;
		case 14u:
			*hl = read16(channel_word_addr(wMusicMainLoopStart_ADDR, ch));
			break;
		case 15u: {
			uint8_t count = wAudioArg;
			*hl = (uint16_t)(*hl + 1u);
			uint16_t sp = GetChannelStackPointer(ch);
			write16(sp, *hl);
			gb_write8((uint16_t)(sp + 2u), count);
			SetChannelStackPointer(ch, (uint16_t)(sp + 3u));
			break;
		}
		case 16u: {
			uint16_t sp = (uint16_t)(GetChannelStackPointer(ch) - 1u);
			uint8_t count = (uint8_t)(gb_read8(sp) - 1u);
			if (count != 0u) {
				gb_write8(sp, count);
				*hl = read16((uint16_t)(sp - 2u));
			} else {
				SetChannelStackPointer(ch, (uint16_t)(sp - 2u));
			}
			break;
		}
		case 17u:
			*hl = (uint16_t)(wAudioArg | ((uint16_t)gb_read8((uint16_t)(wAudioArg_ADDR + 1u)) << 8u));
			break;
		case 18u: {
			uint16_t sp = GetChannelStackPointer(ch);
			uint16_t operand = *hl;
			write16(sp, operand);
			uint16_t target = (uint16_t)(wAudioArg | ((uint16_t)gb_read8((uint16_t)(wAudioArg_ADDR + 1u)) << 8u));
			SetChannelStackPointer(ch, (uint16_t)(sp + 2u));
			*hl = target;
			break;
		}
		case 19u: {
			uint16_t sp = (uint16_t)(GetChannelStackPointer(ch) - 2u);
			*hl = (uint16_t)(read16(sp) + 2u);
			SetChannelStackPointer(ch, sp);
			break;
		}
		case 20u:
			gb_write8(channel_addr(wMusicFrequencyOffset_ADDR, ch), wAudioArg);
			*hl = (uint16_t)(*hl + 1u);
			break;
		case 21u:
			gb_write8(channel_addr(wMusicDuty1_ADDR, ch), (uint8_t)(wAudioArg & 0xC0u));
			*hl = (uint16_t)(*hl + 1u);
			break;
		case 22u:
			gb_write8(channel_addr(wMusicVolume_ADDR, ch), wAudioArg);
			*hl = (uint16_t)(*hl + 1u);
			break;
		case 23u:
			wMusicWave = wAudioArg;
			wMusicWaveChange = 1u;
			*hl = (uint16_t)(*hl + 1u);
			break;
		case 24u:
			gb_write8(channel_addr(wMusicCutoff_ADDR, ch), wAudioArg);
			*hl = (uint16_t)(*hl + 1u);
			break;
		case 25u:
			gb_write8(channel_addr(wMusicEcho_ADDR, ch), wAudioArg);
			*hl = (uint16_t)(*hl + 1u);
			break;
		case 26u:
			gb_write8(channel_addr(wMusicVibratoType_ADDR, ch), wAudioArg);
			gb_write8(channel_addr(wMusicVibratoType2_ADDR, ch), wAudioArg);
			*hl = (uint16_t)(*hl + 1u);
			break;
		case 27u:
			gb_write8(channel_addr(wMusicVibratoDelay_ADDR, ch), wAudioArg);
			*hl = (uint16_t)(*hl + 1u);
			break;
		case 28u:
			gb_write8(channel_addr(wMusicPitchOffset_ADDR, ch), wAudioArg);
			*hl = (uint16_t)(*hl + 1u);
			break;
		case 29u: {
			uint16_t addr = channel_addr(wMusicPitchOffset_ADDR, ch);
			gb_write8(addr, (uint8_t)(wAudioArg + gb_read8(addr)));
			*hl = (uint16_t)(*hl + 1u);
			break;
		}
		}
	}
}
/* <<< factory PlayNextNote */

/* >>> factory Music_speed */
/* music.asm:780-788 */
void Music_speed(uint16_t caller_stream, uint8_t ch)
{
	gb_write8(channel_addr(wMusicSpeed_ADDR, ch), wAudioArg);
	caller_stream = (uint16_t)(caller_stream + 1u);
	play_next_from(caller_stream, ch);
}
/* <<< factory Music_speed */

/* >>> factory Music_octave */
/* music.asm:790-806 */
void Music_octave(uint16_t caller_stream, uint8_t ch, uint8_t cmd)
{
	uint8_t octave = (uint8_t)((cmd & 7u) - 1u);
	if (ch == 2u)
		octave = (uint8_t)(octave + 1u);
	gb_write8(channel_addr(wMusicOctave_ADDR, ch), octave);
	play_next_from(caller_stream, ch);
}
/* <<< factory Music_octave */

/* >>> factory Music_inc_octave */
/* music.asm:808-812 */
void Music_inc_octave(uint16_t caller_stream, uint8_t ch)
{
	uint16_t addr = channel_addr(wMusicOctave_ADDR, ch);
	gb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));
	play_next_from(caller_stream, ch);
}
/* <<< factory Music_inc_octave */

/* >>> factory Music_dec_octave */
/* music.asm:814-818 */
void Music_dec_octave(uint16_t caller_stream, uint8_t ch)
{
	uint16_t addr = channel_addr(wMusicOctave_ADDR, ch);
	gb_write8(addr, (uint8_t)(gb_read8(addr) - 1u));
	play_next_from(caller_stream, ch);
}
/* <<< factory Music_dec_octave */

/* >>> factory Music_tie */
/* music.asm:820-824 */
void Music_tie(uint16_t caller_stream, uint8_t ch)
{
	gb_write8(channel_addr(wMusicTie_ADDR, ch), 0x80u);
	play_next_from(caller_stream, ch);
}
/* <<< factory Music_tie */

/* >>> factory Music_stereo_panning */
/* music.asm:826-848 */
void Music_stereo_panning(uint16_t caller_stream, uint8_t ch)
{
	uint8_t value = wAudioArg;
	caller_stream = (uint16_t)(caller_stream + 1u);
	uint8_t mask = 0xEEu;
	for (uint8_t spin = 0u; spin < ch; spin++) {
		value = (uint8_t)((value << 1u) | (value >> 7u));
		mask = (uint8_t)((mask << 1u) | (mask >> 7u));
	}
	wMusicStereoPanning = (uint8_t)((wMusicStereoPanning & mask) | value);
	play_next_from(caller_stream, ch);
}
/* <<< factory Music_stereo_panning */

/* >>> factory Music_MainLoop */
/* music.asm:850-860 */
void Music_MainLoop(uint16_t caller_stream, uint8_t ch)
{
	write16(channel_word_addr(wMusicMainLoopStart_ADDR, ch),
	        (uint16_t)(caller_stream - 1u));
	play_next_from(caller_stream, ch);
}
/* <<< factory Music_MainLoop */

/* >>> factory Music_EndMainLoop */
/* music.asm:862-870 */
void Music_EndMainLoop(uint16_t caller_stream, uint8_t ch)
{
	(void)caller_stream;
	uint16_t stream = read16(channel_word_addr(wMusicMainLoopStart_ADDR, ch));
	play_next_from(stream, ch);
}
/* <<< factory Music_EndMainLoop */

/* >>> factory Music_Loop */
/* music.asm:872-887 */
void Music_Loop(uint16_t caller_stream, uint8_t ch)
{
	uint16_t continuation = (uint16_t)(caller_stream + 1u);
	uint16_t sp = GetChannelStackPointer(ch);
	write16(sp, continuation);
	gb_write8((uint16_t)(sp + 2u), wAudioArg);
	SetChannelStackPointer(ch, (uint16_t)(sp + 3u));
	play_next_from(continuation, ch);
}
/* <<< factory Music_Loop */

/* >>> factory Music_EndLoop */
/* music.asm:889-907 */
void Music_EndLoop(uint16_t caller_stream, uint8_t ch)
{
	uint16_t sp = (uint16_t)(GetChannelStackPointer(ch) - 1u);
	uint8_t count = (uint8_t)(gb_read8(sp) - 1u);
	if (count != 0u) {
		gb_write8(sp, count);
		caller_stream = read16((uint16_t)(sp - 2u));
	} else {
		SetChannelStackPointer(ch, (uint16_t)(sp - 2u));
	}
	play_next_from(caller_stream, ch);
}
/* <<< factory Music_EndLoop */

/* >>> factory Music_jp */
/* music.asm:909-915 */
void Music_jp(uint16_t caller_stream, uint8_t ch)
{
	(void)caller_stream;
	uint16_t stream = (uint16_t)(wAudioArg | ((uint16_t)gb_read8((uint16_t)(wAudioArg_ADDR + 1u)) << 8u));
	play_next_from(stream, ch);
}
/* <<< factory Music_jp */

/* >>> factory Music_call */
/* music.asm:917-931 */
void Music_call(uint16_t caller_stream, uint8_t ch)
{
	uint16_t sp = GetChannelStackPointer(ch);
	write16(sp, caller_stream);
	uint16_t target = (uint16_t)(wAudioArg | ((uint16_t)gb_read8((uint16_t)(wAudioArg_ADDR + 1u)) << 8u));
	SetChannelStackPointer(ch, (uint16_t)(sp + 2u));
	play_next_from(target, ch);
}
/* <<< factory Music_call */

/* >>> factory Music_ret */
/* music.asm:933-944 */
void Music_ret(uint16_t caller_stream, uint8_t ch)
{
	(void)caller_stream;
	uint16_t sp = (uint16_t)(GetChannelStackPointer(ch) - 2u);
	uint16_t stream = (uint16_t)(read16(sp) + 2u);
	SetChannelStackPointer(ch, sp);
	play_next_from(stream, ch);
}
/* <<< factory Music_ret */

/* >>> part one_byte_command */
static void one_byte_command(uint16_t caller_stream, uint8_t ch, uint16_t address, uint8_t value)
{
	gb_write8(channel_addr(address, ch), value);
	play_next_from((uint16_t)(caller_stream + 1u), ch);
}
/* <<< part one_byte_command */

/* >>> factory Music_frequency_offset */
/* music.asm:946-955 */
void Music_frequency_offset(uint16_t caller_stream, uint8_t ch)
{
	one_byte_command(caller_stream, ch, wMusicFrequencyOffset_ADDR, wAudioArg);
}
/* <<< factory Music_frequency_offset */

/* >>> factory Music_duty */
/* music.asm:957-967 */
void Music_duty(uint16_t caller_stream, uint8_t ch)
{
	one_byte_command(caller_stream, ch, wMusicDuty1_ADDR, (uint8_t)(wAudioArg & 0xC0u));
}
/* <<< factory Music_duty */

/* >>> factory Music_volume */
/* music.asm:969-978 */
void Music_volume(uint16_t caller_stream, uint8_t ch)
{
	one_byte_command(caller_stream, ch, wMusicVolume_ADDR, wAudioArg);
}
/* <<< factory Music_volume */

/* >>> factory Music_wave */
/* music.asm:980-989 */
void Music_wave(uint16_t caller_stream, uint8_t ch)
{
	wMusicWave = wAudioArg;
	wMusicWaveChange = 1u;
	play_next_from((uint16_t)(caller_stream + 1u), ch);
}
/* <<< factory Music_wave */

/* >>> factory Music_cutoff */
/* music.asm:991-1000 */
void Music_cutoff(uint16_t caller_stream, uint8_t ch)
{
	one_byte_command(caller_stream, ch, wMusicCutoff_ADDR, wAudioArg);
}
/* <<< factory Music_cutoff */

/* >>> factory Music_echo */
/* music.asm:1002-1011 */
void Music_echo(uint16_t caller_stream, uint8_t ch)
{
	one_byte_command(caller_stream, ch, wMusicEcho_ADDR, wAudioArg);
}
/* <<< factory Music_echo */

/* >>> factory Music_vibrato_type */
/* music.asm:1013-1025 */
void Music_vibrato_type(uint16_t caller_stream, uint8_t ch)
{
	gb_write8(channel_addr(wMusicVibratoType_ADDR, ch), wAudioArg);
	gb_write8(channel_addr(wMusicVibratoType2_ADDR, ch), wAudioArg);
	play_next_from((uint16_t)(caller_stream + 1u), ch);
}
/* <<< factory Music_vibrato_type */

/* >>> factory Music_vibrato_delay */
/* music.asm:1027-1036 */
void Music_vibrato_delay(uint16_t caller_stream, uint8_t ch)
{
	one_byte_command(caller_stream, ch, wMusicVibratoDelay_ADDR, wAudioArg);
}
/* <<< factory Music_vibrato_delay */

/* >>> factory Music_pitch_offset */
/* music.asm:1038-1047 */
void Music_pitch_offset(uint16_t caller_stream, uint8_t ch)
{
	one_byte_command(caller_stream, ch, wMusicPitchOffset_ADDR, wAudioArg);
}
/* <<< factory Music_pitch_offset */

/* >>> factory Music_adjust_pitch_offset */
/* music.asm:1049-1059 */
void Music_adjust_pitch_offset(uint16_t caller_stream, uint8_t ch)
{
	uint16_t addr = channel_addr(wMusicPitchOffset_ADDR, ch);
	gb_write8(addr, (uint8_t)(wAudioArg + gb_read8(addr)));
	play_next_from((uint16_t)(caller_stream + 1u), ch);
}
/* <<< factory Music_adjust_pitch_offset */

/* >>> factory Music_end */
/* music.asm:1061-1066 */
void Music_end(uint16_t caller_stream, uint8_t ch)
{
	(void)caller_stream;
	gb_write8(channel_addr(wMusicIsPlaying_ADDR, ch), 0u);
}
/* <<< factory Music_end */

/* >>> factory GetChannelStackPointer */
/* music.asm:1071-1078 */
uint16_t GetChannelStackPointer(uint8_t ch)
{
	return read16((uint16_t)(wMusicChannelStackPointers_ADDR + (uint16_t)ch * 2u));
}
/* <<< factory GetChannelStackPointer */

/* >>> factory SetChannelStackPointer */
/* music.asm:1081-1090 */
void SetChannelStackPointer(uint8_t ch, uint16_t sp)
{
	write16((uint16_t)(wMusicChannelStackPointers_ADDR + (uint16_t)ch * 2u), sp);
}
/* <<< factory SetChannelStackPointer */

/* >>> factory PlayNextNote_pop */
/* music.asm:1092-1094 */
void PlayNextNote_pop(uint16_t caller_stream, uint8_t ch)
{
	PlayNextNote(&caller_stream, ch);
}
/* <<< factory PlayNextNote_pop */

/* >>> factory Music_f4714 */
/* music.asm:1096-1133 */
void Music_f4714(void)
{
	g_rom_bank = MUSIC_BANK;
	if ((wdd8c & 0x01u) != 0u)
		return;
	if (wddb7 == 0u) {
		wMusicTie = 0u;
		gb_write8(APU_AUD1ENV, AUD1ENV_UP);
		gb_write8(APU_AUD1HIGH, AUD1HIGH_RESTART);
		return;
	}
	uint8_t d = 0u;
	if (wMusicTie != 0x80u) {
		gb_write8(APU_AUD1ENV, wMusicVolume);
		d = AUD1HIGH_RESTART;
	}
	wMusicTie = 2u;
	gb_write8(APU_AUD1SWEEP, AUD1SWEEP_DOWN);
	gb_write8(APU_AUD1LEN, wMusicDuty1);
	gb_write8(APU_AUD1LOW, wMusicCh1CurPitch);
	gb_write8(APU_AUD1HIGH, (uint8_t)(wMusicCh1CurOctave | d));
}
/* <<< factory Music_f4714 */

/* >>> factory Music_f475a */
/* music.asm:1135-1170 */
void Music_f475a(void)
{
	g_rom_bank = MUSIC_BANK;
	if ((wdd8c & 0x02u) != 0u)
		return;
	if (wddb8 == 0u) {
		wMusicTie_PTR[1] = 0u;
		gb_write8(APU_AUD2ENV, AUD2ENV_UP);
		gb_write8(APU_AUD2HIGH, AUD2HIGH_RESTART);
		return;
	}
	uint8_t d = 0u;
	if (wMusicTie_PTR[1] != 0x80u) {
		gb_write8(APU_AUD2ENV, wMusicVolume_PTR[1]);
		d = AUD2HIGH_RESTART;
	}
	wMusicTie_PTR[1] = 2u;
	gb_write8(APU_AUD2LEN, wMusicDuty2);
	gb_write8(APU_AUD2LOW, wMusicCh2CurPitch);
	gb_write8(APU_AUD2HIGH, (uint8_t)(wMusicCh2CurOctave | d));
}
/* <<< factory Music_f475a */

/* >>> factory Music_f479c */
/* music.asm:1172-1215 */
void Music_f479c(void)
{
	g_rom_bank = MUSIC_BANK;
	if ((wdd8c & 0x04u) != 0u)
		return;
	uint8_t d = 0u;
	if (wMusicWaveChange != 0u) {
		gb_write8(APU_AUD3ENA, 0u);
		LoadWaveInstrument();
		d = AUD3HIGH_RESTART;
	}
	if (wddb9 == 0u) {
		wMusicTie = 0u;
		gb_write8(APU_AUD3ENA, 0u);
		return;
	}
	if (wMusicTie_PTR[2] != 0x80u) {
		gb_write8(APU_AUD3LEVEL, wMusicVolume_PTR[2]);
		gb_write8(APU_AUD3ENA, 0u);
		d = AUD3HIGH_RESTART;
	}
	wMusicTie_PTR[2] = 2u;
	gb_write8(APU_AUD3LEN, 0u);
	gb_write8(APU_AUD3LOW, wMusicCh3CurPitch);
	gb_write8(APU_AUD3ENA, AUD3ENA_ON);
	gb_write8(APU_AUD3HIGH, (uint8_t)(wMusicCh3CurOctave | d));
}
/* <<< factory Music_f479c */

/* >>> factory LoadWaveInstrument */
/* music.asm:1217-1239 */
void LoadWaveInstrument(void)
{
	g_rom_bank = MUSIC_BANK;
	uint16_t source = read16((uint16_t)(ADR_WAVE_INSTRUMENTS + (uint16_t)wMusicWave * 2u));
	for (uint8_t i = 0u; i < AUD3WAVE_SIZE; i++)
		gb_write8((uint16_t)(APU_WAVE + i), gb_read8((uint16_t)(source + i)));
	wMusicWaveChange = 0u;
}
/* <<< factory LoadWaveInstrument */

/* >>> factory Music_f480a */
/* music.asm:1241-1272 */
void Music_f480a(void)
{
	g_rom_bank = MUSIC_BANK;
	if ((wdd8c & 0x08u) != 0u)
		return;
	if (wddba == 0u) {
		wddef = 0u;
		gb_write8(APU_AUD4ENV, AUD4ENV_UP);
		gb_write8(APU_AUD4GO, AUD4GO_RESTART);
		return;
	}
	gb_write8(APU_AUD4LEN, wddab);
	gb_write8(APU_AUD4ENV, wddac);
	gb_write8(APU_AUD4POLY, gb_read8((uint16_t)(wddab_ADDR + 2u)));
	gb_write8(APU_AUD4GO, gb_read8((uint16_t)(wddab_ADDR + 3u)));
}
/* <<< factory Music_f480a */

/* >>> factory Music_f4839 */
/* music.asm:1274-1297 */
void Music_f4839(void)
{
	g_rom_bank = MUSIC_BANK;
	if ((wdd8c & 0x08u) != 0u) {
		wddef = 0u;
		return;
	}
	uint16_t pointer = read16(wdded_ADDR);
	uint8_t value = gb_read8(pointer);
	if (value == 0xFFu) {
		wddef = 0u;
		gb_write8(APU_AUD4ENV, AUD4ENV_UP);
		gb_write8(APU_AUD4GO, AUD4GO_RESTART);
		return;
	}
	gb_write8(APU_AUD4POLY, value);
	write16(wdded_ADDR, (uint16_t)(pointer + 1u));
}
/* <<< factory Music_f4839 */

/* >>> factory Music_f485a */
/* music.asm:1299-1305 */
void Music_f485a(uint8_t ch)
{
	uint16_t frequency = UpdateVibrato(ch);
	Music_f490b(ch, frequency);
}
/* <<< factory Music_f485a */

/* >>> factory Music_f4866 */
/* music.asm:1307-1339 */
void Music_f4866(void)
{
	g_rom_bank = MUSIC_BANK;
	gb_write8(APU_VOL, wMusicPanning);
	uint8_t d = wdd8c;
	uint8_t a = wMusicStereoPanning;
	if (d != 0u) {
		uint8_t low = d & 0x0Fu;
		d = (uint8_t)(low | (uint8_t)(low << 4u));
		uint8_t e = (uint8_t)(d ^ 0xFFu);
		a = (uint8_t)(wdd85 & d);
		d = a;
		a = (uint8_t)(wMusicStereoPanning & e);
		a = (uint8_t)(a | d);
	}
	d = a;
	uint8_t e = (uint8_t)((wddf0 ^ 0xFFu) & 0x0Fu);
	e = (uint8_t)(e | (uint8_t)(e << 4u));
	gb_write8(APU_TERM, (uint8_t)(d & e));
}
/* <<< factory Music_f4866 */

/* >>> factory UpdateVibrato */
/* music.asm:1341-1424 */
uint16_t UpdateVibrato(uint8_t ch)
{
	uint8_t delay = gb_read8(channel_addr(wMusicVibratoDelay_ADDR, ch));
	uint16_t base = read16(channel_word_addr(wMusicCh1CurPitch_ADDR, ch));
	if (delay == 0u)
		return base;
	uint16_t delay_addr = channel_addr(wdde3_ADDR, ch);
	if (delay != gb_read8(delay_addr)) {
		gb_write8(delay_addr, (uint8_t)(gb_read8(delay_addr) + 1u));
		return base;
	}
	for (;;) {
		uint8_t type = gb_read8(channel_addr(wMusicVibratoType_ADDR, ch));
		uint16_t table = read16((uint16_t)(ADR_VIBRATO_TYPES + (uint16_t)type * 2u));
		uint16_t position_addr = channel_addr(wdddb_ADDR, ch);
		uint8_t position = gb_read8(position_addr);
		gb_write8(position_addr, (uint8_t)(position + 1u));
		uint16_t entry = (uint16_t)(table + position);
		uint8_t delta = gb_read8(entry);
		if (delta == 0x80u) {
			gb_write8(position_addr, 0u);
			uint8_t next_type = gb_read8((uint16_t)(entry + 1u));
			if (next_type != 0x80u)
				gb_write8(channel_addr(wMusicVibratoType_ADDR, ch), next_type);
			continue;
		}
		uint8_t low = (uint8_t)base;
		uint8_t high = (uint8_t)(base >> 8u);
		if ((delta & 0x80u) == 0u) {
			uint16_t sum = (uint16_t)low + delta;
			low = (uint8_t)sum;
			high = (uint8_t)((high + (uint8_t)(sum >> 8u)) & 0x07u);
		} else {
			uint8_t magnitude = (uint8_t)((uint8_t)(delta ^ 0xFFu) + 1u);
			uint8_t borrow = low < magnitude ? 1u : 0u;
			low = (uint8_t)(low - magnitude);
			high = (uint8_t)((high - borrow) & 0x07u);
		}
		return (uint16_t)(((uint16_t)high << 8u) | low);
	}
}
/* <<< factory UpdateVibrato */

/* >>> factory Music_f490b */
/* music.asm:1426-1477 */
void Music_f490b(uint8_t ch, uint16_t de)
{
	g_rom_bank = MUSIC_BANK;
	uint8_t low = (uint8_t)de;
	uint8_t high = (uint8_t)(de >> 8u);
	if (ch == 0u) {
		if (wMusicVibratoDelay == 0u || (wdd8c & 0x01u) != 0u)
			return;
		gb_write8(APU_AUD1LOW, low);
		gb_write8(APU_AUD1LEN, (uint8_t)(gb_read8(APU_AUD1LEN) & (uint8_t)~AUD1LEN_TIMER));
		gb_write8(APU_AUD1HIGH, (uint8_t)(high & 0x3Fu));
		return;
	}
	if (ch == 1u) {
		if (wMusicVibratoDelay_PTR[1] == 0u || (wdd8c & 0x02u) != 0u)
			return;
		gb_write8(APU_AUD2LOW, low);
		gb_write8(APU_AUD2LEN, (uint8_t)(gb_read8(APU_AUD2LEN) & (uint8_t)~AUD2LEN_TIMER));
		gb_write8(APU_AUD2HIGH, high);
		return;
	}
	if (ch != 2u || wMusicVibratoDelay_PTR[2] == 0u || (wdd8c & 0x04u) != 0u)
		return;
	gb_write8(APU_AUD3LOW, low);
	gb_write8(APU_AUD3LEN, 0u);
	gb_write8(APU_AUD3HIGH, high);
}
/* <<< factory Music_f490b */

/* >>> factory Music_f4967 */
/* music.asm:1479-1500 */
MusicFrequencyResult Music_f4967(uint8_t ch, uint16_t de)
{
	uint16_t frequency = de;
	uint8_t offset = gb_read8(channel_addr(wMusicFrequencyOffset_ADDR, ch));
	if ((offset & 0x80u) != 0u)
		frequency = (uint16_t)(frequency - (uint8_t)(offset ^ 0xFFu));
	else
		frequency = (uint16_t)(frequency + offset);
	return (MusicFrequencyResult){(uint8_t)(frequency >> 8u), (uint8_t)frequency};
}
/* <<< factory Music_f4967 */

/* >>> factory Music_f4980 */
/* music.asm:1502-1531 */
void Music_f4980(void)
{
	g_rom_bank = MUSIC_BANK;
	uint8_t d = wdd8c;
	uint8_t a = d;
	if ((d & 0x01u) == 0u) {
		a = AUD1ENV_UP;
		gb_write8(APU_AUD1ENV, a);
		a = (uint8_t)((a << 4u) | (a >> 4u));
		gb_write8(APU_AUD1HIGH, a);
	}
	if ((d & 0x02u) == 0u) {
		a = (uint8_t)((a << 4u) | (a >> 4u));
		gb_write8(APU_AUD2ENV, a);
		a = (uint8_t)((a << 4u) | (a >> 4u));
		gb_write8(APU_AUD2HIGH, a);
	}
	if ((d & 0x08u) == 0u) {
		a = (uint8_t)((a << 4u) | (a >> 4u));
		gb_write8(APU_AUD4ENV, a);
		a = (uint8_t)((a << 4u) | (a >> 4u));
		gb_write8(APU_AUD4GO, a);
	}
	if ((d & 0x04u) == 0u)
		gb_write8(APU_AUD3LEVEL, AUD3LEVEL_MUTE);
}
/* <<< factory Music_f4980 */

/* >>> factory CheckForEndOfSong */
/* music.asm:1533-1547 */
void CheckForEndOfSong(void)
{
	g_rom_bank = MUSIC_BANK;
	uint8_t sum = 0u;
	for (uint8_t ch = 0u; ch < 4u; ch++)
		sum = (uint8_t)(sum + gb_read8(channel_addr(wMusicIsPlaying_ADDR, ch)));
	if (sum == 0u)
		wCurSongID = 0x80u;
}
/* <<< factory CheckForEndOfSong */

/* >>> factory Music_PauseSong */
/* music.asm:1549-1555 */
void Music_PauseSong(void)
{
	g_rom_bank = MUSIC_BANK;
	Music_f4980();
	BackupSong();
	StopAllChannels();
}
/* <<< factory Music_PauseSong */

/* >>> factory Music_ResumeSong */
/* music.asm:1557-1563 */
void Music_ResumeSong(void)
{
	g_rom_bank = MUSIC_BANK;
	Music_f4980();
	StopAllChannels();
	LoadBackup();
}
/* <<< factory Music_ResumeSong */

/* >>> factory BackupSong */
/* music.asm:1565-1670 */
void BackupSong(void)
{
	g_rom_bank = MUSIC_BANK;
	wCurSongIDBackup = wCurSongID;
	wCurSongBankBackup = wCurSongBank;
	wMusicStereoPanningBackup = wMusicStereoPanning;
	uint16_t hl = wMusicDuty1_ADDR;
	uint16_t de = wMusicDuty1Backup_ADDR;
	CopyData(&hl, &de, 4u);
	wMusicWaveBackup = wMusicWave;
	wMusicWaveChangeBackup = wMusicWaveChange;
	hl = wMusicIsPlaying_ADDR; de = wMusicIsPlayingBackup_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicTie_ADDR; de = wMusicTieBackup_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicChannelPointers_ADDR; de = wMusicChannelPointersBackup_ADDR; CopyData(&hl, &de, 8u);
	hl = wMusicMainLoopStart_ADDR; de = wMusicMainLoopStartBackup_ADDR; CopyData(&hl, &de, 8u);
	wde76 = wddab; wde77 = wddac;
	hl = wMusicOctave_ADDR; de = wMusicOctaveBackup_ADDR; CopyData(&hl, &de, 4u);
	hl = wddb3_ADDR; de = wde7c_ADDR; CopyData(&hl, &de, 4u);
	hl = wddb7_ADDR; de = wde80_ADDR; CopyData(&hl, &de, 4u);
	hl = wddbb_ADDR; de = wde84_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicCutoff_ADDR; de = wMusicCutoffBackup_ADDR; CopyData(&hl, &de, 4u);
	hl = wddc3_ADDR; de = wde8c_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicEcho_ADDR; de = wMusicEchoBackup_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicPitchOffset_ADDR; de = wMusicPitchOffsetBackup_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicSpeed_ADDR; de = wMusicSpeedBackup_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicVibratoType2_ADDR; de = wMusicVibratoType2Backup_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicVibratoDelay_ADDR; de = wMusicVibratoDelayBackup_ADDR; CopyData(&hl, &de, 4u);
	for (uint8_t i = 0u; i < 4u; i++)
		gb_write8(channel_addr(wdddb_ADDR, i), 0u);
	hl = wMusicVolume_ADDR; de = wMusicVolumeBackup_ADDR; CopyData(&hl, &de, 3u);
	hl = wMusicFrequencyOffset_ADDR; de = wMusicFrequencyOffsetBackup_ADDR; CopyData(&hl, &de, 3u);
	hl = wdded_ADDR; de = wdeaa_ADDR; CopyData(&hl, &de, 2u);
	wdeac = 0u;
	hl = wMusicChannelStackPointers_ADDR; de = wMusicChannelStackPointersBackup_ADDR; CopyData(&hl, &de, 8u);
	hl = wMusicCh1Stack_ADDR; de = wMusicCh1StackBackup_ADDR; CopyData(&hl, &de, 0x30u);
}
/* <<< factory BackupSong */

/* >>> factory LoadBackup */
/* music.asm:1672-1772 */
void LoadBackup(void)
{
	g_rom_bank = MUSIC_BANK;
	wCurSongID = wCurSongIDBackup;
	wCurSongBank = wCurSongBankBackup;
	wMusicStereoPanning = wMusicStereoPanningBackup;
	uint16_t hl = wMusicDuty1Backup_ADDR;
	uint16_t de = wMusicDuty1_ADDR;
	CopyData(&hl, &de, 4u);
	wMusicWave = wMusicWaveBackup;
	wMusicWaveChange = 1u;
	hl = wMusicIsPlayingBackup_ADDR; de = wMusicIsPlaying_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicTieBackup_ADDR; de = wMusicTie_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicChannelPointersBackup_ADDR; de = wMusicChannelPointers_ADDR; CopyData(&hl, &de, 8u);
	hl = wMusicMainLoopStartBackup_ADDR; de = wMusicMainLoopStart_ADDR; CopyData(&hl, &de, 8u);
	wddab = wde76; wddac = wde77;
	hl = wMusicOctaveBackup_ADDR; de = wMusicOctave_ADDR; CopyData(&hl, &de, 4u);
	hl = wde7c_ADDR; de = wddb3_ADDR; CopyData(&hl, &de, 4u);
	hl = wde80_ADDR; de = wddb7_ADDR; CopyData(&hl, &de, 4u);
	hl = wde84_ADDR; de = wddbb_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicCutoffBackup_ADDR; de = wMusicCutoff_ADDR; CopyData(&hl, &de, 4u);
	hl = wde8c_ADDR; de = wddc3_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicEchoBackup_ADDR; de = wMusicEcho_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicPitchOffsetBackup_ADDR; de = wMusicPitchOffset_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicSpeedBackup_ADDR; de = wMusicSpeed_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicVibratoType2Backup_ADDR; de = wMusicVibratoType2_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicVibratoDelayBackup_ADDR; de = wMusicVibratoDelay_ADDR; CopyData(&hl, &de, 4u);
	hl = wMusicVolumeBackup_ADDR; de = wMusicVolume_ADDR; CopyData(&hl, &de, 3u);
	hl = wMusicFrequencyOffsetBackup_ADDR; de = wMusicFrequencyOffset_ADDR; CopyData(&hl, &de, 3u);
	hl = wdeaa_ADDR; de = wdded_ADDR; CopyData(&hl, &de, 2u);
	wddef = wdeac;
	hl = wMusicChannelStackPointersBackup_ADDR; de = wMusicChannelStackPointers_ADDR; CopyData(&hl, &de, 8u);
	hl = wMusicCh1StackBackup_ADDR; de = wMusicCh1Stack_ADDR; CopyData(&hl, &de, 0x30u);
}
/* <<< factory LoadBackup */

/* >>> factory CopyData */
/* music.asm:1775-1783 */
void CopyData(uint16_t *hl, uint16_t *de, uint8_t n)
{
	uint8_t count = n;
	do {
		gb_write8(*de, gb_read8(*hl));
		*hl = (uint16_t)(*hl + 1u);
		*de = (uint16_t)(*de + 1u);
	} while (--count != 0u);
}
/* <<< factory CopyData */
