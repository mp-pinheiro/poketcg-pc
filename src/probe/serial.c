#include "home/serial.h"
#include "probe.h"
#include "mem.h"

static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)((uint16_t)hi << 8 | lo);
}

static void adapt_SerialTimerHandler(ProbeState *s)
{
	(void)s;
	SerialTimerHandler();
}

static void adapt_Func_0cc5(ProbeState *s)
{
	Func0cc5Result r = Func_0cc5(s->a, s->b, s->c, s->e);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->e = r.e;
	s->f = r.f;
}

static void adapt_SerialHandler(ProbeState *s)
{
	(void)s;
	SerialHandler();
}

static void adapt_SerialHandleRecv(ProbeState *s)
{
	SerialHandleRecvResult r = SerialHandleRecv(s->a, s->d);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_SerialHandleSend(ProbeState *s)
{
	SerialHandleSendResult r = SerialHandleSend(s->d, s->e);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

/* Exit carry is entry carry passed through untouched; SerialSendByte only
 * returns the freshly computed Z/H bits (see serial.h), so the adapter ORs
 * them onto s->f's own C bit, same as load_deck.c's LoadDeck adapter. */
static void adapt_SerialSendByte(ProbeState *s)
{
	uint8_t zh = SerialSendByte(s->a);
	s->f = (uint8_t)(zh | (s->f & 0x10u));
}

static void adapt_Func_0e32(ProbeState *s)
{
	SerialRecvReadyResult r = Func_0e32();
	s->a = r.a;
	s->f = r.f;
}

static void adapt_SerialRecvByte(ProbeState *s)
{
	SerialByteResult r = SerialRecvByte();
	s->a = r.a;
	s->f = r.f;
}

static void adapt_SerialExchangeBytes(ProbeState *s)
{
	SerialExchangeResult r = SerialExchangeBytes(s->c, s->hl, pair(s->d, s->e));
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_Func_0e8e(ProbeState *s)
{
	s->a = Func_0e8e();
}

static void adapt_ResetSerial(ProbeState *s)
{
	(void)s;
	ResetSerial();
}

static void adapt_ClearSerialData(ProbeState *s)
{
	(void)s;
	ClearSerialData();
}

static void adapt_SerialSendBytes(ProbeState *s)
{
	SerialSendBytesResult r = SerialSendBytes(s->hl, pair(s->b, s->c));
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_SerialRecvBytes(ProbeState *s)
{
	SerialRecvBytesResult r = SerialRecvBytes(s->hl, pair(s->b, s->c));
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}

/* >>> factory DuelTransmissionError */
static void adapt_DuelTransmissionError(ProbeState *s)
{
	(void)s;
	DuelTransmissionError();
}
/* <<< factory DuelTransmissionError */

/* >>> factory SerialRecv8Bytes */
static void adapt_SerialRecv8Bytes(ProbeState *s)
{
	SerialRecv8BytesResult r = SerialRecv8Bytes();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory SerialRecv8Bytes */

/* >>> factory ExchangeRNG */
static void adapt_ExchangeRNG(ProbeState *s)
{
	ExchangeRNGResult r = ExchangeRNG(s->b, s->c, (uint16_t)(s->d << 8 | s->e), s->hl);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory ExchangeRNG */

/* >>> factory SerialSend8Bytes */
static void adapt_SerialSend8Bytes(ProbeState *s)
{
	SerialSend8Bytes(s->a, s->f, s->b, s->c, (uint16_t)(s->d << 8 | s->e), s->hl);
}
/* <<< factory SerialSend8Bytes */

/* >>> factory LinkOpponentTurnFrameFunction */
static void adapt_LinkOpponentTurnFrameFunction(ProbeState *s)
{
	LinkOppTurnResult r = LinkOpponentTurnFrameFunction();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory LinkOpponentTurnFrameFunction */

/* >>> factory SetOppAction_SerialSendDuelData */
static void adapt_SetOppAction_SerialSendDuelData(ProbeState *s)
{
	SetOppActionSerialSendResult r =
		SetOppAction_SerialSendDuelData(s->a, (uint16_t)(s->d << 8 | s->e));
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory SetOppAction_SerialSendDuelData */

/* >>> factory SerialRecvDuelData */
static void adapt_SerialRecvDuelData(ProbeState *s)
{
	SerialRecvDuelDataResult r = SerialRecvDuelData(s->b, s->c, (uint16_t)(s->d << 8 | s->e), s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory SerialRecvDuelData */

/* >>> factory UnreferencedGoToSerialReturnAddress */
static void adapt_UnreferencedGoToSerialReturnAddress(ProbeState *s)
{
	UnreferencedGoToSerialReturnAddressResult r = UnreferencedGoToSerialReturnAddress(s->hl);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory UnreferencedGoToSerialReturnAddress */

const ProbeEntry probe_entries_serial[] = {
	{ "SerialTimerHandler", adapt_SerialTimerHandler },
	{ "Func_0cc5", adapt_Func_0cc5 },
	{ "SerialHandler", adapt_SerialHandler },
	{ "SerialHandleRecv", adapt_SerialHandleRecv },
	{ "SerialHandleSend", adapt_SerialHandleSend },
	{ "SerialSendByte", adapt_SerialSendByte },
	{ "Func_0e32", adapt_Func_0e32 },
	{ "SerialRecvByte", adapt_SerialRecvByte },
	{ "SerialExchangeBytes", adapt_SerialExchangeBytes },
	{ "Func_0e8e", adapt_Func_0e8e },
	{ "ResetSerial", adapt_ResetSerial },
	{ "ClearSerialData", adapt_ClearSerialData },
	{ "SerialSendBytes", adapt_SerialSendBytes },
	{ "SerialRecvBytes", adapt_SerialRecvBytes },
	{ "DuelTransmissionError", adapt_DuelTransmissionError },
	{ "SerialRecv8Bytes", adapt_SerialRecv8Bytes },
	{ "ExchangeRNG", adapt_ExchangeRNG },
	{ "SerialSend8Bytes", adapt_SerialSend8Bytes },
	{ "LinkOpponentTurnFrameFunction", adapt_LinkOpponentTurnFrameFunction },
	{ "SetOppAction_SerialSendDuelData", adapt_SetOppAction_SerialSendDuelData },
	{ "SerialRecvDuelData", adapt_SerialRecvDuelData },
	{ "UnreferencedGoToSerialReturnAddress", adapt_UnreferencedGoToSerialReturnAddress },
	{ NULL, NULL },
};
