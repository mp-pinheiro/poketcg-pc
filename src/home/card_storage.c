/* >>> part includes */
#include "home/card_storage.h"
#include <stddef.h>
/* <<< part includes */


/* >>> part card_id_is_valid */
static uint8_t card_id_is_valid(CardId id)
{
	return (uint8_t)(id <= CARD_ID_MAX);
}
/* <<< part card_id_is_valid */

/* >>> part CompressCardIdDeck */
uint8_t CompressCardIdDeck(const CardId *cards, uint8_t *compressed)
{
	if (cards == NULL || compressed == NULL)
		return 0u;
	for (uint8_t index = 0u; index < CARD_DECK_SIZE; index++)
		if (!card_id_is_valid(cards[index]))
			return 0u;
	uint8_t *out = compressed;
	for (uint8_t group = 0u; group < 7u; group++) {
		uint8_t command = 0u;
		for (uint8_t bit = 0u; bit < 8u; bit++)
			if ((cards[group * 8u + bit] & 0x0100u) != 0u)
				command |= (uint8_t)(1u << (7u - bit));
		*out++ = command;
		for (uint8_t bit = 0u; bit < 8u; bit++)
			*out++ = (uint8_t)cards[group * 8u + bit];
	}
	uint8_t command = 0u;
	for (uint8_t bit = 0u; bit < 4u; bit++)
		if ((cards[56u + bit] & 0x0100u) != 0u)
			command |= (uint8_t)(1u << (7u - bit));
	*out++ = command;
	for (uint8_t bit = 0u; bit < 4u; bit++)
		*out++ = (uint8_t)cards[56u + bit];
	return (uint8_t)(out - compressed == CARD_DECK_COMPRESSED_SIZE);
}
/* <<< part CompressCardIdDeck */

/* >>> part DecompressCardIdDeck */
uint8_t DecompressCardIdDeck(const uint8_t *compressed, CardId *cards)
{
	if (compressed == NULL || cards == NULL)
		return 0u;
	const uint8_t *in = compressed;
	for (uint8_t group = 0u; group < 7u; group++) {
		uint8_t command = *in++;
		for (uint8_t bit = 0u; bit < 8u; bit++)
			cards[group * 8u + bit] = (CardId)(*in++ | ((command >> (7u - bit) & 1u) << 8));
	}
	uint8_t command = *in++;
	for (uint8_t bit = 0u; bit < 4u; bit++)
		cards[56u + bit] = (CardId)(*in++ | ((command >> (7u - bit) & 1u) << 8));
	return (uint8_t)(in - compressed == CARD_DECK_COMPRESSED_SIZE);
}
/* <<< part DecompressCardIdDeck */
