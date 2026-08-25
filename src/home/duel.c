#include "home/duel.h"

#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/duel_core.h"
#include "home/card_color.h"
#include "home/substatus.h"
#include "home/print_text.h"
#include "home/switch_sram.h"
#include "home/menus.h"
#include "home/frames.h"
#include "mem.h"

/* HIGH(wOpponentDuelVariables), the value hWhoseTurn carries on the opponent's turn. */
#define OPPONENT_TURN ((uint8_t)(wOpponentDuelVariables_ADDR >> 8))
#define PLAYER_TURN ((uint8_t)(wPlayerDuelVariables_ADDR >> 8))

/* duel.asm:1316-1323: [hWhoseTurn << 8 | a], the current turn holder's duelvar a. */
DuelistVarResult GetTurnDuelistVariable(uint8_t a)
{
	uint16_t address = (uint16_t)(((uint16_t)hWhoseTurn << 8) | a);
	return (DuelistVarResult){gb_read8(address), address};
}

/* duel.asm:1325-1337: the other player's duelvar a. */
DuelistVarResult GetNonTurnDuelistVariable(uint8_t a)
{
	uint8_t turn = hWhoseTurn == PLAYER_TURN ? OPPONENT_TURN : PLAYER_TURN;
	uint16_t address = (uint16_t)(((uint16_t)turn << 8) | a);
	return (DuelistVarResult){gb_read8(address), address};
}

/* duel.asm:2364-2371: the other player becomes the turn holder. */
void SwapTurn(void)
{
	hWhoseTurn = hWhoseTurn == PLAYER_TURN ? OPPONENT_TURN : PLAYER_TURN;
}

/* duel.asm:762-777: deck index -> card id, from the turn holder's deck.
 * `ld hl, wPlayerDeck / add hl, de / ld a, [hl]` leaves hl = deck + a. */
DeckCardResult _GetCardIDFromDeckIndex(uint8_t a)
{
	uint16_t deck = hWhoseTurn == PLAYER_TURN ? wPlayerDeck_ADDR : wOpponentDeck_ADDR;
	return (DeckCardResult){gb_read8((uint16_t)(deck + a)), (uint16_t)(deck + a)};
}

/* duel.asm:701-711: id in de, af and hl preserved (both pushed and popped). */
uint16_t GetCardIDFromDeckIndex(uint8_t a)
{
	return _GetCardIDFromDeckIndex(a).a;
}

/* duel.asm:661-668: id in a and c, b = 0, hl preserved. */
DeckCardResult GetCardIDFromDeckIndex_bc(uint8_t a, uint16_t hl)
{
	return (DeckCardResult){_GetCardIDFromDeckIndex(a).a, hl};
}

/* duel.asm:670-684: the temp-list entry in a, shadowed in hTempCardIndex_ff98,
 * hl and de preserved. */
DeckCardResult GetCardInDuelTempList_OnlyDeckIndex(uint8_t a, uint16_t hl)
{
	uint8_t entry = gb_read8((uint16_t)(wDuelTempList_ADDR + a));
	hTempCardIndex_ff98 = entry;
	return (DeckCardResult){entry, hl};
}

/* duel.asm:686-699: entry in a (reloaded after the call), id in de, hl preserved. */
DeckEntryResult GetCardInDuelTempList(uint8_t a, uint16_t hl)
{
	uint8_t entry = gb_read8((uint16_t)(wDuelTempList_ADDR + a));
	hTempCardIndex_ff98 = entry;
	uint16_t id = GetCardIDFromDeckIndex(entry);
	return (DeckEntryResult){entry, (uint8_t)(id >> 8), (uint8_t)id, hl};
}

/* duel.asm:778-812. `push af` keeps the deck index for the trainer conversion;
 * de carries the card id through both calls, so the final `ld a, e` is the id's
 * low byte. Every other register is restored by the pops. */
static uint8_t load_card_data_from_deck_index(uint8_t a, uint16_t buffer, void (*load)(uint8_t))
{
	uint16_t id = GetCardIDFromDeckIndex(a);
	load((uint8_t)id);
	(void)ConvertSpecialTrainerCardToPokemon(a, buffer, id);
	return (uint8_t)id;
}

uint8_t LoadCardDataToBuffer1_FromDeckIndex(uint8_t a)
{
	return load_card_data_from_deck_index(a, wLoadedCard1_ADDR,
					      LoadCardDataToBuffer1_FromCardID);
}

uint8_t LoadCardDataToBuffer2_FromDeckIndex(uint8_t a)
{
	return load_card_data_from_deck_index(a, wLoadedCard2_ADDR,
					      LoadCardDataToBuffer2_FromCardID);
}

/* duel.asm:2011-2030. `sub e` then `sbc d` borrows the high byte; `and $80` on the
 * 8-bit result is the sign of the 16-bit subtraction, so a set sign means the
 * damage exceeded the HP and it clamps to zero. The tail is `or a / jr z / scf`,
 * so carry is set exactly when HP remains non-zero. */
SubtractHPResult SubtractHP(uint16_t hl, uint16_t de)
{
	uint8_t hp = gb_read8(hl);
	uint16_t damage = de;
	uint8_t remaining;
	if ((uint16_t)hp >= damage) {
		remaining = (uint8_t)(hp - damage);
	} else {
		remaining = 0;
	}
	gb_write8(hl, remaining);
	/* `or a` sets Z on zero; `scf` then sets C on non-zero. */
	uint8_t f = remaining ? 0x10u : 0x80u;
	return (SubtractHPResult){remaining, f};
}

#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK 0xbau
#define DUELVARS_DECK_CARDS 0x7eu
#define DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE 0xedu
#define DECK_SIZE 60u

/* duel.asm:398-431. Copies DECK_SIZE - n remaining deck ids into wDuelTempList.
 * The `or a; ret` tail leaves carry clear on the non-empty path, so the exit is
 * Z-only; the empty path is `scf`. Exit hl is page + $BA on both paths (the
 * GetTurnDuelistVariable residue equals where the copy loop ends). */
CardListResult CreateDeckCardList(uint8_t c, uint16_t de)
{
	DuelistVarResult not_in_deck = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	if (not_in_deck.a >= DECK_SIZE) {
		/* b/c/de are never touched on this path. The `cp DECK_SIZE` above left Z
		 * set iff n == 60 exactly, and `scf` preserves it. */
		gb_write8(wDuelTempList_ADDR, 0xFF);
		uint8_t f = (uint8_t)(0x10u | (not_in_deck.a == DECK_SIZE ? 0x80u : 0x00u));
		return (CardListResult){0xFF, 0, c, (uint8_t)(de >> 8), (uint8_t)de, f,
					not_in_deck.hl};
	}
	uint8_t count = (uint8_t)(DECK_SIZE - not_in_deck.a);
	uint16_t src = (uint16_t)(((uint16_t)hWhoseTurn << 8) |
				  (DUELVARS_DECK_CARDS + not_in_deck.a));
	uint16_t dst = wDuelTempList_ADDR;
	for (uint8_t i = 0; i < count; i++)
		gb_write8((uint16_t)(dst + i), gb_read8((uint16_t)(src + i)));
	gb_write8((uint16_t)(dst + count), 0xFF);
	/* `dec b / jr nz` leaves b = 0; c is the count it was loaded with. */
	return (CardListResult){count, 0, count, (uint8_t)((dst + count) >> 8),
				(uint8_t)(dst + count), 0x00u, not_in_deck.hl};
}

/* duel.asm:713-746. `ld a, b / or a / jr nz / scf` sets carry iff the compacted
 * list is empty; every other register is pushed and popped, so a is the only
 * remaining output besides the flag. */
TempListResult RemoveCardFromDuelTempList(uint8_t a)
{
	uint16_t src = wDuelTempList_ADDR;
	uint16_t dst = wDuelTempList_ADDR;
	uint8_t count = 0;
	for (;;) {
		uint8_t entry = gb_read8(src++);
		if (entry == 0xFF)
			break;
		if (entry != a) {
			gb_write8(dst++, entry);
			count++;
		}
	}
	gb_write8(dst, 0xFF);
	/* `or a` set Z on the empty exit, then `scf` keeps it: Z+C. */
	return (TempListResult){count, count ? 0x00u : 0x90u};
}

/* duel.asm:747-761. The terminator `cp $ff` on the $FF byte leaves Z+N ($C0);
 * only a carries the count. */
TempListResult CountCardsInDuelTempList(void)
{
	uint8_t count = 0;
	while (gb_read8((uint16_t)(wDuelTempList_ADDR + count)) != 0xFF)
		count++;
	return (TempListResult){count, 0xC0u};
}

#define DUELVARS_HAND 0x42u
#define DUELVARS_NUMBER_OF_CARDS_IN_HAND 0xeeu
#define DUELVARS_CARD_LOCATIONS 0x00u
#define DUELVARS_ARENA_CARD 0xbbu
#define DUELVARS_ARENA_CARD_HP 0xc8u
#define CARD_LOCATION_JUST_DRAWN 0x40u
#define TYPE_ENERGY_F 3u
#define PLAY_AREA_MASK 0x10u

/* duel.asm:2306-2320. The final `sub [hl]` borrows when the damage exceeds the
 * max HP; c keeps the HP, a the difference, and the borrow is the exit carry. */
CardDamageResult GetCardDamageAndMaxHP(uint8_t e)
{
	uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
	(void)LoadCardDataToBuffer2_FromDeckIndex(deck_index);
	uint8_t damage = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + e)).a;
	uint8_t max_hp = gb_read8(wLoadedCard2HP_ADDR);
	uint8_t difference = (uint8_t)(max_hp - damage);
	/* `sub [hl]`: N always, H on the low-nibble borrow, C on the full-byte borrow,
	 * Z when the difference is zero. */
	uint8_t f = 0x40u;
	if ((max_hp & 0x0Fu) < (damage & 0x0Fu))
		f |= 0x20u;
	if (max_hp < damage)
		f |= 0x10u;
	if (!difference)
		f |= 0x80u;
	return (CardDamageResult){difference, max_hp, f};
}

/* duel.asm:526-533: b = hand count, hl = page + $41 + count, de = wDuelTempList. */
HandListResult FindLastCardInHand(uint8_t c)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	return (HandListResult){(uint8_t)(DUELVARS_HAND - 1u + count), count, c,
				(uint8_t)(wDuelTempList_ADDR >> 8), (uint8_t)wDuelTempList_ADDR,
				0x00u, (uint16_t)(((uint16_t)hWhoseTurn << 8) |
						  (DUELVARS_HAND - 1u + count))};
}

/* duel.asm:473-500. Walks the hand backward from the last card, skipping
 * just-drawn cards. Exit a = hand count, carry iff the hand is empty. */
HandListResult CreateHandCardList(uint8_t c)
{
	HandListResult last = FindLastCardInHand(c);
	uint8_t count = last.b;
	uint16_t src = last.hl;
	uint16_t dst = wDuelTempList_ADDR;
	for (uint8_t i = 0; i < count; i++) {
		uint8_t deck_index = gb_read8(src--);
		uint8_t location = gb_read8((uint16_t)(((uint16_t)hWhoseTurn << 8) | deck_index));
		if (!(location & CARD_LOCATION_JUST_DRAWN))
			gb_write8(dst++, deck_index);
	}
	gb_write8(dst, 0xFF);
	uint8_t hand_count = gb_read8((uint16_t)(((uint16_t)hWhoseTurn << 8) |
						   DUELVARS_NUMBER_OF_CARDS_IN_HAND));
	uint8_t f = hand_count ? 0x00u : 0x90u;
	return (HandListResult){hand_count, 0, c, (uint8_t)(dst >> 8), (uint8_t)dst, f,
				(uint16_t)(((uint16_t)hWhoseTurn << 8) |
					   DUELVARS_NUMBER_OF_CARDS_IN_HAND)};
}

/* duel.asm:435-470. Location-masked scan of the 60 card locations; energies of the
 * requested play-area location go into wDuelTempList. Exit a = the first entry,
 * carry iff the list is empty. */
HandListResult CreateArenaOrBenchEnergyCardList(uint8_t a)
{
	uint8_t location_mask = (uint8_t)(a | PLAY_AREA_MASK);
	uint16_t dst = wDuelTempList_ADDR;
	uint8_t first = 0xFF;
	for (uint8_t i = 0; i < DECK_SIZE; i++) {
		if (gb_read8((uint16_t)(((uint16_t)hWhoseTurn << 8) | i)) != location_mask)
			continue;
		(void)LoadCardDataToBuffer2_FromDeckIndex(i);
		if (!(gb_read8(wLoadedCard2Type_ADDR) & (uint8_t)(1u << TYPE_ENERGY_F)))
			continue;
		gb_write8(dst++, i);
		if (first == 0xFF)
			first = i;
	}
	gb_write8(dst, 0xFF);
	uint8_t f;
	if (first == 0xFF)
		f = 0x90u; /* `cp $ff` set Z, `scf` kept it */
	else
		f = first ? 0x00u : 0x80u; /* `or a` on the first entry */
	return (HandListResult){first, 0, location_mask, (uint8_t)(dst >> 8), (uint8_t)dst,
				f, (uint16_t)(((uint16_t)hWhoseTurn << 8) + DECK_SIZE)};
}

#include "home/random.h"
/* >>> factory statics */
#define DUELVARS_PRIZES 0xecu
#define PRIZES_6 0x06u

#include "home/bg_map.h"
#include "home/objects.h"
#include "home/random.h"
#include "home/tiles.h"
#define CONSOLE_CGB_8BF2 0x02u
#define TRUE_8BF2 0x01u
#define DUELVARS_PRIZES_8BF2 0xECu
#define PRIZE_TILE_8BF2 0xACu
#define PRIZE_TILE_CGB_ATTR_8BF2 0x02u
#define VBK_REG_8BF2 0xFF4Fu

#include "home/random.h"
#include "home/sound.h"
#include "home/deck_check.h"
#include "home/objects.h"

#define YOPA_PAD_A       0x01u
#define YOPA_PAD_B       0x02u
#define YOPA_PAD_RIGHT   0x10u
#define YOPA_PAD_LEFT    0x20u
#define YOPA_PAD_UP      0x40u
#define YOPA_PAD_DOWN    0x80u
#define YOPA_SFX_CURSOR  0x01u
#define YOPA_MENU_CANCEL 0xFFu
#define YOPA_MENU_CONFIRM 0x01u
#define YOPA_PRIZES_3    0x03u
#define YOPA_PRIZES_5    0x05u
#define YOPA_BLINK_MASK  0x0Fu
#define YOPA_BLINK_BIT   0x10u
#define YOPA_ITEM_LEN    0x07u

