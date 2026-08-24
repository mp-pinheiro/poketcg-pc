#ifndef POKETCG_HOME_IR_CORE_H
#define POKETCG_HOME_IR_CORE_H

#include <stdint.h>

/* >>> factory StoreRegistersInIRDataBuffer */
void StoreRegistersInIRDataBuffer(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t *hl);
/* <<< factory StoreRegistersInIRDataBuffer */
/* >>> factory LoadRegistersFromIRDataBuffer */
typedef struct { uint8_t a, f, b, c, d, e; uint16_t hl; } IRRegisterState;
IRRegisterState LoadRegistersFromIRDataBuffer(void);
/* <<< factory LoadRegistersFromIRDataBuffer */
/* >>> factory ReturnZFlagUnsetAndCarryFlagSet */
typedef struct {
	uint8_t a;
	uint8_t f;
} ReturnZFlagUnsetAndCarryFlagSetResult;

ReturnZFlagUnsetAndCarryFlagSetResult ReturnZFlagUnsetAndCarryFlagSet(void);
/* <<< factory ReturnZFlagUnsetAndCarryFlagSet */
/* >>> factory TransmitIRBit */
typedef struct {
	uint8_t a;
	uint8_t f;
} TransmitIRBitResult;
TransmitIRBitResult TransmitIRBit(uint8_t a, uint8_t f, uint16_t hl);
/* <<< factory TransmitIRBit */
/* >>> factory ReturnZFlagUnsetAndCarryFlagSet2 */
ReturnZFlagUnsetAndCarryFlagSetResult ReturnZFlagUnsetAndCarryFlagSet2(void);
/* <<< factory ReturnZFlagUnsetAndCarryFlagSet2 */
/* >>> factory ReceiveByteThroughIR */
typedef struct { uint8_t a; uint8_t f; } ReceiveByteThroughIRResult;
ReceiveByteThroughIRResult ReceiveByteThroughIR(void);
/* <<< factory ReceiveByteThroughIR */
/* >>> factory ReceiveByteThroughIR_ZeroIfUnsuccessful */
ReceiveByteThroughIRResult ReceiveByteThroughIR_ZeroIfUnsuccessful(void);
/* <<< factory ReceiveByteThroughIR_ZeroIfUnsuccessful */
/* >>> factory ReceiveNBytesToHLThroughIR */
ReceiveByteThroughIRResult ReceiveNBytesToHLThroughIR(uint16_t hl, uint8_t c);
/* <<< factory ReceiveNBytesToHLThroughIR */
/* >>> factory TransmitByteThroughIR */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; uint16_t de; uint16_t bc; } TransmitByteThroughIRResult;
TransmitByteThroughIRResult TransmitByteThroughIR(uint8_t a, uint16_t hl_in, uint16_t de, uint16_t bc);
/* <<< factory TransmitByteThroughIR */
/* >>> factory Func_1971e */
typedef struct { uint8_t a; uint8_t f; } Func_1971eResult;
Func_1971eResult Func_1971e(void);
/* <<< factory Func_1971e */
#endif /* POKETCG_HOME_IR_CORE_H */
