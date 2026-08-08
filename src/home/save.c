#include "home/save.h"

#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/card_collection.h"
#include "home/clear_saved_duel.h"
#include "home/switch_sram.h"
#include "mem.h"

/* WRAMToSRAMMapper:: save.asm:461-497, ROM bank 4. 6 bytes/entry: dw addr, dw count,
 * db min, db max; terminated by a zero address word. */
#define WRAM_TO_SRAM_MAPPER 0x5498u
#define NUM_PC_PACKS 15
#define PACK_UNOPENED 0x80

static const uint8_t *mapper_entry(unsigned index)
{
	return rom_ptr(0x04, (uint16_t)(WRAM_TO_SRAM_MAPPER + index * 6u));
}

/* Mapper sources are WRAM except for the four .EmptySRAMSlot entries ($556C), which
 * live in this file's own ROM bank. The asm reads them via the implicit code bank. */
static uint8_t save_src_read8(uint16_t addr)
{
	return addr < 0x8000 ? *rom_ptr(0x04, addr) : gb_read8(addr);
}

/* CopyGeneralSaveDataToSRAM:: save.asm:93-179 */
void CopyGeneralSaveDataToSRAM(uint16_t de)
{
	uint16_t header = de;
	uint16_t dst = (uint16_t)(de + (sGeneralSaveDataHeaderEnd_ADDR - sGeneralSaveData_ADDR));
	uint16_t byte_count = 0, checksum = 0;
	unsigned i;

	gb_write8(wGeneralSaveDataByteCount_ADDR + 0, 0);
	gb_write8(wGeneralSaveDataByteCount_ADDR + 1, 0);
	gb_write8(wGeneralSaveDataCheckSum_ADDR + 0, 0);
	gb_write8(wGeneralSaveDataCheckSum_ADDR + 1, 0);

	for (i = 0;; i++) {
		const uint8_t *p = mapper_entry(i);
		uint16_t src = (uint16_t)(p[0] | (uint16_t)p[1] << 8);
		uint16_t count;
		uint32_t n;

		/* save.asm:110-114 stores the (possibly terminating) source word into
		 * wTempPointer before testing it, so on the terminator wTempPointer
		 * ends at $0000 - unlike LoadGeneralSaveDataFromDE's walk. */
		gb_write8(wTempPointer_ADDR + 0, p[0]);
		gb_write8(wTempPointer_ADDR + 1, p[1]);
		if (src == 0)
			break;

		count = (uint16_t)(p[2] | (uint16_t)p[3] << 8);
		byte_count = (uint16_t)(byte_count + count);
		gb_write8(wGeneralSaveDataByteCount_ADDR + 0, (uint8_t)byte_count);
		gb_write8(wGeneralSaveDataByteCount_ADDR + 1, (uint8_t)(byte_count >> 8));

		n = count ? count : 0x10000u;
		while (n--) {
			uint8_t v = save_src_read8(src++);

			gb_write8(dst++, v);
			checksum = (uint16_t)(checksum + v);
			gb_write8(wGeneralSaveDataCheckSum_ADDR + 0, (uint8_t)checksum);
			gb_write8(wGeneralSaveDataCheckSum_ADDR + 1, (uint8_t)(checksum >> 8));
		}
		gb_write8(wTempPointer_ADDR + 0, (uint8_t)src);
		gb_write8(wTempPointer_ADDR + 1, (uint8_t)(src >> 8));
	}

	gb_write8(header++, 0x08);
	gb_write8(header++, 0x00);
	gb_write8(header++, (uint8_t)byte_count);
	gb_write8(header++, (uint8_t)(byte_count >> 8));
	gb_write8(header++, (uint8_t)checksum);
	gb_write8(header, (uint8_t)(checksum >> 8));
}

