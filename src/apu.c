#include "apu.h"

#include <string.h>

#define FRAME_SEQUENCER_PERIOD 8192u

typedef struct {
	int enabled;
	int dac;
	uint16_t frequency;
	uint32_t timer;
	uint32_t period;
	uint8_t duty;
	uint8_t duty_step;
	uint16_t length;
	int length_enable;
	uint8_t volume;
	uint8_t envelope_initial;
	int envelope_add;
	uint8_t envelope_period;
	uint8_t envelope_timer;
	uint8_t sweep_period;
	int sweep_negate;
	uint8_t sweep_shift;
	uint8_t sweep_timer;
	uint16_t sweep_shadow;
	int sweep_enabled;
	uint8_t wave_position;
	uint8_t wave_sample;
	uint8_t wave_volume_code;
	uint16_t lfsr;
	int lfsr_width7;
	uint8_t noise_shift;
	uint8_t noise_divisor;
} Channel;

static struct {
	int power;
	uint8_t registers[0x30];
	Channel ch[4];
	uint32_t sequencer_cycles;
	uint8_t sequencer_step;
	uint32_t sample_cycles;
	uint8_t nr50;
	uint8_t nr51;
	uint8_t host_master_volume;
	uint8_t host_music_volume;
	uint8_t host_sfx_mask;
	int host_mono;
} g_apu;

static const uint8_t DUTY_TABLE[4] = {0x01u, 0x81u, 0x87u, 0x7Eu};
static const uint8_t NOISE_DIVISORS[8] = {8u, 16u, 32u, 48u, 64u, 80u, 96u, 112u};

static uint32_t square_period(uint16_t frequency)
{
	return (uint32_t)(2048u - (frequency & 0x7FFu)) * 4u;
}

static uint32_t wave_period(uint16_t frequency)
{
	return (uint32_t)(2048u - (frequency & 0x7FFu)) * 2u;
}

static uint32_t noise_period(const Channel *ch)
{
	return (uint32_t)NOISE_DIVISORS[ch->noise_divisor & 7u] << ch->noise_shift;
}

void apu_reset(void)
{
	memset(&g_apu, 0, sizeof g_apu);
	g_apu.ch[3].lfsr = 0x7FFFu;
	g_apu.host_master_volume = 100u;
	g_apu.host_music_volume = 100u;
}

void apu_set_host_mix(uint8_t master_volume, uint8_t music_volume,
	int mono, uint8_t sfx_mask)
{
	g_apu.host_master_volume = master_volume > 100u ? 100u : master_volume;
	g_apu.host_music_volume = music_volume > 100u ? 100u : music_volume;
	g_apu.host_mono = mono != 0;
	g_apu.host_sfx_mask = sfx_mask;
}

uint8_t apu_status(void)
{
	uint8_t status = g_apu.power ? 0xF0u : 0x70u;
	for (unsigned i = 0; i < 4; i++)
		if (g_apu.ch[i].enabled)
			status |= (uint8_t)(1u << i);
	return status;
}

static void trigger_square(Channel *ch, unsigned index)
{
	ch->enabled = 1;
	if (ch->length == 0u)
		ch->length = 64u;
	ch->period = square_period(ch->frequency);
	ch->timer = ch->period;
	ch->envelope_timer = ch->envelope_period ? ch->envelope_period : 8u;
	ch->volume = ch->envelope_initial;
	if (index == 0u) {
		ch->sweep_shadow = ch->frequency;
		ch->sweep_timer = ch->sweep_period ? ch->sweep_period : 8u;
		ch->sweep_enabled = ch->sweep_period != 0u || ch->sweep_shift != 0u;
		if (ch->sweep_shift != 0u) {
			uint16_t shifted = (uint16_t)(ch->sweep_shadow >> ch->sweep_shift);
			uint16_t next = ch->sweep_negate ? (uint16_t)(ch->sweep_shadow - shifted)
			                                : (uint16_t)(ch->sweep_shadow + shifted);
			if (next > 2047u)
				ch->enabled = 0;
		}
	}
	if (!ch->dac)
		ch->enabled = 0;
}

static void trigger_wave(Channel *ch)
{
	ch->enabled = 1;
	if (ch->length == 0u)
		ch->length = 256u;
	ch->period = wave_period(ch->frequency);
	ch->timer = ch->period;
	ch->wave_position = 0u;
	if (!ch->dac)
		ch->enabled = 0;
}