/* duel.asm:1701-1943 helper: [wTransitionTablePtr] as a 16-bit address. */
static uint16_t yoopa_table_ptr(void)
{
	return (uint16_t)(gb_read8(wTransitionTablePtr_ADDR) |
		(uint16_t)gb_read8((uint16_t)(wTransitionTablePtr_ADDR + 1u)) << 8);
}

/* duel.asm:1701-1943 .draw_cursor */
static void yoopa_draw_cursor(void)
{
	ZeroObjectPositions();
	uint16_t de = yoopa_table_ptr();
	uint16_t hl = HtimesL((uint16_t)((uint16_t)YOPA_ITEM_LEN << 8 | wYourOrOppPlayAreaCurPosition));
	hl = (uint16_t)(hl + de);
	uint8_t d = gb_read8(hl);
	uint8_t e = gb_read8((uint16_t)(hl + 1u));
	uint8_t b = gb_read8((uint16_t)(hl + 2u));
	SetOneObjectAttributes(e, d, 0x00u, b);
}

#include "home/tiles.h"

#define BPA_DUELVARS_NUM_POKEMON 0xEFu
#define BPA_DUELVARS_BENCH1_STAGE 0xCFu
#define BPA_MAX_PLAY_AREA_POKEMON 0x06u
#define BPA_CONSOLE_CGB 0x02u
#define BPA_TILE_STAGE_BASE 0xE4u
#define BPA_TILE_TWO_STAGE 0xECu
#define BPA_TILE_TWO_STAGE_ALT 0xF0u
#define BPA_TILE_EMPTY_SLOT 0xF4u
#define BPA_RECT_STEPS_TILES 0x0102u
#define BPA_RECT_STEPS_FLAT 0x0000u
#define BPA_SYM_SPACE 0x00u
#define BPA_SYM_CURSOR_R 0x01u
#define BPA_RVBK 0xFF4Fu

#include "home/tiles.h"
#include "home/bg_map.h"

#define V0_TILES0 0x8000u
#define CONSOLE_CGB 0x02u
#define R_VBK 0xFF4Fu
#define PRIZE_TILE 0xACu
#define PRIZE_TILE_CGB_ATTR 0x02u

static const uint8_t kCursorTileData[16] = {
	0xE0u, 0xC0u, 0x98u, 0xB0u, 0x84u, 0x8Cu, 0x83u, 0x82u,
	0x86u, 0x8Fu, 0x9Du, 0xBEu, 0xF4u, 0xF8u, 0x50u, 0x60u
};

#include "generated/wram.h"

#include "home/bg_map.h"

#include "generated/wram.h"
#include "home/duel.h"
#define SYM_SPACE 0x00u

#include "home/duel.h"
#include "generated/wram.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/serial.h"
#define OPPACTION_BEGIN_ATTACK 0x08u
#define TRUE 0x01u

#include "home/duel.h"
#include "home/tiles.h"
#include "generated/wram.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/frames.h"
#include "home/empty_screen.h"
#include "home/tiles.h"
#include "home/objects.h"
#include "mem.h"
#define PLAYER_TURN 0xC2u
#define OPPONENT_TURN 0xC3u

#include "home/deck_configuration.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "generated/wram.h"
#define TX_END 0x00u
#define TX_SYMBOL 0x05u
#define SYM_CROSS 0x2du
#define HandText_2 0x024eu

#include "home/deck_configuration.h"
#include "home/tiles.h"
#include "home/process_text.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/duel.h"
#include "home/switch_sram.h"
#include "home/core.h"
#include "generated/wram.h"
#include "generated/sram.h"
#include "mem.h"

#include "home/duel.h"
#define SYM_CURSOR_R 0x0Fu

#include "home/duel.h"
#include "home/sound.h"
#include "home/deck_check.h"
#define B_CURSOR_BLINK_PERIOD 0x04u
#define CURSOR_BLINK_PERIOD_MASK 0x0Fu
#define MENU_CANCEL 0xFFu
#define MENU_CONFIRM 0x01u
#define SFX_CURSOR 0x01u
#define B_PAD_LEFT 5u
#define B_PAD_RIGHT 4u
#define B_PAD_UP 6u
#define B_PAD_DOWN 7u
#define PAD_A 0x01u
#define PAD_B 0x02u
#define WCE5E_ADDR 0xCE5Eu

#include "home/duel.h"
#include "generated/wram.h"
#define DECK_SIZE 0x3Cu
#define DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE 0xEDu
#define DUELVARS_NUMBER_OF_CARDS_IN_HAND 0xEEu
#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK 0xBAu
#define PLAYER_ICON_COORDS 0x4635u
#define OPPONENT_ICON_COORDS 0x463Bu

#include "home/duel.h"
#include "generated/wram.h"
#include "generated/hram.h"

#include "home/core.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define hTempPlayAreaLocation_ff9d_ADDR 0xFF9Du

#include "home/duel.h"
#include "home/empty_screen.h"
#include "home/tiles.h"
#include "home/objects.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define PLAYER_ICON_COORDINATES_ADDR 0x4BE6u
#define OPP_ICON_COORDINATES_ADDR 0x4BECu
#define wTileMapFill_ADDR 0xCAB6u
#define wCheckMenuPlayAreaWhichDuelist_ADDR 0xCE50u
#define wCheckMenuPlayAreaWhichLayout_ADDR 0xCE51u
#define wIsSwapTurnPending_ADDR 0xCE56u

#include "home/duel.h"
#include "home/serial.h"
#include "home/duel_core.h"
#include "home/effect_commands.h"
#define EFFECTCMDTYPE_BEFORE_DAMAGE 0x03u
#define EFFECTCMDTYPE_INITIAL_EFFECT_2 0x02u
#define EFFECTCMDTYPE_REQUIRE_SELECTION 0x05u
#define OPPACTION_DUEL_MAIN_SCENE 0x16u
#define OPPACTION_EXECUTE_PKMN_POWER_EFFECT 0x0du
#define OPPACTION_USE_PKMN_POWER 0x0cu

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/tiles.h"
#include "mem.h"

#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#include "home/duel.h"
#include "home/frames.h"
#include "home/credits_sequence_commands.h"
#include "home/lcd.h"
#include "home/objects.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "home/tiles.h"
#define DuelistsPlayAreaText 0x0247u

#include "generated/wram.h"
#include "home/duel.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "home/lcd.h"
#include "mem.h"

#include "home/duel.h"
#include "home/menus.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#define DUELVARS_ARENA_CARD 0xBBu
#define PokemonsAttackText 0x0035u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "home/duel_core.h"
#include "home/menus.h"
#include "home/print_text.h"
#include "mem.h"
#define WasUnsuccessfulText 0x014au

#include "home/core.h"
#include "home/duel.h"
#include "home/tiles.h"
#include "home/card_data.h"
#include "generated/wram.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/credits_sequence_commands.h"
#include "home/duel.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/objects.h"
#include "home/process_text.h"
#include "home/tiles.h"
#define CHECK_PLAY_AREA 0x0Au
/* <<< factory statics */

/* duel.asm:541-563. `or a / ret z` on entry; otherwise swap each of the first a
 * deck bytes with [de + Random(c)], where de starts at hl. Exit a is the byte
 * swapped into the last position; the tail pops restore every other register. */
ShuffleCardsResult ShuffleCards(uint8_t a, uint16_t hl)
{
	if (!a)
		return (ShuffleCardsResult){0, 0x80u};
	uint8_t c = a;
	uint16_t de = hl;
	uint8_t last = 0;
	for (uint8_t i = 0; i < a; i++) {
		uint16_t target = (uint16_t)(de + Random(c));
		uint8_t swap = gb_read8(target);
		uint8_t moving = gb_read8((uint16_t)(hl + i));
		gb_write8((uint16_t)(hl + i), swap);
		gb_write8(target, moving);
		last = moving;
	}
	/* The final `dec b` from 1 leaves Z+N on the way out. */
	return (ShuffleCardsResult){last, 0xC0u};
}

#define HTEMP_LIST_PTR 0xFF99u
#define HTEMP_CARD_ID 0xFF9Bu

static uint16_t list_ptr(void)
{
	return (uint16_t)(gb_read8(HTEMP_LIST_PTR) |
			  (uint16_t)gb_read8((uint16_t)(HTEMP_LIST_PTR + 1u)) << 8);
}

static void list_set_ptr(uint16_t ptr)
{
	gb_write8(HTEMP_LIST_PTR, (uint8_t)ptr);
	gb_write8((uint16_t)(HTEMP_LIST_PTR + 1u), (uint8_t)(ptr >> 8));
}

/* duel.asm:589-648. The terminator is $FF, whose bit 7 is the loop-exit test. Each
 * pass finds the lowest-ID card in the remaining span and swaps it to the front,
 * then advances the pointer; the final `bit 7, [hl]` on the terminator leaves
 * Z clear and H set. */
SortResult SortCardsInListByID(uint8_t b, uint8_t c, uint16_t de)
{
	for (;;) {
		uint16_t ptr = list_ptr();
		if (gb_read8(ptr) & 0x80u) {
			/* `bit 7, [hl]` on the $FF terminator: Z clear, H set. */
			return (SortResult){(uint8_t)ptr, b, c, (uint8_t)(de >> 8), (uint8_t)de,
						0x20u, ptr};
		}
		uint16_t lowest_pos = ptr;
		uint16_t lowest_id = GetCardIDFromDeckIndex_bc(gb_read8(ptr), 0).a;
		uint16_t scan = (uint16_t)(ptr + 1u);
		while (!(gb_read8(scan) & 0x80u)) {
			uint16_t candidate = GetCardIDFromDeckIndex_bc(gb_read8(scan), 0).a;
			/* The asm's `cp / jr c, .not_lower_id` updates the slot on EQUAL ids
			 * too (only a strictly smaller current-lowest keeps the slot), so the
			 * sort is unstable: the last equal card moves to the front. */
			if (candidate <= lowest_id) {
				lowest_id = candidate;
				lowest_pos = scan;
			}
			scan++;
		}
		uint8_t front = gb_read8(ptr);
		gb_write8(ptr, gb_read8(lowest_pos));
		gb_write8(lowest_pos, front);
		/* Every pass ends with b = 0 (GetCardIDFromDeckIndex_bc's `ld b, $0`),
		 * c = the swapped-out front, de = the lowest-card position. */
		b = 0;
		c = front;
		de = lowest_pos;
		list_set_ptr((uint16_t)(ptr + 1u));
	}
}

/* duel.asm:578-587. Point the list pointer at wDuelTempList and sort it. On an
 * empty list the first terminator check returns with the entry registers intact. */
SortResult SortCardsInDuelTempListByID(uint8_t b, uint8_t c, uint16_t de)
{
	list_set_ptr(wDuelTempList_ADDR);
	return SortCardsInListByID(b, c, de);
}

/* duel.asm:502-525. Copies the hand (newest last) into wDuelTempList, sorts it,
 * then writes it back from the last hand position down, so the lowest id lands at
 * the newest slot. The trailing `dec b` leaves Z+N and a = the last copied value;
 * hl ends one before the first hand card (page + $41). */
HandSortResult SortHandCardsByID(void)
{
	HandListResult last = FindLastCardInHand(0);
	uint8_t count = last.b;
	uint16_t src = last.hl;
	uint16_t dst = wDuelTempList_ADDR;
	for (uint8_t i = 0; i < count; i++)
		gb_write8(dst++, gb_read8(src--));
	gb_write8(dst, 0xFF);
	/* The sort's exit c (its last swap front) survives to the routine's exit. */
	SortResult sorted = SortCardsInDuelTempListByID(0, 0, wDuelTempList_ADDR);
	dst = wDuelTempList_ADDR;
	uint16_t hand = (uint16_t)(((uint16_t)hWhoseTurn << 8) | (DUELVARS_HAND - 1u + count));
	uint8_t last_card = 0;
	for (uint8_t i = 0; i < count; i++) {
		last_card = gb_read8(dst++);
		gb_write8(hand--, last_card);
	}
	return (HandSortResult){last_card, 0, sorted.c, (uint8_t)(dst >> 8), (uint8_t)dst,
				0xC0u, (uint16_t)(((uint16_t)hWhoseTurn << 8) + DUELVARS_HAND - 1u)};
}

/* duel.asm:1915-1922. The table is `db $80, $40, $20, $10, $08, $04, $02, $01`
 * (InvertedPowersOf2, 00:1A1A). Entry a is a color index; all other registers
 * are preserved. */
uint8_t TranslateColorToWR(uint8_t a)
{
	return rom_ptr(0u, 0x1A1Au)[a];
}

/* duel.asm:1290-1315. Entry hl must already hold the card-locations page; the
 * routine only walks l from 0 to 60. `ld a, c / pop bc` leaves a = the count and
 * restores bc, so the only other exit is hl = page + 60. */
CardCountResult CountCardIDInLocation(uint8_t b, uint8_t e, uint16_t hl)
{
	uint8_t count = 0;
	for (uint8_t l = 0; l < DECK_SIZE; l++) {
		if (gb_read8((uint16_t)(hl + l)) != b)
			continue;
		if (_GetCardIDFromDeckIndex(l).a != e)
			continue;
		count++;
	}
	return (CardCountResult){count, (uint16_t)(hl + DECK_SIZE)};
}

/* duel.asm:2331-2357. PowersOf2 (00:11B7) is `db $01..$80`. The rra x3 folds a's
 * top five bits into the group index. */
AttackFlagResult CheckLoadedAttackFlag(uint8_t a)
{
	uint8_t bit = (uint8_t)(1u << (a & 0x07u));
	uint8_t group = (uint8_t)((a >> 3) & 0x1Fu);
	uint8_t value = (uint8_t)(gb_read8((uint16_t)(wLoadedAttackFlag1_ADDR + group)) & bit);
	/* Oracle-observed exits: scf on the set path leaves C only; the clear path
	 * carries Z+H from the final `and b` (0xA0). */
	uint8_t f = value ? 0x10u : 0xA0u;
	return (AttackFlagResult){value, f};
}

/* duel.asm:369-397. Reads the discard pile backward into wDuelTempList; carry is
 * set iff the pile is empty (`or a / ret nz / scf`, so the empty exit is Z+C).
 * `inc b / dec b` leaves b = 0 on both paths; c is never touched. */
