#include "home/challenge_machine.h"

#include "generated/sram.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "mem.h"
/* >>> factory statics */
#include "home/challenge_machine.h"
#include "home/random.h"
#include "home/switch_sram.h"
#include "generated/sram.h"
#include "mem.h"

#define CLUB_MASTERS_START 0x18u
#define GRAND_MASTERS_START 0x20u
#define NUM_CHALLENGE_MACHINE_OPPONENTS 0x05u

/* challenge_machine.asm:781-789 ChallengeMachine_FinalOpponentProbabilities.
 * Pairs of (probability weight, opponent id); the last weight is a catch-all. */
static const uint8_t ChallengeMachine_FinalOpponentProbabilities[16] = {
	56u, (uint8_t)(GRAND_MASTERS_START + 0u),
	56u, (uint8_t)(GRAND_MASTERS_START + 1u),
	56u, (uint8_t)(GRAND_MASTERS_START + 2u),
	56u, (uint8_t)(GRAND_MASTERS_START + 3u),
	8u, (uint8_t)(GRAND_MASTERS_START + 4u),
	8u, (uint8_t)(GRAND_MASTERS_START + 5u),
	8u, (uint8_t)(GRAND_MASTERS_START + 6u),
	255u, (uint8_t)(GRAND_MASTERS_START + 7u),
};

#include "home/copy.h"
#include "home/switch_sram.h"
#include "mem.h"

#define NAME_BUFFER_LENGTH 0x10u
#define TRUE_VALUE 0x01u
#define WIN_CAP_HIGH 0x03u
#define WIN_CAP_LOW 0xE7u

/* wChallengeMachineOpponent is not exposed by generated/wram.h in this build. */
#define wChallengeMachineOpponent_ADDR 0xD692u

#include "generated/sram.h"
#include "generated/wram.h"
#include "home/switch_sram.h"

#include "home/challenge_machine.h"
#include "generated/sram.h"
#include "home/switch_sram.h"
#include "mem.h"

#include "home/challenge_machine.h"
#include "home/switch_sram.h"
#define sPlayerInChallengeMachine_ADDR 0xBA44u
#define sTotalChallengeMachineWins_ADDR 0xBA45u
#define sPresentConsecutiveWins_ADDR 0xBA47u
#define sPresentConsecutiveWinsBackup_ADDR 0xBA49u

#include "home/challenge_machine.h"
#include "home/switch_sram.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "generated/sram.h"
#define ConsecutiveWinsEndedAtText 0x07e2u

#include "home/challenge_machine.h"
#include "home/switch_sram.h"
#include "home/sound.h"
#include "home/play_song.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "generated/sram.h"
#define MUSIC_MEDAL 0x1du
#define ConsecutiveWinRecordIncreasedText 0x07e8u
#define sConsecutiveWinRecordIncreased_ADDR 0xBA68u
#define sMaximumConsecutiveWins_ADDR 0xBA56u

#include "home/switch_sram.h"
#include "home/sound.h"
#include "home/play_song.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "generated/sram.h"
#define Defeated5OpponentsText 0x07e6u
#define WonAgainstXOpponentsText 0x07e5u

#include "home/npc_data.h"
#include "generated/wram.h"
#include "mem.h"
#define CHALLENGE_MACHINE_DATA_BANK_500 0x04u
#define CHALLENGE_MACHINE_OPPONENT_DECK_IDS_ADDR_500 0x7707u

#include "home/empty_screen.h"
#include "home/print_stats.h"
#include "home/switch_sram.h"
#include "home/bg_map.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/challenge_machine.h"
#include "mem.h"

#include "home/challenge_machine.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "mem.h"

#include "home/challenge_machine.h"
#include "home/switch_sram.h"
#include "generated/wram.h"
#include "generated/sram.h"
#include "mem.h"
#define CHALLENGE_MACHINE_PRIZES_ADDR 0x7362u