/* ValidateGeneralSaveDataFromDE:: save.asm:218-344 */
void ValidateGeneralSaveDataFromDE(uint16_t de)
{
	uint8_t header0 = gb_read8((uint16_t)(de + 0));
	uint8_t header1 = gb_read8((uint16_t)(de + 1));
	uint16_t byte_count = (uint16_t)(gb_read8((uint16_t)(de + 2)) |
					  (uint16_t)gb_read8((uint16_t)(de + 3)) << 8);
	uint16_t checksum = (uint16_t)(gb_read8((uint16_t)(de + 4)) |
					(uint16_t)gb_read8((uint16_t)(de + 5)) << 8);
	uint16_t payload = (uint16_t)(de + (sGeneralSaveDataHeaderEnd_ADDR - sGeneralSaveData_ADDR));
	uint8_t residue;
	unsigned i;

	/* The count and checksum residues live in WRAM, not in registers: the asm seeds
	 * them from the header (save.asm:226-241), subtracts in place, and the final
	 * header test ORs them straight back out (save.asm:307-315). Both are observable
	 * outputs, so every store the asm makes is mirrored here. */
	gb_write8(wGeneralSaveDataByteCount_ADDR + 0, (uint8_t)byte_count);
	gb_write8(wGeneralSaveDataByteCount_ADDR + 1, (uint8_t)(byte_count >> 8));
	gb_write8(wGeneralSaveDataCheckSum_ADDR + 0, (uint8_t)checksum);
	gb_write8(wGeneralSaveDataCheckSum_ADDR + 1, (uint8_t)(checksum >> 8));
	gb_write8(wNumSRAMValidationErrors_ADDR, 0);

	for (i = 0;; i++) {
		const uint8_t *p = mapper_entry(i);
		uint16_t addr = (uint16_t)(p[0] | (uint16_t)p[1] << 8);
		uint16_t count;
		uint8_t min, max;
		uint32_t n;

		if (addr == 0)
			break;
		count = (uint16_t)(p[2] | (uint16_t)p[3] << 8);
		min = p[4];
		max = p[5];
		byte_count = (uint16_t)(byte_count - count);
		gb_write8(wGeneralSaveDataByteCount_ADDR + 0, (uint8_t)byte_count);
		gb_write8(wGeneralSaveDataByteCount_ADDR + 1, (uint8_t)(byte_count >> 8));

		/* Every byte of this entry is range-checked against the same entry's
		 * min/max - save.asm:267,294 push/pop hl around the whole byte loop. */
		n = count ? count : 0x10000u;
		while (n--) {
			uint8_t v = gb_read8(payload++);

			checksum = (uint16_t)(checksum - v);
			gb_write8(wGeneralSaveDataCheckSum_ADDR + 0, (uint8_t)checksum);
			gb_write8(wGeneralSaveDataCheckSum_ADDR + 1, (uint8_t)(checksum >> 8));
			if (v < min || v > max)
				gb_write8(wNumSRAMValidationErrors_ADDR,
					  (uint8_t)(gb_read8(wNumSRAMValidationErrors_ADDR) + 1));
		}
	}

	residue = (uint8_t)((uint8_t)(header0 - 0x08) | (uint8_t)(header1 - 0x00));
	residue = (uint8_t)(residue | (uint8_t)byte_count | (uint8_t)(byte_count >> 8));
	residue = (uint8_t)(residue | (uint8_t)checksum | (uint8_t)(checksum >> 8));
	if (residue)
		gb_write8(wNumSRAMValidationErrors_ADDR,
			  (uint8_t)(gb_read8(wNumSRAMValidationErrors_ADDR) + 1));

	/* save.asm:324 restores de to the original argument (not the advanced payload
	 * pointer) before these final copies. */
	gb_write8(wPlayTimeHourMinutes_ADDR + 0,
		  gb_read8((uint16_t)(de + (sPlayTimeCounter_ADDR + 2 - sGeneralSaveData_ADDR))));
	gb_write8(wPlayTimeHourMinutes_ADDR + 1,
		  gb_read8((uint16_t)(de + (sPlayTimeCounter_ADDR + 3 - sGeneralSaveData_ADDR))));
	gb_write8(wPlayTimeHourMinutes_ADDR + 2,
		  gb_read8((uint16_t)(de + (sPlayTimeCounter_ADDR + 4 - sGeneralSaveData_ADDR))));

	gb_write8(wMedalCount_ADDR,
		  gb_read8((uint16_t)(de + (sGeneralSaveDataHeaderEnd_ADDR - sGeneralSaveData_ADDR))));
	gb_write8(wCurOverworldMap_ADDR,
		  gb_read8((uint16_t)(de + (sGeneralSaveDataHeaderEnd_ADDR - sGeneralSaveData_ADDR) + 1)));
}