CardListResult CreateDiscardPileCardList(uint8_t c)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE).a;
	uint16_t src = (uint16_t)(((uint16_t)hWhoseTurn << 8) | ((DUELVARS_DECK_CARDS - 1u) + count));
	uint16_t dst = wDuelTempList_ADDR;
	for (uint8_t i = 0; i < count; i++)
		gb_write8((uint16_t)(dst + i), gb_read8((uint16_t)(src - i)));
	gb_write8((uint16_t)(dst + count), 0xFF);
	uint8_t f = count ? 0x00u : 0x90u;
	return (CardListResult){count, 0, c, (uint8_t)((dst + count) >> 8),
				(uint8_t)(dst + count), f,
				(uint16_t)(((uint16_t)hWhoseTurn << 8) |
					      DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE)};
}

/* Text ID of the fallback opponent name. */
#define PLAYER2_TEXT_ID 0x0092u

/* CopyPlayerName's `.loop` tail. CopyOpponentName's name-buffer path jumps straight
 * into it, so the DisableSRAM runs on that path too even though it never enabled SRAM. */
static CopyTextResult copy_name_loop(uint16_t hl, uint16_t de)
{
	uint8_t a;

	do {
		a = gb_read8(hl++);
		gb_write8(de++, a);
	} while (a);
	de--;
	DisableSRAM();
	return (CopyTextResult){a, (uint8_t)(de >> 8), (uint8_t)de, hl};
}

CopyTextResult CopyPlayerName(uint16_t de)
{
	EnableSRAM();
	return copy_name_loop(sPlayerName_ADDR, de);
}

CopyTextResult CopyOpponentName(uint16_t de)
{
	uint16_t name = (uint16_t)(gb_read8(wOpponentName_ADDR) |
		(uint16_t)gb_read8((uint16_t)(wOpponentName_ADDR + 1u)) << 8);

	if (name)
		return CopyText(name, de);
	if (gb_read8(wNameBuffer_ADDR))
		return copy_name_loop(wNameBuffer_ADDR, de);
	return CopyText(PLAYER2_TEXT_ID, de);
}

#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xefu
#define DUELVARS_PRIZES 0xecu
#define CARD_LOCATION_DECK 0x00u
#define CARD_LOCATION_HAND 0x01u
#define CARD_LOCATION_DISCARD_PILE 0x02u
#define DUELVARS_ARENA_CARD_FLAGS 0xc2u
#define DUELVARS_ARENA_CARD_STAGE 0xceu
#define DUELVARS_ARENA_CARD_CHANGED_TYPE 0xd4u
#define DUELVARS_ARENA_CARD_ATTACHED_DEFENDER 0xdau
#define DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER 0xe0u
#define DUELVARS_ARENA_CARD_SUBSTATUS1 0xe7u
#define DUELVARS_ARENA_CARD_SUBSTATUS2 0xe8u
#define DUELVARS_ARENA_CARD_CHANGED_WEAKNESS 0xe9u
#define DUELVARS_ARENA_CARD_CHANGED_RESISTANCE 0xeau
#define DUELVARS_ARENA_CARD_SUBSTATUS3 0xebu
#define DUELVARS_ARENA_CARD_STATUS 0xf0u
#define DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX 0xf2u
#define SUBSTATUS3_THIS_TURN_DOUBLE_DAMAGE_F 0u
#define CAN_EVOLVE_THIS_TURN 0x80u
#define NUM_TYPES 8u
#define TYPE_PKMN 0x07u
#define PLUSPOWER 0xd8u
#define DEFENDER 0xd9u
#define ATTACK_DATA_LEN 0x13u
#define MAX_PLAY_AREA_POKEMON 6u
#define PLAY_AREA_ARENA 0u
#define COLORLESS 6u

/* duel.asm:60-104. */
CardListResult CopyDeckData(uint16_t de)
{
	uint16_t deck = hWhoseTurn == PLAYER_TURN ? wPlayerDeck_ADDR : wOpponentDeck_ADDR;
	uint16_t last_slot = (uint16_t)(deck + DECK_SIZE - 1u);
	uint16_t dst = deck;
	uint8_t last_value;
	uint8_t f;

	gb_write8(last_slot, 0);
	for (;;) {
		uint8_t count = gb_read8(de++);
		uint8_t id;

		if (!count)
			break;
		id = gb_read8(de++);
		for (uint8_t i = 0; i < count; i++)
			gb_write8(dst++, id);
	}
	gb_write8(wDeckName_ADDR, gb_read8(de++));
	gb_write8((uint16_t)(wDeckName_ADDR + 1u), gb_read8(de));

	/* The trailing `ld bc, DECK_SIZE - 1` (re-deriving hl for the final check)
	 * overwrites b/c unconditionally: b = 0, c = DECK_SIZE - 1 always. */
	last_value = gb_read8(last_slot);
	f = last_value ? 0x00u : 0x90u;

	return (CardListResult){last_value, 0, (uint8_t)(DECK_SIZE - 1u), (uint8_t)(de >> 8),
				(uint8_t)de, f, last_slot};
}

/* duel.asm:107-120. Verified exhaustively (all 256 byte values) against the
 * `rr l / adc 0` carry-ring: it computes popcount. */
uint8_t CountPrizes(void)
{
	uint8_t mask = GetTurnDuelistVariable(DUELVARS_PRIZES).a;
	uint8_t count = 0;

	while (mask) {
		count = (uint8_t)(count + (mask & 1u));
		mask = (uint8_t)(mask >> 1);
	}
	return count;
}

/* duel.asm:124-137. */
ShuffleDeckResult ShuffleDeck(uint8_t c, uint8_t e)
{
	uint8_t turn = hWhoseTurn;
	uint16_t page = (uint16_t)((uint16_t)turn << 8);
	uint8_t not_in_deck = gb_read8((uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK));
	uint8_t count = (uint8_t)(DECK_SIZE - not_in_deck);
	uint16_t deck_offset = (uint16_t)(page | (uint8_t)(DUELVARS_DECK_CARDS + not_in_deck));
	ShuffleCardsResult r = ShuffleCards(count, deck_offset);

	return (ShuffleDeckResult){r.a, count, c, turn, e, r.f, deck_offset};
}

/* duel.asm:142-161. */
DrawCardResult DrawCardFromDeck(void)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t not_in_deck_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	uint8_t not_in_deck = gb_read8(not_in_deck_addr);
	uint8_t card;

	if (not_in_deck >= DECK_SIZE) {
		uint8_t f = (uint8_t)(0x10u | (not_in_deck == DECK_SIZE ? 0x80u : 0x00u));
		return (DrawCardResult){not_in_deck, f};
	}
	gb_write8(not_in_deck_addr, (uint8_t)(not_in_deck + 1u));
	card = gb_read8((uint16_t)(page | (uint8_t)(DUELVARS_DECK_CARDS + not_in_deck)));
	gb_write8((uint16_t)(page | card), CARD_LOCATION_JUST_DRAWN);
	return (DrawCardResult){card, card ? 0x00u : 0x80u};
}

/* duel.asm:165-180. */
void ReturnCardToDeck(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t not_in_deck_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	uint8_t not_in_deck = (uint8_t)(gb_read8(not_in_deck_addr) - 1u);

	gb_write8(not_in_deck_addr, not_in_deck);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_DECK_CARDS + not_in_deck)), a);
	gb_write8((uint16_t)(page | a), CARD_LOCATION_DECK);
}

/* duel.asm:185-217. */
void SearchCardInDeckAndAddToHand(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t not_in_deck_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	uint8_t not_in_deck = gb_read8(not_in_deck_addr);
	uint8_t in_deck = (uint8_t)(DECK_SIZE - not_in_deck);
	uint16_t loc_addr = (uint16_t)(page | a);
	uint16_t hl = (uint16_t)(page | (uint8_t)(DUELVARS_DECK_CARDS + DECK_SIZE - 1u));
	uint16_t de = hl;

	gb_write8(not_in_deck_addr, (uint8_t)(not_in_deck + 1u));
	gb_write8(loc_addr, (uint8_t)(gb_read8(loc_addr) | CARD_LOCATION_JUST_DRAWN));
	for (uint8_t i = 0; i < in_deck; i++) {
		uint8_t card = gb_read8(hl--);

		if (card == a)
			continue;
		gb_write8(de--, card);
	}
}

/* duel.asm:221-242. */
void AddCardToHand(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t count_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	uint8_t count = (uint8_t)(gb_read8(count_addr) + 1u);

	gb_write8((uint16_t)(page | a), CARD_LOCATION_HAND);
	gb_write8(count_addr, count);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_HAND - 1u + count)), a);
}

/* duel.asm:246-280. */
void RemoveCardFromHand(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t count_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	uint8_t count = gb_read8(count_addr);
	uint16_t src = (uint16_t)(page | DUELVARS_HAND);
	uint16_t dst = src;

	if (!count)
		return;
	for (uint8_t i = 0; i < count; i++) {
		uint8_t card = gb_read8(src++);

		if (card == a) {
			gb_write8(count_addr, (uint8_t)(gb_read8(count_addr) - 1u));
			continue;
		}
		gb_write8(dst++, card);
	}
}

/* duel.asm:294-311. */
void PutCardInDiscardPile(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t count_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE);
	uint8_t count = (uint8_t)(gb_read8(count_addr) + 1u);

	gb_write8((uint16_t)(page | a), CARD_LOCATION_DISCARD_PILE);
	gb_write8(count_addr, count);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_DECK_CARDS - 1u + count)), a);
}

/* duel.asm:284-311. */
MoveCardResult MoveHandCardToDiscardPile(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t hl = (uint16_t)(page | a);
	uint8_t masked = (uint8_t)(gb_read8(hl) & (uint8_t)~CARD_LOCATION_JUST_DRAWN);

	if (masked != CARD_LOCATION_HAND) {
		uint8_t f = 0x40u;

		if ((masked & 0x0Fu) < (CARD_LOCATION_HAND & 0x0Fu))
			f |= 0x20u;
		if (masked < CARD_LOCATION_HAND)
			f |= 0x10u;
		return (MoveCardResult){masked, f, hl};
	}
	RemoveCardFromHand(a);
	PutCardInDiscardPile(a);
	return (MoveCardResult){a, 0xC0u, hl};
}

/* duel.asm:316-346. */
MoveDiscardResult MoveDiscardPileCardToHand(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t loc_addr = (uint16_t)(page | a);
	uint16_t count_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE);
	uint8_t count = gb_read8(count_addr);
	uint16_t src, dst;
	uint8_t last_carry;
	uint8_t f;

	gb_write8(loc_addr, (uint8_t)(gb_read8(loc_addr) | CARD_LOCATION_JUST_DRAWN));
	if (!count)
		return (MoveDiscardResult){0, 0x80u};
	gb_write8(count_addr, (uint8_t)(count - 1u));
	src = (uint16_t)(page | DUELVARS_DECK_CARDS);
	dst = src;
	last_carry = 0;
	for (uint8_t i = 0; i < count; i++) {
		uint8_t card = gb_read8(src++);

		last_carry = card < a ? 1u : 0u;
		if (card == a)
			continue;
		gb_write8(dst++, card);
	}
	f = (uint8_t)(0xC0u | (last_carry ? 0x10u : 0x00u));
	return (MoveDiscardResult){a, f};
}

/* duel.asm:350-362. PowersOf2 (00:11B7) is `db $01..$80`. */
CheckPrizeResult CheckPrizeTaken(uint8_t a)
{
	uint8_t mask = rom_ptr(0u, 0x11B7u)[a];
	uint8_t comp = (uint8_t)~mask;
	DuelistVarResult prizes = GetTurnDuelistVariable(DUELVARS_PRIZES);
	uint8_t result = (uint8_t)(prizes.a & mask);
	uint8_t f = (uint8_t)(0x20u | (result ? 0x00u : 0x80u));

	return (CheckPrizeResult){result, comp, mask, f, prizes.hl};
}

/* duel.asm:650-657. Identical to entering the top of SortCardsInListByID's own
 * loop. */
SortResult SortCardsInListByID_CheckForListTerminator(uint8_t b, uint8_t c, uint16_t de)
{
	return SortCardsInListByID(b, c, de);
}

/* duel.asm:879-915. */
EvolveResult CheckIfCanEvolveInto(uint8_t d, uint8_t e)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t card2_idx = gb_read8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + e)));
	uint16_t flags_addr;
	uint8_t flags;

	(void)LoadCardDataToBuffer2_FromDeckIndex(card2_idx);
	(void)LoadCardDataToBuffer1_FromDeckIndex(d);
	if (gb_read8(wLoadedCard1PreEvoName_ADDR) != gb_read8(wLoadedCard2Name_ADDR))
		return (EvolveResult){0, 0, d, e, 0x90u, wLoadedCard2Name_ADDR};
	if (gb_read8((uint16_t)(wLoadedCard1PreEvoName_ADDR + 1u)) !=
	    gb_read8((uint16_t)(wLoadedCard2Name_ADDR + 1u)))
		return (EvolveResult){0, 0, d, e, 0x90u, (uint16_t)(wLoadedCard2Name_ADDR + 1u)};

	flags_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_FLAGS + e));
	flags = (uint8_t)(gb_read8(flags_addr) & CAN_EVOLVE_THIS_TURN);
	if (flags)
		return (EvolveResult){flags, 0, d, e, 0x00u, flags_addr};
	return (EvolveResult){0x01u, 0, d, e, 0x10u, flags_addr};
}

/* duel.asm:922-957. */
EvolveResult CheckIfCanEvolveInto_BasicToStage2(uint8_t d, uint8_t e)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t flags_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_FLAGS + e));
	uint8_t flags = (uint8_t)(gb_read8(flags_addr) & CAN_EVOLVE_THIS_TURN);
	uint8_t basic_idx;
	uint16_t stage1_name;
	uint8_t byte1;

	if (!flags)
		return (EvolveResult){0, 0, d, e, 0x90u, flags_addr};

	basic_idx = gb_read8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + e)));
	(void)LoadCardDataToBuffer2_FromDeckIndex(basic_idx);
	(void)LoadCardDataToBuffer1_FromDeckIndex(d);
	stage1_name = (uint16_t)(gb_read8(wLoadedCard1PreEvoName_ADDR) |
		((uint16_t)gb_read8((uint16_t)(wLoadedCard1PreEvoName_ADDR + 1u)) << 8));
	LoadCardDataToBuffer1_FromName(stage1_name);

	if (gb_read8(wLoadedCard1PreEvoName_ADDR) != gb_read8(wLoadedCard2Name_ADDR))
		return (EvolveResult){0, 0, d, e, 0x90u, wLoadedCard2Name_ADDR};
	byte1 = gb_read8((uint16_t)(wLoadedCard1PreEvoName_ADDR + 1u));
	if (byte1 != gb_read8((uint16_t)(wLoadedCard2Name_ADDR + 1u)))
		return (EvolveResult){0, 0, d, e, 0x90u, (uint16_t)(wLoadedCard2Name_ADDR + 1u)};
	return (EvolveResult){byte1, 0, d, e, byte1 ? 0x00u : 0x80u,
				(uint16_t)(wLoadedCard2Name_ADDR + 1u)};
}

