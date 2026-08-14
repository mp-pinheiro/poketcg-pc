#ifndef POKETCG_HOME_SERIAL_H
#define POKETCG_HOME_SERIAL_H

#include <stdint.h>

/* poketcg/src/home/serial.asm */

void SerialTimerHandler(void);

/* Func_0cc5:: serial.asm:38-95. Entry a selects the branch: a==0 polls
 * wSerialRecvCounter once; a!=0 kicks an SC_INTERNAL transfer and spins on
 * it -- no ISR ever runs mid-call, so that branch needs
 * wSerialRecvCounter pre-seeded nonzero or the call never returns. hl
 * always ends at wSerialRecvCounter's address regardless of case
 * (residue, omitted). b/c are preserved except on the $29-success path,
 * where a 2048-iteration delay loop leaves them 0. */
typedef struct {
	uint8_t a, b, c, e, f;
} Func0cc5Result;
Func0cc5Result Func_0cc5(uint8_t a, uint8_t b, uint8_t c, uint8_t e);

/* SerialHandler:: serial.asm:97-147. push af/hl/de/bc at entry, popped
 * before `reti`, so every register is preserved on every path. The
 * `.wait_for_completion` spin on rSC bit 7 only runs when wSerialOp!=0 --
 * seed rSC with bit 7 clear there or the call never returns. */
void SerialHandler(void);

/* SerialHandleRecv:: serial.asm:151-209. hl exits at one of three fixed
 * WRAM cells depending on branch (not residue: it varies with the case).
 * d is 0 only on the buffer-write path, entry-preserved otherwise. f is
 * omitted: no callsite ever reads it, and deriving it exactly requires
 * threading entry carry through `dec e`/`cpl`, neither of which SET
 * touches. */
typedef struct {
	uint8_t a, d, e;
	uint16_t hl;
} SerialHandleRecvResult;
SerialHandleRecvResult SerialHandleRecv(uint8_t a, uint8_t d);

/* SerialHandleSend:: serial.asm:213-260. hl lands on wSerialSendSave/
 * wSerialSendBufToggle (fixed) on the two no-data paths, or
 * wSerialSendBuf+index (WRAM-dependent) on the send path. d is 0 only on
 * the send path, entry-preserved otherwise; e likewise holds
 * wSerialSendBufIndex's pre-increment value only there. f omitted: no
 * callsite reads it. */
typedef struct {
	uint8_t a, d, e;
	uint16_t hl;
} SerialHandleSendResult;
SerialHandleSendResult SerialHandleSend(uint8_t d, uint8_t e);

/* SerialSendByte:: serial.asm:263-291. a/b/c/d/e/hl round-trip through
 * push/pop verbatim. `.loop_wait` only advances once the ring isn't full
 * ((wSerialSendBufIndex-1)&$1F != wcb80); nothing drains it mid-call, so
 * a case must satisfy that at entry or the call never returns. The only
 * flag-setter after the mid-routine `pop af` is `inc [hl]` on
 * wSerialSendBufToggle, which never touches C -- so exit carry is a pure
 * passthrough of entry carry, and the adapter ORs it onto this routine's
 * returned Z/H bits. */
uint8_t SerialSendByte(uint8_t a);

/* Func_0e32:: serial.asm:294-299. No prologue; b/c/d/e/hl never referenced
 * (preserved). Exit a is wSerialRecvCounter's raw value; carry is set iff it
 * is nonzero (LinkOpponentTurnFrameFunction branches on this). */
typedef struct {
	uint8_t a, f;
} SerialRecvReadyResult;
SerialRecvReadyResult Func_0e32(void);

/* SerialRecvByte:: serial.asm:302-332. hl is pushed once at entry and
 * popped at every exit; de is pushed/popped around the only path that
 * touches it -- so b/c/d/e/hl are all preserved regardless of branch.
 * Exit carry is set iff no byte was queued (wSerialRecvCounter==0 and
 * wSerialFlags==0), which is true on every call here unless a case
 * pre-seeds wSerialRecvCounter/wSerialRecvBuf/wcba3 as already arrived. */
typedef struct {
	uint8_t a, f;
} SerialByteResult;
SerialByteResult SerialRecvByte(void);

/* SerialExchangeBytes:: serial.asm:335-369. b is a local iteration
 * counter (b=c at entry) with no prologue to restore it, so exit b/c are
 * real derived values, not residue. Every receive that finds
 * wSerialRecvCounter==0 returns carry, so b can only reach 0 through
 * pre-seeded receive data -- see SerialRecvByte. */
typedef struct {
	uint8_t a, b, c, f;
	uint16_t hl, de;
} SerialExchangeResult;
SerialExchangeResult SerialExchangeBytes(uint8_t c, uint16_t hl, uint16_t de);

/* Func_0e8e:: serial.asm:372-384. Arms an SC_EXTERNAL transfer and
 * enables the serial interrupt. b/c/hl/f end at the same fixed constants
 * as ClearSerialData on every call (residue, omitted); d/e are never
 * touched. */
uint8_t Func_0e8e(void);

/* ResetSerial:: serial.asm:387-393, falls through into
 * ClearSerialData::397-407. a/b/c/hl/f end at fixed constants on every
 * call (residue, omitted); d/e are never touched. */
void ResetSerial(void);
void ClearSerialData(void);

/* SerialSendBytes:: serial.asm:410-428. `push bc` wraps the whole body
 * and is popped at both exits -- the live bc is decremented as the loop
 * counter, but the popped value is always the untouched entry bc, so
 * b/c/d/e are all preserved. bc==0 means 65536 per the zero-means-
 * maximum rule, but wSerialSendBuf only has 32 slots and nothing drains
 * it mid-call, so no count past ~31 can complete -- see
 * tests/cases/serial.py for the boundary rationale. */
typedef struct {
	uint8_t a, f;
	uint16_t hl;
} SerialSendBytesResult;
SerialSendBytesResult SerialSendBytes(uint16_t hl, uint16_t bc);

/* SerialRecvBytes:: serial.asm:431-454. Same push/pop-bc shape as
 * SerialSendBytes, so b/c/d/e are preserved. The asm's `halt` on an
 * empty queue can never wake up here (no ISR fires); every case must
 * pre-seed enough already-arrived bytes that SerialRecvByte never
 * returns carry. Same untestable bc==0 boundary as SerialSendBytes. */
typedef struct {
	uint8_t a, f;
	uint16_t hl;
} SerialRecvBytesResult;
SerialRecvBytesResult SerialRecvBytes(uint16_t hl, uint16_t bc);

/* >>> factory DuelTransmissionError */
void DuelTransmissionError(void);
/* <<< factory DuelTransmissionError */
/* >>> factory SerialRecv8Bytes */
/* SerialRecv8Bytes:: serial.asm:656-689. Receives 8 bytes into wTempSerialBuf
 * via SerialRecvBytes; on carry, jp's into DuelTransmissionError (control
 * leaves this routine). The bytes are loaded back out with two push de / pop
 * pairs: pop af yields a=buf[1], f=buf[0] (pop af reads f's low nibble as
 * zero on hardware), pop hl yields hl=buf[3]<<8|buf[2]; the third word stays
 * in de (d=buf[5], e=buf[4]) and the last in bc (c=buf[6], b=buf[7]). No
 * entry register is read and none are preserved. */
typedef struct {
	uint8_t a, f, b, c, d, e;
	uint16_t hl;
} SerialRecv8BytesResult;
SerialRecv8BytesResult SerialRecv8Bytes(void);
/* <<< factory SerialRecv8Bytes */
#endif