/* LoadGeneralSaveDataFromDE:: save.asm:380-448 */
void LoadGeneralSaveDataFromDE(uint16_t de)
{
	uint16_t src = (uint16_t)(de + (sGeneralSaveDataHeaderEnd_ADDR - sGeneralSaveData_ADDR));
	unsigned i;

	EnableSRAM();

	gb_write8(wTempPointer_ADDR + 0, (uint8_t)src);
	gb_write8(wTempPointer_ADDR + 1, (uint8_t)(src >> 8));

	for (i = 0;; i++) {
		const uint8_t *p = mapper_entry(i);
		uint16_t dst = (uint16_t)(p[0] | (uint16_t)p[1] << 8);
		uint16_t count;
		uint32_t n;

		if (dst == 0)
			break;
		count = (uint16_t)(p[2] | (uint16_t)p[3] << 8);
		/* p[4]/p[5] (min/max) are ignored on the load path - save.asm:408-412. */

		n = count ? count : 0x10000u;
		while (n--)
			/* dst can be $556C (.EmptySRAMSlot); gb_write8 below $8000 decodes
			 * that as an MBC5 register write, not a memory write - the RAM
			 * bank select this whole slice exists to model. */
			gb_write8(dst++, gb_read8(src++));

		gb_write8(wTempPointer_ADDR + 0, (uint8_t)src);
		gb_write8(wTempPointer_ADDR + 1, (uint8_t)(src >> 8));
	}

	EnableSRAM();
	gb_write8(wAnimationsDisabled_ADDR, gb_read8(sAnimationsDisabled_ADDR));
	gb_write8(wTextSpeed_ADDR, gb_read8(sTextSpeed_ADDR));
	DisableSRAM();
}

/* WriteDataToBackup:: save.asm:569-588. Per-byte bank flip, not hoisted: hBankSRAM
 * is observable mid-loop and the flip itself is the behaviour under test. */
void WriteDataToBackup(uint16_t hl, uint16_t bc)
{
	uint8_t saved = hBankSRAM;
	uint32_t n = bc ? bc : 0x10000u;

	while (n--) {
		uint8_t v;

		BankswitchSRAM(0x00);
		v = gb_read8(hl);
		BankswitchSRAM(0x02);
		gb_write8(hl, v);
		hl++;
	}
	BankswitchSRAM(saved);
	DisableSRAM();
}

/* LoadDataFromBackup:: save.asm:602-622. Mirror of WriteDataToBackup with the bank
 * order swapped: read backup (bank 2) first, then write the main bank (bank 0). */
void LoadDataFromBackup(uint16_t hl, uint16_t bc)
{
	uint8_t saved = hBankSRAM;
	uint32_t n = bc ? bc : 0x10000u;

	while (n--) {
		uint8_t v;

		BankswitchSRAM(0x02);
		v = gb_read8(hl);
		BankswitchSRAM(0x00);
		gb_write8(hl, v);
		hl++;
	}
	BankswitchSRAM(saved);
	DisableSRAM();
}

/* WriteBackupGeneralSaveData:: save.asm:562-565 */
void WriteBackupGeneralSaveData(void)
{
	WriteDataToBackup(sGeneralSaveData_ADDR, (uint16_t)(sGeneralSaveDataEnd_ADDR - sGeneralSaveData_ADDR));
}

/* WriteBackupCardAndDeckSaveData:: save.asm:557-560 */
void WriteBackupCardAndDeckSaveData(void)
{
	WriteDataToBackup(sCardCollection_ADDR,
			   (uint16_t)(sCardAndDeckSaveDataEnd_ADDR - sCardAndDeckSaveData_ADDR));
}

/* LoadBackupGeneralSaveData:: save.asm:595-598 */
void LoadBackupGeneralSaveData(void)
{
	LoadDataFromBackup(sGeneralSaveData_ADDR, (uint16_t)(sGeneralSaveDataEnd_ADDR - sGeneralSaveData_ADDR));
}

/* LoadBackupCardAndDeckSaveData:: save.asm:590-593 */
void LoadBackupCardAndDeckSaveData(void)
{
	LoadDataFromBackup(sCardCollection_ADDR,
			    (uint16_t)(sCardAndDeckSaveDataEnd_ADDR - sCardAndDeckSaveData_ADDR));
}

/* CP 1 on wNumSRAMValidationErrors: Z if n==1, N always, H if the low nibble
 * borrows, C if n<1. Both validators branch on the resulting carry. */