#include "home/challenge_machine.h"
#include "home/copy.h"
#include "home/switch_sram.h"
#include "home/text_box.h"
#include "home/init_menu.h"
#include "home/labels.h"
#include "home/process_text.h"
#include "generated/wram.h"
#include "mem.h"
#define CHALLENGE_MACHINE_RECORD_HOLDER_NAME_ADDR 0xBA58u
#define CHALLENGE_MACHINE_PLAYER_SCORE_LABELS_ADDR 0x74F2u
#define CHALLENGE_MACHINE_PLAYER_SCORE_VALUES_ADDR 0x750Fu

#include "generated/wram.h"
#include "generated/sram.h"
#include "home/challenge_machine.h"
#include "home/switch_sram.h"
#include "home/print_text.h"
#include "home/menus.h"
#include "mem.h"
#define NthOpponentIsText 0x07dbu
#define WouldYouLikeToBeginTheDuelText 0x07dcu
#define XConsecutiveWinsNthOpponentIsText 0x07dau

#include "home/switch_sram.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "generated/sram.h"
#include "mem.h"
#define CHALLENGE_MACHINE_NOT_DUELLED_ICON_TEXT 0x07F3u
#define CHALLENGE_MACHINE_DUEL_WON_ICON_TEXT 0x07F4u
#define CHALLENGE_MACHINE_DUEL_LOST_ICON_TEXT 0x07F5u
static const uint16_t challenge_machine_duel_result_icons[3] = {
	CHALLENGE_MACHINE_NOT_DUELLED_ICON_TEXT,
	CHALLENGE_MACHINE_DUEL_WON_ICON_TEXT,
	CHALLENGE_MACHINE_DUEL_LOST_ICON_TEXT,
};
/* <<< factory statics */

ChallengeMachineCheckResult ChallengeMachine_CheckIfOpponentAlreadySelected(uint8_t a, uint8_t c)
{
	uint16_t hl = sChallengeMachineOpponents_ADDR;
	uint16_t n = c ? c : 0x100u;
	while (n--) {
		if (a == gb_read8(hl))
			return (ChallengeMachineCheckResult){hl, 0x90u};
		hl = (uint16_t)(hl + 1u);
	}
	return (ChallengeMachineCheckResult){hl, a ? 0x00u : 0x80u};
}

ChallengeMachinePrintResult ChallengeMachine_PrintText(uint16_t hl, uint8_t b, uint8_t c)
{
	uint16_t text = (uint16_t)(gb_read8(hl) | ((uint16_t)gb_read8((uint16_t)(hl + 1u)) << 8));
	InitTextPrinting(b, c);
	TextResult result = PrintTextNoDelay(text, b, c);
	return (ChallengeMachinePrintResult){result.hl, b, c};
}

/* >>> factory ChallengeMachine_PickOpponentSequence */
/* challenge_machine.asm:697-779. No arguments and no register outputs: a/f are
 * whatever DisableSRAM leaves, hl is loop residue ($BA55), c is 0 after the
 * clear loop. The whole contract is the SRAM image. */
