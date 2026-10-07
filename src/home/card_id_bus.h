#ifndef POKETCG_HOME_CARD_ID_BUS_H
#define POKETCG_HOME_CARD_ID_BUS_H

/* >>> part includes */
#include <stdint.h>

#include "home/card_id.h"
/* <<< part includes */

/* >>> part card_id_read */
CardId card_id_read(uint16_t *address);
/* <<< part card_id_read */
/* >>> part card_id_read_at */
CardId card_id_read_at(uint16_t address);
/* <<< part card_id_read_at */
/* >>> part card_id_write */
void card_id_write(uint16_t *address, CardId id);
/* <<< part card_id_write */
/* >>> part card_id_index_address */
uint16_t card_id_index_address(uint16_t base, uint8_t index);
/* <<< part card_id_index_address */
/* >>> part card_id_deck_bytes */
uint16_t card_id_deck_bytes(uint8_t count);
/* <<< part card_id_deck_bytes */

/* >>> part card_id_collection_bytes */
uint16_t card_id_collection_bytes(void);
/* <<< part card_id_collection_bytes */
/* >>> part card_gfx_prepare */
uint16_t card_gfx_prepare(uint16_t source);
/* <<< part card_gfx_prepare */
/* >>> part card_gfx_finish */
void card_gfx_finish(uint16_t source);
/* <<< part card_gfx_finish */
/* >>> part script_pointer_read */
uint16_t script_pointer_read(uint8_t *bank);
/* <<< part script_pointer_read */
/* >>> part script_pointer_write */
void script_pointer_write(uint16_t address, uint8_t bank);
/* <<< part script_pointer_write */
#endif
