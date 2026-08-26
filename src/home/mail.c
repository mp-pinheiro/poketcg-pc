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

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/overworld.h"
#include "home/sound.h"

#define NUM_MAILS 0x0Fu
#define PAD_CTRL_PAD 0xF0u
#define SFX_CURSOR 0x01u
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

/* >>> factory UpdateMailMenuCursor */
/* mail.asm:317-321 */
void UpdateMailMenuCursor(void)
{
	if ((wCursorBlinkTimer & 0x10u) == 0u)
		ShowMailMenuCursor();
	else
		HideMailMenuCursor();
}
/* <<< factory UpdateMailMenuCursor */

/* >>> factory PCMailHandleDPadInput */
void PCMailHandleDPadInput(void)
{
	static const uint8_t transition[15][4] = {
		{0x0c, 0x01, 0x03, 0x02},
		{0x0d, 0x02, 0x04, 0x00},
		{0x0e, 0x00, 0x05, 0x01},
		{0x00, 0x04, 0x06, 0x05},
		{0x01, 0x05, 0x07, 0x03},
		{0x02, 0x03, 0x08, 0x04},
		{0x03, 0x07, 0x09, 0x08},
		{0x04, 0x08, 0x0a, 0x06},
		{0x05, 0x06, 0x0b, 0x07},
		{0x06, 0x0a, 0x0c, 0x0b},
		{0x07, 0x0b, 0x0d, 0x09},
		{0x08, 0x09, 0x0e, 0x0a},
		{0x09, 0x0d, 0x00, 0x0e},
		{0x0a, 0x0e, 0x01, 0x0c},
		{0x0b, 0x0c, 0x02, 0x0d},
	};
	if ((gb_read8(hDPadHeld_ADDR) & PAD_CTRL_PAD) == 0u)
		return;
	GetDirectionFromDPadResult direction = GetDirectionFromDPad(gb_read8(hDPadHeld_ADDR));
	gb_write8(wPCLastDirectionPressed_ADDR, direction.a);
	uint8_t previous = gb_read8(wPCPackSelection_ADDR);
	HideMailMenuCursor();
	for (;;) {
		uint8_t selection = gb_read8(wPCPackSelection_ADDR);
		uint8_t next = transition[selection][direction.a];
		gb_write8(wPCPackSelection_ADDR, next);
		if (gb_read8((uint16_t)(wPCPacks_ADDR + next)) != 0u)
			break;
	}
	uint8_t selection = gb_read8(wPCPackSelection_ADDR);
	if (selection != previous)
		PlaySFX(SFX_CURSOR);
	ShowMailMenuCursor();
	gb_write8(wCursorBlinkTimer_ADDR, 0u);
}
/* <<< factory PCMailHandleDPadInput */

/* >>> factory GetPCPackNameTextID */
uint16_t GetPCPackNameTextID(uint8_t a)
{
	return (uint16_t)(0x035Du + (uint16_t)a);
}
/* <<< factory GetPCPackNameTextID */

/* >>> factory PrintPCPackName */
PrintPCPackNameResult PrintPCPackName(uint8_t a)
{
	uint16_t text_id = GetPCPackNameTextID(a);
	PCPackCoordinates coords = GetPCPackCoordinates(a);
	InitTextPrinting(coords.b, coords.c);
	TextResult printed = PrintTextNoDelay(text_id, coords.b, coords.c);
	return (PrintPCPackNameResult){printed.a};
}
/* <<< factory PrintPCPackName */
