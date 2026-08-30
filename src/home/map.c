#include "home/map.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/sound.h"
#include "home/switch_rom.h"
#include "mem.h"
/* >>> factory statics */
#include "home/warp.h"
#define BANK_HANDLE_MAP_WARP 7u

#include "generated/sram.h"
#include "home/scripting.h"
#include "home/switch_sram.h"
#define EVENT_RECEIVED_LEGENDARY_CARDS 0x22u

#include "home/map.h"
#include "home/switch_rom.h"
#include "home/animation.h"
#include "home/overworld.h"
#include "home/npc_core.h"
#include "home/load_animation.h"
#include "home/random.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define HIDE_ALL_NPC_SPRITES 7u

#include "generated/wram.h"
#include "generated/sram.h"
#include "home/switch_sram.h"
#include "home/save.h"
#include "home/core.h"
#define GAME_EVENT_DUEL 0x01u
/* <<< factory statics */

#define BANK_EXECUTE_NPC_MOVEMENT 0x03u
#define LOADED_NPC_MAX            8u
#define LOADED_NPC_LENGTH         12u
#define OWMAP_ISHIHARAS_HOUSE     0x02u
#define OWMAP_CHALLENGE_HALL      0x0Bu
#define OWMAP_POKEMON_DOME        0x0Cu
#define MUSIC_RONALD              0x0Fu

static uint16_t permission_address(uint8_t b, uint8_t c)
{
	uint8_t x = (uint8_t)(b >> 1);
	uint8_t y = (uint8_t)(c >> 1);
	return (uint16_t)(wPermissionMap_ADDR + (uint16_t)((uint8_t)(y << 4) | x));
}

PermissionResult GetPermissionByteOfMapPosition(uint8_t b, uint8_t c)
{
	uint16_t hl = permission_address(b, c);
	return (PermissionResult){(uint8_t)(hl - wPermissionMap_ADDR), hl};
}

uint8_t GetPermissionOfMapPosition(uint8_t b, uint8_t c)
{
	return gb_read8(permission_address(b, c));
}

void SetPermissionOfMapPosition(uint8_t a, uint8_t b, uint8_t c)
{
	gb_write8(permission_address(b, c), a);
}

uint8_t UpdatePermissionOfMapPosition(uint8_t a, uint8_t b, uint8_t c)
{
	uint16_t address = permission_address(b, c);
	uint8_t result = (uint8_t)(gb_read8(address) & (uint8_t)~a);
	gb_write8(address, result);
	return result;
}

PermissionResult GetItemInLoadedNPCIndex(uint8_t a, uint8_t l)
{
	if (a >= 8u)
		a = 0;
	uint8_t offset = (uint8_t)(a * 12u + l);
	return (PermissionResult){offset, (uint16_t)(wLoadedNPCs_ADDR + offset)};
}

PermissionResult GetLoadedNPCID(uint8_t a)
{
	return GetItemInLoadedNPCIndex(a, 0);
}

/* GameEvent_Overworld:: poketcg/src/home/map.asm:61-63. `scf` sets C, clears
 * N/H, and leaves Z exactly as the caller left it. */
uint8_t GameEvent_Overworld(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}

void CopyGfxDataFromTempBank(uint16_t *hl, uint16_t *de, uint8_t b, uint8_t c)
{
	uint8_t saved = hBankROM;

	BankswitchROM(wTempPointerBank);
	CopyGfxData(hl, de, b, c);
	BankswitchROM(saved);
}

/* FindLoadedNPC:: poketcg/src/home/map.asm:291-319. hl/bc/de are saved and
 * restored around the whole search, so only a, f and wLoadedNPCTempIndex are
 * real outputs. */
NPCSearchResult FindLoadedNPC(void)
{
	uint8_t target = wTempNPC;
	uint16_t entry = wLoadedNPCs_ADDR;
	uint8_t index;

	wLoadedNPCTempIndex = 0;
	for (index = 0; index < LOADED_NPC_MAX; index++, entry = (uint16_t)(entry + LOADED_NPC_LENGTH)) {
		if (gb_read8(entry) == target) {
			wLoadedNPCTempIndex = index;
			return (NPCSearchResult){index, (uint8_t)(index == 0 ? 0x80u : 0x00u)};
		}
	}
	return (NPCSearchResult){target, 0x90u};
}

