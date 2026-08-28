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

#define PACK_UNOPENED_F 0x07u

#include "home/give_booster_pack.h"
#include "home/init_menu.h"
#include "home/lcd.h"
#include "home/print_text.h"
#include "home/process_text.h"

/* PCMailBoosterPacks' booster ids (mail.asm:294-311). NUM_MAILS and
 * PACK_UNOPENED_F are already defined by this file's earlier ports and are not
 * repeated here. */
#define BOOSTER_COLOSSEUM_NEUTRAL 0x00u
#define BOOSTER_COLOSSEUM_FIRE 0x02u
#define BOOSTER_COLOSSEUM_TRAINER 0x06u
#define BOOSTER_EVOLUTION_NEUTRAL 0x07u
#define BOOSTER_EVOLUTION_GRASS 0x08u
#define BOOSTER_EVOLUTION_FIGHTING 0x0bu
#define BOOSTER_EVOLUTION_TRAINER 0x0du
#define BOOSTER_MYSTERY_NEUTRAL 0x0eu
#define BOOSTER_MYSTERY_WATER_COLORLESS 0x10u
#define BOOSTER_MYSTERY_LIGHTNING_COLORLESS 0x11u
#define BOOSTER_MYSTERY_TRAINER_COLORLESS 0x13u
#define BOOSTER_LABORATORY_NEUTRAL 0x14u
#define BOOSTER_LABORATORY_PSYCHIC 0x17u
#define BOOSTER_LABORATORY_TRAINER 0x18u

#define MailBoosterPackAlreadyOpenedText 0x0419u

#include "home/labels.h"
#include "home/lcd_enable_frame.h"
#include "home/text_box.h"

/* mail.asm:136 (PCMailHandleAInput). PAD_A is 1 << B_PAD_A with B_PAD_A = 0,
 * so $01. MailScreenLabels is the bank-4 label list at 04:47d2 (poketcg.sym),
 * loaded as a plain 16-bit pointer exactly like status.c's StatusScreenLabels. */
#define PAD_A 0x01u
#define SFX_CONFIRM 0x02u
#define MailScreenLabels 0x47D2u

/* PCMailTextPages' text ids (mail.asm:200-261). `tx Label` expands to
 * `dw Label_`, the textpointer index from text_offsets.asm:1029-1052. */
#define Mail1Part1Text 0x0401u
#define Mail1Part2Text 0x0402u
#define Mail2Part1Text 0x0403u
#define Mail2Part2Text 0x0404u
#define Mail3Part1Text 0x0405u
#define Mail3Part2Text 0x0406u
#define Mail4Part1Text 0x0407u
#define Mail4Part2Text 0x0408u
#define Mail5Part1Text 0x0409u
#define Mail5Part2Text 0x040Au
#define Mail6Part1Text 0x040Bu
#define Mail6Part2Text 0x040Cu
#define Mail7Part1Text 0x040Du
#define Mail7Part2Text 0x040Eu
#define Mail8Part1Text 0x040Fu
#define Mail8Part2Text 0x0410u
#define Mail9Part1Text 0x0411u
#define Mail9Part2Text 0x0412u
#define Mail10Part1Text 0x0413u
#define Mail11Part1Text 0x0414u
#define Mail12Part1Text 0x0415u
#define Mail13Part1Text 0x0416u
#define Mail14Part1Text 0x0417u
#define Mail15Part1Text 0x0418u
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

/* >>> factory PrintObtainedPCPacks */
void PrintObtainedPCPacks(void)
{
	uint8_t *pack_ptr = &wPCPacks;
	for (uint8_t index = 0; index < NUM_PC_PACKS; index++) {
		uint8_t pack = *pack_ptr++;
		if (pack != 0u)
			(void)PrintPCPackName(index);
	}
}
/* <<< factory PrintObtainedPCPacks */

/* >>> factory BlinkUnopenedPCPacks */
/* mail.asm:429-470 */
void BlinkUnopenedPCPacks(void)
{
	for (uint8_t index = 0; index < NUM_PC_PACKS; index++) {
		uint8_t pack = gb_read8((uint16_t)(wPCPacks_ADDR + index));
		if (pack == 0u)
			continue;
		if ((pack & (uint8_t)(1u << PACK_UNOPENED_F)) == 0u)
			continue;
		uint8_t phase = (uint8_t)(wCursorBlinkTimer & 0x0cu);
		if (phase == 0u)
			(void)PrintPCPackName(index);
		else if (phase == 0x0cu)
			PrintEmptyPCPackName(index);
	}
}
/* <<< factory BlinkUnopenedPCPacks */

/* >>> factory TryOpenPCMailBoosterPack */
/* mail.asm:263-292. The low 7 bits of wSelectedPCPack index
 * PCMailBoosterPacks (asm:294-311), a two-byte row per mail; a zero second id
 * means that mail grants a single pack. */