/* duel.asm:814-822. */
EvolveResult EvolvePokemonCardIfPossible(uint8_t c)
{
	uint8_t card_idx = hTempCardIndex_ff98;
	uint8_t slot = hTempPlayAreaLocation_ff9d;
	EvolveResult check = CheckIfCanEvolveInto(card_idx, slot);
	EvolveResult evolved;

	if (check.f & 0x10u)
		return (EvolveResult){check.a, c, card_idx, slot, check.f, check.hl};
	evolved = EvolvePokemonCard();
	return (EvolveResult){evolved.a, evolved.c, card_idx, evolved.e, evolved.f, evolved.hl};
}

/* duel.asm:824-869. */
EvolveResult EvolvePokemonCard(void)
{
	uint8_t slot = hTempPlayAreaLocation_ff9d;
	uint8_t card_idx = hTempCardIndex_ff98;
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t arena_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + slot));
	uint8_t pre_evo_idx = gb_read8(arena_addr);
	uint16_t hp_addr;
	uint8_t old_hp2, new_hp1, diff;
	uint16_t stage_addr;
	uint8_t stage;

	gb_write8(wPreEvolutionPokemonCard_ADDR, pre_evo_idx);
	(void)LoadCardDataToBuffer2_FromDeckIndex(pre_evo_idx);
	gb_write8(arena_addr, card_idx);
	(void)LoadCardDataToBuffer1_FromDeckIndex(card_idx);

	hp_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_HP + slot));
	old_hp2 = gb_read8(wLoadedCard2HP_ADDR);
	new_hp1 = gb_read8(wLoadedCard1HP_ADDR);
	diff = (uint8_t)(new_hp1 - old_hp2);
	gb_write8(hp_addr, (uint8_t)(diff + gb_read8(hp_addr)));

	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_FLAGS + slot)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_CHANGED_TYPE + slot)), 0);
	if (slot == 0)
		ClearAllStatusConditions();

	stage_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_STAGE + slot));
	stage = gb_read8(wLoadedCard1Stage_ADDR);
	gb_write8(stage_addr, stage);
	return (EvolveResult){stage, old_hp2, 0, slot, stage ? 0x00u : 0x80u, stage_addr};
}

/* duel.asm:962-989. a/f are always 0/$80 (the entry `xor a`, untouched
 * afterward) and omitted from CONTRACT, matching SwapTurn's precedent. */
void ClearAllStatusConditions(void)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t sub3_addr = (uint16_t)(page | DUELVARS_ARENA_CARD_SUBSTATUS3);
	uint16_t addr = (uint16_t)(page | DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX);

	gb_write8((uint16_t)(page | DUELVARS_ARENA_CARD_STATUS), 0);
	gb_write8((uint16_t)(page | DUELVARS_ARENA_CARD_SUBSTATUS1), 0);
	gb_write8((uint16_t)(page | DUELVARS_ARENA_CARD_SUBSTATUS2), 0);
	gb_write8((uint16_t)(page | DUELVARS_ARENA_CARD_CHANGED_WEAKNESS), 0);
	gb_write8((uint16_t)(page | DUELVARS_ARENA_CARD_CHANGED_RESISTANCE), 0);
	gb_write8(sub3_addr, (uint8_t)(gb_read8(sub3_addr) &
				       (uint8_t)~(1u << SUBSTATUS3_THIS_TURN_DOUBLE_DAMAGE_F)));
	for (int i = 0; i < 8; i++)
		gb_write8((uint16_t)(addr + i), 0);
}

/* duel.asm:1058-1064. */
PutHandResult PutHandCardInPlayArea(uint8_t a, uint8_t e)
{
	uint16_t hl = (uint16_t)(((uint16_t)hWhoseTurn << 8) | a);
	uint8_t result = (uint8_t)(e | PLAY_AREA_MASK);

	RemoveCardFromHand(a);
	gb_write8(hl, result);
	return (PutHandResult){result, hl};
}

/* duel.asm:996-1049. */
PutHandPokemonResult PutHandPokemonCardInPlayArea(uint8_t a, uint8_t f)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint16_t page;
	uint8_t slot;
	uint16_t arena_addr, stage_addr;

	if (count.a >= MAX_PLAY_AREA_POKEMON) {
		/* `pop af` restores the caller's entry flags before `scf` forces C;
		 * Z (and a itself) come from the caller, not from this `cp`. */
		uint8_t exit_f = (uint8_t)((f & 0x80u) | 0x10u);
		return (PutHandPokemonResult){a, exit_f, count.hl};
	}
	gb_write8(count.hl, (uint8_t)(count.a + 1u));
	slot = count.a;
	page = (uint16_t)((uint16_t)hWhoseTurn << 8);

	(void)PutHandCardInPlayArea(a, slot);
	arena_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + slot));
	gb_write8(arena_addr, a);
	(void)LoadCardDataToBuffer2_FromDeckIndex(a);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_HP + slot)),
		 gb_read8(wLoadedCard2HP_ADDR));
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_FLAGS + slot)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_CHANGED_TYPE + slot)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER + slot)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_ATTACHED_DEFENDER + slot)), 0);
	stage_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_STAGE + slot));
	gb_write8(stage_addr, gb_read8(wLoadedCard2Stage_ADDR));
	if (slot == 0)
		ClearAllStatusConditions();
	return (PutHandPokemonResult){slot, slot ? 0x00u : 0x80u, stage_addr};
}

/* duel.asm:1091-1111. */
EmptySlotResult EmptyPlayAreaSlot(uint8_t e)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t last;
	uint16_t last_addr;
	uint8_t f;

	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + e)), 0xFFu);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_HP + e)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_STAGE + e)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_CHANGED_TYPE + e)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_ATTACHED_DEFENDER + e)), 0);
	last = (uint8_t)(DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER + e);
	last_addr = (uint16_t)(page | last);
	gb_write8(last_addr, 0);

	f = last ? 0x00u : 0x80u;
	if ((uint8_t)(DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER & 0x0Fu) + (e & 0x0Fu) > 0x0Fu)
		f |= 0x20u;
	if ((uint32_t)DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER + e > 0xFFu)
		f |= 0x10u;
	return (EmptySlotResult){last, 0, f, last_addr};
}

/* duel.asm:1068-1087. */
MoveAreaResult MovePlayAreaCardToDiscardPile(uint8_t e)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t count_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t location = (uint8_t)(e | PLAY_AREA_MASK);

	(void)EmptyPlayAreaSlot(e);
	gb_write8(count_addr, (uint8_t)(gb_read8(count_addr) - 1u));
	for (uint8_t l = 0; l < DECK_SIZE; l++) {
		uint16_t addr = (uint16_t)(page | l);

		if (gb_read8(addr) == location)
			PutCardInDiscardPile(l);
	}
	/* EmptyPlayAreaSlot's `ld d, 0` (before its 2nd-6th writes) survives
	 * unmodified to this exit. */
	return (MoveAreaResult){DECK_SIZE, 0, 0xC0u, (uint16_t)(page | DECK_SIZE)};
}

/* duel.asm:1148-1215 / 1143-1146. */
SwapAreaResult SwapPlayAreaPokemon(uint8_t d, uint8_t e)
{
	if (e == d)
		return (SwapAreaResult){e, d, 0xC0u};

	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	static const uint8_t fields[7] = {
		DUELVARS_ARENA_CARD, DUELVARS_ARENA_CARD_HP, DUELVARS_ARENA_CARD_FLAGS,
		DUELVARS_ARENA_CARD_STAGE, DUELVARS_ARENA_CARD_CHANGED_TYPE,
		DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER, DUELVARS_ARENA_CARD_ATTACHED_DEFENDER,
	};
	uint8_t marked_d, marked_e;

	for (int i = 0; i < 7; i++) {
		uint16_t addr_e = (uint16_t)(page | (uint8_t)(fields[i] + e));
		uint16_t addr_d = (uint16_t)(page | (uint8_t)(fields[i] + d));
		uint8_t tmp = gb_read8(addr_d);

		gb_write8(addr_d, gb_read8(addr_e));
		gb_write8(addr_e, tmp);
	}
	marked_d = (uint8_t)(d | PLAY_AREA_MASK);
	marked_e = (uint8_t)(e | PLAY_AREA_MASK);
	for (uint8_t l = 0; l < DECK_SIZE; l++) {
		uint16_t addr = (uint16_t)(page | l);
		uint8_t loc = gb_read8(addr);

		if (loc == marked_e)
			gb_write8(addr, marked_d);
		else if (loc == marked_d)
			gb_write8(addr, marked_e);
	}
	return (SwapAreaResult){DECK_SIZE, d, 0xC0u};
}

SwapAreaResult SwapArenaWithBenchPokemon(uint8_t e)
{
	ClearAllStatusConditions();
	return SwapPlayAreaPokemon(PLAY_AREA_ARENA, e);
}

/* duel.asm:1122-1137. */
ShiftResult ShiftTurnPokemonToFirstPlayAreaSlots(void)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t write_slot = PLAY_AREA_ARENA;
	uint16_t hl;

	for (uint8_t scan_slot = PLAY_AREA_ARENA; scan_slot < MAX_PLAY_AREA_POKEMON; scan_slot++) {
		uint16_t addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + scan_slot));

		if (!(gb_read8(addr) & 0x80u)) {
			(void)SwapPlayAreaPokemon(scan_slot, write_slot);
			write_slot++;
		}
	}
	hl = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + MAX_PLAY_AREA_POKEMON));
	return (ShiftResult){MAX_PLAY_AREA_POKEMON, MAX_PLAY_AREA_POKEMON, write_slot, 0xC0u, hl};
}

/* duel.asm:1114-1119. */
ShiftResult ShiftAllPokemonToFirstPlayAreaSlots(void)
{
	ShiftResult r;

	(void)ShiftTurnPokemonToFirstPlayAreaSlots();
	SwapTurn();
	r = ShiftTurnPokemonToFirstPlayAreaSlots();
	SwapTurn();
	return r;
}

/* duel.asm:1221-1284. */
EnergiesResult GetPlayAreaCardAttachedEnergies(uint8_t e)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t location = (uint8_t)(PLAY_AREA_MASK | e);
	uint8_t sum;

	for (uint8_t t = 0; t < NUM_TYPES; t++)
		gb_write8((uint16_t)(wAttachedEnergies_ADDR + t), 0);
	for (uint8_t l = 0; l < DECK_SIZE; l++) {
		uint8_t type, color;
		uint16_t addr;

		if (gb_read8((uint16_t)(page | l)) != location)
			continue;
		(void)LoadCardDataToBuffer2_FromDeckIndex(l);
		type = gb_read8(wLoadedCard2Type_ADDR);
		if (!(type & (1u << TYPE_ENERGY_F)))
			continue;
		color = (uint8_t)(type & TYPE_PKMN);
		addr = (uint16_t)(wAttachedEnergies_ADDR + color);
		gb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));
		if (color == COLORLESS)
			gb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));
	}
	sum = 0;
	for (uint8_t t = 0; t < NUM_TYPES; t++)
		sum = (uint8_t)(sum + gb_read8((uint16_t)(wAttachedEnergies_ADDR + t)));
	gb_write8(wTotalAttachedEnergies_ADDR, sum);
	return (EnergiesResult){sum, 0xC0u};
}

/* duel.asm:1442-1467. */
AttackCopyResult CopyAttackDataAndDamage(uint8_t e)
{
	uint8_t card_id = gb_read8(wLoadedCard1ID_ADDR);
	uint16_t src = (e == 1) ? wLoadedCard1Atk2_ADDR : wLoadedCard1Atk1_ADDR;
	uint16_t dst = wLoadedAttack_ADDR;
	uint8_t damage;

	gb_write8(wTempCardID_ccc2_ADDR, card_id);
	for (uint8_t i = 0; i < ATTACK_DATA_LEN; i++)
		gb_write8(dst++, gb_read8(src++));
	damage = gb_read8(wLoadedAttackDamage_ADDR);
	gb_write8(wDamage_ADDR, damage);
	gb_write8((uint16_t)(wDamage_ADDR + 1u), 0);
	gb_write8(wNoDamageOrEffect_ADDR, 0);
	gb_write8(wDealtDamage_ADDR, 0);
	gb_write8((uint16_t)(wDealtDamage_ADDR + 1u), 0);
	return (AttackCopyResult){0, 0, 0x80u, (uint16_t)(wDealtDamage_ADDR + 1u), dst};
}

/* duel.asm:1434-1440. */
AttackCopyResult CopyAttackDataAndDamage_FromDeckIndex(uint8_t d, uint8_t e)
{
	gb_write8(wSelectedAttack_ADDR, e);
	hTempCardIndex_ff9f = d;
	(void)LoadCardDataToBuffer1_FromDeckIndex(d);
	return CopyAttackDataAndDamage(e);
}

/* duel.asm:1415-1427. */
AttackCopyResult CopyAttackDataAndDamage_FromCardID(uint8_t a, uint8_t d, uint8_t e)
{
	gb_write8(wSelectedAttack_ADDR, e);
	hTempCardIndex_ff9f = d;
	LoadCardDataToBuffer1_FromCardID(a);
	return CopyAttackDataAndDamage(e);
}

/* duel.asm:1621-1623. `scf` sets C, clears N/H, leaves Z untouched. */
uint8_t ReturnCarry(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}

/* duel.asm:1793-1803. f omitted: its last flag-setting instruction is inside
 * the opaque LoadCardDataToBuffer1_FromDeckIndex call. */
