#include "home/mail.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/bg_map.h"

#include "home/print_text.h"
#include "home/process_text.h"

#define SYM_CURSOR_R 0x0Fu
#define SYM_SPACE 0x00u
#define EMPTY_MAIL_NAME_TEXT 0x035Cu
/* <<< factory statics */

#define NUM_PC_PACKS 15
#define PACK_UNOPENED 0x80

static const uint8_t pc_mail_coordinates[NUM_PC_PACKS][2] = {
	{1, 2}, {7, 2}, {13, 2},
	{1, 4}, {7, 4}, {13, 4},
	{1, 6}, {7, 6}, {13, 6},
	{1, 8}, {7, 8}, {13, 8},
	{1, 10}, {7, 10}, {13, 10},
};

PCPackCoordinates GePCPackSelectionCoordinates(void)
{
	uint8_t selection = gb_read8(wPCPackSelection_ADDR);
	return (PCPackCoordinates){
		pc_mail_coordinates[selection][0],
		pc_mail_coordinates[selection][1],
	};
}

void TryGivePCPack(uint8_t id)
{
	uint16_t slot = wPCPacks_ADDR;
	uint8_t count = NUM_PC_PACKS;

	do {
		if ((uint8_t)(gb_read8(slot) & 0x7f) == id)
			return;
		slot++;
	} while (--count);

	slot = wPCPacks_ADDR;
	count = NUM_PC_PACKS;
	do {
		if ((uint8_t)(gb_read8(slot) & 0x7f) == 0) {
			gb_write8(slot, (uint8_t)(id | PACK_UNOPENED));
			return;
		}
		slot++;
	} while (--count);
}

/* >>> factory InitPCPacks */

/* mail.asm:5-20 */
void InitPCPacks(void)
{
	gb_write8(wPCPackSelection_ADDR, 0u);

	uint16_t addr = wPCPacks_ADDR;
	uint8_t count = NUM_PC_PACKS;
	do {
		gb_write8(addr, 0u);
		addr++;
	} while (--count);

	TryGivePCPack(1u);
}
/* <<< factory InitPCPacks */

/* >>> factory DrawMailMenuCursor */

/* mail.asm:328-333 */
void DrawMailMenuCursor(uint8_t symbol)
{
	PCPackCoordinates coords = GePCPackSelectionCoordinates();
	WriteByteToBGMap0(symbol, coords.b, coords.c);
}
/* <<< factory DrawMailMenuCursor */

/* >>> factory GetPCPackCoordinates */

/* mail.asm:459-470 */
PCPackCoordinates GetPCPackCoordinates(uint8_t pack)
{
	uint8_t saved = gb_read8(wPCPackSelection_ADDR);
	gb_write8(wPCPackSelection_ADDR, pack);
	PCPackCoordinates coords = GePCPackSelectionCoordinates();
	coords.b++;
	gb_write8(wPCPackSelection_ADDR, saved);
	return coords;
}
/* <<< factory GetPCPackCoordinates */

/* >>> factory ShowMailMenuCursor */
/* mail.asm:322-324 */
void ShowMailMenuCursor(void)
{
	DrawMailMenuCursor(SYM_CURSOR_R);
}
/* <<< factory ShowMailMenuCursor */

/* >>> factory HideMailMenuCursor */
/* mail.asm:325-327 */
void HideMailMenuCursor(void)
{
	DrawMailMenuCursor(SYM_SPACE);
}
/* <<< factory HideMailMenuCursor */

/* >>> factory PrintEmptyPCPackName */
/* mail.asm:414-427 */
void PrintEmptyPCPackName(uint8_t pack)
{
	PCPackCoordinates coords = GetPCPackCoordinates(pack);
	InitTextPrinting(coords.b, coords.c);
	(void)PrintTextNoDelay(EMPTY_MAIL_NAME_TEXT, coords.b, coords.c);
}
/* <<< factory PrintEmptyPCPackName */
