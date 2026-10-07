#include "save_import.h"

#include "generated/constants.h"
#include "generated/save_import_layout.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/load_deck.h"
#include "home/save.h"
#include "home/switch_sram.h"
#include "mem.h"
#include "persistence.h"
#include "profile.h"

#include <errno.h>
#include <stdio.h>
#include <string.h>

#define SRAM_WINDOW 0xA000u
#define SRAM_BANK_SIZE 0x2000u
#define BACKUP_BANK 2u

_Static_assert(VANILLA_DECK_STRUCT_SIZE == DECK_NAME_SIZE + DECK_SIZE, "vanilla decks hold one byte per card");
_Static_assert(VANILLA_CARD_COLLECTION_SIZE <= CARD_COLLECTION_SIZE, "the vanilla collection fits");
_Static_assert(VANILLA_DECK_TRAILER_SIZE == sCardAndDeckSaveDataEnd_ADDR - sCurrentlySelectedDeck_ADDR,
	"the deck trailer keeps its size");
_Static_assert(sCardAndDeckSaveDataEnd_ADDR - sCardCollection_ADDR <= SRAM_BANK_SIZE, "card data stays in bank 0");

static const uint8_t kSramSignature[] = {0x04u, 0x21u, 0x05u};

static const uint8_t *vanilla_byte(const uint8_t *image, uint8_t bank, uint16_t address)
{
	return image + bank * SRAM_BANK_SIZE + (address - SRAM_WINDOW);
}

static uint8_t *extended_byte(uint16_t address)
{
	return g_sram + (address - SRAM_WINDOW);
}

static int vanilla_diary_is_valid(const uint8_t *image)
{
	if (memcmp(vanilla_byte(image, 0u, SRAM_WINDOW), kSramSignature, sizeof kSramSignature) != 0)
		return 0;
	const uint8_t *header = vanilla_byte(image, BACKUP_BANK, VANILLA_GENERAL_HEADER_ADDR);
	const uint8_t *payload = vanilla_byte(image, BACKUP_BANK, VANILLA_GENERAL_PAYLOAD_ADDR);
	uint16_t sum = 0u;
	for (uint16_t i = 0u; i < VANILLA_GENERAL_PAYLOAD_SIZE; i++)
		sum = (uint16_t)(sum + payload[i]);
	return header[0] == 0x08u && header[1] == 0x00u &&
		(uint16_t)(header[2] | header[3] << 8) == VANILLA_GENERAL_PAYLOAD_SIZE &&
		(uint16_t)(header[4] | header[5] << 8) == sum;
}

static uint8_t mask_shift(uint8_t mask)
{
	uint8_t shift = 0u;
	while (!(mask & 1u)) {
		mask >>= 1;
		shift++;
	}
	return shift;
}

static void import_event_vars(const uint8_t *vanilla, uint8_t *extended)
{
	memset(extended, 0, SAVE_IMPORT_EVENT_VARS_SIZE);
	for (size_t i = 0u; i < sizeof kSaveImportEvents / sizeof kSaveImportEvents[0]; i++) {
		const SaveImportEvent *event = &kSaveImportEvents[i];
		uint8_t value = (uint8_t)((vanilla[event->vanilla_offset] & event->vanilla_mask) >>
			mask_shift(event->vanilla_mask));
		uint8_t placed = (uint8_t)((value << mask_shift(event->extended_mask)) & event->extended_mask);
		extended[event->extended_offset] = (uint8_t)((extended[event->extended_offset] &
			(uint8_t)~event->extended_mask) | placed);
	}
}

static void import_general_payload(const uint8_t *image)
{
	const uint8_t *source = vanilla_byte(image, BACKUP_BANK, VANILLA_GENERAL_PAYLOAD_ADDR);
	uint8_t *target = extended_byte(sGeneralSaveDataHeaderEnd_ADDR);
	size_t skip = 0u;
	for (uint16_t offset = 0u; offset < VANILLA_GENERAL_PAYLOAD_SIZE; offset++) {
		if (skip < sizeof kSaveImportGeneralSkips && kSaveImportGeneralSkips[skip] == offset) {
			skip++;
			continue;
		}
		*target++ = source[offset];
	}
	import_event_vars(vanilla_byte(image, BACKUP_BANK, VANILLA_EVENT_VARS_ADDR), extended_byte(sEventVars_ADDR));
	uint8_t *game_event = extended_byte(sActiveGameEvent_ADDR);
	*game_event = *game_event < sizeof kSaveImportGameEvents ? kSaveImportGameEvents[*game_event] : 0u;
	uint8_t *pc_item = extended_byte(sSelectedPCMenuItem_ADDR);
	*pc_item = *pc_item < sizeof kSaveImportPcMenuItems ? kSaveImportPcMenuItems[*pc_item] : 0u;
}

static void import_deck(const uint8_t *vanilla_deck, uint16_t extended_deck)
{
	memcpy(extended_byte(extended_deck), vanilla_deck, DECK_NAME_SIZE);
	for (uint8_t card = 0u; card < DECK_SIZE; card++) {
		gb_write8((uint16_t)(wPlayerDeck_ADDR + card * 2u), vanilla_deck[DECK_NAME_SIZE + card]);
		gb_write8((uint16_t)(wPlayerDeck_ADDR + card * 2u + 1u), 0u);
	}
	CompressDeckToSRAM(wPlayerDeck_ADDR, (uint16_t)(extended_deck + DECK_NAME_SIZE));
}