/* GetNextNPCMovementByte:: poketcg/src/home/map.asm:321-333. The final `pop bc`
 * restores entry b/c despite the mid-routine `ld c, a`; only a is a real output. */
uint8_t GetNextNPCMovementByte(uint16_t bc)
{
	uint8_t saved = hBankROM;
	uint8_t value;

	BankswitchROM(BANK_EXECUTE_NPC_MOVEMENT);
	value = gb_read8(bc);
	BankswitchROM(saved);
	return value;
}

static uint8_t compare_flags(uint8_t lhs, uint8_t rhs)
{
	uint8_t result = (uint8_t)(lhs - rhs);
	uint8_t flags = 0x40u;

	if (result == 0)
		flags |= 0x80u;
	if ((lhs & 0x0Fu) < (rhs & 0x0Fu))
		flags |= 0x20u;
	if (lhs < rhs)
		flags |= 0x10u;
	return flags;
}

SongResult PlayDefaultSong(void)
{
	uint8_t assert_result = AssertSongFinished();
	uint8_t song = GetDefaultSong();
	uint8_t flags;

	if (assert_result == 1u) {
		flags = compare_flags(song, wSongOverride);
		if ((flags & 0x80u) != 0)
			return (SongResult){song, flags};
	}

	flags = compare_flags(song, 0x1Fu);
	if ((flags & 0x10u) != 0) {
		wSongOverride = song;
		PlaySong(song);
	}
	return (SongResult){song, flags};
}

uint8_t GetDefaultSong(void)
{
	if (!wRonaldIsInMap)
		return wDefaultSong;
	if (wOverworldMapSelection == OWMAP_ISHIHARAS_HOUSE
	    || wOverworldMapSelection == OWMAP_CHALLENGE_HALL
	    || wOverworldMapSelection == OWMAP_POKEMON_DOME)
		return wDefaultSong;
	return MUSIC_RONALD;
}

/* >>> factory HandleMapWarp */

/* HandleMapWarp:: poketcg/src/home/map.asm:251-259. Bankswitches to
 * _HandleMapWarp's bank, runs it, then restores the caller's bank. The
 * asm's `pop af` after the call discards _HandleMapWarp's a/f entirely,
 * and its only caller (engine/overworld/overworld.asm:1049) never reads
 * a/f afterward, so this wrapper has no register outputs -- the WRAM
 * writes _HandleMapWarp performs are the entire observable contract. */
void HandleMapWarp(void)
{
	uint8_t saved = hBankROM;

	BankswitchROM(BANK_HANDLE_MAP_WARP);
	(void)_HandleMapWarp();
	BankswitchROM(saved);
}
/* <<< factory HandleMapWarp */

/* >>> factory GetReceivedLegendaryCards */
GetReceivedLegendaryCardsResult GetReceivedLegendaryCards(void)
{
	uint8_t a = GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS);
	EnableSRAM();
	sReceivedLegendaryCards = a;
	DisableSRAM();
	return (GetReceivedLegendaryCardsResult){a, (uint8_t)(a == 0u ? 0x80u : 0u)};
}
/* <<< factory GetReceivedLegendaryCards */

/* >>> factory OverworldDoFrameFunction */
void OverworldDoFrameFunction(void)
{
	if (wOverworldNPCFlags & (1u << HIDE_ALL_NPC_SPRITES))
		return;
	uint8_t saved_bank = hBankROM;
	BankswitchROM(3u);
	(void)SetScreenScrollWram();
	Func_c554();
	BankswitchROM(7u);
	HandleAllNPCMovement();
	HandleAllSpriteAnimations();
	BankswitchROM(32u);
	DoLoadedFramesetSubgroupsFrame();
	(void)UpdateRNGSources();
	BankswitchROM(saved_bank);
}
/* <<< factory OverworldDoFrameFunction */

/* >>> factory GameEvent_Duel */
uint8_t GameEvent_Duel(void)
{
	wActiveGameEvent = GAME_EVENT_DUEL;
	wSongOverride = 0u;
	EnableSRAM();
	sPlayerInChallengeMachine = 0u;
	DisableSRAM();
	SaveGeneralSaveData();
	StartDuel_VSAIOpp();
	return 0x10u;
}
/* <<< factory GameEvent_Duel */