LoadEffectResult LoadNonPokemonCardEffectCommands(void)
{
	uint8_t idx = hTempCardIndex_ff9f;
	uint8_t b0, b1;

	(void)LoadCardDataToBuffer1_FromDeckIndex(idx);
	b0 = gb_read8(wLoadedCard1EffectCommands_ADDR);
	b1 = gb_read8((uint16_t)(wLoadedCard1EffectCommands_ADDR + 1u));
	gb_write8(wLoadedAttackEffectCommands_ADDR, b0);
	gb_write8((uint16_t)(wLoadedAttackEffectCommands_ADDR + 1u), b1);
	return (LoadEffectResult){b1, (uint16_t)(wLoadedCard1EffectCommands_ADDR + 1u),
				  (uint16_t)(wLoadedAttackEffectCommands_ADDR + 1u)};
}

/* duel.asm:1976-1988 / 1991-2006. a/f flow through the opaque HtimesL leaf and
 * are omitted. */
PowerModifierResult ApplyAttachedPlusPower(uint8_t b, uint16_t de)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t count = CountCardIDInLocation(b, PLUSPOWER, page).a;
	uint16_t product = (uint16_t)(count * 10u);

	return (PowerModifierResult){product, (uint16_t)(de + product)};
}

PowerModifierResult ApplyAttachedDefender(uint8_t b, uint16_t de)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t count = CountCardIDInLocation(b, DEFENDER, page).a;
	uint16_t product = (uint16_t)(count * 20u);

	return (PowerModifierResult){product, (uint16_t)(de - product)};
}

/* duel.asm:2273-2298. Exit d/e are genuine unpredictable loop residue
 * (clobbered by GetCardIDFromDeckIndex on every match) and omitted. */
DiscardIfInPlayResult MoveCardToDiscardPileIfInPlayArea(uint16_t de, uint8_t page)
{
	uint8_t c = (uint8_t)de;
	uint8_t b = (uint8_t)(de >> 8);

	for (uint8_t l = 0; l < DECK_SIZE; l++) {
		uint16_t loc_addr = (uint16_t)(((uint16_t)page << 8) | l);
		uint16_t id;

		if (!(gb_read8(loc_addr) & PLAY_AREA_MASK))
			continue;
		id = GetCardIDFromDeckIndex(l);
		if ((uint8_t)id != c)
			continue;
		if ((uint8_t)(id >> 8) != b)
			continue;
		PutCardInDiscardPile(l);
	}
	return (DiscardIfInPlayResult){DECK_SIZE, b, c, 0xC0u,
				       (uint16_t)(((uint16_t)page << 8) | DECK_SIZE)};
}

#define CARD_LOCATION_ARENA 0x10u
#define WEAKNESS  (1u << 1)
#define RESISTANCE (1u << 2)

uint16_t ApplyDamageModifiers_DamageToTarget(void)
{
	gb_write8(wDamageEffectiveness_ADDR, 0);

	uint8_t lo = gb_read8(wDamage_ADDR);
	uint8_t hi_byte = gb_read8((uint16_t)(wDamage_ADDR + 1u));
	if (!(hi_byte | lo))
		return 0;

	hTempPlayAreaLocation_ff9d = 0;
	uint16_t de = (uint16_t)((uint16_t)hi_byte << 8 | lo);

	if (hi_byte & 0x80u) {
		de &= (uint16_t)~0x8000u;
		gb_write8(wDamageEffectiveness_ADDR, 0);
		de = HandleDoubleDamageSubstatus(de);
	} else {
		de = HandleDoubleDamageSubstatus(de);
		if (!de)
			return 0;

		uint8_t color = GetPlayAreaCardColor(hTempPlayAreaLocation_ff9d);
		uint8_t wr = TranslateColorToWR(color);

		SwapTurn();
		uint8_t weakness = GetArenaCardWeakness();
		SwapTurn();
		if (weakness & wr) {
			de <<= 1;
			gb_write8(wDamageEffectiveness_ADDR, (uint8_t)(gb_read8(wDamageEffectiveness_ADDR) | WEAKNESS));
		}

		SwapTurn();
		uint8_t resistance = GetArenaCardResistance();
		SwapTurn();
		if (resistance & wr) {
			de = (uint16_t)(de - 30u);
			gb_write8(wDamageEffectiveness_ADDR, (uint8_t)(gb_read8(wDamageEffectiveness_ADDR) | RESISTANCE));
		}
	}

	{
		PowerModifierResult r = ApplyAttachedPlusPower(CARD_LOCATION_ARENA, de);
		de = r.de;
	}
	SwapTurn();
	{
		PowerModifierResult r = ApplyAttachedDefender(CARD_LOCATION_ARENA, de);
		de = r.de;
	}
	de = HandleDamageReduction(de);
	if (de & 0x8000u)
		de = 0;
	SwapTurn();
	return de;
}

uint16_t ApplyDamageModifiers_DamageToSelf(void)
{
	gb_write8(wDamageEffectiveness_ADDR, 0);

	uint8_t lo = gb_read8(wDamage_ADDR);
	uint8_t hi_byte = gb_read8((uint16_t)(wDamage_ADDR + 1u));
	uint8_t nonzero = (uint8_t)(hi_byte | lo);
	if (!nonzero)
		return 0;

	uint16_t de = (uint16_t)((uint16_t)hi_byte << 8 | lo);
	uint8_t color = GetArenaCardColor();
	uint8_t wr = TranslateColorToWR(color);

	uint8_t weakness = GetArenaCardWeakness();
	if (weakness & wr) {
		de <<= 1;
		gb_write8(wDamageEffectiveness_ADDR, (uint8_t)(gb_read8(wDamageEffectiveness_ADDR) | WEAKNESS));
	}
	uint8_t resistance = GetArenaCardResistance();
	if (resistance & wr) {
		de = (uint16_t)(de - 30u);
		gb_write8(wDamageEffectiveness_ADDR, (uint8_t)(gb_read8(wDamageEffectiveness_ADDR) | RESISTANCE));
	}

	{
		PowerModifierResult r = ApplyAttachedPlusPower(CARD_LOCATION_ARENA, de);
		de = r.de;
	}
	{
		PowerModifierResult r = ApplyAttachedDefender(CARD_LOCATION_ARENA, de);
		de = r.de;
	}


	if (de & 0x8000u)
		return 0;
	return de;
}
uint8_t GetPlayAreaCardRetreatCost(void)
{
	uint8_t slot = hTempPlayAreaLocation_ff9d;
	uint8_t deck_idx = GetTurnDuelistVariable((uint8_t)(slot + 0xBBu)).a;
	LoadCardDataToBuffer1_FromDeckIndex(deck_idx);
	return GetLoadedCard1RetreatCost();
}

#define WAS_KNOCKED_OUT_TEXT 0x0081u

uint8_t DrawWideTextBox_WaitForInput_ReturnCarry(uint16_t hl)
{
	return (uint8_t)(DrawWideTextBox_WaitForInput(hl).f | 0x10u);
}

uint8_t PrintKnockedOut(void)
{
	uint8_t card_id = wTempNonTurnDuelistCardID;
	LoadCardDataToBuffer1_FromCardID(card_id);
	uint16_t name = (uint16_t)(gb_read8(wLoadedCard1Name_ADDR)
		| (uint16_t)gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)) << 8);
	LoadTxRam2(name);
	DrawWideTextBox_PrintText(WAS_KNOCKED_OUT_TEXT);
	DoAFrames(40);
	return 0x90u;
}
KnockoutCheckResult PrintPlayAreaCardKnockedOutIfNoHP(uint8_t a)
{
	uint8_t e_val = a;
	uint8_t hp = GetTurnDuelistVariable((uint8_t)(a + DUELVARS_ARENA_CARD_HP)).a;
	if (hp)
		return (KnockoutCheckResult){hp, 0x00u};
	uint8_t saved = wTempNonTurnDuelistCardID;
	uint8_t deck_idx = GetTurnDuelistVariable((uint8_t)(e_val + DUELVARS_ARENA_CARD)).a;
	LoadCardDataToBuffer1_FromDeckIndex(deck_idx);
	wTempNonTurnDuelistCardID = wLoadedCard1ID;
	PrintKnockedOut();
	wTempNonTurnDuelistCardID = saved;
	return (KnockoutCheckResult){saved, 0x90u};
}


DuelRoutineResult UpdateArenaCardIDsAndClearTwoTurnDuelVars(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	hTempCardIndex_ff9f = arena.a;
	uint16_t card_id = GetCardIDFromDeckIndex(arena.a);
	wTempTurnDuelistCardID = (uint8_t)card_id;
	SwapTurn();
	arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	card_id = GetCardIDFromDeckIndex(arena.a);
	wTempNonTurnDuelistCardID = (uint8_t)card_id;
	SwapTurn();
	wSentAttackDataToLinkOpponent = 0;
	wStatusConditionQueueIndex = 0;
	wEffectFailed = 0;
	wIsDamageToSelf = 0;
	wDefendingWasForcedToSwitch = 0;
	wMetronomeEnergyCost = 0;
	wNoEffectFromWhichStatus = 0;
	ClearNonTurnTemporaryDuelvars_CopyStatus();
	(void)a;
	(void)e;
	(void)f;
	DuelistVarResult clear_start =
		GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX);
	return (DuelRoutineResult){0, 0x80u, b, c,
		(uint8_t)(card_id >> 8), (uint8_t)card_id,
		(uint16_t)(clear_start.hl + 7u)};
}

DuelRoutineResult ClearNonTurnTemporaryDuelvars_ResetCarry(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	ClearNonTurnTemporaryDuelvars();
	(void)a;
	(void)f;
	(void)hl;
	return (DuelRoutineResult){0, 0x80u, b, c, d, e,
		(uint16_t)(GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX).hl + 7u)};
}

uint8_t PrintKnockedOutIfHLZero(uint16_t hl)
{
	if (gb_read8(hl) != 0)
		return 0x00u;
	(void)PrintKnockedOut();
	return 0x90u;
}

/* >>> factory GetFirstSetPrizeCard */
/* duel.asm:2134-2188 */
uint8_t GetFirstSetPrizeCard(uint8_t a)
{
	uint8_t c = a;
	uint8_t prizes = gb_read8((uint16_t)((uint16_t)hWhoseTurn << 8 | DUELVARS_PRIZES));
	uint8_t remaining = PRIZES_6;

	for (;;) {
		uint8_t mask = 1u;
		uint8_t shifts = c;
		while (shifts != 0u) {
			mask = (uint8_t)(mask << 1);
			shifts--;
		}
		if ((mask & prizes) != 0u)
			return c;
		remaining--;
		if (remaining == 0u)
			return 0u;
		c++;
		if (c == PRIZES_6)
			c = 0u;
	}
}
/* <<< factory GetFirstSetPrizeCard */

/* >>> factory DrawCheckMenuCursor_YourOrOppPlayArea */
/* duel.asm:1347-1367 */
TempListResult DrawCheckMenuCursor_YourOrOppPlayArea(uint8_t a)
{
	uint8_t tile = a;
	uint16_t hl = (uint16_t)(((uint16_t)wCheckMenuCursorXPosition << 8) | 10u);
	uint8_t b, c;
	TempListResult r;

	hl = HtimesL(hl);
	b = (uint8_t)((uint8_t)hl + 1u);
	c = (uint8_t)((uint8_t)(wCheckMenuCursorYPosition << 1) + 14u);
	WriteByteToBGMap0(tile, b, c);
	r.a = tile;
	r.f = (uint8_t)(tile ? 0x00u : 0x80u);
	return r;
}
/* <<< factory DrawCheckMenuCursor_YourOrOppPlayArea */

/* >>> factory ZeroObjectPositionsWithCopyToggleOn */
/* duel.asm:1893-1897 */
void ZeroObjectPositionsWithCopyToggleOn(void)
{
	ZeroObjectPositions();
	wVBlankOAMCopyToggle = TRUE_8BF2;
}
/* <<< factory ZeroObjectPositionsWithCopyToggleOn */

/* >>> factory YourOrOppPlayAreaScreen_HandleInput */
/* duel.asm:1701-1943 */
void YourOrOppPlayAreaScreen_HandleInput(void)
{
	uint8_t next = 0u;

	for (;;) {
		next = 0u;
		wMenuInputSFX = 0u;
		uint8_t pos = wYourOrOppPlayAreaCurPosition;
		wPrizeCardCursorTemporaryPosition = pos;
		uint16_t hl = HtimesL((uint16_t)((uint16_t)YOPA_ITEM_LEN << 8 | pos));
		hl = (uint16_t)(hl + yoopa_table_ptr());

		uint8_t dpad = hDPadHeld;
		uint8_t moved = 0u;
		uint8_t nv = 0u;
		if (dpad != 0u) {
			uint16_t tbl = (uint16_t)(hl + 3u);
			if (dpad & YOPA_PAD_UP) {
				nv = gb_read8(tbl);
				moved = 1u;
			} else {
				tbl = (uint16_t)(tbl + 1u);
				if (dpad & YOPA_PAD_DOWN) {
					nv = gb_read8(tbl);
					moved = 1u;
				} else {
					tbl = (uint16_t)(tbl + 1u);
					if (dpad & YOPA_PAD_RIGHT) {
						nv = gb_read8(tbl);
						moved = 1u;
					} else {
						tbl = (uint16_t)(tbl + 1u);
						if (dpad & YOPA_PAD_LEFT) {
							nv = gb_read8(tbl);
							moved = 1u;
						}
					}
				}
			}
		}

		if (!moved)
			break;

		wYourOrOppPlayAreaCurPosition = nv;
		if (nv >= 0x08u) {
			next = 1u;
			break;
		}

		uint8_t a = nv;
		uint8_t restart = 0u;
		for (;;) {
			uint8_t b = 1u;
			while (a != 0u) {
				b = (uint8_t)(b << 1);
				a--;
			}
			if ((uint8_t)(wDuelInitialPrizesUpperBitsSet & b) != 0u) {
				next = 1u;
				break;
			}
			if (wPrizeCardCursorTemporaryPosition != 0x06u) {
				restart = 1u;
				break;
			}
			uint8_t dp = hDPadHeld;
			if (!(dp & YOPA_PAD_RIGHT) && !(dp & YOPA_PAD_LEFT)) {
				restart = 1u;
				break;
			}
			if (wDuelInitialPrizes >= YOPA_PRIZES_5) {
				next = 1u;
				break;
			}
			if (wYourOrOppPlayAreaCurPosition == 5u)
				wYourOrOppPlayAreaCurPosition = 3u;
			else
				wYourOrOppPlayAreaCurPosition = 2u;
			if (wDuelInitialPrizes < YOPA_PRIZES_3)
				wYourOrOppPlayAreaCurPosition = (uint8_t)(wYourOrOppPlayAreaCurPosition - 2u);
			a = wYourOrOppPlayAreaCurPosition;
			wPrizeCardCursorTemporaryPosition = a;
		}
		if (restart)
			continue;
		break;
	}

	if (next) {
		wMenuInputSFX = YOPA_SFX_CURSOR;
		wCheckMenuCursorBlinkCounter = 0u;
	}

	uint8_t keys = (uint8_t)(hKeysPressed & (YOPA_PAD_A | YOPA_PAD_B));
	if (keys != 0u) {
		if (keys & YOPA_PAD_A) {
			yoopa_draw_cursor();
			PlaySFXConfirmOrCancel(YOPA_MENU_CONFIRM);
		} else {
			PlaySFXConfirmOrCancel(YOPA_MENU_CANCEL);
		}
		return;
	}

	if (wMenuInputSFX != 0u)
		PlaySFX(wMenuInputSFX);

	uint8_t cnt = wCheckMenuCursorBlinkCounter;
	wCheckMenuCursorBlinkCounter = (uint8_t)(cnt + 1u);
	if ((uint8_t)(cnt & YOPA_BLINK_MASK) != 0u)
		return;
	if (wCheckMenuCursorBlinkCounter & YOPA_BLINK_BIT) {
		ZeroObjectPositionsWithCopyToggleOn();
		return;
	}
	yoopa_draw_cursor();
}
/* <<< factory YourOrOppPlayAreaScreen_HandleInput */