void ChallengeMachine_PickOpponentSequence(void)
{
	EnableSRAM();

	/* first opponent: any club member */
	gb_write8(sChallengeMachineOpponents_ADDR, Random(CLUB_MASTERS_START));

	/* second opponent: reroll while it duplicates the first */
	for (;;) {
		uint8_t a = Random(CLUB_MASTERS_START);
		ChallengeMachineCheckResult r =
			ChallengeMachine_CheckIfOpponentAlreadySelected(a, 1u);
		if (!(r.f & 0x10u)) {
			gb_write8((uint16_t)(sChallengeMachineOpponents_ADDR + 1u), a);
			break;
		}
	}

	/* third opponent: reroll while it duplicates either earlier pick */
	for (;;) {
		uint8_t a = Random(CLUB_MASTERS_START);
		ChallengeMachineCheckResult r =
			ChallengeMachine_CheckIfOpponentAlreadySelected(a, 2u);
		if (!(r.f & 0x10u)) {
			gb_write8((uint16_t)(sChallengeMachineOpponents_ADDR + 2u), a);
			break;
		}
	}

	/* fourth opponent: a club master, no duplicate check */
	{
		uint8_t a = Random((uint8_t)(GRAND_MASTERS_START - CLUB_MASTERS_START));
		a = (uint8_t)(a + CLUB_MASTERS_START);
		gb_write8((uint16_t)(sChallengeMachineOpponents_ADDR + 3u), a);
	}

	/* fifth opponent: weighted pick from the probability table */
	{
		uint8_t a = UpdateRNGSources();
		uint8_t i = 0;
		while (a >= ChallengeMachine_FinalOpponentProbabilities[i]) {
			a = (uint8_t)(a - ChallengeMachine_FinalOpponentProbabilities[i]);
			i = (uint8_t)(i + 2u);
		}
		gb_write8((uint16_t)(sChallengeMachineOpponents_ADDR + 4u),
			ChallengeMachine_FinalOpponentProbabilities[i + 1u]);
	}

	gb_write8(sChallengeMachineOpponentNumber_ADDR, 0u);
	gb_write8(sConsecutiveWinRecordIncreased_ADDR, 0u);
	for (uint8_t i = 0; i < NUM_CHALLENGE_MACHINE_OPPONENTS; i++)
		gb_write8((uint16_t)(sChallengeMachineDuelResults_ADDR + i), 0u);

	gb_write8(sPresentConsecutiveWins_ADDR,
		gb_read8(sPresentConsecutiveWinsBackup_ADDR));
	gb_write8((uint16_t)(sPresentConsecutiveWins_ADDR + 1u),
		gb_read8((uint16_t)(sPresentConsecutiveWinsBackup_ADDR + 1u)));

	DisableSRAM();
}
/* <<< factory ChallengeMachine_PickOpponentSequence */

/* >>> factory ChallengeMachine_GetCurrentOpponent */
/* challenge_machine.asm:152-162 */
ChallengeMachineOpponentResult ChallengeMachine_GetCurrentOpponent(void)
{
	EnableSRAM();
	uint8_t e = gb_read8(sChallengeMachineOpponentNumber_ADDR);
	uint16_t hl = (uint16_t)(sChallengeMachineOpponents_ADDR + e);
	uint8_t a = gb_read8(hl);
	gb_write8(wChallengeMachineOpponent_ADDR, a);
	DisableSRAM();
	return (ChallengeMachineOpponentResult){ .hl = hl, .d = 0, .e = e };
}
/* <<< factory ChallengeMachine_GetCurrentOpponent */

/* >>> factory ChallengeMachine_IncrementHLMax999 */
/* challenge_machine.asm:239-256. hl points at a little-endian 16-bit counter.
 * The value is incremented unless it is already 999; hl exits advanced to the
 * high byte on the increment path and left on the low byte on the skip path. */
uint16_t ChallengeMachine_IncrementHLMax999(uint16_t hl)
{
	EnableSRAM();
	uint8_t high = gb_read8((uint16_t)(hl + 1));
	if (high == WIN_CAP_HIGH && gb_read8(hl) == WIN_CAP_LOW) {
		DisableSRAM();
		return hl;
	}
	uint8_t low = gb_read8(hl);
	uint8_t sum = (uint8_t)(low + 1u);
	gb_write8(hl, sum);
	hl = (uint16_t)(hl + 1);
	uint8_t carry = (uint8_t)(sum < low ? 1u : 0u);
	gb_write8(hl, (uint8_t)(gb_read8(hl) + carry));
	DisableSRAM();
	return hl;
}
/* <<< factory ChallengeMachine_IncrementHLMax999 */

