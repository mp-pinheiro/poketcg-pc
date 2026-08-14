#include "home/serial.h"

#include "generated/wram.h"
#include "home/printer.h"
#include "mem.h"
/* >>> factory statics */
#include "home/menus.h"
#include "home/print_text.h"
#include "home/sound.h"

#define MUSIC_STOP 0x00u
#define TransmissionErrorText 0x0055u

#include "home/serial.h"

#include "generated/wram.h"
#include "mem.h"
/* <<< factory statics */

#define rSB 0xFF01u
#define rSC 0xFF02u
#define rIF 0xFF0Fu
#define rIE 0xFFFFu
#define SC_EXTERNAL 0x00u
#define SC_INTERNAL 0x01u
#define SC_START 0x80u
#define IE_SERIAL 0x08u

/* serial.asm:2-36. Driven at ~240 Hz by TimerHandler. The two opcode paths are
 * mutually exclusive ($29 = begin a transfer, $12 = check for timeout); any other
 * value returns immediately. Registers b/c/d/e are untouched on every path. */
void SerialTimerHandler(void)
{
	uint8_t op = gb_read8(wSerialOp_ADDR);
	if (op == 0x29u) {
		/* `ldh a, [rSC] / add a / ret c`: bit 7 of rSC (transfer in progress)
		 * lands in carry, so a transfer already active exits early. */
		if (gb_read8(rSC) & 0x80u)
			return;
		gb_write8(rSC, SC_INTERNAL);
		gb_write8(rSC, (uint8_t)(SC_START | SC_INTERNAL));
		return;
	}
	if (op != 0x12u)
		return;

	/* serial.asm:18-36. If the serial counter advanced since the last call the
	 * transfer is progressing and the timeout counter resets; otherwise it counts
	 * up and sets wSerialFlags bit 7 once it reaches 4 (~60 Hz). */
	if (gb_read8(wSerialCounter_ADDR) != gb_read8(wSerialCounter2_ADDR)) {
		gb_write8(wSerialCounter2_ADDR, gb_read8(wSerialCounter_ADDR));
		gb_write8(wSerialTimeoutCounter_ADDR, 0);
		return;
	}
	gb_write8(wSerialCounter2_ADDR, gb_read8(wSerialCounter_ADDR));
	uint8_t timeout = (uint8_t)(gb_read8(wSerialTimeoutCounter_ADDR) + 1u);
	if (timeout < 4u) {
		gb_write8(wSerialTimeoutCounter_ADDR, timeout);
		return;
	}
	gb_write8(wSerialTimeoutCounter_ADDR, timeout);
	gb_write8(wSerialFlags_ADDR, (uint8_t)(gb_read8(wSerialFlags_ADDR) | 0x80u));
}

Func0cc5Result Func_0cc5(uint8_t a, uint8_t b, uint8_t c, uint8_t e)
{
	if (a == 0) {
		if (gb_read8(wSerialRecvCounter_ADDR) == 0)
			return (Func0cc5Result){0, b, c, e, 0x80u};
		gb_write8(wSerialRecvCounter_ADDR, 0);
		e = 0x12u;
		if (gb_read8(wSerialRecvBuf_ADDR) != 0x29u)
			return (Func0cc5Result){0, b, c, e, 0x90u};
	} else {
		gb_write8(rSB, 0x29u);
		gb_write8(rSC, SC_INTERNAL);
		gb_write8(rSC, (uint8_t)(SC_START | SC_INTERNAL));
		while (gb_read8(wSerialRecvCounter_ADDR) == 0)
			;
		gb_write8(wSerialRecvCounter_ADDR, 0);
		e = 0x29u;
		if (gb_read8(wSerialRecvBuf_ADDR) != 0x12u)
			return (Func0cc5Result){0, b, c, e, 0x90u};
	}

	gb_write8(wSerialSendBufIndex_ADDR, 0);
	gb_write8(wcb80_ADDR, 0);
	gb_write8(wSerialSendBufToggle_ADDR, 0);
	gb_write8(wSerialSendSave_ADDR, 0);
	gb_write8(wcba3_ADDR, 0);
	gb_write8(wSerialRecvIndex_ADDR, 0);
	gb_write8(wSerialRecvCounter_ADDR, 0);
	gb_write8(wSerialLastReadCA_ADDR, 0);
	/* e==$12 (no delay loop): `cp $29` leaves Z clear -> f=$10. e==$29 (delay
	 * loop runs): the loop's last `or b` leaves Z set (bc wrapped to 0),
	 * untouched by the `scf` that follows -> f=$90. */
	uint8_t f = 0x10u;
	if (e == 0x29u) {
		for (uint16_t n = 0x0800u; n != 0; n--)
			;
		b = 0;
		c = 0;
		f = 0x90u;
	}
	gb_write8(wSerialOp_ADDR, e);
	return (Func0cc5Result){e, b, c, e, f};
}

