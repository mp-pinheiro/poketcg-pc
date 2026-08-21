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
#endif /* POKETCG_HOME_IR_CORE_H */