/* >>> factory ChallengeMachine_CheckForNewRecord */
/* challenge_machine.asm:260-286. No register inputs are consumed; on the
 * no-record path hl exits at sMaximumConsecutiveWins+1 when the high bytes
 * differ and at sMaximumConsecutiveWins when they match, and bc/de pass
 * through. On the new-record path the copy setup leaves hl=sPlayerName,
 * de=sChallengeMachineRecordHolderName and bc=NAME_BUFFER_LENGTH, all of which
 * CopyDataHLtoDE_SaveRegisters restores. */
ChallengeMachineRecordResult ChallengeMachine_CheckForNewRecord(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	EnableSRAM();
	uint8_t max_high = gb_read8((uint16_t)(sMaximumConsecutiveWins_ADDR + 1));
	uint8_t present_high = gb_read8((uint16_t)(sPresentConsecutiveWins_ADDR + 1));
	uint16_t hl = (uint16_t)(sMaximumConsecutiveWins_ADDR + 1);
	int new_record;
	if (present_high != max_high) {
		new_record = present_high > max_high;
	} else {
		hl = sMaximumConsecutiveWins_ADDR;
		uint8_t max_low = gb_read8(hl);
		uint8_t present_low = gb_read8(sPresentConsecutiveWins_ADDR);
		new_record = present_low > max_low;
	}
	if (new_record) {
		uint8_t low = gb_read8(sPresentConsecutiveWins_ADDR);
		gb_write8(sMaximumConsecutiveWins_ADDR, low);
		gb_write8((uint16_t)(sMaximumConsecutiveWins_ADDR + 1),
			gb_read8((uint16_t)(sPresentConsecutiveWins_ADDR + 1)));
		hl = sPlayerName_ADDR;
		uint16_t de = sChallengeMachineRecordHolderName_ADDR;
		CopyDataHLtoDE_SaveRegisters(hl, de, NAME_BUFFER_LENGTH);
		gb_write8(sConsecutiveWinRecordIncreased_ADDR, TRUE_VALUE);
		b = (uint8_t)(NAME_BUFFER_LENGTH >> 8);
		c = (uint8_t)NAME_BUFFER_LENGTH;
		d = (uint8_t)(de >> 8);
		e = (uint8_t)de;
	}
	DisableSRAM();
	return (ChallengeMachineRecordResult){ .hl = hl, .b = b, .c = c, .d = d, .e = e };
}
/* <<< factory ChallengeMachine_CheckForNewRecord */

/* >>> factory ChallengeMachine_RecordDuelResult */
void ChallengeMachine_RecordDuelResult(void)
{
	EnableSRAM();
	uint8_t opponent = gb_read8(sChallengeMachineOpponentNumber_ADDR);
	uint16_t result_address = (uint16_t)(sChallengeMachineDuelResults_ADDR + opponent);
	uint8_t result = gb_read8(wDuelResult_ADDR);
	if (result == 0u) {
		gb_write8(result_address, 1u);
		DisableSRAM();
		(void)ChallengeMachine_IncrementHLMax999(sPresentConsecutiveWins_ADDR);
		return;
	}
	gb_write8(result_address, 2u);
	DisableSRAM();
}
/* <<< factory ChallengeMachine_RecordDuelResult */