static void trigger_noise(Channel *ch)
{
	ch->enabled = 1;
	if (ch->length == 0u)
		ch->length = 64u;
	ch->period = noise_period(ch);
	ch->timer = ch->period;
	ch->envelope_timer = ch->envelope_period ? ch->envelope_period : 8u;
	ch->volume = ch->envelope_initial;
	ch->lfsr = 0x7FFFu;
	if (!ch->dac)
		ch->enabled = 0;
}

void apu_write(uint16_t address, uint8_t value)
{
	if (address == 0xFF26u) {
		int power = (value & 0x80u) != 0u;
		if (!power && g_apu.power) {
			uint8_t wave[16];
			memcpy(wave, g_apu.registers + 0x20, sizeof wave);
			memset(&g_apu, 0, sizeof g_apu);
			memcpy(g_apu.registers + 0x20, wave, sizeof wave);
			g_apu.ch[3].lfsr = 0x7FFFu;
		} else if (power && !g_apu.power) {
			g_apu.sequencer_step = 0u;
			g_apu.sequencer_cycles = 0u;
		}
		g_apu.power = power;
		return;
	}
	if (address >= 0xFF30u && address <= 0xFF3Fu) {
		g_apu.registers[address - 0xFF10u] = value;
		return;
	}
	if (address < 0xFF10u || address > 0xFF25u)
		return;
	if (!g_apu.power)
		return;
	g_apu.registers[address - 0xFF10u] = value;
	Channel *ch;
	switch (address) {
	case 0xFF10u:
		ch = &g_apu.ch[0];
		ch->sweep_period = (uint8_t)((value >> 4) & 7u);
		ch->sweep_negate = (value & 0x08u) != 0u;
		ch->sweep_shift = (uint8_t)(value & 7u);
		break;
	case 0xFF11u:
	case 0xFF16u:
		ch = &g_apu.ch[address == 0xFF11u ? 0 : 1];
		ch->duty = (uint8_t)(value >> 6);
		ch->length = (uint16_t)(64u - (value & 0x3Fu));
		break;
	case 0xFF12u:
	case 0xFF17u:
	case 0xFF21u:
		ch = &g_apu.ch[address == 0xFF12u ? 0 : (address == 0xFF17u ? 1 : 3)];
		ch->envelope_initial = (uint8_t)(value >> 4);
		ch->envelope_add = (value & 0x08u) != 0u;
		ch->envelope_period = (uint8_t)(value & 7u);
		ch->dac = (value & 0xF8u) != 0u;
		if (!ch->dac)
			ch->enabled = 0;
		break;
	case 0xFF13u:
	case 0xFF18u:
	case 0xFF1Du:
		ch = &g_apu.ch[address == 0xFF13u ? 0 : (address == 0xFF18u ? 1 : 2)];
		ch->frequency = (uint16_t)((ch->frequency & 0x700u) | value);
		ch->period = address == 0xFF1Du ? wave_period(ch->frequency) : square_period(ch->frequency);
		break;
	case 0xFF14u:
	case 0xFF19u:
	case 0xFF1Eu: {
		unsigned index = address == 0xFF14u ? 0u : (address == 0xFF19u ? 1u : 2u);
		ch = &g_apu.ch[index];
		ch->frequency = (uint16_t)((ch->frequency & 0xFFu) | ((value & 7u) << 8));
		ch->period = index == 2u ? wave_period(ch->frequency) : square_period(ch->frequency);
		ch->length_enable = (value & 0x40u) != 0u;
		if (value & 0x80u) {
			if (index == 2u)
				trigger_wave(ch);
			else
				trigger_square(ch, index);
		}
		break;
	}
	case 0xFF1Au:
		ch = &g_apu.ch[2];
		ch->dac = (value & 0x80u) != 0u;
		if (!ch->dac)
			ch->enabled = 0;
		break;
	case 0xFF1Bu:
		g_apu.ch[2].length = (uint16_t)(256u - value);
		break;
	case 0xFF1Cu:
		g_apu.ch[2].wave_volume_code = (uint8_t)((value >> 5) & 3u);
		break;
	case 0xFF20u:
		g_apu.ch[3].length = (uint16_t)(64u - (value & 0x3Fu));
		break;
	case 0xFF22u:
		ch = &g_apu.ch[3];
		ch->noise_shift = (uint8_t)(value >> 4);
		ch->lfsr_width7 = (value & 0x08u) != 0u;
		ch->noise_divisor = (uint8_t)(value & 7u);
		ch->period = noise_period(ch);
		break;
	case 0xFF23u:
		ch = &g_apu.ch[3];
		ch->length_enable = (value & 0x40u) != 0u;
		if (value & 0x80u)
			trigger_noise(ch);
		break;
	case 0xFF24u:
		g_apu.nr50 = value;
		break;
	case 0xFF25u:
		g_apu.nr51 = value;
		break;
	default:
		break;
	}
}

