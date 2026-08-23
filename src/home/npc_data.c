#include "home/npc_data.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "mem.h"
#define NPC_HEADER_POINTERS_BANK 0x04u
#define NPC_HEADER_POINTERS_ADDR 0x58F5u

#define NPC_DATA_NAME_TEXT 0x07u

#include "home/npc_data.h"
#include "generated/wram.h"
#include "mem.h"
#define NPC_DATA_SCRIPT_PTR 0x05u

#include "generated/wram.h"
#include "mem.h"
#define NPC_DATA_BANK 0x04u
#define CONSOLE_CGB 0x02u

#include "generated/wram.h"
#include "mem.h"
#define NPC_DUEL_CONFIGURATIONS_BANK 0x04u
#define NPC_DUEL_CONFIGURATIONS_ADDR 0x5FAEu

#include "home/npc_data.h"
#include "generated/wram.h"
#include "mem.h"
#define NPC_DATA_DECK_ID 0x0Au
/* <<< factory statics */

/* >>> factory GetNPCHeaderPointer */
GetNPCHeaderPointerResult GetNPCHeaderPointer(uint8_t a)
{
	uint8_t rotated = (uint8_t)((a << 1) | (a >> 7));
	uint8_t low_address = (uint8_t)(NPC_HEADER_POINTERS_ADDR + rotated);
	uint8_t carry = (uint8_t)(low_address < (uint8_t)NPC_HEADER_POINTERS_ADDR);
	uint8_t high_address = (uint8_t)(0x58u + carry);
	uint16_t table_address = (uint16_t)(((uint16_t)high_address << 8) | low_address);
	const uint8_t *entry = rom_ptr(NPC_HEADER_POINTERS_BANK, table_address);
	uint8_t pointer_low = entry[0];
	uint8_t pointer_high = entry[1];
	uint16_t pointer = (uint16_t)(pointer_low | ((uint16_t)pointer_high << 8));
	uint8_t f = 0;
	if (high_address == 0u)
		f |= 0x80u;
	if ((uint8_t)((0x58u & 0x0Fu) + carry) > 0x0Fu)
		f |= 0x20u;
	if ((uint16_t)0x58u + carry > 0xFFu)
		f |= 0x10u;
	return (GetNPCHeaderPointerResult){pointer, pointer_low, f};
}
/* <<< factory GetNPCHeaderPointer */

/* >>> factory SetNPCOpponentNameAndPortrait */
void SetNPCOpponentNameAndPortrait(uint8_t a)
{
	GetNPCHeaderPointerResult result = GetNPCHeaderPointer(a);
	const uint8_t *entry = rom_ptr(NPC_HEADER_POINTERS_BANK, (uint16_t)(result.hl + NPC_DATA_NAME_TEXT));
	gb_write8(wOpponentName_ADDR, entry[0]);
	gb_write8((uint16_t)(wOpponentName_ADDR + 1u), entry[1]);
	gb_write8(wOpponentPortrait_ADDR, entry[2]);
}
/* <<< factory SetNPCOpponentNameAndPortrait */

/* >>> factory GetNPCNameAndScript */
GetNPCNameAndScriptResult GetNPCNameAndScript(uint8_t a)
{
	GetNPCHeaderPointerResult header = GetNPCHeaderPointer(a);
	uint16_t cursor = (uint16_t)(header.hl + NPC_DATA_SCRIPT_PTR);
	const uint8_t *entry = rom_ptr(NPC_HEADER_POINTERS_BANK, cursor);
	uint8_t script_low = entry[0];
	uint8_t script_high = entry[1];
	uint8_t name_low = entry[2];
	uint8_t name_high = entry[3];
	gb_write8(wCurrentNPCNameTx_ADDR, name_low);
	gb_write8((uint16_t)(wCurrentNPCNameTx_ADDR + 1u), name_high);
	uint8_t f = (uint8_t)(header.f & 0x80u);
	if (((uint16_t)(header.hl & 0x0FFFu) + NPC_DATA_SCRIPT_PTR) > 0x0FFFu)
		f |= 0x20u;
	if ((uint32_t)header.hl + NPC_DATA_SCRIPT_PTR > 0xFFFFu)
		f |= 0x10u;
	return (GetNPCNameAndScriptResult){name_high, f, script_high, script_low};
}
/* <<< factory GetNPCNameAndScript */

