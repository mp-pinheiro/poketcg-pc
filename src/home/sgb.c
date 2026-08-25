#include "home/sgb.h"
/* >>> factory statics */
#include "home/sgb.h"
#include "mem.h"

#define SGB_PACKET_SIZE 0x10u
#define JOYP_SGB_START 0x00u
#define JOYP_SGB_ONE 0x10u
#define JOYP_SGB_ZERO 0x20u
#define JOYP_SGB_FINISH 0x30u

#include "home/sgb.h"

#include "home/sgb.h"
#define JOYP_SGB_MLT_REQ 0x03u
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

/* >>> factory InitSGB */
InitSGBResult InitSGB(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	SendSGBResult r = {a, f, b, c, d, e, hl};
	r = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0AD0u); /* MaskEnPacket_Freeze */
	r = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0A50u); /* DataSndPacket1 */
	r = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0A60u); /* DataSndPacket2 */
	r = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0A70u); /* DataSndPacket3 */
	r = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0A80u); /* DataSndPacket4 */
	r = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0A90u); /* DataSndPacket5 */
	r = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0AA0u); /* DataSndPacket6 */
	r = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0AB0u); /* DataSndPacket7 */
	r = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0AC0u); /* DataSndPacket8 */
	r = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0AF0u); /* Pal01Packet_InitSGB */
	r = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0AE0u); /* MaskEnPacket_Cancel */
	return (InitSGBResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory InitSGB */

/* >>> factory DetectSGB */
DetectSGBResult DetectSGB(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	SGBWaitResult w = Wait(60u);
	SendSGBResult r = SendSGB(w.a, w.f, w.b, w.c, w.d, w.e, 0x0BBBu); /* MltReq2Packet */
	uint8_t joyp = (uint8_t)(gb_read8(0xFF00u) & JOYP_SGB_MLT_REQ);
	if (joyp != JOYP_SGB_MLT_REQ) {
		SendSGBResult fail = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0BABu); /* MltReq1Packet */
		return (DetectSGBResult){fail.a, (uint8_t)((fail.f & 0x80u) | 0x10u), fail.b, fail.c, fail.d, fail.e, fail.hl};
	}
	gb_write8(0xFF00u, JOYP_SGB_ZERO);
	(void)gb_read8(0xFF00u);
	(void)gb_read8(0xFF00u);
	gb_write8(0xFF00u, JOYP_SGB_FINISH);
	gb_write8(0xFF00u, JOYP_SGB_ONE);
	for (uint8_t i = 0u; i < 6u; i++)
		(void)gb_read8(0xFF00u);
	gb_write8(0xFF00u, JOYP_SGB_FINISH);
	for (uint8_t i = 0u; i < 3u; i++)
		(void)gb_read8(0xFF00u);
	joyp = (uint8_t)(gb_read8(0xFF00u) & JOYP_SGB_MLT_REQ);
	if (joyp != JOYP_SGB_MLT_REQ) {
		SendSGBResult fail = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0BABu); /* MltReq1Packet */
		return (DetectSGBResult){fail.a, (uint8_t)((fail.f & 0x80u) | 0x10u), fail.b, fail.c, fail.d, fail.e, fail.hl};
	}
	SendSGBResult ok = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0BABu); /* MltReq1Packet */
	return (DetectSGBResult){ok.a, (uint8_t)(ok.a == 0u ? 0x80u : 0x00u), ok.b, ok.c, ok.d, ok.e, ok.hl};
}
/* <<< factory DetectSGB */

/* >>> factory Func_0bcb */
Func_0bcbResult Func_0bcb(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	for (uint16_t i = 0; i < 0x1000u; i++) {
		uint8_t value = gb_read8((uint16_t)(hl + i));
		gb_write8((uint16_t)(0x8800u + i), value);
	}
	uint8_t tilemap_value = 0x80u;
	for (uint8_t row = 0; row < 0x0Du; row++) {
		for (uint8_t col = 0; col < 0x14u; col++) {
			gb_write8((uint16_t)(0x9800u + (uint16_t)row * 0x20u + col), tilemap_value++);
		}
	}
	gb_write8(0xFF40u, 0xC3u);
	gb_write8(0xFF47u, 0xE4u);
	SendSGBResult result = SendSGB(0xC3u, 0x00u, 0x00u, 0x00u, 0x00u, 0x0Cu, (uint16_t)((uint16_t)d << 8 | e));
	return (Func_0bcbResult){result.a, result.f, result.b, result.c, result.d, result.e, result.hl};
}
/* <<< factory Func_0bcb */