static uint8_t cp1_flags(uint8_t n)
{
	return (uint8_t)((n == 1 ? 0x80 : 0) | 0x40 | ((n & 0x0F) == 0 ? 0x20 : 0)
			  | (n == 0 ? 0x10 : 0));
}

/* InvalidateSaveData:: save.asm:4-25 */
void InvalidateSaveData(void)
{
	uint8_t saved = hBankSRAM;

	BankswitchSRAM(2); /* BANK("SRAM2") */
	gb_write8(sBackupGeneralSaveData_ADDR + 0, (uint8_t)(0x08 ^ 0xFF));
	gb_write8(sBackupGeneralSaveData_ADDR + 1, (uint8_t)(0x00 ^ 0xFF));
	BankswitchSRAM(saved);

	DisableSRAM();
	EnableSRAM();
	ClearSavedDuel();
	DisableSRAM();
}

/* UpdateAlbumProgress:: save.asm:73-89. No bank switch: writes into whichever
 * SRAM bank is already selected, not sAlbumProgress's declared bank. */
void UpdateAlbumProgress(uint16_t de)
{
	AlbumProgress ap = GetCardAlbumProgress();

	EnableSRAM();
	gb_write8(wTotalNumCardsCollected_ADDR, ap.d);
	gb_write8(de, ap.d);
	gb_write8(wTotalNumCardsToCollect_ADDR, ap.e);
	gb_write8((uint16_t)(de + 1), ap.e);
	DisableSRAM();
}

/* LoadAlbumProgressFromSRAM:: save.asm:346-354 */
void LoadAlbumProgressFromSRAM(uint16_t de)
{
	gb_write8(wTotalNumCardsCollected_ADDR, gb_read8(de));
	gb_write8(wTotalNumCardsToCollect_ADDR, gb_read8((uint16_t)(de + 1)));
}

/* ValidateBackupGeneralSaveData:: save.asm:183-199 */
ValidateResult ValidateBackupGeneralSaveData(void)
{
	uint8_t saved = hBankSRAM;
	uint8_t n;

	BankswitchSRAM(sBackupGeneralSaveData_BANK);
	ValidateGeneralSaveDataFromDE(sBackupGeneralSaveData_ADDR);
	LoadAlbumProgressFromSRAM(sAlbumProgress_ADDR);
	BankswitchSRAM(saved);
	DisableSRAM();

	n = gb_read8(wNumSRAMValidationErrors_ADDR);
	return (ValidateResult){ .a = n, .f = cp1_flags(n) };
}

/* _ValidateGeneralSaveData:: save.asm:203-214. Unlike ValidateBackupGeneralSaveData,
 * this never bank-switches, so LoadAlbumProgressFromSRAM reads sAlbumProgress's
 * address out of whichever bank is already selected - bank 0 padding on the normal
 * path, not the real bank-2 value. Reproduced as-is; no live caller today. */
ValidateResult _ValidateGeneralSaveData(void)
{
	uint8_t n;

	EnableSRAM();
	ValidateGeneralSaveDataFromDE(sGeneralSaveData_ADDR);
	LoadAlbumProgressFromSRAM(sAlbumProgress_ADDR);
	DisableSRAM();

	n = gb_read8(wNumSRAMValidationErrors_ADDR);
	return (ValidateResult){ .a = n, .f = cp1_flags(n) };
}

/* LoadBackupSaveData:: save.asm:358-370 */
void LoadBackupSaveData(void)
{
	EnableSRAM();
	ClearSavedDuel();
	DisableSRAM();
	LoadBackupGeneralSaveData();
	LoadBackupCardAndDeckSaveData();
	LoadGeneralSaveDataFromDE(sGeneralSaveData_ADDR);
}

/* _LoadGeneralSaveData:: save.asm:372-377 */
void _LoadGeneralSaveData(void)
{
	LoadGeneralSaveDataFromDE(sGeneralSaveData_ADDR);
}

/* _AddCardToCollectionAndUpdateAlbumProgress:: save.asm:529-555. The second pass
 * (marked unintentional in the disassembly) repeats under the restored bank with
 * sAlbumProgress written as the bare literal $b8fe; CreateTempCardCollection reads
 * deck data under two different banks, so the 99-card clamp can genuinely differ
 * between the two passes. Not collapsed. */
