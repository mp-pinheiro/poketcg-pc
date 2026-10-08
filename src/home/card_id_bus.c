/* >>> part includes */
#include "home/card_id_bus.h"

#include "generated/constants.h"
#include "generated/profile_features.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */

/* >>> part card_id_read */
CardId card_id_read(uint16_t *address)
{
	CardId id = gb_read8(*address);
	*address = (uint16_t)(*address + 1u);
#if PROFILE_FEATURE_NINE_BIT_CARD_IDS
	id = (CardId)(id | (CardId)gb_read8(*address) << 8);
	*address = (uint16_t)(*address + 1u);
#endif
	return id;
}
/* <<< part card_id_read */

/* >>> part card_id_read_at */
CardId card_id_read_at(uint16_t address)
{
	return card_id_read(&address);
}
/* <<< part card_id_read_at */

/* >>> part card_id_write */
void card_id_write(uint16_t *address, CardId id)
{
	gb_write8(*address, (uint8_t)(id & 0xFFu));
	*address = (uint16_t)(*address + 1u);
#if PROFILE_FEATURE_NINE_BIT_CARD_IDS
	gb_write8(*address, (uint8_t)(id >> 8));
	*address = (uint16_t)(*address + 1u);
#endif
}
/* <<< part card_id_write */

/* >>> part card_id_index_address */
uint16_t card_id_index_address(uint16_t base, uint8_t index)
{
#if PROFILE_FEATURE_NINE_BIT_CARD_IDS
	return (uint16_t)(base + (uint16_t)index * 2u);
#else
	return (uint16_t)(base + index);
#endif
}
/* <<< part card_id_index_address */

/* >>> part card_id_deck_bytes */
uint16_t card_id_deck_bytes(uint8_t count)
{
#if PROFILE_FEATURE_NINE_BIT_CARD_IDS
	return (uint16_t)count * 2u;
#else
	return count;
#endif
}
/* <<< part card_id_deck_bytes */

/* >>> part card_id_collection_bytes */
uint16_t card_id_collection_bytes(void)
{
	return CARD_COLLECTION_SIZE;
}
/* <<< part card_id_collection_bytes */
/* >>> part card_gfx_prepare */
uint16_t card_gfx_prepare(uint16_t source)
{
#if PROFILE_FEATURE_THREE_PALETTE_CARDS
	uint16_t cursor = source;
	for (uint8_t i = 0u; i < 24u; i++)
		gb_write8((uint16_t)(wCardPalette_ADDR + i), gb_read8(cursor++));
	for (uint8_t i = 0u; i < 0x30u; i++)
		gb_write8((uint16_t)(wCardAttrMap_ADDR + i), gb_read8(cursor++));
	return cursor;
#else
	return source;
#endif
}
/* <<< part card_gfx_prepare */

/* >>> part card_gfx_finish */
void card_gfx_finish(uint16_t source)
{
#if !PROFILE_FEATURE_THREE_PALETTE_CARDS
	uint16_t cursor = wCardPalette_ADDR;
	for (uint8_t i = 0u; i < 8u; i++)
		gb_write8(cursor++, gb_read8(source++));
#else
	(void)source;
#endif
}
/* <<< part card_gfx_finish */
/* >>> part script_pointer_read */
uint16_t script_pointer_read(uint8_t *bank)
{
	*bank = 0u;
#if PROFILE_FEATURE_MULTI_BANK_SCRIPTS
	*bank = wNextScriptBank;
#endif
	return (uint16_t)(wNextScript | ((uint16_t)wNextScript_PTR[1] << 8));
}
/* <<< part script_pointer_read */

/* >>> part script_pointer_write */
void script_pointer_write(uint16_t address, uint8_t bank)
{
	wNextScript = (uint8_t)address;
	wNextScript_PTR[1] = (uint8_t)(address >> 8);
#if PROFILE_FEATURE_MULTI_BANK_SCRIPTS
	wNextScriptBank = bank;
#else
	(void)bank;
#endif
}
/* <<< part script_pointer_write */

/* >>> part card_id_compare_a */
uint8_t card_id_compare_a(CardId id, CardId constant)
{
#if PROFILE_FEATURE_NINE_BIT_CARD_IDS
	if ((id >> 8) != (constant >> 8))
		return (uint8_t)(id >> 8);
#else
	(void)constant;
#endif
	return (uint8_t)(id & 0xFFu);
}
/* <<< part card_id_compare_a */
