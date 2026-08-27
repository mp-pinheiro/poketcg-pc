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

/* >>> factory Func_1a14b */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} Func_1a14bResult;

Func_1a14bResult Func_1a14b(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory Func_1a14b */
/* >>> factory Func_1a025 */
void Func_1a025(void);
/* <<< factory Func_1a025 */
/* >>> factory ResetPrinterCommunicationSettings */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} ResetPrinterCommunicationSettingsResult;

ResetPrinterCommunicationSettingsResult ResetPrinterCommunicationSettings(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ResetPrinterCommunicationSettings */
/* >>> factory ClearPrinterGfxBuffer */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} ClearPrinterGfxBufferResult;

ClearPrinterGfxBufferResult ClearPrinterGfxBuffer(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ClearPrinterGfxBuffer */
/* >>> factory GetPrinterContrastSerialData */
typedef struct { uint8_t a; uint16_t hl; } GetPrinterContrastSerialDataResult;
GetPrinterContrastSerialDataResult GetPrinterContrastSerialData(void);
/* <<< factory GetPrinterContrastSerialData */
/* >>> factory PrepareForPrinterCommunications */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } PrepareForPrinterCommunicationsResult;
PrepareForPrinterCommunicationsResult PrepareForPrinterCommunications(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PrepareForPrinterCommunications */
/* >>> factory CheckDataCompression */
typedef struct { uint8_t a; uint8_t e; uint8_t f; uint16_t hl; } CheckDataCompressionResult;
CheckDataCompressionResult CheckDataCompression(uint8_t c, uint16_t hl);
/* <<< factory CheckDataCompression */
/* >>> factory CompressDataForPrinterSerialTransfer */
typedef struct { uint16_t bc; uint16_t hl; uint8_t d; uint8_t e; } CompressDataForPrinterSerialTransferResult;
CompressDataForPrinterSerialTransferResult CompressDataForPrinterSerialTransfer(void);
/* <<< factory CompressDataForPrinterSerialTransfer */
/* >>> factory LoadCardInfoForPrinter */
void LoadCardInfoForPrinter(uint8_t b, uint8_t c, uint16_t *hl);
/* <<< factory LoadCardInfoForPrinter */
/* >>> factory PrinterMenu_QuitPrint */
uint8_t PrinterMenu_QuitPrint(uint16_t w0);
/* <<< factory PrinterMenu_QuitPrint */
/* >>> factory DrawBottomCardInfoInSRAMGfxBuffer0 */
void DrawBottomCardInfoInSRAMGfxBuffer0(void);
/* <<< factory DrawBottomCardInfoInSRAMGfxBuffer0 */
/* >>> factory ShowPrinterTransmitting */
void ShowPrinterTransmitting(void);
/* <<< factory ShowPrinterTransmitting */
/* >>> factory SendPrinterPacket */
typedef struct { uint8_t a; uint8_t f; } SendPrinterPacketResult;
SendPrinterPacketResult SendPrinterPacket(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory SendPrinterPacket */
/* >>> factory ShowPrinterConnectionErrorScene */
typedef struct { uint8_t f; } ShowPrinterConnectionErrorSceneResult;
ShowPrinterConnectionErrorSceneResult ShowPrinterConnectionErrorScene(uint8_t a, uint8_t f, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ShowPrinterConnectionErrorScene */
/* >>> factory TryInitPrinterCommunications */
typedef struct {
	uint8_t a;
	uint8_t f;
} TryInitPrinterCommunicationsResult;

TryInitPrinterCommunicationsResult TryInitPrinterCommunications(void);
/* <<< factory TryInitPrinterCommunications */
/* >>> factory ShowPrinterIsNotConnected */
typedef struct { uint8_t f; } ShowPrinterIsNotConnectedResult;
ShowPrinterIsNotConnectedResult ShowPrinterIsNotConnected(uint8_t a, uint8_t f, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ShowPrinterIsNotConnected */
/* >>> factory HandlePrinterError */
typedef struct { uint8_t f; } HandlePrinterErrorResult;
HandlePrinterErrorResult HandlePrinterError(uint8_t f, uint8_t d, uint8_t e);
/* <<< factory HandlePrinterError */
/* >>> factory SendTilesToPrinter */
/* engine/link/printer.asm:391. Entry hl is the tile map; exit hl is the map
 * advanced past both rows (each row consumes `2 tiles` = 32 entries), a/f are
 * the packet result, and caller bc survives on the stack. */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } SendTilesToPrinterResult;
SendTilesToPrinterResult SendTilesToPrinter(uint16_t hl, uint8_t b, uint8_t c);
/* <<< factory SendTilesToPrinter */
/* >>> factory SendPrinterInstructionPacket */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } SendPrinterInstructionPacketResult;
SendPrinterInstructionPacketResult SendPrinterInstructionPacket(uint16_t hl, uint16_t saved_hl);
/* <<< factory SendPrinterInstructionPacket */
/* >>> factory SendPrinterInstructionPacket_1Sheet */
/* SendPrinterInstructionPacket_1Sheet:: engine/link/printer.asm:450, falls
 * through into SendPrinterInstructionPacket::465. Exit a/f are the last
 * packet's result and exit hl is the contrast word this routine pushed,
 * which the fallthrough target's second `pop hl` returns. */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } SendPrinterInstructionPacket_1SheetResult;
SendPrinterInstructionPacket_1SheetResult SendPrinterInstructionPacket_1Sheet(void);
/* <<< factory SendPrinterInstructionPacket_1Sheet */
/* >>> factory _PreparePrinterConnection */
/* engine/link/printer.asm:4, falls through into HandlePrinterError::21.
 * Entry hl is the buffer the data packet points at; entry a/f are dead and
 * b/c/d/e are loaded by the routine itself. The result is carry only: the
 * single caller farcalls this through PreparePrinterConnection and acts on
 * carry, and both error exits end in ShowPrinterConnectionErrorScene, whose
 * ported result is f alone. */
typedef struct { uint8_t f; } PreparePrinterConnectionResult;
PreparePrinterConnectionResult _PreparePrinterConnection(uint16_t hl);
/* <<< factory _PreparePrinterConnection */
#endif
