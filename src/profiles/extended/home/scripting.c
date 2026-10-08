/* >>> part includes */
#include "home/scripting.h"

#include "home/script_entry_dispatch.h"
#include "home/card_id_bus.h"

#include "generated/rom.h"
#include "generated/constants.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/color.h"
#include "home/map_events.h"
/* <<< part includes */
/* --- part EVENT_VAR_MASKS_BANK */
/* >>> part includes_SCRIPT_COMMAND_CHOOSE_STARTER_DECK_BANK */
#include "home/scripting.h"
#include "home/npc_data.h"
#include "home/npc_core.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/overworld.h"
#include "home/scripting.h"
#include "generated/wram.h"
#include "generated/hram.h"

#include "generated/wram.h"
#include "home/map.h"
#include "home/script.h"

#include "generated/wram.h"
#include "home/map.h"
#include "home/script.h"

#include "home/scripting.h"


#include "generated/wram.h"
#include "home/overworld.h"


#include "generated/wram.h"
#include "home/overworld.h"
#include "home/scripting.h"

#include "home/challenge_hall.h"
#include "home/deck_machine_room.h"
#include "home/fighting_club.h"
#include "home/fighting_club_lobby.h"
#include "home/fire_club.h"
#include "home/fire_club_lobby.h"
#include "home/grass_club.h"
#include "home/grass_club_entrance.h"
#include "home/grass_club_lobby.h"
#include "home/hall_of_honor.h"
#include "home/lightning_club.h"
#include "home/lightning_club_lobby.h"
#include "home/mason_laboratory.h"
#include "home/memory.h"
#include "home/npc_core.h"
#include "home/npc_data.h"
#include "home/pokemon_dome.h"
#include "home/pokemon_dome_entrance.h"
#include "home/psychic_club.h"
#include "home/psychic_club_entrance.h"
#include "home/psychic_club_lobby.h"
#include "home/rock_club.h"
#include "home/rock_club_lobby.h"
#include "home/science_club.h"
#include "home/science_club_lobby.h"
#include "home/script.h"
#include "home/water_club.h"

#include "generated/wram.h"
#include "home/lcd_enable_frame.h"
#include "home/overworld.h"
#include "home/scripting.h"

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/lcd_enable_frame.h"
#include "home/overworld.h"
#include "home/menus.h"
#include "home/labels.h"
#include "mem.h"