void TryOpenPCMailBoosterPack(void)
{
	static const uint8_t pc_mail_booster_packs[NUM_MAILS + 1][2] = {
		{0x00, 0x00},
		{BOOSTER_COLOSSEUM_NEUTRAL, 0x00},
		{BOOSTER_LABORATORY_PSYCHIC, 0x00},
		{BOOSTER_EVOLUTION_GRASS, 0x00},
		{BOOSTER_MYSTERY_LIGHTNING_COLORLESS, 0x00},
		{BOOSTER_EVOLUTION_FIGHTING, 0x00},
		{BOOSTER_COLOSSEUM_FIRE, 0x00},
		{BOOSTER_LABORATORY_PSYCHIC, 0x00},
		{BOOSTER_LABORATORY_PSYCHIC, 0x00},
		{BOOSTER_MYSTERY_WATER_COLORLESS, 0x00},
		{BOOSTER_COLOSSEUM_NEUTRAL, BOOSTER_EVOLUTION_NEUTRAL},
		{BOOSTER_MYSTERY_NEUTRAL, BOOSTER_LABORATORY_NEUTRAL},
		{BOOSTER_COLOSSEUM_TRAINER, 0x00},
		{BOOSTER_EVOLUTION_TRAINER, 0x00},
		{BOOSTER_MYSTERY_TRAINER_COLORLESS, 0x00},
		{BOOSTER_LABORATORY_TRAINER, 0x00},
	};

	wAnotherBoosterPack = 0u;
	uint8_t pack = wSelectedPCPack;
	if ((pack & (uint8_t)(1u << PACK_UNOPENED_F)) != 0u) {
		const uint8_t *entry = pc_mail_booster_packs[pack & 0x7fu];
		/* Both results are dead: `ld a, $01` overwrites the first call's a,
		 * and the second call is followed only by DisableLCD, so the flag
		 * byte GiveBoosterPack hands back is never read either. */
		(void)GiveBoosterPack(entry[0], 0u);
		wAnotherBoosterPack = 1u;
		if (entry[1] != 0u)
			(void)GiveBoosterPack(entry[1], 0u);
	} else {
		(void)InitMenuScreen();
		(void)SetupText(0x30u, 0xffu);
		(void)PrintScrollableText_NoTextBoxLabel(MailBoosterPackAlreadyOpenedText);
	}
	DisableLCD();
}
/* <<< factory TryOpenPCMailBoosterPack */

/* >>> factory PCMailHandleAInput */
/* mail.asm:136-198. PCMailTextPages (asm:200-261) is a 16-row table of two
 * text ids per mail; row 0 is the unused NULL pair and a zero second id means
 * that mail has no page two. The row index is the pack byte with bit 7
 * stripped, exactly as TryOpenPCMailBoosterPack indexes its own table. */
void PCMailHandleAInput(void)
{
	static const uint16_t pc_mail_text_pages[NUM_MAILS + 1][2] = {
		{0x0000u, 0x0000u},
		{Mail1Part1Text, Mail1Part2Text},
		{Mail2Part1Text, Mail2Part2Text},
		{Mail3Part1Text, Mail3Part2Text},
		{Mail4Part1Text, Mail4Part2Text},
		{Mail5Part1Text, Mail5Part2Text},
		{Mail6Part1Text, Mail6Part2Text},
		{Mail7Part1Text, Mail7Part2Text},
		{Mail8Part1Text, Mail8Part2Text},
		{Mail9Part1Text, Mail9Part2Text},
		{Mail10Part1Text, 0x0000u},
		{Mail11Part1Text, 0x0000u},
		{Mail12Part1Text, 0x0000u},
		{Mail13Part1Text, 0x0000u},
		{Mail14Part1Text, 0x0000u},
		{Mail15Part1Text, 0x0000u},
	};

	if ((hKeysPressed & PAD_A) == 0u)
		return;

	PlaySFX(SFX_CONFIRM);
	PrintObtainedPCPacks();
	ShowMailMenuCursor();

	uint16_t slot = (uint16_t)(wPCPacks_ADDR + wPCPackSelection);
	uint8_t pack = gb_read8(slot);
	wSelectedPCPack = pack;
	pack &= 0x7Fu;
	gb_write8(slot, pack);
	if (pack == 0u)
		return;

	const uint16_t *pages = pc_mail_text_pages[pack];
	uint16_t label = GetPCPackNameTextID(wPCPackSelection);
	(void)PrintScrollableText_WithTextBoxLabel(pages[0], label);
	TryOpenPCMailBoosterPack();

	(void)InitMenuScreen();
	uint16_t hl = SetupText(0x30u, 0xFFu);
	DrawRegularTextBox(&hl, 0u, 20u, 12u, 0u, 0u);
	(void)PrintLabels(MailScreenLabels, 0u, 0u);
	PrintObtainedPCPacks();
	ShowMailMenuCursor();
	(void)FlashWhiteScreen();

	/* `ld a, [hli] / ld h, [hl] / ld l, a / or h` tests both bytes of the
	 * second pointer, so the page is skipped only when the whole word is 0. */
	uint16_t page_two = pages[1];
	if (page_two != 0u) {
		label = GetPCPackNameTextID(wPCPackSelection);
		(void)PrintScrollableText_WithTextBoxLabel(page_two, label);
	}

	hl = page_two;
	DrawRegularTextBox(&hl, 0u, 20u, 6u, 0u, 12u);
	(void)PrintLabels(MailScreenLabels, 0u, 0u);
	DoFrameIfLCDEnabled();
}
/* <<< factory PCMailHandleAInput */
