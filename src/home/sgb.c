#include "home/sgb.h"
/* >>> factory statics */
#include "home/sgb.h"
#include "mem.h"

#define SGB_PACKET_SIZE 0x10u
#define JOYP_SGB_START 0x00u
#define JOYP_SGB_ONE 0x10u
#define JOYP_SGB_ZERO 0x20u
#define JOYP_SGB_FINISH 0x30u
/* <<< factory statics */

/* sgb.asm:258-274. The delay loop has no observable effects beyond its
 * register residue: DE and A end at zero, and the final OR leaves Z set. */
SGBWaitResult Wait(uint16_t bc)
{
	uint32_t count = bc ? bc : 0x10000u;

	while (count--) {
		uint16_t de = 1750u;
		do {
			de--;
		} while (de != 0);
	}

	return (SGBWaitResult){0, 0x80u, 0, 0, 0, 0};
}

/* >>> factory SendSGB */
SendSGBResult SendSGB(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t packet_count = (uint8_t)(gb_read8(hl) & 0x07u);
	if (packet_count == 0u)
		return (SendSGBResult){0u, 0xA0u, b, c, d, e, hl};

	for (uint8_t pkt = packet_count; pkt != 0u; pkt--) {
		gb_write8(0xFF00u, JOYP_SGB_START);
		gb_write8(0xFF00u, JOYP_SGB_FINISH);
		for (uint8_t byte_count = SGB_PACKET_SIZE; byte_count != 0u; byte_count--) {
			uint8_t data = gb_read8(hl);
			hl = (uint16_t)(hl + 1u);
			for (uint8_t bit = 8u; bit != 0u; bit--) {
				gb_write8(0xFF00u, (data & 1u) != 0u ? JOYP_SGB_ONE : JOYP_SGB_ZERO);
				gb_write8(0xFF00u, JOYP_SGB_FINISH);
				data = (uint8_t)(data >> 1);
			}
		}
		gb_write8(0xFF00u, JOYP_SGB_ZERO);
		gb_write8(0xFF00u, JOYP_SGB_FINISH);
	}
	SGBWaitResult wait = Wait(4u);
	return (SendSGBResult){wait.a, wait.f, wait.b, wait.c, wait.d, wait.e, hl};
}
/* <<< factory SendSGB */