/* >>> factory ChallengeMachine_Initialize */
ChallengeMachineInitializeResult ChallengeMachine_Initialize(void)
{
	EnableSRAM();
	uint8_t initialized = 0u;
	if (gb_read8(sChallengeMachineMagic_ADDR) == 0xE3u &&
		gb_read8((uint16_t)(sChallengeMachineMagic_ADDR + 1u)) == 0x95u) {
		initialized = 1u;
	} else {
		uint16_t hl = sChallengeMachineMagic_ADDR;
		uint8_t c = (uint8_t)(sChallengeMachineEnd_ADDR - sChallengeMachineStart_ADDR);
		gb_write8(hl++, 0xE3u);
		gb_write8(hl++, 0x95u);
		while (c != 0u) {
			gb_write8(hl++, 0u);
			c--;
		}
		const uint8_t *text = rom_ptr(0x04u, 0x7674u);
		for (uint8_t i = 0u; i < NAME_BUFFER_LENGTH; i++)
			gb_write8((uint16_t)(sChallengeMachineRecordHolderName_ADDR + i), text[i]);
		gb_write8(sMaximumConsecutiveWins_ADDR, 1u);
		gb_write8((uint16_t)(sMaximumConsecutiveWins_ADDR + 1u), 0u);
	}
	uint8_t a = gb_read8(sPlayerInChallengeMachine_ADDR);
	DisableSRAM();
	return (ChallengeMachineInitializeResult){.a = a, .f = initialized ? 0xC0u : 0x80u};
}
/* <<< factory ChallengeMachine_Initialize */

/* >>> factory ChallengeMachine_Reset */
void ChallengeMachine_Reset(void)
{
	(void)ChallengeMachine_Initialize();
	EnableSRAM();
	gb_write8(sTotalChallengeMachineWins_ADDR, 0u);
	gb_write8((uint16_t)(sTotalChallengeMachineWins_ADDR + 1u), 0u);
	gb_write8(sPresentConsecutiveWins_ADDR, 0u);
	gb_write8((uint16_t)(sPresentConsecutiveWins_ADDR + 1u), 0u);
	gb_write8(sPresentConsecutiveWinsBackup_ADDR, 0u);
	gb_write8((uint16_t)(sPresentConsecutiveWinsBackup_ADDR + 1u), 0u);
	gb_write8(sPlayerInChallengeMachine_ADDR, 0u);
	DisableSRAM();
}
/* <<< factory ChallengeMachine_Reset */

/* >>> factory ChallengeMachine_PrintFinalConsecutiveWinStreak */
ChallengeMachinePrintFinalConsecutiveWinStreakResult ChallengeMachine_PrintFinalConsecutiveWinStreak(uint16_t hl)
{
	EnableSRAM();
	uint8_t low = gb_read8(sPresentConsecutiveWins_ADDR);
	gb_write8(wTxRam3_ADDR, low);
	uint8_t high = gb_read8((uint16_t)(sPresentConsecutiveWins_ADDR + 1u));
	gb_write8((uint16_t)(wTxRam3_ADDR + 1u), high);
	if (high == 0u && low < 2u) {
		DisableSRAM();
		return (ChallengeMachinePrintFinalConsecutiveWinStreakResult){0x70u, hl};
	}
	WaitResult printed = PrintScrollableText_NoTextBoxLabel(ConsecutiveWinsEndedAtText);
	DisableSRAM();
	return (ChallengeMachinePrintFinalConsecutiveWinStreakResult){printed.f, ConsecutiveWinsEndedAtText};
}
/* <<< factory ChallengeMachine_PrintFinalConsecutiveWinStreak */

/* >>> factory ChallengeMachine_ShowNewRecord */
ChallengeMachineShowNewRecordResult ChallengeMachine_ShowNewRecord(uint16_t hl)
{
	EnableSRAM();
	uint8_t increased = gb_read8(sConsecutiveWinRecordIncreased_ADDR);
	if (increased == 0u)
		return (ChallengeMachineShowNewRecordResult){0u, 0x80u, hl};

	uint8_t low = gb_read8(sMaximumConsecutiveWins_ADDR);
	gb_write8(wTxRam3_ADDR, low);
	uint8_t high = gb_read8((uint16_t)(sMaximumConsecutiveWins_ADDR + 1u));
	gb_write8((uint16_t)(wTxRam3_ADDR + 1u), high);
	DisableSRAM();
	PauseSong();
	PlaySong(MUSIC_MEDAL);
	(void)PrintScrollableText_NoTextBoxLabel(ConsecutiveWinRecordIncreasedText);
	WaitForSongToFinish();
	ResumeSong();
	return (ChallengeMachineShowNewRecordResult){0u, 0u, hl};
}
/* <<< factory ChallengeMachine_ShowNewRecord */

