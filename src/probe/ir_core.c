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

/* >>> factory ReceiveByteThroughIR_ZeroIfUnsuccessful */
static void adapt_ReceiveByteThroughIR_ZeroIfUnsuccessful(ProbeState *s)
{
	ReceiveByteThroughIRResult r = ReceiveByteThroughIR_ZeroIfUnsuccessful();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ReceiveByteThroughIR_ZeroIfUnsuccessful */

/* >>> factory ReceiveNBytesToHLThroughIR */
static void adapt_ReceiveNBytesToHLThroughIR(ProbeState *s)
{
	ReceiveByteThroughIRResult r = ReceiveNBytesToHLThroughIR(s->hl, s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ReceiveNBytesToHLThroughIR */

/* >>> factory TransmitByteThroughIR */
static void adapt_TransmitByteThroughIR(ProbeState *s)
{
	TransmitByteThroughIRResult r = TransmitByteThroughIR(s->a, s->hl, (uint16_t)(((uint16_t)s->d << 8) | s->e), (uint16_t)(((uint16_t)s->b << 8) | s->c));
	s->a = r.a; s->f = r.f; s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8); s->e = (uint8_t)r.de;
	s->b = (uint8_t)(r.bc >> 8); s->c = (uint8_t)r.bc;
}
/* <<< factory TransmitByteThroughIR */

/* >>> factory Func_1971e */
static void adapt_Func_1971e(ProbeState *s)
{
	Func_1971eResult r = Func_1971e();
	s->a = r.a; s->f = r.f;
}
/* <<< factory Func_1971e */

/* >>> factory TransmitNBytesFromHLThroughIR */
static void adapt_TransmitNBytesFromHLThroughIR(ProbeState *s)
{
	TransmitNBytesFromHLThroughIRResult r = TransmitNBytesFromHLThroughIR(s->hl, s->c);
	s->a = r.a; s->f = r.f; s->hl = r.hl;
}
/* <<< factory TransmitNBytesFromHLThroughIR */

/* >>> factory Func_19705 */
static void adapt_Func_19705(ProbeState *s)
{
	Func_19705Result r = Func_19705();
	s->a = r.a; s->f = r.f;
}
/* <<< factory Func_19705 */

/* >>> factory TransmitIRDataBuffer */
static void adapt_TransmitIRDataBuffer(ProbeState *s)
{
	TransmitIRDataBufferResult r = TransmitIRDataBuffer();
	s->a = r.a; s->f = r.f;
}
/* <<< factory TransmitIRDataBuffer */

/* >>> factory ReceiveIRDataBuffer */
static void adapt_ReceiveIRDataBuffer(ProbeState *s)
{
	ReceiveIRDataBufferResult r = ReceiveIRDataBuffer();
	s->a = r.a; s->f = r.f;
}
/* <<< factory ReceiveIRDataBuffer */

/* >>> factory ClearRP */
static void adapt_ClearRP(ProbeState *s)
{
	ClearRP();
	s->a = 0x00u;
}
/* <<< factory ClearRP */

/* >>> factory StartIRCommunications */
static void adapt_StartIRCommunications(ProbeState *s)
{
	(void)s;
	StartIRCommunications();
}
/* <<< factory StartIRCommunications */

/* >>> factory CloseIRCommunications */
static void adapt_CloseIRCommunications(ProbeState *s)
{
	(void)s;
	CloseIRCommunications();
}
/* <<< factory CloseIRCommunications */

/* >>> factory SafelyCloseIRCommunications */
static void adapt_SafelyCloseIRCommunications(ProbeState *s)
{
	(void)s;
	SafelyCloseIRCommunications();
}
/* <<< factory SafelyCloseIRCommunications */

/* >>> factory TrySendIRRequest */
static void adapt_TrySendIRRequest(ProbeState *s)
{
	TrySendIRRequestResult result = TrySendIRRequest();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory TrySendIRRequest */

/* >>> factory TransmitRegistersThroughIR */
static void adapt_TransmitRegistersThroughIR(ProbeState *s)
{
	TransmitRegistersThroughIRResult r = TransmitRegistersThroughIR(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory TransmitRegistersThroughIR */

/* >>> factory RequestCloseIRCommunication */
static void adapt_RequestCloseIRCommunication(ProbeState *s)
{
	RequestCloseIRCommunicationResult r = RequestCloseIRCommunication();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory RequestCloseIRCommunication */

/* >>> factory RequestDataTransmissionThroughIR */
static void adapt_RequestDataTransmissionThroughIR(ProbeState *s)
{
	RequestDataTransmissionThroughIRResult result = RequestDataTransmissionThroughIR(s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	}
/* <<< factory RequestDataTransmissionThroughIR */

const ProbeEntry probe_entries_ir_core[] = {
	{ "StoreRegistersInIRDataBuffer", adapt_StoreRegistersInIRDataBuffer },
	{ "LoadRegistersFromIRDataBuffer", adapt_LoadRegistersFromIRDataBuffer },
	{ "ReturnZFlagUnsetAndCarryFlagSet", adapt_ReturnZFlagUnsetAndCarryFlagSet },
	{ "TransmitIRBit", adapt_TransmitIRBit },
	{ "ReturnZFlagUnsetAndCarryFlagSet2", adapt_ReturnZFlagUnsetAndCarryFlagSet2 },
	{ "ReceiveByteThroughIR", adapt_ReceiveByteThroughIR },
	{ "ReceiveByteThroughIR_ZeroIfUnsuccessful", adapt_ReceiveByteThroughIR_ZeroIfUnsuccessful },
	{ "ReceiveNBytesToHLThroughIR", adapt_ReceiveNBytesToHLThroughIR },
	{ "TransmitByteThroughIR", adapt_TransmitByteThroughIR },
	{ "Func_1971e", adapt_Func_1971e },
	{ "TransmitNBytesFromHLThroughIR", adapt_TransmitNBytesFromHLThroughIR },
	{ "Func_19705", adapt_Func_19705 },
	{ "TransmitIRDataBuffer", adapt_TransmitIRDataBuffer },
	{ "ReceiveIRDataBuffer", adapt_ReceiveIRDataBuffer },
	{ "ClearRP", adapt_ClearRP },
	{ "StartIRCommunications", adapt_StartIRCommunications },
	{ "CloseIRCommunications", adapt_CloseIRCommunications },
	{ "SafelyCloseIRCommunications", adapt_SafelyCloseIRCommunications },
	{ "TrySendIRRequest", adapt_TrySendIRRequest },
	{ "TransmitRegistersThroughIR", adapt_TransmitRegistersThroughIR },
	{ "RequestCloseIRCommunication", adapt_RequestCloseIRCommunication },
	{ "RequestDataTransmissionThroughIR", adapt_RequestDataTransmissionThroughIR },
	{ NULL, NULL },
};