void _AddCardToCollectionAndUpdateAlbumProgress(uint8_t a)
{
	uint8_t saved;

	gb_write8(wCardToAddToCollection_ADDR, a);

	saved = hBankSRAM;
	BankswitchSRAM(sAlbumProgress_BANK);
	AddCardToCollection(gb_read8(wCardToAddToCollection_ADDR));
	UpdateAlbumProgress(sAlbumProgress_ADDR);
	BankswitchSRAM(saved);
	DisableSRAM();

	AddCardToCollection(gb_read8(wCardToAddToCollection_ADDR));
	UpdateAlbumProgress(0xB8FE);
}

/* EventVarMasks and MedalEvents live in ROM bank 3 (scripting.asm:388/355), read
 * via the code bank there -- a farcall target. Both are 2- and 1-byte records. */
#define EVENT_VAR_MASKS 0x4B37u
#define MEDAL_EVENTS    0x4B15u
#define EV_ISHIHARA_MENT 0x1eu
#define EV_LEGENDARY     0x22u
#define EV_MEDAL_COUNT   0x2eu
#define OWMAP_ISHIHARA   0x02u
#define OWMAP_MYSTERY    0x0du
#define OWMAP_MASON      0x01u
#define MAP_MASON        0x01u
#define DIR_SOUTH        0x02u

/* GetEventVar:: scripting.asm:366-382. Returns wEventVars+offset and stashes the
 * mask in wLoadedEventBits, exactly as the asm leaves it for Get/SetEventValue. */
static uint16_t get_event_var(uint8_t ev)
{
	const uint8_t *p = rom_ptr(0x03, (uint16_t)(EVENT_VAR_MASKS + (uint16_t)ev * 2u));

	gb_write8(wLoadedEventBits_ADDR, p[1]);
	return (uint16_t)(wEventVars_ADDR + p[0]);
}

/* GetEventValue:: scripting.asm:213-230. */
static uint8_t get_event_value(uint8_t ev)
{
	uint16_t addr = get_event_var(ev);
	uint8_t mask = gb_read8(wLoadedEventBits_ADDR);
	uint8_t c = gb_read8(addr);

	while (!(mask & 1)) {
		mask = (uint8_t)(mask >> 1);
		c = (uint8_t)(c >> 1);
	}
	return (uint8_t)(mask & c);
}

/* SetEventValue:: scripting.asm:248-270. The shift loop uses a copy; the merge
 * re-reads the original field mask from wLoadedEventBits, as the asm does. */
static void set_event_value(uint8_t ev, uint8_t value)
{
	uint16_t addr = get_event_var(ev);
	uint8_t mask = gb_read8(wLoadedEventBits_ADDR);
	uint8_t c = value;
	uint8_t m = mask;

	while (!(m & 1)) {
		m = (uint8_t)(m >> 1);
		c = (uint8_t)(c << 1);
	}
	gb_write8(addr, (uint8_t)((gb_read8(addr) & (uint8_t)~mask) | (uint8_t)(c & mask)));
}

/* TryGivePCPack:: mail.asm:509-544. */
static void try_give_pc_pack(uint8_t id)
{
	uint16_t hl = wPCPacks_ADDR;
	uint8_t c = NUM_PC_PACKS;

	do {
		if ((uint8_t)(gb_read8(hl) & 0x7f) == id)
			return;
		hl++;
	} while (--c);

	hl = wPCPacks_ADDR;
	c = NUM_PC_PACKS;
	do {
		if ((uint8_t)(gb_read8(hl) & 0x7f) == 0) {
			gb_write8(hl, (uint8_t)(id | PACK_UNOPENED));
			return;
		}
		hl++;
	} while (--c);
}

/* TryGiveMedalPCPacks:: scripting.asm:311-353. The three grants are fall-through
 * (not else-if): >=8 gives $c/$b/$a, >=7 gives $b/$a, >=3 gives $a. Returns the
 * medal count, restored from a pushed copy after the grants. */
static uint8_t try_give_medal_pc_packs(void)
{
	const uint8_t *events = rom_ptr(0x03, MEDAL_EVENTS);
	uint8_t count = 0;
	int i;

	for (i = 0; i < 8; i++)
		if (get_event_value(events[i]))
			count++;

	set_event_value(EV_MEDAL_COUNT, count);
	if (count >= 8)
		try_give_pc_pack(0x0c);
	if (count >= 7)
		try_give_pc_pack(0x0b);
	if (count >= 3)
		try_give_pc_pack(0x0a);
	return count;
}

