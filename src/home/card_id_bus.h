#ifndef POKETCG_HOME_CARD_ID_BUS_H
#define POKETCG_HOME_CARD_ID_BUS_H

#include <stdint.h>

#include "home/card_id.h"

CardId card_id_read(uint16_t *address);
CardId card_id_read_at(uint16_t address);
void card_id_write(uint16_t *address, CardId id);
uint16_t card_id_index_address(uint16_t base, uint8_t index);
uint16_t card_id_deck_bytes(uint8_t count);

uint16_t card_id_collection_bytes(void);
uint16_t card_gfx_prepare(uint16_t source);
void card_gfx_finish(uint16_t source);
uint16_t script_pointer_read(uint8_t *bank);
void script_pointer_write(uint16_t address, uint8_t bank);
#endif
