#include "home/glossary.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "generated/hram.h"
#include "home/frames.h"
#include "home/text_box.h"
#include "home/menus.h"
#include "home/credits_sequence_commands.h"
#include "home/lcd.h"
#include "home/process_text.h"
#include "home/duel.h"
#include "home/deck_check.h"
#include "home/print_text.h"
#include "home/objects.h"
#include "mem.h"
#define PAD_B 0x02u
#define PAD_SELECT 0x04u
#define DOUBLE_SPACED 0x00u
#define MENU_CANCEL 0xffu
#define MENU_CONFIRM 0x01u
#define SINGLE_SPACED 0x01u
#define TRUE 0x01u
#define TX_END 0x00u
#define TX_SYMBOL 0x05u
#define ChooseWordAndPressAButtonText 0x02f9u
#define GlossaryMenuPage1Text 0x02f7u
#define GlossaryMenuPage2Text 0x02f8u
#define PokemonCardGlossaryText 0x02f6u
/* <<< factory statics */

/* >>> factory OpenGlossaryScreen */
#define SYM_1 0x21u
#define SYM_2 0x22u
#define SYM_SLASH 0x2Eu
#define GLOSSARY_TRANSITION_TABLE 0x4C8Eu /* bank 2: OpenGlossaryScreen_TransitionTable */
#define GLOSSARY_DATA1 0x4607u            /* bank 6: GlossaryData1 */
#define GLOSSARY_DATA2 0x4634u            /* bank 6: GlossaryData2 */
#define GLOSSARY_BANK 6u

/* glossary.asm:83-122 `.print_menu` */
static void glossary_print_menu(void)
{
	uint16_t text = wDefaultText_ADDR;
	gb_write8(text++, TX_SYMBOL);
	gb_write8(text++, (uint8_t)(wGlossaryPageNo + SYM_1));
	gb_write8(text++, TX_SYMBOL);
	gb_write8(text++, SYM_SLASH);
	gb_write8(text++, TX_SYMBOL);
	gb_write8(text++, SYM_2);
	gb_write8(text, TX_END);
	InitTextPrinting(16u, 1u);
	text = wDefaultText_ADDR;
	ProcessText(&text);
	InitTextPrinting(1u, 3u);
	(void)ProcessTextFromID(wGlossaryPageNo != 0u ? GlossaryMenuPage2Text : GlossaryMenuPage1Text);
}

/* glossary.asm:65-81 `.display_menu` */
static void glossary_display_menu(void)
{
	wTileMapFill = 0u;
	ZeroObjectPositions();
	wVBlankOAMCopyToggle = TRUE;
	DoFrame();
	EmptyScreen();
	Set_OBJ_8x8();
	LoadCursorTile();
	InitTextPrinting(5u, 0u);
	(void)ProcessTextFromID(PokemonCardGlossaryText);
	glossary_print_menu();
	(void)DrawWideTextBox_PrintText(ChooseWordAndPressAButtonText);
}

/* glossary.asm:125-192 `.print_description`: entry `a` of the page's
 * five-byte glossary_entry table (x, title text id, description text id). */
static void glossary_print_description(uint8_t a)
{
	wTileMapFill = 0u;
	EmptyScreen();
	InitTextPrinting(5u, 0u);
	(void)ProcessTextFromID(PokemonCardGlossaryText);
	uint16_t box = 0u;
	DrawRegularTextBox(&box, 0u, 20u, 14u, 0u, 4u);
	const uint8_t *entry = rom_ptr(GLOSSARY_BANK,
		(uint16_t)((wGlossaryPageNo != 0u ? GLOSSARY_DATA2 : GLOSSARY_DATA1) + (uint16_t)a * 5u));
	InitTextPrinting(entry[0], 2u);
	(void)ProcessTextFromID((uint16_t)(entry[1] | ((uint16_t)entry[2] << 8)));
	InitTextPrinting(1u, 5u);
	wLineSeparation = SINGLE_SPACED;
	(void)ProcessTextFromID((uint16_t)(entry[3] | ((uint16_t)entry[4] << 8)));
	wLineSeparation = DOUBLE_SPACED;
	EnableLCD();
	do {
		DoFrame();
	} while ((hKeysPressed & PAD_B) == 0u);
	PlaySFXConfirmOrCancel(MENU_CANCEL);
}

/* glossary.asm:1-56. The cursor walks the bank-2 transition table through
 * YourOrOppPlayAreaScreen_HandleInput; every item exists (upper bits $FF). */
void OpenGlossaryScreen(void)
{
	wGlossaryPageNo = 0u;
	glossary_display_menu();
	wInPlayAreaCurPosition = 0u;
	wMenuInputTablePointer = (uint8_t)GLOSSARY_TRANSITION_TABLE;
	*(wMenuInputTablePointer_PTR + 1) = (uint8_t)(GLOSSARY_TRANSITION_TABLE >> 8);
	wDuelInitialPrizesUpperBitsSet = 0xffu;
	wCheckMenuCursorBlinkCounter = 0u;
	for (;;) {
		wVBlankOAMCopyToggle = TRUE;
		DoFrame();
		if ((hKeysPressed & PAD_SELECT) != 0u) {
			PlaySFXConfirmOrCancel(MENU_CONFIRM);
			wGlossaryPageNo ^= 1u;
			glossary_print_menu();
			continue;
		}
		YourOrOppPlayAreaScreenInputResult input = YourOrOppPlayAreaScreen_HandleInput();
		if ((input.f & 0x10u) == 0u)
			continue;
		if (input.a == MENU_CANCEL) {
			ZeroObjectPositionsWithCopyToggleOn();
			return;
		}
		ZeroObjectPositionsWithCopyToggleOn();
		if (input.a == 0x09u) {
			wGlossaryPageNo ^= 1u;
			glossary_print_menu();
			continue;
		}
		glossary_print_description(input.a);
		glossary_display_menu();
		wCheckMenuCursorBlinkCounter = 0u;
	}
}
/* <<< factory OpenGlossaryScreen */
