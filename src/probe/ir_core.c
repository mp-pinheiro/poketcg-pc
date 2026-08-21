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

const ProbeEntry probe_entries_ir_core[] = {
	{ "StoreRegistersInIRDataBuffer", adapt_StoreRegistersInIRDataBuffer },
	{ "LoadRegistersFromIRDataBuffer", adapt_LoadRegistersFromIRDataBuffer },
	{ "ReturnZFlagUnsetAndCarryFlagSet", adapt_ReturnZFlagUnsetAndCarryFlagSet },
	{ "TransmitIRBit", adapt_TransmitIRBit },
	{ NULL, NULL },
};
