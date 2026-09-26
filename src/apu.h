#ifndef POKETCG_APU_H
#define POKETCG_APU_H

#include <stddef.h>
#include <stdint.h>

#define APU_CLOCK_HZ 4194304u
#define APU_SAMPLE_RATE 44100u
#define APU_CYCLES_PER_FRAME 70224u

typedef struct {
	uint16_t address;
	uint8_t value;
	uint8_t phase;
} ApuFrameWrite;

void apu_reset(void);
void apu_write(uint16_t address, uint8_t value);
void apu_set_host_mix(uint8_t master_volume, uint8_t music_volume,
                      uint8_t sfx_volume, int mono, uint8_t sfx_mask);
uint8_t apu_status(void);
void apu_render_frame(int16_t *stereo_out, size_t frames_out,
                      const ApuFrameWrite *writes, size_t write_count,
                      unsigned phases_per_frame);

#endif