#include "home/scripting.h"
#include "home/switch_rom.h"
#include "generated/wram.h"
/* <<< part includes_SCRIPT_COMMAND_CHOOSE_STARTER_DECK_BANK */
/* >>> factory GetEventVar */
GetEventVarResult GetEventVar(uint8_t a, uint8_t f, uint8_t b, uint8_t c)
{
	(void)f;
	uint16_t bc = (uint16_t)a * 2u;
	const uint8_t *entry = rom_ptr(EventVarMasks_BANK, (uint16_t)(EVENT_VAR_MASKS + bc));
	uint8_t flags = (bc & 0xFF00u) == 0 ? 0x80u : 0u;
	uint8_t offset = entry[0];
	if (((wEventVars_ADDR & 0x0FFFu) + (offset & 0x0FFFu)) > 0x0FFFu)
		flags |= 0x20u;
	if ((uint32_t)wEventVars_ADDR + offset > 0xFFFFu)
		flags |= 0x10u;

	gb_write8(wLoadedEventBits_ADDR, entry[1]);
	return (GetEventVarResult){entry[1], flags, b, c,
	                           (uint16_t)(wEventVars_ADDR + entry[0])};
}
/* <<< factory GetEventVar */
/* --- factory GetScriptArgs5AfterPointer */
/* >>> factory ScriptCommand_JumpIfCardInCollection */
/* scripting.asm:1019-1036 */
JumpIfCardInCollectionResult ScriptCommand_JumpIfCardInCollection(uint8_t b, uint8_t c)
{
	uint16_t card = (uint16_t)(((uint16_t)b << 8) | c);
	CardCountResult cnt = GetCardCountInCollection(card);
	if (cnt.a == 0) {
		SetScriptControlByteFail();
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
		return (JumpIfCardInCollectionResult){r.a, r.f, 0u, r.c,
			(uint8_t)(card >> 8), (uint8_t)card};
	}
	SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
	if (args.f & 0x80u) {
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
		return (JumpIfCardInCollectionResult){r.a, r.f, args.b, r.c,
			(uint8_t)(card >> 8), (uint8_t)card};
	}
	(void)SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
	return (JumpIfCardInCollectionResult){args.a, args.f, args.b, args.c,
		(uint8_t)(card >> 8), (uint8_t)card};
}
/* <<< factory ScriptCommand_JumpIfCardInCollection */
/* >>> factory ScriptCommand_GiveCard */
/* scripting.asm:1056-1063 */
IncreaseScriptPointerResult ScriptCommand_GiveCard(uint8_t b, uint8_t c)
{
	uint16_t card = (uint16_t)(((uint16_t)b << 8) | c);
	if (card == 0u)
		card = (uint16_t)(wCardReceived |
			((uint16_t)wCardReceived_PTR[1] << 8));
	AddCardToCollection(card);
	return IncreaseScriptPointerBy3();
}
/* <<< factory ScriptCommand_GiveCard */
/* >>> factory ScriptCommand_TakeCard */
/* scripting.asm:1066-1069 */
IncreaseScriptPointerResult ScriptCommand_TakeCard(uint8_t b, uint8_t c)
{
	RemoveCardFromCollection((uint16_t)(((uint16_t)b << 8) | c));
	return IncreaseScriptPointerBy3();
}
/* <<< factory ScriptCommand_TakeCard */
/* >>> factory ScriptCommand_SetSpriteAttributes */
/* scripting.asm:1276-1306. Records the current NPC in wLoadedNPCTempIndex,
 * reads 3 script bytes, clears the directionless bit in that NPC's flags
 * item and ORs the third script byte into it, then restarts the NPC
 * animation with b on CGB or c on DMG. Entry bc is only consumed after the
 * push/pop pair restores it. */