/* >>> factory DrawPlayArea_BenchCards */
/* duel.asm:877-1029 */
void DrawPlayArea_BenchCards(uint8_t c, uint8_t d, uint8_t e)
{
	uint8_t page = wCheckMenuPlayAreaWhichDuelist;
	uint16_t src;
	uint8_t count, n, b;

	if (page != wCheckMenuPlayAreaWhichLayout) {
		d = (uint8_t)(d + (uint8_t)(c * 4u));
		c = (uint8_t)(0u - c);
		page = wCheckMenuPlayAreaWhichDuelist;
	}

	count = gb_read8((uint16_t)(((uint16_t)page << 8) | BPA_DUELVARS_NUM_POKEMON));
	src = (uint16_t)(((uint16_t)page << 8) | BPA_DUELVARS_BENCH1_STAGE);

	for (;;) {
		uint8_t stage, tile;

		count = (uint8_t)(count - 1u);
		if (count == 0u)
			break;
		stage = gb_read8(src);
		src = (uint16_t)(src + 1u);
		tile = (uint8_t)((uint8_t)(stage << 2) + BPA_TILE_STAGE_BASE);
		FillRectangle(tile, 2u, 2u, (uint16_t)((uint16_t)d << 8 | e),
			BPA_RECT_STEPS_TILES);
		if (wConsole == BPA_CONSOLE_CGB) {
			uint8_t color = (tile == BPA_TILE_TWO_STAGE
				|| tile == BPA_TILE_TWO_STAGE_ALT) ? 0x01u : 0x02u;

			gb_write8(BPA_RVBK, 1u);
			FillRectangle(color, 2u, 2u,
				(uint16_t)((uint16_t)d << 8 | e), BPA_RECT_STEPS_FLAT);
			gb_write8(BPA_RVBK, 0u);
		}
		d = (uint8_t)(d + c);
	}

	count = gb_read8((uint16_t)(((uint16_t)page << 8) | BPA_DUELVARS_NUM_POKEMON));
	n = (uint8_t)(BPA_MAX_PLAY_AREA_POKEMON - count);
	if (n == 0u)
		return;

	b = (uint8_t)(n + 1u);
	for (;;) {
		b = (uint8_t)(b - 1u);
		if (b == 0u)
			break;
		FillRectangle(BPA_TILE_EMPTY_SLOT, 2u, 2u,
			(uint16_t)((uint16_t)d << 8 | e), BPA_RECT_STEPS_TILES);
		if (wConsole == BPA_CONSOLE_CGB) {
			gb_write8(BPA_RVBK, 1u);
			FillRectangle(0x02u, 2u, 2u,
				(uint16_t)((uint16_t)d << 8 | e), BPA_RECT_STEPS_FLAT);
			gb_write8(BPA_RVBK, 0u);
		}
		d = (uint8_t)(d + c);
	}
}
/* <<< factory DrawPlayArea_BenchCards */

/* >>> factory EraseCheckMenuCursor_YourOrOppPlayArea */
/* duel.asm:1340-1341 */
TempListResult EraseCheckMenuCursor_YourOrOppPlayArea(void)
{
	return DrawCheckMenuCursor_YourOrOppPlayArea(BPA_SYM_SPACE);
}
/* <<< factory EraseCheckMenuCursor_YourOrOppPlayArea */

/* >>> factory LoadCursorTile */
/* duel.asm:1687-1700. Copies the 16-byte cursor tile into v0Tiles0 and falls
 * through into YourOrOppPlayAreaScreen_HandleInput. The .tile_data label is a
 * ROM literal in this routine's own bank, so it is materialized as a C table
 * and written byte-for-byte to the same destination. */
void LoadCursorTile(void)
{
	uint16_t dst = V0_TILES0;
	uint8_t i;

	for (i = 0u; i < 16u; i++)
		gb_write8((uint16_t)(dst + i), kCursorTileData[i]);
	YourOrOppPlayAreaScreen_HandleInput();
}
/* <<< factory LoadCursorTile */

/* >>> factory Func_8bf2 */
/* duel.asm:2073-2118. Walks the turn-check duelist's DUELVARS_PRIZES bitmask
 * one bit per initial prize, drawing tile $AC (both branches load the same
 * tile) at the coordinate pair read from the entry hl table. On CGB the same
 * rectangle is redrawn in VRAM bank 1 with attribute $02. Entry a/b are dead;
 * exit a/f are the shifted bitmask and the last `srl a` flags (or the entry
 * flags when the loop body never runs), b is the terminating counter, d/e the
 * last coordinate pair read, hl the advanced table pointer, c preserved. */
PrizeTileResult Func_8bf2(uint8_t f, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t page = wCheckMenuPlayAreaWhichDuelist;
	uint8_t saved_a = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_PRIZES));
	uint8_t saved_f = f;
	uint8_t b = 0u;

	for (;;) {
		uint8_t carry;
		uint16_t de;

		b = (uint8_t)(b + 1u);
		if ((uint8_t)(wDuelInitialPrizes + 1u) == b)
			break;

		carry = (uint8_t)(saved_a & 1u);
		saved_a = (uint8_t)(saved_a >> 1);
		saved_f = (uint8_t)((saved_a ? 0u : 0x80u) | (carry ? 0x10u : 0u));

		e = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		d = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		de = (uint16_t)(((uint16_t)d << 8) | e);

		FillRectangle(PRIZE_TILE, 1u, 1u, de, 0x0000u);
		if (wConsole == CONSOLE_CGB) {
			gb_write8(R_VBK, 1u);
			FillRectangle(PRIZE_TILE_CGB_ATTR, 1u, 1u, de, 0x0000u);
			gb_write8(R_VBK, 0u);
		}
	}

	return (PrizeTileResult){saved_a, saved_f, b, d, e, hl};
}
/* <<< factory Func_8bf2 */

/* >>> factory GetDuelInitialPrizesUpperBitsSet */
void GetDuelInitialPrizesUpperBitsSet(void)
{
	uint8_t a = wDuelInitialPrizes;
	uint8_t b = 0x01u;
	while (a != 0u) {
		b = (uint8_t)(b << 1);
		--a;
	}
	--b;
	a = (uint8_t)(b | 0xC0u);
	wDuelInitialPrizesUpperBitsSet = a;
}
/* <<< factory GetDuelInitialPrizesUpperBitsSet */

/* >>> factory DrawYourOrOppPlayArea_DrawArrows */
void DrawYourOrOppPlayArea_DrawArrows(uint8_t a, uint8_t b)
{
	uint8_t tile = b;
	switch (a) {
	case 0:
		WriteByteToBGMap0(tile, 5u, 5u);
		WriteByteToBGMap0(tile, 0u, 10u);
		WriteByteToBGMap0(tile, 4u, 10u);
		WriteByteToBGMap0(tile, 8u, 10u);
		WriteByteToBGMap0(tile, 12u, 10u);
		WriteByteToBGMap0(tile, 16u, 10u);
		break;
	case 1:
		WriteByteToBGMap0(tile, 14u, 7u);
		break;
	case 2:
		WriteByteToBGMap0(tile, 14u, 5u);
		break;
	case 3:
		WriteByteToBGMap0(tile, 5u, 7u);
		WriteByteToBGMap0(tile, 0u, 3u);
		WriteByteToBGMap0(tile, 4u, 3u);
		WriteByteToBGMap0(tile, 8u, 3u);
		WriteByteToBGMap0(tile, 12u, 3u);
		WriteByteToBGMap0(tile, 16u, 3u);
		break;
	case 4:
		WriteByteToBGMap0(tile, 0u, 5u);
		break;
	case 5:
		WriteByteToBGMap0(tile, 0u, 8u);
		break;
	default:
		break;
	}
}
/* <<< factory DrawYourOrOppPlayArea_DrawArrows */

/* >>> factory DrawYourOrOppPlayArea_EraseArrows */
void DrawYourOrOppPlayArea_EraseArrows(void)
{
	uint8_t a = wYourOrOppPlayAreaLastCursorPosition;
	DrawYourOrOppPlayArea_DrawArrows(a, SYM_SPACE);
}
/* <<< factory DrawYourOrOppPlayArea_EraseArrows */

/* >>> factory DrawYourOrOppPlayArea_RefreshArrows */
void DrawYourOrOppPlayArea_RefreshArrows(uint8_t a)
{
	uint8_t cursor_x = gb_read8(wCheckMenuCursorXPosition_ADDR);
	uint8_t cursor_y = gb_read8(wCheckMenuCursorYPosition_ADDR);
	uint8_t position = (uint8_t)((uint8_t)(cursor_y << 1u) + cursor_x + (uint8_t)(a * 3u));
	if (position != gb_read8(wYourOrOppPlayAreaLastCursorPosition_ADDR)) {
		DrawYourOrOppPlayArea_EraseArrows();
		gb_write8(wYourOrOppPlayAreaLastCursorPosition_ADDR, position);
		DrawYourOrOppPlayArea_DrawArrows(position, 0xF8u);
	}
}
/* <<< factory DrawYourOrOppPlayArea_RefreshArrows */

/* >>> factory SendAttackDataToLinkOpponent */
void SendAttackDataToLinkOpponent(void)
{
	if (wSentAttackDataToLinkOpponent != 0u)
		return;
	uint8_t saved_temp = hTemp_ffa0;
	uint8_t saved_card = hTempCardIndex_ff9f;
	wSentAttackDataToLinkOpponent = TRUE;
	hTempCardIndex_ff9f = wPlayerAttackingCardIndex;
	hTemp_ffa0 = wPlayerAttackingAttackIndex;
	SetOppActionSerialSendResult action =
		SetOppAction_SerialSendDuelData(OPPACTION_BEGIN_ATTACK, 0u);
	(void)ExchangeRNG(0u, 0u, action.de, 0u);
	hTempCardIndex_ff9f = saved_card;
	hTemp_ffa0 = saved_temp;
}
/* <<< factory SendAttackDataToLinkOpponent */

/* >>> factory DrawPlayArea_PrizeCards */
void DrawPlayArea_PrizeCards(uint16_t hl)
{
	GetDuelInitialPrizesUpperBitsSet();
	uint8_t page = wCheckMenuPlayAreaWhichDuelist;
	uint16_t prize_addr = (uint16_t)(((uint16_t)page << 8) | DUELVARS_PRIZES);
	uint8_t prize_bits = gb_read8(prize_addr);
	uint8_t count = wDuelInitialPrizes;
	for (uint8_t b = 0u; b < count; ++b) {
		uint8_t taken = (uint8_t)(prize_bits & 1u);
		prize_bits = (uint8_t)(prize_bits >> 1);
		uint8_t tile = taken != 0u ? 0xDCu : 0xE0u;
		uint8_t x = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint8_t y = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint16_t de = (uint16_t)(((uint16_t)y << 8) | x);
		FillRectangle(tile, 2u, 2u, de, 0x0102u);
		if (wConsole == CONSOLE_CGB) {
			gb_write8(0xFF4Fu, 1u);
			FillRectangle(0x02u, 2u, 2u, de, 0x0000u);
			gb_write8(0xFF4Fu, 0u);
		}
	}
}
/* <<< factory DrawPlayArea_PrizeCards */

/* >>> factory _DrawPlayersPrizeAndBenchCards */
void _DrawPlayersPrizeAndBenchCards(void)
{
	static const uint8_t player_coords[] = {6u, 0u, 6u, 2u, 8u, 0u, 8u, 2u, 10u, 0u, 10u, 2u};
	static const uint8_t opponent_coords[] = {4u, 18u, 4u, 16u, 2u, 18u, 2u, 16u, 0u, 18u, 0u, 16u};
	const uint16_t coords_addr = 0xC100u;
	for (uint8_t i = 0u; i < sizeof(player_coords); ++i)
		gb_write8((uint16_t)(coords_addr + i), player_coords[i]);
	gb_write8(wTileMapFill_ADDR, 0u);
	ZeroObjectPositions();
	wVBlankOAMCopyToggle = TRUE;
	DoFrame();
	EmptyScreen();
	(void)LoadSymbolsFont();
	(void)LoadDeckAndDiscardPileIcons();
	wCheckMenuPlayAreaWhichDuelist = PLAYER_TURN;
	wCheckMenuPlayAreaWhichLayout = PLAYER_TURN;
	DrawPlayArea_PrizeCards(coords_addr);
	DrawPlayArea_BenchCards(3u, 5u, 10u);
	for (uint8_t i = 0u; i < sizeof(opponent_coords); ++i)
		gb_write8((uint16_t)(coords_addr + i), opponent_coords[i]);
	wCheckMenuPlayAreaWhichDuelist = OPPONENT_TURN;
	DrawPlayArea_PrizeCards(coords_addr);
	DrawPlayArea_BenchCards(3u, 1u, 0u);
}
/* <<< factory _DrawPlayersPrizeAndBenchCards */