/* OverworldMap_GetOWMapID:: overworld_map.asm:165-179. */
static uint8_t overworld_map_get_owmap_id(void)
{
	uint8_t sel = gb_read8(wOverworldMapSelection_ADDR);

	if (sel != OWMAP_ISHIHARA)
		return sel;
	if (get_event_value(EV_ISHIHARA_MENT))
		return sel;
	return OWMAP_MYSTERY;
}

/* GetReceivedLegendaryCards:: map.asm:148-154. */
static void get_received_legendary_cards(void)
{
	uint8_t a = get_event_value(EV_LEGENDARY);

	EnableSRAM();
	gb_write8(sReceivedLegendaryCards_ADDR, a);
	DisableSRAM();
}

/* BackupPlayerPosition:: overworld.asm:279-288. */
static void backup_player_position(void)
{
	gb_write8(wTempMap_ADDR, gb_read8(wCurMap_ADDR));
	gb_write8(wTempPlayerXCoord_ADDR, gb_read8(wPlayerXCoord_ADDR));
	gb_write8(wTempPlayerYCoord_ADDR, gb_read8(wPlayerYCoord_ADDR));
	gb_write8(wTempPlayerDirection_ADDR, gb_read8(wPlayerDirection_ADDR));
}

/* SaveGeneralSaveDataFromDE:: save.asm:52-68. */
void SaveGeneralSaveDataFromDE(uint16_t de)
{
	EnableSRAM();
	gb_write8(wMedalCount_ADDR, try_give_medal_pc_packs());
	gb_write8(wCurOverworldMap_ADDR, overworld_map_get_owmap_id());
	CopyGeneralSaveDataToSRAM(de);
	DisableSRAM();
}

/* _SaveGeneralSaveData:: save.asm:41-49. */
void _SaveGeneralSaveData(void)
{
	get_received_legendary_cards();
	SaveGeneralSaveDataFromDE(sGeneralSaveData_ADDR);
	UpdateAlbumProgress(sAlbumProgress_ADDR);
}

/* SaveAndBackupData:: save.asm:30-39. */
void SaveAndBackupData(void)
{
	SaveGeneralSaveDataFromDE(sGeneralSaveData_ADDR);
	UpdateAlbumProgress(sAlbumProgress_ADDR);
	WriteBackupGeneralSaveData();
	WriteBackupCardAndDeckSaveData();
}

/* _SaveGame:: save.asm:506-527. The farcall to BackupPlayerPosition becomes a
 * plain call under the Phase 1 transform. */
void _SaveGame(uint8_t c)
{
	if (c) {
		gb_write8(wTempPlayerXCoord_ADDR, 0x02);
		gb_write8(wTempPlayerYCoord_ADDR, 0x04);
		gb_write8(wTempPlayerDirection_ADDR, DIR_SOUTH);
		gb_write8(wTempMap_ADDR, MAP_MASON);
		gb_write8(wOverworldMapSelection_ADDR, OWMAP_MASON);
	} else {
		backup_player_position();
	}
	SaveAndBackupData();
}

/* SaveGeneralSaveData:: save.asm:1-3. farcall trampoline, no push/pop around it,
 * so it is register-transparent to _SaveGeneralSaveData. */
void SaveGeneralSaveData(void)
{
	_SaveGeneralSaveData();
}

/* LoadGeneralSaveData:: save.asm:5-7. Same trampoline shape as SaveGeneralSaveData. */
void LoadGeneralSaveData(void)
{
	_LoadGeneralSaveData();
}

/* ValidateGeneralSaveData:: save.asm:9-11. Same trampoline shape. */
ValidateResult ValidateGeneralSaveData(void)
{
	return _ValidateGeneralSaveData();
}

/* AddCardToCollectionAndUpdateAlbumProgress:: save.asm:15-17. Same trampoline
 * shape; a is the consumed card ID, passed straight through. */
void AddCardToCollectionAndUpdateAlbumProgress(uint8_t a)
{
	_AddCardToCollectionAndUpdateAlbumProgress(a);
}

/* SaveGame:: save.asm:19-30. Unlike its four siblings above, this pushes af/bc/de/hl
 * before the farcall and pops them back after, so every entry register survives
 * regardless of what _SaveGame does -- and c is hardcoded to 0 (the "save at current
 * position" branch) before the farcall, so the caller's c is never actually read by
 * the callee despite being preserved back out. */
void SaveGame(void)
{
	_SaveGame(0);
}