static void clock_length(Channel *ch)
{
	if (ch->length_enable && ch->length > 0u) {
		ch->length--;
		if (ch->length == 0u)
			ch->enabled = 0;
	}
}

static void clock_envelope(Channel *ch)
{
	if (ch->envelope_period == 0u)
		return;
	if (ch->envelope_timer > 0u)
		ch->envelope_timer--;
	if (ch->envelope_timer == 0u) {
		ch->envelope_timer = ch->envelope_period;
		if (ch->envelope_add && ch->volume < 15u)
			ch->volume++;
		else if (!ch->envelope_add && ch->volume > 0u)
			ch->volume--;
	}
}

static void clock_sweep(Channel *ch)
{
	if (ch->sweep_timer > 0u)
		ch->sweep_timer--;
	if (ch->sweep_timer != 0u)
		return;
	ch->sweep_timer = ch->sweep_period ? ch->sweep_period : 8u;
	if (!ch->sweep_enabled || ch->sweep_period == 0u)
		return;
	uint16_t shifted = (uint16_t)(ch->sweep_shadow >> ch->sweep_shift);
	uint16_t next = ch->sweep_negate ? (uint16_t)(ch->sweep_shadow - shifted)
	                                : (uint16_t)(ch->sweep_shadow + shifted);
	if (next > 2047u) {
		ch->enabled = 0;
		return;
	}
	if (ch->sweep_shift != 0u) {
		ch->sweep_shadow = next;
		ch->frequency = next;
		ch->period = square_period(next);
		shifted = (uint16_t)(next >> ch->sweep_shift);
		next = ch->sweep_negate ? (uint16_t)(next - shifted) : (uint16_t)(next + shifted);
		if (next > 2047u)
			ch->enabled = 0;
	}
}

static void clock_sequencer(void)
{
	uint8_t step = g_apu.sequencer_step;
	if ((step & 1u) == 0u) {
		for (unsigned i = 0; i < 4; i++)
			clock_length(&g_apu.ch[i]);
	}
	if (step == 2u || step == 6u)
		clock_sweep(&g_apu.ch[0]);
	if (step == 7u) {
		clock_envelope(&g_apu.ch[0]);
		clock_envelope(&g_apu.ch[1]);
		clock_envelope(&g_apu.ch[3]);
	}
	g_apu.sequencer_step = (uint8_t)((step + 1u) & 7u);
}

static void step_square(Channel *ch, uint32_t cycles)
{
	if (ch->period == 0u)
		return;
	while (cycles >= ch->timer) {
		cycles -= ch->timer;
		ch->timer = ch->period;
		ch->duty_step = (uint8_t)((ch->duty_step + 1u) & 7u);
	}
	ch->timer -= cycles;
}

static void step_wave(Channel *ch, uint32_t cycles)
{
	if (ch->period == 0u)
		return;
	while (cycles >= ch->timer) {
		cycles -= ch->timer;
		ch->timer = ch->period;
		ch->wave_position = (uint8_t)((ch->wave_position + 1u) & 31u);
		uint8_t byte = g_apu.registers[0x20u + (ch->wave_position >> 1)];
		ch->wave_sample = (ch->wave_position & 1u) ? (uint8_t)(byte & 0x0Fu) : (uint8_t)(byte >> 4);
	}
	ch->timer -= cycles;
}

