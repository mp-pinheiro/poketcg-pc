#include "home/ir_core.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory StoreRegistersInIRDataBuffer */
static void adapt_StoreRegistersInIRDataBuffer(ProbeState *s)
{
	StoreRegistersInIRDataBuffer(s->a, s->f, s->b, s->c, s->d, s->e, &s->hl);
}
/* <<< factory StoreRegistersInIRDataBuffer */

/* >>> factory LoadRegistersFromIRDataBuffer */
static void adapt_LoadRegistersFromIRDataBuffer(ProbeState *s)
{
	IRRegisterState r = LoadRegistersFromIRDataBuffer();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory LoadRegistersFromIRDataBuffer */

/* >>> factory ReturnZFlagUnsetAndCarryFlagSet */
static void adapt_ReturnZFlagUnsetAndCarryFlagSet(ProbeState *s)
{
	ReturnZFlagUnsetAndCarryFlagSetResult result = ReturnZFlagUnsetAndCarryFlagSet();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory ReturnZFlagUnsetAndCarryFlagSet */

/* >>> factory TransmitIRBit */
static void adapt_TransmitIRBit(ProbeState *s)
{
	TransmitIRBitResult result = TransmitIRBit(s->a, s->f, s->hl);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory TransmitIRBit */

/* >>> factory ReturnZFlagUnsetAndCarryFlagSet2 */
static void adapt_ReturnZFlagUnsetAndCarryFlagSet2(ProbeState *s)
{
	ReturnZFlagUnsetAndCarryFlagSetResult result = ReturnZFlagUnsetAndCarryFlagSet2();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory ReturnZFlagUnsetAndCarryFlagSet2 */

/* >>> factory ReceiveByteThroughIR */
static void adapt_ReceiveByteThroughIR(ProbeState *s)
{
	ReceiveByteThroughIRResult r = ReceiveByteThroughIR();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ReceiveByteThroughIR */

const ProbeEntry probe_entries_ir_core[] = {
	{ "StoreRegistersInIRDataBuffer", adapt_StoreRegistersInIRDataBuffer },
	{ "LoadRegistersFromIRDataBuffer", adapt_LoadRegistersFromIRDataBuffer },
	{ "ReturnZFlagUnsetAndCarryFlagSet", adapt_ReturnZFlagUnsetAndCarryFlagSet },
	{ "TransmitIRBit", adapt_TransmitIRBit },
	{ "ReturnZFlagUnsetAndCarryFlagSet2", adapt_ReturnZFlagUnsetAndCarryFlagSet2 },
	{ "ReceiveByteThroughIR", adapt_ReceiveByteThroughIR },
	{ NULL, NULL },
};