void SerialHandler(void)
{
	if (gb_read8(wPrinterPacketSequence_ADDR) != 0) {
		ExecutePrinterPacketSequence(gb_read8(wPrinterPacketSequence_ADDR), 0, 0);
	} else if (gb_read8(wSerialOp_ADDR) != 0) {
		uint8_t rb = gb_read8(rSB);
		SerialHandleRecv(rb, 0);
		SerialHandleSendResult send = SerialHandleSend(0, 0);
		while (gb_read8(rSC) & 0x80u)
			;
		gb_write8(rSB, send.a);
		if (gb_read8(wSerialOp_ADDR) != 0x29u)
			gb_write8(rSC, (uint8_t)(SC_START | SC_EXTERNAL));
	} else {
		gb_write8(wSerialRecvCounter_ADDR, 1);
		gb_write8(wSerialRecvBuf_ADDR, gb_read8(rSB));
		gb_write8(rSB, 0xACu);
		if (gb_read8(wSerialRecvBuf_ADDR) != 0x12u)
			gb_write8(rSC, (uint8_t)(SC_START | SC_EXTERNAL));
	}
	gb_write8(wSerialCounter_ADDR, (uint8_t)(gb_read8(wSerialCounter_ADDR) + 1u));
}

SerialHandleRecvResult SerialHandleRecv(uint8_t a, uint8_t d)
{
	uint8_t e = (uint8_t)(gb_read8(wSerialLastReadCA_ADDR) - 1u);
	if (e == 0) {
		gb_write8(wSerialLastReadCA_ADDR, 0);
		a = (uint8_t)~a;
	} else {
		if (a == 0xACu)
			return (SerialHandleRecvResult){a, d, e, wSerialLastReadCA_ADDR};
		if (a == 0xCAu) {
			gb_write8(wSerialLastReadCA_ADDR, (uint8_t)(gb_read8(wSerialLastReadCA_ADDR) + 1u));
			return (SerialHandleRecvResult){a, d, e, wSerialLastReadCA_ADDR};
		}
		if (a == 0x00u || a == 0xFFu) {
			gb_write8(wSerialFlags_ADDR, (uint8_t)(gb_read8(wSerialFlags_ADDR) | 0x40u));
			return (SerialHandleRecvResult){a, d, e, wSerialFlags_ADDR};
		}
		a = (uint8_t)(a ^ 0xC0u);
	}

	e = gb_read8(wSerialRecvIndex_ADDR);
	uint8_t full_check = (uint8_t)((gb_read8(wcba3_ADDR) - 1u) & 0x1Fu);
	if (full_check == e) {
		gb_write8(wSerialFlags_ADDR, (uint8_t)(gb_read8(wSerialFlags_ADDR) | 0x01u));
		return (SerialHandleRecvResult){a, d, e, wSerialFlags_ADDR};
	}
	d = 0;
	gb_write8((uint16_t)(wSerialRecvBuf_ADDR + e), a);
	gb_write8(wSerialRecvIndex_ADDR, (uint8_t)((e + 1u) & 0x1Fu));
	gb_write8(wSerialRecvCounter_ADDR, (uint8_t)(gb_read8(wSerialRecvCounter_ADDR) + 1u));
	gb_write8(wSerialFlags_ADDR, 0);
	return (SerialHandleRecvResult){0, d, e, wSerialRecvCounter_ADDR};
}