static void step_noise(Channel *ch, uint32_t cycles)
{
	if (ch->period == 0u)
		return;
	while (cycles >= ch->timer) {
		cycles -= ch->timer;
		ch->timer = ch->period;
		uint16_t bit = (uint16_t)((ch->lfsr ^ (ch->lfsr >> 1)) & 1u);
		ch->lfsr = (uint16_t)((ch->lfsr >> 1) | (bit << 14));
		if (ch->lfsr_width7)
			ch->lfsr = (uint16_t)((ch->lfsr & ~(1u << 6)) | (bit << 6));
	}
	ch->timer -= cycles;
}

static void advance(uint32_t cycles)
{
	if (!g_apu.power)
		return;
	g_apu.sequencer_cycles += cycles;
	while (g_apu.sequencer_cycles >= FRAME_SEQUENCER_PERIOD) {
		g_apu.sequencer_cycles -= FRAME_SEQUENCER_PERIOD;
		clock_sequencer();
	}
	step_square(&g_apu.ch[0], cycles);
	step_square(&g_apu.ch[1], cycles);
	step_wave(&g_apu.ch[2], cycles);
	step_noise(&g_apu.ch[3], cycles);
}

static int channel_output(unsigned index)
{
	const Channel *ch = &g_apu.ch[index];
	if (!ch->enabled || !ch->dac)
		return 0;
	unsigned amplitude;
	switch (index) {
	case 0:
	case 1:
		amplitude = ((DUTY_TABLE[ch->duty] >> ch->duty_step) & 1u) ? ch->volume : 0u;
		break;
	case 2: {
		uint8_t code = ch->wave_volume_code;
		amplitude = code == 0u ? 0u : (unsigned)(ch->wave_sample >> (code - 1u));
		break;
	}
	default:
		amplitude = ((~ch->lfsr) & 1u) ? ch->volume : 0u;
		break;
	}
	return (int)amplitude * 2 - 15;
}

static void mix(int16_t *out)
{
	int music_left = 0;
	int music_right = 0;
	int sfx_left = 0;
	int sfx_right = 0;
	if (g_apu.power) {
		for (unsigned i = 0; i < 4; i++) {
			int sample = channel_output(i);
			int *left = (g_apu.host_sfx_mask & (1u << i)) ? &sfx_left : &music_left;
			int *right = (g_apu.host_sfx_mask & (1u << i)) ? &sfx_right : &music_right;
			if (g_apu.nr51 & (1u << (i + 4)))
				*left += sample;
			if (g_apu.nr51 & (1u << i))
				*right += sample;
		}
		music_left *= ((g_apu.nr50 >> 4) & 7) + 1;
		music_right *= (g_apu.nr50 & 7) + 1;
		sfx_left *= ((g_apu.nr50 >> 4) & 7) + 1;
		sfx_right *= (g_apu.nr50 & 7) + 1;
	}
	int left = (music_left * g_apu.host_music_volume / 100 + sfx_left)
		* g_apu.host_master_volume / 100;
	int right = (music_right * g_apu.host_music_volume / 100 + sfx_right)
		* g_apu.host_master_volume / 100;
	if (g_apu.host_mono) {
		int mono = (left + right) / 2;
		left = mono;
		right = mono;
	}
	out[0] = (int16_t)(left * 32);
	out[1] = (int16_t)(right * 32);
}

void apu_render_frame(int16_t *stereo_out, size_t frames_out,
                      const ApuFrameWrite *writes, size_t write_count,
                      unsigned phases_per_frame)
{
	if (!phases_per_frame)
		phases_per_frame = 1u;
	size_t next_write = 0;
	uint64_t cycle_numerator = 0;
	for (size_t i = 0; i < frames_out; i++) {
		size_t phase_frame = frames_out;
		while (next_write < write_count) {
			unsigned phase = writes[next_write].phase;
			if (phase >= phases_per_frame)
				phase = phases_per_frame - 1u;
			phase_frame = (size_t)phase * frames_out / phases_per_frame;
			if (phase_frame > i)
				break;
			apu_write(writes[next_write].address, writes[next_write].value);
			next_write++;
		}
		cycle_numerator += APU_CLOCK_HZ;
		uint32_t cycles = (uint32_t)(cycle_numerator / APU_SAMPLE_RATE);
		cycle_numerator -= (uint64_t)cycles * APU_SAMPLE_RATE;
		advance(cycles);
		mix(stereo_out + i * 2);
	}
	while (next_write < write_count) {
		apu_write(writes[next_write].address, writes[next_write].value);
		next_write++;
	}
}