/* >>> factory ChallengeMachine_DuelWon */
ChallengeMachineDuelWonResult ChallengeMachine_DuelWon(void)
{
	EnableSRAM();
	uint8_t opponent_number = gb_read8(sChallengeMachineOpponentNumber_ADDR);
	gb_write8(wTxRam3_ADDR, (uint8_t)(opponent_number + 1u));
	gb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0u);
	DisableSRAM();
	if (opponent_number == NUM_CHALLENGE_MACHINE_OPPONENTS - 1u) {
		PauseSong();
		PlaySong(MUSIC_MEDAL);
		WaitResult r = PrintScrollableText_NoTextBoxLabel(Defeated5OpponentsText);
		WaitForSongToFinish();
		ResumeSong();
		return (ChallengeMachineDuelWonResult){r.f};
	}
	WaitResult r2 = PrintScrollableText_NoTextBoxLabel(WonAgainstXOpponentsText);
	return (ChallengeMachineDuelWonResult){r2.f};
}
/* <<< factory ChallengeMachine_DuelWon */

/* >>> factory ChallengeMachine_GetOpponentNameAndDeck */
ChallengeMachine_GetOpponentNameAndDeckResult ChallengeMachine_GetOpponentNameAndDeck(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t opponent = gb_read8(wChallengeMachineOpponent_ADDR);
	uint16_t de = (uint16_t)opponent;
	uint16_t table_hl = (uint16_t)(CHALLENGE_MACHINE_OPPONENT_DECK_IDS_ADDR_500 + de);
	uint8_t deck_id = *rom_ptr(CHALLENGE_MACHINE_DATA_BANK_500, table_hl);
	gb_write8(wNPCDuelDeckID_ADDR, deck_id);

	uint8_t h_flag = (((CHALLENGE_MACHINE_OPPONENT_DECK_IDS_ADDR_500 & 0x0FFFu) + (de & 0x0FFFu)) > 0x0FFFu) ? 0x20u : 0u;
	uint8_t c_flag = (((uint32_t)CHALLENGE_MACHINE_OPPONENT_DECK_IDS_ADDR_500 + (uint32_t)de) > 0xFFFFu) ? 0x10u : 0u;
	uint8_t f_after_add = (uint8_t)((f & 0x80u) | h_flag | c_flag);

	_GetChallengeMachineDuelConfigurationsResult r = _GetChallengeMachineDuelConfigurations(deck_id, f_after_add, b, c, 0u, opponent, table_hl);
	return (ChallengeMachine_GetOpponentNameAndDeckResult){r.a, r.f, r.b, r.c, d, e, r.hl};
}
/* <<< factory ChallengeMachine_GetOpponentNameAndDeck */

/* >>> factory ChallengeMachine_PrintScores */
void ChallengeMachine_PrintScores(uint16_t hl)
{
	for (;;) {
		EnableSRAM();
		uint8_t e = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint8_t d = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint16_t de = (uint16_t)(((uint16_t)d << 8) | e);
		if (de == 0u)
			break;
		uint8_t b = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint8_t c = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint16_t saved_hl = hl;

		uint8_t lo = gb_read8(de);
		de = (uint16_t)(de + 1u);
		uint8_t hi = gb_read8(de);
		uint16_t word = (uint16_t)(((uint16_t)hi << 8) | lo);
		(void)ConvertWordToNumericalDigits(word);

		uint16_t dest = BCCoordToBGMap0Address(b, c);
		uint16_t src = wDecimalChars_ADDR;
		SafeCopyDataHLtoDE(&src, &dest, 3u);

		hl = saved_hl;
	}
	DisableSRAM();
}
/* <<< factory ChallengeMachine_PrintScores */