/* >>> factory DrawPlayArea_HandText */
DrawPlayArea_HandTextResult DrawPlayArea_HandText(uint8_t b, uint8_t c, uint16_t hl)
{
	uint8_t d = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	uint8_t e = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	uint16_t saved_hl = hl;

	InitTextPrinting(d, e);
	(void)ProcessTextFromID(HandText_2);

	CalculateOnesAndTensDigits(b);
	uint8_t ones = gb_read8(wDecimalDigitsSymbols_ADDR);
	uint8_t tens = gb_read8((uint16_t)(wDecimalDigitsSymbols_ADDR + 1u));
	b = ones;

	uint16_t p = wDefaultText_ADDR;
	gb_write8(p, TX_SYMBOL); p++;
	gb_write8(p, SYM_CROSS); p++;
	gb_write8(p, TX_SYMBOL); p++;
	gb_write8(p, tens); p++;
	gb_write8(p, TX_SYMBOL); p++;
	gb_write8(p, b); p++;
	gb_write8(p, TX_END);

	uint16_t text_hl = wDefaultText_ADDR;
	ProcessText(&text_hl);

	return (DrawPlayArea_HandTextResult){b, c, saved_hl};
}
/* <<< factory DrawPlayArea_HandText */

/* >>> factory DrawPlayArea_IconWithValue */
void DrawPlayArea_IconWithValue(uint8_t a, uint8_t b, uint16_t *hl)
{
	uint16_t coordinates = *hl;
	uint8_t d = gb_read8(coordinates++);
	uint8_t e = gb_read8(coordinates++);
	*hl = coordinates;
	uint16_t de = (uint16_t)(((uint16_t)d << 8) | e);
	FillRectangle(a, 2u, 2u, de, 0x0102u);

	if (wConsole == CONSOLE_CGB) {
		hBankVRAM = 1u;
		gb_write8(0xFF4Fu, 1u);
		FillRectangle(0x02u, 2u, 2u, de, 0x0000u);
		hBankVRAM = 0u;
		gb_write8(0xFF4Fu, 0u);
	}

	d = (uint8_t)(d + 2u);
	e = (uint8_t)(e + 1u);
	InitTextPrinting(d, e);
	CalculateOnesAndTensDigits(b);
	uint8_t ones = gb_read8(wDecimalDigitsSymbols_ADDR);
	uint8_t tens = gb_read8((uint16_t)(wDecimalDigitsSymbols_ADDR + 1u));

	gb_write8(wDefaultText_ADDR, TX_SYMBOL);
	gb_write8((uint16_t)(wDefaultText_ADDR + 1u), SYM_CROSS);
	gb_write8((uint16_t)(wDefaultText_ADDR + 2u), TX_SYMBOL);
	gb_write8((uint16_t)(wDefaultText_ADDR + 3u), tens);
	gb_write8((uint16_t)(wDefaultText_ADDR + 4u), TX_SYMBOL);
	gb_write8((uint16_t)(wDefaultText_ADDR + 5u), ones);
	gb_write8((uint16_t)(wDefaultText_ADDR + 6u), TX_END);

	uint16_t text_ptr = wDefaultText_ADDR;
	ProcessText(&text_ptr);
}
/* <<< factory DrawPlayArea_IconWithValue */

/* >>> factory SaveDuelStateToSRAM */
void SaveDuelStateToSRAM(void)
{
	BankswitchSRAM(sBackupCurrentDuel_BANK);
	SaveDuelData();
	BankswitchSRAM(0u);
	EnableSRAM();
	uint8_t old = gb_read8(s0a008_ADDR);
	gb_write8(s0a008_ADDR, (uint8_t)(old + 1u));
	DisableSRAM();
	uint8_t masked = (uint8_t)(old & 0x03u);
	uint16_t buffer = (uint16_t)(sDuelBuffer0_ADDR + (uint16_t)masked * 0x0400u);
	BankswitchSRAM(sDuelBuffer0_BANK);

	DuelistVarResult r1 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint8_t turnCardId = (uint8_t)GetCardIDFromDeckIndex(r1.a);
	wTempTurnDuelistCardID = turnCardId;
	SwapTurn();
	DuelistVarResult r2 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint8_t nonTurnCardId = (uint8_t)GetCardIDFromDeckIndex(r2.a);
	wTempNonTurnDuelistCardID = nonTurnCardId;
	SwapTurn();

	EnableSRAM();
	gb_write8(buffer, wDuelTurns);
	gb_write8((uint16_t)(buffer + 1u), wTempNonTurnDuelistCardID);
	gb_write8((uint16_t)(buffer + 2u), wTempTurnDuelistCardID);
	DisableSRAM();

	uint16_t de = (uint16_t)(buffer + 0x10u);
	SaveDuelDataToDE(de);
	BankswitchSRAM(0u);
}
/* <<< factory SaveDuelStateToSRAM */

/* >>> factory DisplayCheckMenuCursor_YourOrOppPlayArea */
TempListResult DisplayCheckMenuCursor_YourOrOppPlayArea(void)
{
	return DrawCheckMenuCursor_YourOrOppPlayArea(SYM_CURSOR_R);
}
/* <<< factory DisplayCheckMenuCursor_YourOrOppPlayArea */

/* >>> factory HandleCheckMenuInput_YourOrOppPlayArea */
TempListResult HandleCheckMenuInput_YourOrOppPlayArea(void)
{
	gb_write8(wMenuInputSFX_ADDR, 0u);
	uint8_t d = gb_read8(wCheckMenuCursorXPosition_ADDR);
	uint8_t e = gb_read8(wCheckMenuCursorYPosition_ADDR);

	uint8_t dpad = gb_read8(hDPadHeld_ADDR);
	if (dpad != 0u) {
		uint8_t latch = (uint8_t)(gb_read8(WCE5E_ADDR) & 0x80u);
		if (latch == 0u) {
			uint8_t horiz;
			if (dpad & (1u << B_PAD_LEFT)) {
				horiz = 1u;
			} else if (dpad & (1u << B_PAD_RIGHT)) {
				horiz = 1u;
			} else {
				horiz = 0u;
			}
			if (horiz) {
				uint8_t low7 = (uint8_t)(gb_read8(WCE5E_ADDR) & 0x7Fu);
				if (low7 != 0u) {
					if (e != 0u) {
						e = (uint8_t)(e + 1u);
					}
				} else {
					if (e == 0u) {
						e = (uint8_t)(e - 1u);
					}
				}
				d = (uint8_t)(d ^ 0x01u);
				goto erase;
			}
		}
		if (dpad & (1u << B_PAD_UP)) {
			if (d != 0u) {
				d = (uint8_t)(d - 1u);
			}
			e = (uint8_t)(e ^ 0x01u);
			goto erase;
		}
		if (dpad & (1u << B_PAD_DOWN)) {
			if (d != 0u) {
				d = (uint8_t)(d - 1u);
			}
			e = (uint8_t)(e ^ 0x01u);
			goto erase;
		}
		goto skip;

	erase:
		gb_write8(wMenuInputSFX_ADDR, SFX_CURSOR);
		(void)EraseCheckMenuCursor_YourOrOppPlayArea();
		gb_write8(wCheckMenuCursorXPosition_ADDR, d);
		gb_write8(wCheckMenuCursorYPosition_ADDR, e);
		gb_write8(wCheckMenuCursorBlinkCounter_ADDR, 0u);
	}

skip:
	uint8_t keys = (uint8_t)(gb_read8(hKeysPressed_ADDR) & (PAD_A | PAD_B));
	if (keys != 0u) {
		if (keys & PAD_A) {
			(void)DisplayCheckMenuCursor_YourOrOppPlayArea();
			PlaySFXConfirmOrCancel(MENU_CONFIRM);
			return (TempListResult){MENU_CONFIRM, 0x10u};
		}
		PlaySFXConfirmOrCancel(MENU_CANCEL);
		return (TempListResult){MENU_CANCEL, 0x10u};
	}

	uint8_t sfx = gb_read8(wMenuInputSFX_ADDR);
	if (sfx != 0u) {
		PlaySFX(sfx);
	}

	uint8_t old_counter = gb_read8(wCheckMenuCursorBlinkCounter_ADDR);
	uint8_t new_counter = (uint8_t)(old_counter + 1u);
	gb_write8(wCheckMenuCursorBlinkCounter_ADDR, new_counter);
	uint8_t masked = (uint8_t)(old_counter & CURSOR_BLINK_PERIOD_MASK);
	if (masked != 0u) {
		return (TempListResult){masked, 0x20u};
	}

	if ((new_counter & (1u << B_CURSOR_BLINK_PERIOD)) == 0u) {
		return DrawCheckMenuCursor_YourOrOppPlayArea(SYM_CURSOR_R);
	}
	return EraseCheckMenuCursor_YourOrOppPlayArea();
}
/* <<< factory HandleCheckMenuInput_YourOrOppPlayArea */

/* >>> factory DrawYourOrOppPlayArea_Icons */
void DrawYourOrOppPlayArea_Icons(uint8_t a)
{
	uint16_t coords = (a != 0u) ? OPPONENT_ICON_COORDS : PLAYER_ICON_COORDS;
	uint8_t page = wCheckMenuPlayAreaWhichDuelist;

	uint8_t hand_count = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_IN_HAND));
	DrawPlayArea_HandTextResult r1 = DrawPlayArea_HandText(hand_count, 0u, coords);
	coords = r1.hl;

	page = wCheckMenuPlayAreaWhichDuelist;
	uint8_t not_in_deck = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK));
	uint8_t deck_count = (uint8_t)(DECK_SIZE - not_in_deck);
	DrawPlayArea_IconWithValue(0xD4u, deck_count, &coords);

	page = wCheckMenuPlayAreaWhichDuelist;
	uint8_t discard_count = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE));
	DrawPlayArea_IconWithValue(0xD8u, discard_count, &coords);
}
/* <<< factory DrawYourOrOppPlayArea_Icons */

/* >>> factory DrawInPlayArea_Icons */
void DrawInPlayArea_Icons(uint16_t hl)
{
	uint8_t page = hWhoseTurn;
	uint8_t hand_count = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_IN_HAND));
	DrawPlayArea_HandTextResult r1 = DrawPlayArea_HandText(hand_count, 0u, hl);
	uint16_t coords = r1.hl;

	page = hWhoseTurn;
	uint8_t not_in_deck = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK));
	uint8_t deck_count = (uint8_t)(DECK_SIZE - not_in_deck);
	DrawPlayArea_IconWithValue(0xD4u, deck_count, &coords);

	page = hWhoseTurn;
	uint8_t discard_count = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE));
	DrawPlayArea_IconWithValue(0xD8u, discard_count, &coords);
}
/* <<< factory DrawInPlayArea_Icons */

/* >>> factory DisplayUsePokemonPowerScreen_WaitForInput */
uint8_t DisplayUsePokemonPowerScreen_WaitForInput(uint16_t hl)
{
	DisplayUsePokemonPowerScreen();
	return DrawWideTextBox_WaitForInput_ReturnCarry(hl);
}
/* <<< factory DisplayUsePokemonPowerScreen_WaitForInput */

/* >>> factory _DrawPlayAreaToPlacePrizeCards */
void _DrawPlayAreaToPlacePrizeCards(void)
{
	gb_write8(wTileMapFill_ADDR, 0u);
	ZeroObjectPositions();
	EmptyScreen();
	(void)LoadSymbolsFont();
	(void)LoadPlacingThePrizesScreenTiles();

	uint8_t turn = gb_read8(hWhoseTurn_ADDR);
	gb_write8(wCheckMenuPlayAreaWhichLayout_ADDR, turn);
	gb_write8(wCheckMenuPlayAreaWhichDuelist_ADDR, turn);

	DrawPlayArea_BenchCards(3u, 0u, 10u);

	uint16_t coords = PLAYER_ICON_COORDINATES_ADDR;
	uint8_t page = gb_read8(wCheckMenuPlayAreaWhichDuelist_ADDR);
	uint8_t hand_count = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_IN_HAND));
	DrawPlayArea_HandTextResult r1 = DrawPlayArea_HandText(hand_count, 0u, coords);
	coords = r1.hl;
	page = gb_read8(wCheckMenuPlayAreaWhichDuelist_ADDR);
	uint8_t not_in_deck = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK));
	uint8_t deck_count = (uint8_t)(DECK_SIZE - not_in_deck);
	DrawPlayArea_IconWithValue(0xD4u, deck_count, &coords);
	page = gb_read8(wCheckMenuPlayAreaWhichDuelist_ADDR);
	uint8_t discard_count = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE));
	DrawPlayArea_IconWithValue(0xD8u, discard_count, &coords);

	FillRectangle(0xA0u, 4u, 3u, 0x0806u, 0x0104u);

	SwapTurn();
	gb_write8(wIsSwapTurnPending_ADDR, TRUE);
	turn = gb_read8(hWhoseTurn_ADDR);
	gb_write8(wCheckMenuPlayAreaWhichDuelist_ADDR, turn);

	DrawPlayArea_BenchCards(3u, 6u, 0u);

	coords = OPP_ICON_COORDINATES_ADDR;
	page = gb_read8(wCheckMenuPlayAreaWhichDuelist_ADDR);
	hand_count = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_IN_HAND));
	r1 = DrawPlayArea_HandText(hand_count, 0u, coords);
	coords = r1.hl;
	page = gb_read8(wCheckMenuPlayAreaWhichDuelist_ADDR);
	not_in_deck = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK));
	deck_count = (uint8_t)(DECK_SIZE - not_in_deck);
	DrawPlayArea_IconWithValue(0xD4u, deck_count, &coords);
	page = gb_read8(wCheckMenuPlayAreaWhichDuelist_ADDR);
	discard_count = gb_read8((uint16_t)(((uint16_t)page << 8) | DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE));
	DrawPlayArea_IconWithValue(0xD8u, discard_count, &coords);

	FillRectangle(0xA0u, 4u, 3u, 0x0803u, 0x0104u);
	SwapTurn();
}
/* <<< factory _DrawPlayAreaToPlacePrizeCards */