/* >>> factory LoadNPCSpriteData */
LoadNPCSpriteDataResult LoadNPCSpriteData(uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	GetNPCHeaderPointerResult header = GetNPCHeaderPointer(a);
	const uint8_t *entry = rom_ptr(NPC_DATA_BANK, header.hl);
	wTempNPC = entry[0];
	wNPCSpriteID = entry[1];
	wNPCAnim = entry[2];
	uint8_t cgb_anim = entry[3];
	wNPCAnimFlags = entry[4];
	uint8_t console = wConsole;
	uint8_t out_a = console;
	uint8_t f = 0x40u;
	if (console == CONSOLE_CGB) {
		out_a = cgb_anim;
		wNPCAnim = cgb_anim;
		f |= 0x80u;
	}
	if ((uint8_t)(console & 0x0Fu) < (uint8_t)(CONSOLE_CGB & 0x0Fu))
		f |= 0x20u;
	if (console < CONSOLE_CGB)
		f |= 0x10u;
	return (LoadNPCSpriteDataResult){out_a, f, b, c, d, e, hl};
}
/* <<< factory LoadNPCSpriteData */

/* >>> factory _GetNPCDuelConfigurations */
_GetNPCDuelDuelConfigurationsResult _GetNPCDuelConfigurations(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t deck_id = gb_read8(wNPCDuelDeckID_ADDR);
	const uint8_t *entry = rom_ptr(NPC_DUEL_CONFIGURATIONS_BANK, NPC_DUEL_CONFIGURATIONS_ADDR);
	for (;;) {
		a = entry[0];
		if (a == 0xFFu) {
			f = 0xC0u;
			break;
		}
		if (a == deck_id) {
			gb_write8(wOpponentPortrait_ADDR, entry[1]);
			gb_write8(wOpponentName_ADDR, entry[2]);
			gb_write8((uint16_t)(wOpponentName_ADDR + 1u), entry[3]);
			a = entry[4];
			gb_write8(wNPCDuelPrizes_ADDR, a);
			f = 0x90u;
			break;
		}
		entry += 10u;
	}
	return (_GetNPCDuelDuelConfigurationsResult){a, f, b, c, d, e, hl};
}
/* <<< factory _GetNPCDuelConfigurations */

/* >>> factory SetNPCDeckIDAndDuelTheme */
SetNPCDeckIDAndDuelThemeResult SetNPCDeckIDAndDuelTheme(uint8_t a)
{
	GetNPCHeaderPointerResult header = GetNPCHeaderPointer(a);
	uint8_t f = (uint8_t)(header.f & 0x80u);
	if (((uint16_t)(header.hl & 0x0FFFu) + NPC_DATA_DECK_ID) > 0x0FFFu)
		f |= 0x20u;
	if ((uint32_t)header.hl + NPC_DATA_DECK_ID > 0xFFFFu)
		f |= 0x10u;
	const uint8_t *entry = rom_ptr(NPC_DATA_BANK, (uint16_t)(header.hl + NPC_DATA_DECK_ID));
	uint8_t deck_id = entry[0];
	uint8_t duel_theme = entry[1];
	gb_write8(wNPCDuelDeckID_ADDR, deck_id);
	gb_write8(wDuelTheme_ADDR, duel_theme);
	return (SetNPCDeckIDAndDuelThemeResult){duel_theme, f};
}
/* <<< factory SetNPCDeckIDAndDuelTheme */