SetSpriteAttributesResult ScriptCommand_SetSpriteAttributes(uint8_t b, uint8_t c)
{
	wLoadedNPCTempIndex = wScriptNPC;
	PermissionResult item = GetItemInLoadedNPCIndex(wScriptNPC, LOADED_NPC_FLAGS);
	uint8_t flags = (uint8_t)(gb_read8(item.hl) &
		(uint8_t)~(1u << NPC_FLAG_DIRECTIONLESS_F));
	gb_write8(item.hl, (uint8_t)(flags | b));
	(void)SetNPCAnimation(c);
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy3();
	return (SetSpriteAttributesResult){r.a, r.f, r.c};
}
/* <<< factory ScriptCommand_SetSpriteAttributes */
/* --- factory ScriptCommand_BattleCenter */
/* >>> factory SetNextScript */
uint16_t SetNextScript(uint8_t a, uint16_t bc)
{
	script_pointer_write(bc, a);
	wOverworldMode = 0x03u;
	return wNextScriptBank_ADDR;
}
/* <<< factory SetNextScript */
/* >>> factory ScriptCommand_JumpIfEnoughCardsOwned */
JumpIfCardInCollectionResult ScriptCommand_JumpIfEnoughCardsOwned(uint8_t b, uint8_t c)
{
	uint16_t owned = GetAmountOfCardsOwned();
	uint16_t target = (uint16_t)(((uint16_t)b << 8) | c);
	if (owned >= target) {
		SetScriptControlBytePass();
		GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
		if (args.f & 0x80u) {
			IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
			return (JumpIfCardInCollectionResult){r.a, r.f, args.b, r.c};
		}
		(void)SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
		return (JumpIfCardInCollectionResult){args.a, args.f, args.b, args.c};
	}
	SetScriptControlByteFail();
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
	return (JumpIfCardInCollectionResult){r.a, r.f, b, r.c};
}
/* <<< factory ScriptCommand_JumpIfEnoughCardsOwned */
/* >>> factory ScriptCommand_RemoveAllEnergyCardsFromCollection */
ScriptCommand_RemoveAllEnergyCardsResult ScriptCommand_RemoveAllEnergyCardsFromCollection(uint8_t b)
{
	uint8_t b_reg = b;
	uint16_t card = GRASS_ENERGY;
	for (;;) {
		CardCountResult count = GetCardCountInCollection(card);
		if ((count.f & 0x10u) == 0u) {
			b_reg = count.a;
			while (b_reg != 0u) {
				RemoveCardFromCollection(card);
				--b_reg;
			}
		}
		card = (uint16_t)(card + 1u);
		if (card < (uint16_t)(DOUBLE_COLORLESS_ENERGY + 1u))
			continue;
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy1();
		return (ScriptCommand_RemoveAllEnergyCardsResult){
			r.a, r.f, b_reg, r.c, (uint8_t)(card >> 8), (uint8_t)card};
	}
}
/* <<< factory ScriptCommand_RemoveAllEnergyCardsFromCollection */
/* >>> factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */
ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult ScriptCommand_JumpIfAnyEnergyCardsInCollection(void)
{
	uint8_t total = 0u;
	uint16_t card = GRASS_ENERGY;
	for (;;) {
		CardCountResult count = GetCardCountInCollection(card);
		total = (uint8_t)(total + count.a);
		card = (uint16_t)(card + 1u);
		if (card < (uint16_t)(DOUBLE_COLORLESS_ENERGY + 1u))
			continue;
		break;
	}
	if (total == 0u) {
		SetScriptControlByteFail();
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy3();
		return (ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult){
			r.a, r.f, 0u, r.c, (uint8_t)(card >> 8), (uint8_t)card};
	}
	SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs1AfterPointer();
	if (args.f & 0x80u) {
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy3();
		return (ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult){
			r.a, r.f, args.b, r.c, (uint8_t)(card >> 8), (uint8_t)card};
	}
	(void)SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
	return (ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult){
		args.a, args.f, args.b, args.c, (uint8_t)(card >> 8), (uint8_t)card};
}
/* <<< factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */
/* >>> factory SetNextNPCAndScript */
SetNextNPCAndScriptResult SetNextNPCAndScript(uint16_t bc, uint16_t hl)
{
	(void)FindLoadedNPC();
	wScriptNPC = wLoadedNPCTempIndex;
	SetNewScriptNPCResult npc = SetNewScriptNPC(hl);
	SetNextScript(wNextScriptBank, bc);
	return (SetNextNPCAndScriptResult){OWMODE_SCRIPT, npc.f,
		(uint8_t)(bc >> 8), (uint8_t)bc, npc.hl};
}
/* <<< factory SetNextNPCAndScript */
/* >>> factory ScriptCommand_JumpIfCardOwned */
JumpIfCardInCollectionResult ScriptCommand_JumpIfCardOwned(uint8_t b, uint8_t c)
{
	uint16_t card = (uint16_t)(((uint16_t)b << 8) | c);
	CardCountResult cnt = GetCardCountInCollectionAndDecks(card);
	if (cnt.a == 0) {
		SetScriptControlByteFail();
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
		return (JumpIfCardInCollectionResult){r.a, r.f, 0u, r.c,
			(uint8_t)(card >> 8), (uint8_t)card};
	}
	SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
	if (args.f & 0x80u) {
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
		return (JumpIfCardInCollectionResult){r.a, r.f, args.b, r.c,
			(uint8_t)(card >> 8), (uint8_t)card};
	}
	(void)SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
	return (JumpIfCardInCollectionResult){args.a, args.f, args.b, args.c,
		(uint8_t)(card >> 8), (uint8_t)card};
}
/* <<< factory ScriptCommand_JumpIfCardOwned */
/* >>> factory ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot */
IncreaseScriptPointerResult ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot(uint8_t c)
{
	uint8_t shifted = (uint8_t)(c << 1);
	uint16_t addr = (uint16_t)(wTxRam2_ADDR + shifted);
	CardId event = (CardId)(GetEventValue(EVENT_MAN1_REQUESTED_CARD_ID_LO)
		| ((uint16_t)GetEventValue(EVENT_MAN1_REQUESTED_CARD_ID_HI) << 8));
	uint16_t name = GetCardName(event);
	gb_write8(addr, (uint8_t)(name & 0xFFu));
	gb_write8((uint16_t)(addr + 1u), (uint8_t)(name >> 8));
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot */
/* --- factory Func_c998 */
/* >>> factory LoadOverworld */
LoadOverworldResult LoadOverworld(uint8_t b, uint8_t c)
{
	(void)ZeroOutEventValue(EVENT_PLAYER_ENTERED_CHALLENGE_CUP, 0u, 0u, 0u);
	(void)ZeroOutEventValue(EVENT_CHALLENGE_CUP_OPPONENT_CHOSEN, 0u, 0u, 0u);

	if (GetEventValue(EVENT_CHALLENGE_CUP_1_STATE) == CHALLENGE_CUP_WON) {
		(void)SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
	} else if (GetEventValue(EVENT_CHALLENGE_CUP_2_STATE) == CHALLENGE_CUP_WON) {
		(void)SetEventValue(EVENT_CHALLENGE_CUP_2_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
		(void)SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
	} else if (GetEventValue(EVENT_CHALLENGE_CUP_3_STATE) == CHALLENGE_CUP_WON) {
		(void)SetEventValue(EVENT_CHALLENGE_CUP_3_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
		(void)SetEventValue(EVENT_CHALLENGE_CUP_2_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
		(void)SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
	}

	uint8_t state = GetEventValue(EVENT_MASON_LAB_STATE);
	if (state != 0u)
		return (LoadOverworldResult){state, 0x00u, b, c};
	SetNextScript(Script_BeginGame_BANK, Script_BeginGame);
	return (LoadOverworldResult){0x03u, 0x80u,
		(uint8_t)(Script_BeginGame >> 8), (uint8_t)Script_BeginGame};
}
/* <<< factory LoadOverworld */
/* >>> factory CallMapScriptPointerIfExists */
CallMapScriptResult CallMapScriptPointerIfExists(uint8_t l)
{
	MapScriptResult r = GetMapScriptPointer(l);
	if ((r.f & 0x10u) == 0u)
		return (CallMapScriptResult){r.a, r.f, r.hl};
	uint8_t saved_bank = hBankROM;
	ScriptEntryRegs entered = ScriptEntryEnterWithBank(r.hl, r.a, r.f, r.a, 0u, 0u, 0u);
	return (CallMapScriptResult){saved_bank, r.f, entered.hl};
}
/* <<< factory CallMapScriptPointerIfExists */
/* >>> factory Func_c9c7 */
CallMapScriptResult Func_c9c7(void)
{
	return CallMapScriptPointerIfExists(MAP_SCRIPT_CLOSE_TEXTBOX);
}
/* <<< factory Func_c9c7 */
/* --- factory ScriptCommand_GiftCenter */
/* >>> factory Func_c943 */
Func_c943Result Func_c943(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)a; (void)f;
	uint8_t saved_b = b;
	uint8_t saved_c = c;
	uint8_t saved_d = d;
	uint8_t saved_e = e;
	uint16_t saved_hl = hl;
	MapScriptResult map = GetMapScriptPointer(MAP_SCRIPT_NPCS);
	wMapScriptBank = map.a;
	if (map.f & 0x10u) {
		hl = map.hl;
		for (;;) {
			wTempPointer = (uint8_t)hl;
			gb_write8((uint16_t)(wTempPointer_ADDR + 1u), (uint8_t)(hl >> 8));
			wTempPointerBank = wMapScriptBank;
			CopyBankedDataToDE(NPC_MAP_SIZE, wTempNPC_ADDR);
			if (wTempNPC == 0u)
				break;
			/* scripting.asm:41-49: the record's pre-load pointer, when
			 * not NULL, is called through CallHL2 and its carry decides
			 * whether this NPC is loaded at all (Preload_Sam moves Sam
			 * to the table, Preload_Tech5 shifts the technician). The
			 * table resolves the pointer to its C body at build time. */
			uint16_t preload = (uint16_t)(wLoadNPCFunction |
				((uint16_t)gb_read8((uint16_t)(wLoadNPCFunction_ADDR + 1u)) << 8));
			if (preload == 0u || (ScriptEntryEnter(preload).f & 0x10u) != 0u) {
				(void)LoadNPCSpriteData(wTempNPC, b, c, d, e, hl);
				if (wTempNPC == NPC_AMY && wd3d0 != 0u) {
					wNPCAnim = SPRITE_ANIM_BLUE_NPC_UP;
					wNPCAnimFlags = 0u;
				}
				(void)LoadNPC();
			}
			hl = (uint16_t)(hl + NPC_MAP_SIZE);
		}
	}
	CallMapScriptResult post = CallMapScriptPointerIfExists(MAP_SCRIPT_POST_NPC);
	return (Func_c943Result){post.a, post.f, saved_b, saved_c, saved_d, saved_e, saved_hl};
}
/* <<< factory Func_c943 */
/* >>> factory ScriptCommand_ShowCardReceivedScreen */
IncreaseScriptPointerResult ScriptCommand_ShowCardReceivedScreen(uint8_t b, uint8_t c)
{
	CardId card;

	Func_c2a3();
	if ((uint8_t)(c & b) == 0xFFu)
		card = 0u;
	else if ((uint8_t)(c | b) != 0u)
		card = (CardId)(((uint16_t)b << 8) | c);
	else
		card = (CardId)(gb_read8(wCardReceived_ADDR)
			| ((uint16_t)gb_read8((uint16_t)(wCardReceived_ADDR + 1u)) << 8));

	(void)InitMenuScreen();
	(void)FlashWhiteScreen();
	ShowPromotionalCardScreen(card);
	WhiteOutDMGPals();
	DoFrameIfLCDEnabled();
	(void)ReturnToOverworldNoCallback();
	return IncreaseScriptPointerBy3();
}
/* <<< factory ScriptCommand_ShowCardReceivedScreen */
/* --- factory Script_GiftCenterClerk */
/* >>> factory ScriptCommand_PickNextMan1RequestedCard */
IncreaseScriptPointerResult ScriptCommand_PickNextMan1RequestedCard(void)
{
	uint8_t flags = GetEventValue(EVENT_MAN1_GIFTED_CARD_FLAGS);
	uint8_t index;
	uint8_t mask;
	do {
		index = Random(MAN1_REQUESTED_CARDS_COUNT);
		mask = (uint8_t)(1u << index);
	} while ((mask & flags) != 0u);
	(void)SetEventValue(EVENT_MAN1_GIFTED_CARD_FLAGS, 0u, 0u, (uint8_t)(mask | flags));
	const uint8_t *entry = rom_ptr(MAN1_REQUESTED_CARDS_BANK,
	                               (uint16_t)(MAN1_REQUESTED_CARDS_ADDR + (uint16_t)index * 2u));
	(void)SetEventValue(EVENT_MAN1_REQUESTED_CARD_ID_LO, 0u, 0u, entry[0]);
	(void)SetEventValue(EVENT_MAN1_REQUESTED_CARD_ID_HI, 0u, 0u, entry[1]);
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_PickNextMan1RequestedCard */
/* >>> factory ScriptCommand_JumpIfMan1RequestedCardOwned */
JumpIfCardInCollectionResult ScriptCommand_JumpIfMan1RequestedCardOwned(uint8_t b)
{
	CardId card = (CardId)(GetEventValue(EVENT_MAN1_REQUESTED_CARD_ID_LO)
		| ((uint16_t)GetEventValue(EVENT_MAN1_REQUESTED_CARD_ID_HI) << 8));
	CardCountResult cnt = GetCardCountInCollectionAndDecks(card);
	if ((cnt.f & 0x10u) != 0u) {
		SetScriptControlByteFail();
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy3();
		return (JumpIfCardInCollectionResult){r.a, r.f, b, r.c,
			(uint8_t)(card >> 8), (uint8_t)card};
	}
	SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs1AfterPointer();
	if ((args.f & 0x80u) != 0u) {
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy3();
		return (JumpIfCardInCollectionResult){r.a, r.f, args.b, r.c,
			(uint8_t)(card >> 8), (uint8_t)card};
	}
	(void)SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
	return (JumpIfCardInCollectionResult){args.a, args.f, args.b, args.c,
		(uint8_t)(card >> 8), (uint8_t)card};
}
/* <<< factory ScriptCommand_JumpIfMan1RequestedCardOwned */
/* >>> factory ScriptCommand_JumpIfMan1RequestedCardInCollection */
JumpIfCardInCollectionResult ScriptCommand_JumpIfMan1RequestedCardInCollection(uint8_t b)
{
	CardId card = (CardId)(GetEventValue(EVENT_MAN1_REQUESTED_CARD_ID_LO)
		| ((uint16_t)GetEventValue(EVENT_MAN1_REQUESTED_CARD_ID_HI) << 8));
	CardCountResult cnt = GetCardCountInCollection(card);
	if ((cnt.f & 0x10u) != 0u) {
		SetScriptControlByteFail();
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy3();
		return (JumpIfCardInCollectionResult){r.a, r.f, b, r.c,
			(uint8_t)(card >> 8), (uint8_t)card};
	}
	SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs1AfterPointer();
	if ((args.f & 0x80u) != 0u) {
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy3();
		return (JumpIfCardInCollectionResult){r.a, r.f, args.b, r.c,
			(uint8_t)(card >> 8), (uint8_t)card};
	}
	(void)SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
	return (JumpIfCardInCollectionResult){args.a, args.f, args.b, args.c,
		(uint8_t)(card >> 8), (uint8_t)card};
}
/* <<< factory ScriptCommand_JumpIfMan1RequestedCardInCollection */
/* >>> factory ScriptCommand_RemoveMan1RequestedCardFromCollection */
IncreaseScriptPointerResult ScriptCommand_RemoveMan1RequestedCardFromCollection(void)
{
	RemoveCardFromCollection((CardId)(GetEventValue(EVENT_MAN1_REQUESTED_CARD_ID_LO)
		| ((uint16_t)GetEventValue(EVENT_MAN1_REQUESTED_CARD_ID_HI) << 8)));
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_RemoveMan1RequestedCardFromCollection */
/* >>> factory ScriptCommand_PickChallengeCupPrizeCard */
IncreaseScriptPointerResult ScriptCommand_PickChallengeCupPrizeCard(void)
{
	uint8_t index = (uint8_t)(GetEventValue(EVENT_CHALLENGE_CUP_NUMBER) - 1u);
	if (index >= 2u)
		index = (uint8_t)(Random((uint8_t)(CHALLENGE_CUP_PRIZE_CARD_COUNT - 2u)) + 2u);
	const uint8_t *entry = rom_ptr(CHALLENGE_CUP_PRIZE_CARDS_BANK,
	                               (uint16_t)(CHALLENGE_CUP_PRIZE_CARDS_ADDR + (uint16_t)index * 4u));
	wCardReceived = entry[0];
	gb_write8((uint16_t)(wCardReceived_ADDR + 1u), entry[1]);
	gb_write8(wTxRam2_ADDR, entry[2]);
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), entry[3]);
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_PickChallengeCupPrizeCard */
/* >>> factory ScriptCommand_PickLegendaryCard */
IncreaseScriptPointerResult ScriptCommand_PickLegendaryCard(void)
{
	uint8_t flags = GetEventValue(EVENT_LEGENDARY_CARDS_RECEIVED_FLAGS);
	uint8_t index;
	uint8_t mask;
	for (;;) {
		uint8_t random = (uint8_t)(UpdateRNGSources() & 0x03u);
		mask = (uint8_t)(0x08u >> random);
		if ((mask & flags) == 0u) {
			index = random;
			break;
		}
	}
	const uint8_t *event_entry = rom_ptr(
		LEGENDARY_CARD_EVENTS_BANK,
		(uint16_t)(LEGENDARY_CARD_EVENTS_ADDR + index)
	);
	(void)MaxOutEventValue(event_entry[0], 0u, 0u, 0u);
	const uint8_t *card_entry = rom_ptr(
		LEGENDARY_CARDS_BANK,
		(uint16_t)(LEGENDARY_CARDS_ADDR + (uint16_t)index * 4u)
	);
	wCardReceived = card_entry[0];
	gb_write8((uint16_t)(wCardReceived_ADDR + 1u), card_entry[1]);
	gb_write8(wTxRam2_ADDR, card_entry[2]);
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), card_entry[3]);
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_PickLegendaryCard */
/* === factory FarCallHL */
/* === factory Func_d4fb */
/* === factory ScriptCommand_PrintVariableNPCText */
/* === factory ScriptCommand_PrintVariableText */
/* === factory ShowMultichoiceTextbox */
