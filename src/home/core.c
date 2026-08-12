#include "home/core.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/duel.h"

#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0x2eu
#define DUELVARS_ARENA_CARD_HP 0x01u
#define MENU_CANCEL 0xFFu
#define PAD_A     0x01u
#define PAD_B     0x02u
#define PAD_START 0x08u
#define B_PAD_B_BIT 0x02u
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0x12u
#define DUELVARS_ARENA_CARD_HP                  0x08u
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0x1Au

#define ASLEEP           0x02u
#define CNF_SLP_PRZ       0x0Fu
#define PARALYZED        0x03u
#define DUELVARS_ARENA_CARD_STATUS 0x16u
#define TX_UnableDueToParalysisText 0x0000u
#define TX_UnableDueToSleepText     0x0001u

#define ASLEEP        0x02u
#define CNF_SLP_PRZ   0x0fu
#define PARALYZED     0x03u
#define DUELVARS_ARENA_CARD_STATUS 0x02u

#define FLAG_Z 0x80u
#define FLAG_C 0x10u

#define PARALYZED 0x03u
#define ASLEEP    0x02u

#include "generated/wram.h"
#include "home/card_data.h"

#define TILE_SIZE 16u
#define PAL_SIZE 8u
#define ATTR_BLK_CTRL_INSIDE 1u
#define ATTR_BLK_CTRL_LINE 2u

#define LOAD_LOADED1_CARD_GFX_B 0x30u
#define TILE_SIZE 0x10u
/* <<< factory statics */

/* >>> factory SetLineSeparation */
/* core.asm:4772-4774 */
void SetLineSeparation(uint8_t a)
{
	wLineSeparation = a;
}
/* <<< factory SetLineSeparation */

/* >>> factory PlayAreaScreenMenuFunction */
/* core.asm:5040-5054 */
uint8_t PlayAreaScreenMenuFunction(void)
{
	uint8_t keys = (uint8_t)(hKeysPressed & (PAD_A | PAD_B | PAD_START));
	if (keys == 0u)
		return 0xA0u;
	if (keys & PAD_B) {
		hCurMenuItem = MENU_CANCEL;
		return 0x10u;
	}
	return 0x90u;
}
/* <<< factory PlayAreaScreenMenuFunction */

/* >>> factory SwitchAttackPage */
/* core.asm:1165-1170 */
void SwitchAttackPage(void)
{
	uint8_t v = wAttackPageNumber ^ 0x01u;
	wAttackPageNumber = v;
}
/* <<< factory SwitchAttackPage */

/* >>> factory CopyCGBCardPalette */
/* core.asm:3982-3997 */
void CopyCGBCardPalette(uint8_t a)
{
	uint16_t hl = (uint16_t)(wBackgroundPalettesCGB_ADDR + (uint16_t)(a * PAL_SIZE));
	uint16_t de = wCardPalette_ADDR;
	uint8_t b = PAL_SIZE;

	do {
		uint8_t v = gb_read8(de++);
		gb_write8(hl++, v);
	} while (--b);
}
/* <<< factory CopyCGBCardPalette */

/* >>> factory CreateCardAttrBlkPacket_DataSet */
/* core.asm:4100-4113 */
uint16_t CreateCardAttrBlkPacket_DataSet(uint16_t hl, uint8_t a, uint8_t d, uint8_t e)
{
	gb_write8(hl++, ATTR_BLK_CTRL_INSIDE + ATTR_BLK_CTRL_LINE);
	gb_write8(hl++, a);
	gb_write8(hl++, d);
	gb_write8(hl++, e);
	gb_write8(hl++, (uint8_t)(d + 7u));
	gb_write8(hl++, (uint8_t)(e + 5u));
	return hl;
}
/* <<< factory CreateCardAttrBlkPacket_DataSet */
