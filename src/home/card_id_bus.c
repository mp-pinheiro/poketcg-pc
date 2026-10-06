#include "home/card_id_bus.h"

#include "generated/wram.h"
#include "mem.h"

CardId card_id_read(uint16_t *address)
{
	CardId id = gb_read8(*address);
	*address = (uint16_t)(*address + 1u);
#ifdef POKETCG_PROFILE_EXTENDED
	id = (CardId)(id | (CardId)gb_read8(*address) << 8);
	*address = (uint16_t)(*address + 1u);
#endif
	return id;
}

CardId card_id_read_at(uint16_t address)
{
	return card_id_read(&address);
}

void card_id_write(uint16_t *address, CardId id)
{
	gb_write8(*address, (uint8_t)id);
	*address = (uint16_t)(*address + 1u);
#ifdef POKETCG_PROFILE_EXTENDED
	gb_write8(*address, (uint8_t)(id >> 8));
	*address = (uint16_t)(*address + 1u);
#endif
}

uint16_t card_id_index_address(uint16_t base, uint8_t index)
{
#ifdef POKETCG_PROFILE_EXTENDED
	return (uint16_t)(base + (uint16_t)index * 2u);
#else
	return (uint16_t)(base + index);
#endif
}

uint16_t card_id_deck_bytes(uint8_t count)
{
#ifdef POKETCG_PROFILE_EXTENDED
	return (uint16_t)count * 2u;
#else
	return count;
#endif
}

uint16_t card_id_collection_bytes(void)
{
#ifdef POKETCG_PROFILE_EXTENDED
	return 0x0200u;
#else
	return 0x0100u;
#endif
}
uint16_t card_gfx_prepare(uint16_t source)
{
#ifdef POKETCG_PROFILE_EXTENDED
	uint16_t cursor = source;
	for (uint8_t i = 0u; i < 3u; i++)
		gb_write8((uint16_t)(wCardPalette_ADDR + i), gb_read8(cursor++));
	for (uint8_t i = 0u; i < 0x30u; i++)
		gb_write8((uint16_t)(wCardAttrMap_ADDR + i), gb_read8(cursor++));
	return cursor;
#else
	return source;
#endif
}

void card_gfx_finish(uint16_t source)
{
#ifndef POKETCG_PROFILE_EXTENDED
	uint16_t cursor = wCardPalette_ADDR;
	for (uint8_t i = 0u; i < 8u; i++)
		gb_write8(cursor++, gb_read8(source++));
#else
	(void)source;
#endif
}
uint16_t script_pointer_read(uint8_t *bank)
{
	*bank = 0u;
#ifdef POKETCG_PROFILE_EXTENDED
	*bank = wNextScriptBank;
#endif
	return (uint16_t)(wNextScript | ((uint16_t)wNextScript_PTR[1] << 8));
}

void script_pointer_write(uint16_t address, uint8_t bank)
{
	wNextScript = (uint8_t)address;
	wNextScript_PTR[1] = (uint8_t)(address >> 8);
#ifdef POKETCG_PROFILE_EXTENDED
	wNextScriptBank = bank;
#else
	(void)bank;
#endif
}