SerialHandleSendResult SerialHandleSend(uint8_t d, uint8_t e)
{
	if (gb_read8(wSerialSendSave_ADDR) != 0) {
		uint8_t a = gb_read8(wSerialSendSave_ADDR);
		gb_write8(wSerialSendSave_ADDR, 0);
		return (SerialHandleSendResult){a, d, e, wSerialSendSave_ADDR};
	}
	if (gb_read8(wSerialSendBufToggle_ADDR) == 0)
		return (SerialHandleSendResult){0xACu, d, e, wSerialSendBufToggle_ADDR};

	gb_write8(wSerialSendBufToggle_ADDR, (uint8_t)(gb_read8(wSerialSendBufToggle_ADDR) - 1u));
	e = gb_read8(wSerialSendBufIndex_ADDR);
	d = 0;
	uint16_t hl = (uint16_t)(wSerialSendBuf_ADDR + e);
	gb_write8(wSerialSendBufIndex_ADDR, (uint8_t)((e + 1u) & 0x1Fu));
	uint8_t a = (uint8_t)(gb_read8(hl) ^ 0xC0u);
	if (a == 0xACu || a == 0xCAu || a == 0xFFu || a == 0x00u) {
		a = (uint8_t)~(a ^ 0xC0u);
		gb_write8(wSerialSendSave_ADDR, a);
		a = 0xCAu;
	}
	return (SerialHandleSendResult){a, d, e, hl};
}

uint8_t SerialSendByte(uint8_t a)
{
	uint8_t e;
	for (;;) {
		e = gb_read8(wcb80_ADDR);
		uint8_t chk = (uint8_t)((gb_read8(wSerialSendBufIndex_ADDR) - 1u) & 0x1Fu);
		if (chk != e)
			break;
	}
	gb_write8(wcb80_ADDR, (uint8_t)((e + 1u) & 0x1Fu));
	gb_write8((uint16_t)(wSerialSendBuf_ADDR + e), a);
	uint8_t before = gb_read8(wSerialSendBufToggle_ADDR);
	uint8_t after = (uint8_t)(before + 1u);
	gb_write8(wSerialSendBufToggle_ADDR, after);
	uint8_t f = 0;
	if (after == 0)
		f |= 0x80u;
	if ((before & 0x0Fu) == 0x0Fu)
		f |= 0x20u;
	return f;
}

SerialRecvReadyResult Func_0e32(void)
{
	uint8_t a = gb_read8(wSerialRecvCounter_ADDR);
	return (SerialRecvReadyResult){a, a ? 0x10u : 0x80u};
}

SerialByteResult SerialRecvByte(void)
{
	if (gb_read8(wSerialRecvCounter_ADDR) == 0) {
		uint8_t a = gb_read8(wSerialFlags_ADDR);
		if (a != 0)
			return (SerialByteResult){a, 0x00u};
		return (SerialByteResult){a, 0x90u};
	}
	gb_write8(wSerialRecvCounter_ADDR, (uint8_t)(gb_read8(wSerialRecvCounter_ADDR) - 1u));
	uint8_t idx = gb_read8(wcba3_ADDR);
	uint8_t a = gb_read8((uint16_t)(wSerialRecvBuf_ADDR + idx));
	gb_write8(wcba3_ADDR, (uint8_t)((idx + 1u) & 0x1Fu));
	return (SerialByteResult){a, a ? 0x00u : 0x80u};
}

SerialExchangeResult SerialExchangeBytes(uint8_t c, uint16_t hl, uint16_t de)
{
	uint8_t b = c;
	uint8_t a;
	for (;;) {
		int send_gate = (b < c) || (uint8_t)(b - c) < 0x1Fu;
		if (send_gate && c != 0) {
			uint8_t byte = gb_read8(hl);
			hl = (uint16_t)(hl + 1u);
			SerialSendByte(byte);
			c--;
		}
		if (b != 0) {
			SerialByteResult r = SerialRecvByte();
			if (!(r.f & 0x10u)) {
				gb_write8(de, r.a);
				de = (uint16_t)(de + 1u);
				b--;
			}
		}
		a = gb_read8(wSerialFlags_ADDR);
		if (a != 0)
			return (SerialExchangeResult){a, b, c, 0x10u, hl, de};
		if (c == 0 && b == 0)
			return (SerialExchangeResult){0, 0, 0, 0x80u, hl, de};
	}
}