static unsigned import_decks(const uint8_t *image)
{
	const uint8_t *built = vanilla_byte(image, BACKUP_BANK, VANILLA_BUILT_DECKS_ADDR);
	for (uint8_t deck = 0u; deck < VANILLA_NUM_BUILT_DECKS; deck++)
		import_deck(built + deck * VANILLA_DECK_STRUCT_SIZE,
			(uint16_t)(sDeck1_ADDR + deck * DECK_COMPRESSED_STRUCT_SIZE));
	const uint8_t *saved = vanilla_byte(image, BACKUP_BANK, VANILLA_SAVED_DECKS_ADDR);
	uint8_t slot_of[VANILLA_NUM_SAVED_DECKS];
	uint8_t used[NUM_DECK_SAVE_MACHINE_SLOTS] = {0};
	unsigned dropped = 0u;
	for (uint8_t deck = 0u; deck < VANILLA_NUM_SAVED_DECKS; deck++) {
		slot_of[deck] = NUM_DECK_SAVE_MACHINE_SLOTS;
		if (saved[deck * VANILLA_DECK_STRUCT_SIZE] != 0u && deck < NUM_DECK_SAVE_MACHINE_SLOTS) {
			slot_of[deck] = deck;
			used[deck] = 1u;
		}
	}
	for (uint8_t deck = NUM_DECK_SAVE_MACHINE_SLOTS; deck < VANILLA_NUM_SAVED_DECKS; deck++) {
		if (saved[deck * VANILLA_DECK_STRUCT_SIZE] == 0u)
			continue;
		uint8_t slot = 0u;
		while (slot < NUM_DECK_SAVE_MACHINE_SLOTS && used[slot])
			slot++;
		if (slot == NUM_DECK_SAVE_MACHINE_SLOTS) {
			dropped++;
			continue;
		}
		slot_of[deck] = slot;
		used[slot] = 1u;
	}
	for (uint8_t deck = 0u; deck < VANILLA_NUM_SAVED_DECKS; deck++)
		if (slot_of[deck] < NUM_DECK_SAVE_MACHINE_SLOTS)
			import_deck(saved + deck * VANILLA_DECK_STRUCT_SIZE,
				(uint16_t)(sSavedDeck1_ADDR + slot_of[deck] * DECK_COMPRESSED_STRUCT_SIZE));
	return dropped;
}

static void import_sram(const uint8_t *image)
{
	memset(g_sram, 0, SAVE_PAYLOAD_SIZE);
	memcpy(g_sram, vanilla_byte(image, 0u, SRAM_WINDOW), sCardCollection_ADDR - SRAM_WINDOW);
	for (size_t i = 0u; i < sizeof kSaveImportHeaderCleared / sizeof kSaveImportHeaderCleared[0]; i++)
		memset(extended_byte(kSaveImportHeaderCleared[i].address), 0, kSaveImportHeaderCleared[i].size);
	memset(extended_byte(sCardCollection_ADDR), CARD_NOT_OWNED, CARD_COLLECTION_SIZE);
	memcpy(extended_byte(sCardCollection_ADDR),
		vanilla_byte(image, BACKUP_BANK, VANILLA_CARD_COLLECTION_ADDR), VANILLA_CARD_COLLECTION_SIZE);
	memcpy(extended_byte(sCurrentlySelectedDeck_ADDR),
		vanilla_byte(image, BACKUP_BANK, VANILLA_DECK_TRAILER_ADDR), VANILLA_DECK_TRAILER_SIZE);
	memcpy(extended_byte(SAVE_IMPORT_SHARED_BLOCK_ADDR),
		vanilla_byte(image, 0u, SAVE_IMPORT_SHARED_BLOCK_ADDR), SAVE_IMPORT_SHARED_BLOCK_SIZE);
	import_general_payload(image);
}

int save_import_convert(const char *vanilla_path, const char *extended_path)
{
	static uint8_t image[SAVE_PAYLOAD_SIZE];
	if (sram_read_payload(vanilla_path, PROFILE_ID_VANILLA, image) != 0) {
		fprintf(stderr, "save import: cannot read vanilla save %s: %s\n", vanilla_path, strerror(errno));
		return -1;
	}
	if (!vanilla_diary_is_valid(image)) {
		fprintf(stderr, "save import: %s has no diary save to continue from\n", vanilla_path);
		return -1;
	}
	import_sram(image);
	BankswitchSRAM(0u);
	EnableSRAM();
	unsigned dropped = import_decks(image);
	LoadGeneralSaveDataFromDE(sGeneralSaveData_ADDR);
	BankswitchSRAM(0u);
	EnableSRAM();
	CopyGeneralSaveDataToSRAM(sGeneralSaveData_ADDR);
	UpdateAlbumProgress(sAlbumProgress_ADDR);
	BankswitchSRAM(0u);
	WriteBackupGeneralSaveData();
	WriteBackupCardAndDeckSaveData();
	BankswitchSRAM(0u);
	DisableSRAM();
	if (dropped)
		fprintf(stderr, "save import: %u saved decks did not fit in the %u deck save slots\n",
			dropped, (unsigned)NUM_DECK_SAVE_MACHINE_SLOTS);
	if (sram_save_atomic(extended_path, PROFILE_ID_EXTENDED) != 0) {
		fprintf(stderr, "save import: cannot write %s: %s\n", extended_path, strerror(errno));
		return -1;
	}
	return 0;
}