/* >>> factory UsePokemonPower */
UsePokemonPowerResult UsePokemonPower(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	ResetAttackAnimationIsPlaying();
	TryExecuteEffectCommandFunctionResult initial = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_INITIAL_EFFECT_2);
	a = initial.a;
	f = initial.f;
	c = initial.c;
	hl = initial.hl;
	if ((f & 0x10u) != 0u) {
		f = DisplayUsePokemonPowerScreen_WaitForInput(hl);
		return (UsePokemonPowerResult){a, f, b, c, d, e, (uint16_t)hl};
	}
	TryExecuteEffectCommandFunctionResult selection = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_REQUIRE_SELECTION);
	a = selection.a;
	f = selection.f;
	c = selection.c;
	hl = selection.hl;
	if ((f & 0x10u) != 0u) {
		f = ReturnCarry(f);
		return (UsePokemonPowerResult){a, f, b, c, d, e, (uint16_t)hl};
	}
	SetOppActionSerialSendResult sent = SetOppAction_SerialSendDuelData(OPPACTION_USE_PKMN_POWER, (uint16_t)((uint16_t)d << 8 | e));
	a = sent.a;
	f = sent.f;
	d = (uint8_t)(sent.de >> 8);
	e = (uint8_t)sent.de;
	ExchangeRNGResult rng = ExchangeRNG(b, c, sent.de, hl);
	a = rng.a;
	b = rng.b;
	c = rng.c;
	f = rng.f;
	hl = rng.hl;
	d = (uint8_t)(rng.de >> 8);
	e = (uint8_t)rng.de;
	sent = SetOppAction_SerialSendDuelData(OPPACTION_EXECUTE_PKMN_POWER_EFFECT, rng.de);
	a = sent.a;
	f = sent.f;
	d = (uint8_t)(sent.de >> 8);
	e = (uint8_t)sent.de;
	TryExecuteEffectCommandFunctionResult before_damage = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_BEFORE_DAMAGE);
	a = before_damage.a;
	f = before_damage.f;
	c = before_damage.c;
	hl = before_damage.hl;
	sent = SetOppAction_SerialSendDuelData(OPPACTION_DUEL_MAIN_SCENE, (uint16_t)((uint16_t)d << 8 | e));
	a = sent.a;
	f = sent.f;
	d = (uint8_t)(sent.de >> 8);
	e = (uint8_t)sent.de;
	return (UsePokemonPowerResult){a, f, b, c, d, e, hl};
}
/* <<< factory UsePokemonPower */

/* >>> factory DrawYourOrOppPlayArea_ActiveCardGfx */
void DrawYourOrOppPlayArea_ActiveCardGfx(uint16_t de)
{
	uint8_t page = gb_read8(wCheckMenuPlayAreaWhichDuelist_ADDR);
	uint16_t arena_addr = (uint16_t)(((uint16_t)page << 8) | DUELVARS_ARENA_CARD);
	uint8_t arena_card = gb_read8(arena_addr);
	if (arena_card == 0xFFu)
		return;

	uint8_t turn = gb_read8(hWhoseTurn_ADDR);
	if (turn != page)
		SwapTurn();
	(void)LoadCardDataToBuffer1_FromDeckIndex(arena_card);
	if (turn != page)
		SwapTurn();

	uint16_t gfx = (uint16_t)(gb_read8(wLoadedCard1Gfx_ADDR) |
		(uint16_t)gb_read8((uint16_t)(wLoadedCard1Gfx_ADDR + 1u)) << 8);
	LoadCardGfx(gfx, 0x8A00u, 0x30u, 0x10u);
	SetBGP6OrSGB3ToCardPalette();
	FlushAllPalettesOrSendPal23Packet();
	FillRectangle(0xA0u, 8u, 6u, de, 0x0601u);
	(void)ApplyBGP6OrSGB3ToCardImage(0xA0u, 0u, 8u, 0u,
		(uint8_t)(de >> 8), (uint8_t)de, 0x0601u);
}
/* <<< factory DrawYourOrOppPlayArea_ActiveCardGfx */

/* >>> factory _DrawYourOrOppPlayAreaScreen */
void _DrawYourOrOppPlayAreaScreen(void)
{
	static const uint8_t player_prizes[] = {12u, 2u, 14u, 2u, 12u, 4u, 14u, 4u, 12u, 6u, 14u, 6u};
	static const uint8_t opponent_prizes[] = {12u, 12u, 14u, 12u, 12u, 14u, 14u, 14u, 12u, 16u, 14u, 16u};
	const uint16_t prize_coords = 0xC100u;
	gb_write8(wTileMapFill_ADDR, 0u);
	ZeroObjectPositions();
	gb_write8(wVBlankOAMCopyToggle_ADDR, TRUE);
	DoFrame();
	EmptyScreen();
	Set_OBJ_8x8();
	LoadCursorTile();
	(void)LoadSymbolsFont();
	(void)LoadDeckAndDiscardPileIcons();
	if (wCheckMenuPlayAreaWhichDuelist == PLAYER_TURN) {
		(void)CopyPlayerName(wDefaultText_ADDR);
	} else {
		(void)CopyOpponentName(wDefaultText_ADDR);
	}
	TextLength length = GetTextLengthInTiles(wDefaultText_ADDR);
	uint8_t a = (uint8_t)(6u - length.b);
	a = (uint8_t)((a >> 1u) + 4u);
	InitTextPrinting(a, 0u);
	if (hWhoseTurn != PLAYER_TURN || wCheckMenuPlayAreaWhichDuelist == PLAYER_TURN) {
		(void)PrintTextNoDelay(DuelistsPlayAreaText, a, 0u);
	} else {
		SwapTurn();
		(void)PrintTextNoDelay(DuelistsPlayAreaText, a, 0u);
		SwapTurn();
	}
	if (wCheckMenuPlayAreaWhichDuelist == wCheckMenuPlayAreaWhichLayout) {
		for (uint8_t i = 0u; i < sizeof(player_prizes); ++i)
			gb_write8((uint16_t)(prize_coords + i), player_prizes[i]);
		DrawPlayArea_PrizeCards(prize_coords);
		DrawYourOrOppPlayArea_ActiveCardGfx(0x0602u);
		DrawPlayArea_BenchCards(4u, 1u, 9u);
		DrawYourOrOppPlayArea_Icons(0u);
	} else {
		for (uint8_t i = 0u; i < sizeof(opponent_prizes); ++i)
			gb_write8((uint16_t)(prize_coords + i), opponent_prizes[i]);
		DrawPlayArea_PrizeCards(prize_coords);
		DrawYourOrOppPlayArea_ActiveCardGfx(0x0605u);
		DrawPlayArea_BenchCards(4u, 1u, 2u);
		DrawYourOrOppPlayArea_Icons(1u);
	}
	EnableLCD();
}
/* <<< factory _DrawYourOrOppPlayAreaScreen */

/* >>> factory DrawYourOrOppPlayAreaScreen */
void DrawYourOrOppPlayAreaScreen(uint16_t hl)
{
	wCheckMenuPlayAreaWhichDuelist = (uint8_t)(hl >> 8);
	wCheckMenuPlayAreaWhichLayout = (uint8_t)hl;
	_DrawYourOrOppPlayAreaScreen();
}
/* <<< factory DrawYourOrOppPlayAreaScreen */

/* >>> factory _DrawAIPeekScreen */
void _DrawAIPeekScreen(uint8_t b)
{
	Set_OBJ_8x8();
	LoadCursorTile();
	wIsSwapTurnPending = 0u;

	uint8_t turn = hWhoseTurn;
	uint16_t transition_table;
	if ((b & 0x80u) != 0u) {
		SwapTurn();
		wIsSwapTurnPending = 1u;
		turn = hWhoseTurn;
		transition_table = 0x48FAu;
	} else {
		transition_table = 0x48C2u;
	}

	DrawYourOrOppPlayAreaScreen((uint16_t)(((uint16_t)turn << 8) | turn));
	wMenuInputTablePointer = (uint8_t)transition_table;
	gb_write8((uint16_t)(wMenuInputTablePointer_ADDR + 1u), (uint8_t)(transition_table >> 8));

	uint8_t action = (uint8_t)(b & 0x7Fu);
	if (action == 0x7Fu)
		wYourOrOppPlayAreaCurPosition = 0x07u;
	else if ((action & 0x40u) != 0u)
		wYourOrOppPlayAreaCurPosition = (uint8_t)(action & 0x3Fu);
	else
		wYourOrOppPlayAreaCurPosition = 0x06u;

	yoopa_draw_cursor();
	wVBlankOAMCopyToggle = 1u;
	if (wIsSwapTurnPending != 0u)
		SwapTurn();
}
/* <<< factory _DrawAIPeekScreen */

/* >>> factory PrintPokemonsAttackText */
PrintPokemonsAttackTextResult PrintPokemonsAttackText(void)
{
	DuelistVarResult duelist = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	(void)LoadCardDataToBuffer1_FromDeckIndex(duelist.a);
	CopyCardNameAndLevelResult name = CopyCardNameAndLevel(18u, 0u, 0u, 0u, 0u);
	gb_write8(name.hl, TX_END);
	gb_write8(wTxRam2_ADDR, 0u);
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), 0u);
	gb_write8((uint16_t)(wTxRam2_ADDR + 2u), gb_read8(wLoadedAttackName_ADDR));
	gb_write8((uint16_t)(wTxRam2_ADDR + 3u), gb_read8((uint16_t)(wLoadedAttackName_ADDR + 1u)));
	TextResult text = DrawWideTextBox_PrintText(PokemonsAttackText);
	return (PrintPokemonsAttackTextResult){text.a, text.b, text.c, text.d, text.e, text.hl};
}
/* <<< factory PrintPokemonsAttackText */

/* >>> factory PrintFailedEffectText */
PrintFailedEffectTextResult PrintFailedEffectText(void)
{
	uint8_t failed = gb_read8(wEffectFailed_ADDR);
	if (failed == 0u)
		return (PrintFailedEffectTextResult){0x80u};
	if (failed == 1u) {
		uint16_t status_text = PrintThereWasNoEffectFromStatusText();
		(void)DrawWideTextBox_PrintText(status_text);
		return (PrintFailedEffectTextResult){0x10u};
	}
	DuelistVarResult duelist = GetTurnDuelistVariable((uint8_t)(gb_read8(hTempPlayAreaLocation_ff9d_ADDR) + DUELVARS_ARENA_CARD));
	(void)LoadCardDataToBuffer1_FromDeckIndex(duelist.a);
	CopyCardNameAndLevelResult copied = CopyCardNameAndLevel(18u, 0u, 0u, 0u, 0u);
	gb_write8(copied.hl, 0u);
	LoadTxRam2(0u);
	gb_write8(wTxRam2_b_ADDR, gb_read8(wLoadedAttackName_ADDR));
	gb_write8((uint16_t)(wTxRam2_b_ADDR + 1u), gb_read8((uint16_t)(wLoadedAttackName_ADDR + 1u)));
	(void)DrawWideTextBox_PrintText(WasUnsuccessfulText);
	return (PrintFailedEffectTextResult){0x10u};
}
/* <<< factory PrintFailedEffectText */

/* >>> factory DrawInPlayArea_ActiveCardGfx */
void DrawInPlayArea_ActiveCardGfx(void)
{
	DuelistVarResult result;
	uint16_t gfx;
	gb_write8(wArenaCardsInPlayArea_ADDR, 0u);
	result = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	if (result.a != 0xFFu) {
		gb_write8(wArenaCardsInPlayArea_ADDR, (uint8_t)(gb_read8(wArenaCardsInPlayArea_ADDR) | 0x01u));
		(void)LoadCardDataToBuffer1_FromDeckIndex(result.a);
		gfx = (uint16_t)(gb_read8(wLoadedCard1Gfx_ADDR) | ((uint16_t)gb_read8((uint16_t)(wLoadedCard1Gfx_ADDR + 1u)) << 8));
		LoadCardGfx(gfx, 0x8A00u, 0x30u, 0x08u);
		SetBGP6OrSGB3ToCardPalette();
	}
	result = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD);
	if (result.a != 0xFFu) {
		gb_write8(wArenaCardsInPlayArea_ADDR, (uint8_t)(gb_read8(wArenaCardsInPlayArea_ADDR) | 0x02u));
		SwapTurn();
		(void)LoadCardDataToBuffer1_FromDeckIndex(result.a);
		gfx = (uint16_t)(gb_read8(wLoadedCard1Gfx_ADDR) | ((uint16_t)gb_read8((uint16_t)(wLoadedCard1Gfx_ADDR + 1u)) << 8));
		LoadCardGfx(gfx, 0x9500u, 0x30u, 0x08u);
		SetBGP7OrSGB2ToCardPalette();
		SwapTurn();
	}
	if (gb_read8(wArenaCardsInPlayArea_ADDR) == 0u)
		return;
	FlushAllPalettesOrSendPal23Packet();
	if ((gb_read8(wArenaCardsInPlayArea_ADDR) & 0x01u) != 0u) {
		FillRectangle(0xA0u, 8u, 6u, 0x0609u, 0x0601u);
		(void)ApplyBGP6OrSGB3ToCardImage(0xA0u, 0u, 8u, 6u, 6u, 9u, 0x0601u);
	}
	if ((gb_read8(wArenaCardsInPlayArea_ADDR) & 0x02u) == 0u)
		return;
	SwapTurn();
	FillRectangle(0x50u, 8u, 6u, 0x0602u, 0x0601u);
	(void)ApplyBGP7OrSGB2ToCardImage(0x50u, 0u, 8u, 6u, 6u, 2u, 0x0601u);
	SwapTurn();
}
/* <<< factory DrawInPlayArea_ActiveCardGfx */

/* >>> factory DrawInPlayAreaScreen */
void DrawInPlayAreaScreen(void)
{
	wTileMapFill = 0u;
	ZeroObjectPositions();
	wVBlankOAMCopyToggle = TRUE;
	DoFrame();
	EmptyScreen();
	wDuelDisplayedScreen = CHECK_PLAY_AREA;
	Set_OBJ_8x8();
	LoadCursorTile();
	(void)LoadSymbolsFont();
	(void)LoadDeckAndDiscardPileIcons();
	(void)SetupText(0x80u, 0x9Fu);

	wCheckMenuPlayAreaWhichDuelist = hWhoseTurn;
	wCheckMenuPlayAreaWhichLayout = hWhoseTurn;
	DrawPlayArea_PrizeCards(0x4629u);
	DrawPlayArea_BenchCards(3u, 3u, 15u);
	DrawInPlayArea_Icons(0x4635u);
	SwapTurn();
	wCheckMenuPlayAreaWhichDuelist = hWhoseTurn;
	SwapTurn();
	DrawPlayArea_PrizeCards(0x462Fu);
	DrawPlayArea_BenchCards(3u, 3u, 0u);
	SwapTurn();
	DrawInPlayArea_Icons(0x463Bu);
	SwapTurn();
	DrawInPlayArea_ActiveCardGfx();
}
/* <<< factory DrawInPlayAreaScreen */