/* >>> factory ChallengeMachine_PrintOpponentName */
ChallengeMachinePrintResult ChallengeMachine_PrintOpponentName(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	ChallengeMachine_GetOpponentNameAndDeckResult r1 = ChallengeMachine_GetOpponentNameAndDeck(f, b, c, d, e, hl);
	uint16_t hl2 = (uint16_t)(r1.hl + 2u);
	return ChallengeMachine_PrintText(hl2, r1.b, r1.c);
}
/* <<< factory ChallengeMachine_PrintOpponentName */

/* >>> factory ChallengeMachine_PrintOpponentClubStatus */
ChallengeMachine_PrintOpponentClubStatusResult ChallengeMachine_PrintOpponentClubStatus(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	ChallengeMachine_GetOpponentNameAndDeckResult r1 = ChallengeMachine_GetOpponentNameAndDeck(f, b, c, d, e, hl);
	uint16_t entry_hl = r1.hl;
	uint16_t rank_addr = (uint16_t)(entry_hl + 6u);
	ChallengeMachinePrintResult r2 = ChallengeMachine_PrintText(rank_addr, r1.b, r1.c);
	uint8_t d2 = (uint8_t)(r2.d + 7u);
	InitTextPrinting(d2, r2.e);

	uint16_t elem_addr = (uint16_t)(entry_hl + 8u);
	uint8_t lo = gb_read8(elem_addr);
	uint8_t hi = gb_read8((uint16_t)(elem_addr + 1u));
	uint16_t text_id = (uint16_t)(((uint16_t)hi << 8) | lo);
	uint16_t final_hl = text_id;
	if (text_id != 0u) {
		TextResult r3 = PrintTextNoDelay(text_id, d2, r2.e);
		final_hl = r3.hl;
	}
	ChallengeMachine_PrintOpponentClubStatusResult result = { final_hl, b, c };
	return result;
}
/* <<< factory ChallengeMachine_PrintOpponentClubStatus */

/* >>> factory ChallengeMachine_PrintOpponentInfo */
void ChallengeMachine_PrintOpponentInfo(uint8_t f, uint8_t d, uint8_t e)
{
	uint16_t hl = sChallengeMachineOpponents_ADDR;
	uint8_t c = 2u;
	for (uint8_t i = 0u; i < NUM_CHALLENGE_MACHINE_OPPONENTS; i++) {
		EnableSRAM();
		wChallengeMachineOpponent = gb_read8(hl);
		DisableSRAM();
		(void)ChallengeMachine_PrintOpponentName(f, 14u, c, d, e, hl);
		(void)ChallengeMachine_PrintOpponentClubStatus(f, 4u, c, d, e, hl);
		hl++;
		c = (uint8_t)(c + 2u);
		e = (uint8_t)(e - 1u);
	}
}
/* <<< factory ChallengeMachine_PrintOpponentInfo */

/* >>> factory ChallengeMachine_PrepareDuel */
void ChallengeMachine_PrepareDuel(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)ChallengeMachine_GetOpponentNameAndDeck(f, b, c, d, e, hl);
	EnableSRAM();
	uint8_t opponent_num = gb_read8(sChallengeMachineOpponentNumber_ADDR);
	DisableSRAM();
	uint16_t prize_addr = (uint16_t)(CHALLENGE_MACHINE_PRIZES_ADDR + opponent_num);
	uint8_t prize = gb_read8(prize_addr);
	gb_write8(wNPCDuelPrizes_ADDR, prize);
}
/* <<< factory ChallengeMachine_PrepareDuel */