uint8_t Func_0e8e(void)
{
	ClearSerialData();
	gb_write8(rSB, 0x12u);
	gb_write8(rSC, (uint8_t)(SC_START | SC_EXTERNAL));
	gb_write8(rIF, (uint8_t)(gb_read8(rIF) & (uint8_t)~IE_SERIAL));
	uint8_t ie = (uint8_t)(gb_read8(rIE) | IE_SERIAL);
	gb_write8(rIE, ie);
	return ie;
}

void ResetSerial(void)
{
	gb_write8(rIE, (uint8_t)(gb_read8(rIE) & (uint8_t)~IE_SERIAL));
	gb_write8(rSB, 0);
	gb_write8(rSC, 0);
	ClearSerialData();
}

void ClearSerialData(void)
{
	for (uint16_t addr = wSerialOp_ADDR; addr != wSerialEnd_ADDR; addr++)
		gb_write8(addr, 0);
}

SerialSendBytesResult SerialSendBytes(uint16_t hl, uint16_t bc)
{
	uint32_t n = bc ? bc : 0x10000u;
	for (;;) {
		uint8_t byte = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		SerialSendByte(byte);
		uint8_t flags = gb_read8(wSerialFlags_ADDR);
		if (flags != 0)
			return (SerialSendBytesResult){flags, 0x10u, hl};
		if (--n == 0)
			return (SerialSendBytesResult){0, 0x80u, hl};
	}
}

SerialRecvBytesResult SerialRecvBytes(uint16_t hl, uint16_t bc)
{
	uint32_t n = bc ? bc : 0x10000u;
	for (;;) {
		SerialByteResult r;
		do {
			r = SerialRecvByte();
		} while (r.f & 0x10u);
		gb_write8(hl, r.a);
		hl = (uint16_t)(hl + 1u);
		uint8_t flags = gb_read8(wSerialFlags_ADDR);
		if (flags != 0)
			return (SerialRecvBytesResult){flags, 0x10u, hl};
		if (--n == 0)
			return (SerialRecvBytesResult){0, 0x80u, hl};
	}
}

/* >>> factory DuelTransmissionError */
/* serial.asm:523-540. The tail (`ld sp, hl` from wDuelReturnAddress, then
 * `ret`) unwinds the real GB stack straight back to the outer duel loop's
 * saved frame instead of returning to this routine's own caller; that has
 * no C equivalent and no observable register contract of its own. */
void DuelTransmissionError(void)
{
	LoadTxRam3(gb_read8(wSerialFlags_ADDR));
	(void)DrawWideTextBox_WaitForInput(TransmissionErrorText);
	gb_write8(wDuelResult_ADDR, (uint8_t)-1);
	PlaySong(MUSIC_STOP);
	ResetSerial();
}
/* <<< factory DuelTransmissionError */

/* >>> factory SerialRecv8Bytes */
/* serial.asm:656-689. SerialRecvBytes fills wTempSerialBuf (carry jp's away
 * to DuelTransmissionError); the two push de / pop pairs then map buffer
 * words onto registers. pop af reads f's low nibble as zero on hardware,
 * hence the mask. */
SerialRecv8BytesResult SerialRecv8Bytes(void)
{
	SerialRecvBytesResult r = SerialRecvBytes(wTempSerialBuf_ADDR, 0x0008u);
	if (r.f & 0x10u)
		DuelTransmissionError();
	uint16_t p = wTempSerialBuf_ADDR;
	return (SerialRecv8BytesResult){
		gb_read8(p + 1u),
		gb_read8(p) & 0xF0u,
		gb_read8(p + 7u),
		gb_read8(p + 6u),
		gb_read8(p + 5u),
		gb_read8(p + 4u),
		(uint16_t)(gb_read8(p + 3u) << 8 | gb_read8(p + 2u)),
	};
}
/* <<< factory SerialRecv8Bytes */
