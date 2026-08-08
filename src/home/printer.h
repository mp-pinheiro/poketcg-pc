#ifndef POKETCG_HOME_PRINTER_H
#define POKETCG_HOME_PRINTER_H

#include <stdint.h>

/* poketcg/src/home/printer.asm */

/* SendNextPrinterPacketByte:: printer.asm:184-203, falls through into
 * SendByteThroughSerialData::206-212. Sends the byte at wSerialDataPtr,
 * advances that pointer, and folds the byte into wPrinterPacketChecksum. a/hl
 * are always the fixed residue SendByteThroughSerialData/the checksum's
 * hl+1 leave behind, so both are omitted; b/c are never touched. Exit d/e are
 * the advanced pointer's high byte and the byte just sent -- not a pointer
 * pair (`ld e,a` overwrites e with the sent byte after the pointer writeback
 * already landed in WRAM). */
typedef struct {
	uint8_t d, e;
} SendNextPrinterPacketByteResult;
SendNextPrinterPacketByteResult SendNextPrinterPacketByte(void);

/* SendByteThroughSerialData:: printer.asm:206-212. Exit a is always
 * SC_START|SC_INTERNAL regardless of entry (residue, omitted); b/c/d/e/hl
 * are never touched. */
void SendByteThroughSerialData(uint8_t a);

/* ExecutePrinterPacketSequence:: printer.asm:80-179. One state-machine step;
 * entry a selects one of 12 local handlers via JumpToFunctionInTable (all 12
 * targets are local labels of this same routine, not unported engine code,
 * so this is a plain switch, not taxonomy #4). b/c are never touched. Entry
 * hl is always overwritten by the dispatch before any handler runs, and only
 * .GetStatusAndFinishSequence (a==12) never touches hl again afterward --
 * its exit hl would be the dispatch's own jump-table residue (a linked ROM
 * code address), so hl is left out entirely, uniformly across every case.
 * d/e are preserved on the checksum/dummy-byte/status handlers (8-12) and
 * overwritten with SendNextPrinterPacketByte's own exit on 1-5/6(has data)/7.
 * Real domain is a in [1,12]; SerialHandler only ever calls this when
 * wPrinterPacketSequence is already in that range. */
typedef struct {
	uint8_t a, d, e;
} ExecutePrinterPacketSequenceResult;
ExecutePrinterPacketSequenceResult ExecutePrinterPacketSequence(uint8_t a, uint8_t d, uint8_t e);

#endif