/* >>> factory ChallengeMachine_DrawScoreScreen */
void ChallengeMachine_DrawScoreScreen(void)
{
	(void)InitMenuScreen();
	(void)SetupText(0x30u, 0xBFu);

	uint16_t box1_hl = 0;
	DrawRegularTextBox(&box1_hl, 0u, 20u, 13u, 0u, 0u);

	uint16_t box2_hl = 0;
	DrawRegularTextBox(&box2_hl, 0u, 20u, 6u, 0u, 12u);

	EnableSRAM();
	uint16_t src_hl = CHALLENGE_MACHINE_RECORD_HOLDER_NAME_ADDR;
	uint16_t dst_de = wDefaultText_ADDR;
	CopyDataHLtoDE(&src_hl, &dst_de, NAME_BUFFER_LENGTH);
	DisableSRAM();

	wTxRam2 = 0u;
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), 0u);

	(void)PrintLabels(CHALLENGE_MACHINE_PLAYER_SCORE_LABELS_ADDR, 0u, 0u);
	ChallengeMachine_PrintScores(CHALLENGE_MACHINE_PLAYER_SCORE_VALUES_ADDR);
}
/* <<< factory ChallengeMachine_DrawScoreScreen */

/* >>> factory ChallengeMachine_AreYouReady */
ChallengeMachine_AreYouReadyResult ChallengeMachine_AreYouReady(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	EnableSRAM();
	a = (uint8_t)(gb_read8(sChallengeMachineOpponentNumber_ADDR) + 1u);
	gb_write8(wTxRam3_ADDR, a);
	gb_write8(wTxRam3_b_ADDR, a);
	gb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0u);
	gb_write8((uint16_t)(wTxRam3_b_ADDR + 1u), 0u);
	hl = NthOpponentIsText;
	uint8_t streak_hi = gb_read8((uint16_t)(sPresentConsecutiveWins_ADDR + 1u));
	uint8_t streak_lo = gb_read8(sPresentConsecutiveWins_ADDR);
	if (streak_hi != 0u || streak_lo >= 2u) {
		hl = XConsecutiveWinsNthOpponentIsText;
		gb_write8(wTxRam3_ADDR, streak_lo);
		gb_write8((uint16_t)(wTxRam3_ADDR + 1u), streak_hi);
	}
	DisableSRAM();
	ChallengeMachine_GetOpponentNameAndDeckResult deck = ChallengeMachine_GetOpponentNameAndDeck(f, b, c, d, e, hl);
	(void)deck;
	gb_write8(wTxRam2_ADDR, gb_read8(wOpponentName_ADDR));
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), gb_read8((uint16_t)(wOpponentName_ADDR + 1u)));
	WaitResult text = PrintScrollableText_NoTextBoxLabel(hl);
	(void)text;
	HandleYesOrNoMenuResult menu = YesOrNoMenuWithText_SetCursorToYes(WouldYouLikeToBeginTheDuelText);
	f = menu.f;
	a = menu.a;
	return (ChallengeMachine_AreYouReadyResult){a, f};
}
/* <<< factory ChallengeMachine_AreYouReady */

/* >>> factory ChallengeMachine_PrintDuelResultIcons */
void ChallengeMachine_PrintDuelResultIcons(void)
{
	uint16_t hl = sChallengeMachineDuelResults_ADDR;
	uint8_t c = NUM_CHALLENGE_MACHINE_OPPONENTS;
	uint8_t d = 1u;
	uint8_t e = 2u;
	while (c != 0u) {
		uint16_t saved_hl = hl;
		uint8_t saved_c = c;
		uint8_t saved_d = d;
		uint8_t saved_e = e;
		InitTextPrinting(d, e);
		EnableSRAM();
		uint8_t result = gb_read8(hl);
		e = (uint8_t)(result + result);
		d = 0u;
		(void)PrintTextNoDelay(challenge_machine_duel_result_icons[result], d, e);
		e = saved_e;
		d = saved_d;
		c = saved_c;
		hl = saved_hl;
		hl = (uint16_t)(hl + 1u);
		e = (uint8_t)(e + 1u);
		e = (uint8_t)(e + 1u);
		c = (uint8_t)(c - 1u);
	}
	DisableSRAM();
}
/* <<< factory ChallengeMachine_PrintDuelResultIcons */
