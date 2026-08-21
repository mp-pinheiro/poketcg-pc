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
