#include "home/map.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/copy.h"
#include "home/switch_rom.h"
#include "home/sound.h"

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

void PlayDefaultSong(void)
{
	uint8_t finished = AssertSongFinished();
	uint8_t song = GetDefaultSong();

	if (!finished || song != wSongOverride) {
		if (song < 0x1Fu) {
			wSongOverride = song;
			PlaySong(song);
		}
	}
}
/*
 * Event handlers 1-6 are banked routines outside this port's dependency set.
 * Preserve their dispatch selection and entry flags until those handlers land.
 */
ExecuteGameEventResult _ExecuteGameEvent(uint8_t f)
{
	uint8_t event = wGameEvent;

	if (event == 0)
		return (ExecuteGameEventResult){event, GameEvent_Overworld(f)};

	return (ExecuteGameEventResult){event >= 7 ? 6 : event, f};
}
