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
void OpenGlossaryScreen(void)
{
	wGlossaryPageNo = 0u;
	wTileMapFill = 0u;
	ZeroObjectPositions();
	wVBlankOAMCopyToggle = TRUE;
	DoFrame();
	EmptyScreen();
	Set_OBJ_8x8();
	LoadCursorTile();
	InitTextPrinting(5u, 0u);
	(void)ProcessTextFromID(PokemonCardGlossaryText);
	uint8_t page = wGlossaryPageNo;
	InitTextPrinting(16u, 1u);
	uint16_t text = wDefaultText_ADDR;
	gb_write8(text++, TX_SYMBOL);
	gb_write8(text++, (uint8_t)(page + 1u));
	gb_write8(text++, TX_SYMBOL);
	gb_write8(text++, 0x2fu);
	gb_write8(text++, TX_SYMBOL);
	gb_write8(text++, 0x02u);
	gb_write8(text, TX_END);
	text = wDefaultText_ADDR;
	ProcessText(&text);
	InitTextPrinting(1u, 3u);
	(void)ProcessTextFromID(page ? GlossaryMenuPage2Text : GlossaryMenuPage1Text);
	(void)DrawWideTextBox_PrintText(ChooseWordAndPressAButtonText);
	wInPlayAreaCurPosition = 0u;
	wMenuInputTablePointer = 0u;
	*(wMenuInputTablePointer_PTR + 1) = 0u;
	wDuelInitialPrizesUpperBitsSet = 0xffu;
	wCheckMenuCursorBlinkCounter = 0u;
	uint8_t item = 0xffu;
	for (;;) {
		wVBlankOAMCopyToggle = TRUE;
		DoFrame();
		uint8_t keys = hKeysPressed;
		if ((keys & PAD_SELECT) != 0u) {
			PlaySFXConfirmOrCancel(MENU_CONFIRM);
			wGlossaryPageNo ^= 1u;
			(void)ProcessTextFromID(wGlossaryPageNo ? GlossaryMenuPage2Text : GlossaryMenuPage1Text);
			continue;
		}
		if ((keys & PAD_B) != 0u) {
			ZeroObjectPositionsWithCopyToggleOn();
			if ((uint8_t)(item + 1u) == 0u)
				wDuelInitialPrizesUpperBitsSet = 0xffu;
			else
				wDuelInitialPrizesUpperBitsSet = 0u;
			PlaySFXConfirmOrCancel(MENU_CANCEL);
			return;
		}
		YourOrOppPlayAreaScreen_HandleInput();
	}
}
/* <<< factory OpenGlossaryScreen */
