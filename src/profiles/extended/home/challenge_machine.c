/* >>> part includes */
#include "home/challenge_machine.h"

#include "generated/text_ids.h"
#include "generated/rom.h"
#include "generated/constants.h"
#include "generated/sram.h"
#include "home/core.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "home/save.h"
#include "mem.h"
/* <<< part includes */
/* >>> part CHALLENGE_MACHINE_NOT_DUELLED_ICON_TEXT */
#define CHALLENGE_MACHINE_NOT_DUELLED_ICON_TEXT ChallengeMachineNotDuelledIconText
/* <<< part CHALLENGE_MACHINE_NOT_DUELLED_ICON_TEXT */
/* >>> part CHALLENGE_MACHINE_DUEL_WON_ICON_TEXT */
#define CHALLENGE_MACHINE_DUEL_WON_ICON_TEXT ChallengeMachineDuelWonIconText
/* <<< part CHALLENGE_MACHINE_DUEL_WON_ICON_TEXT */
/* >>> part CHALLENGE_MACHINE_DUEL_LOST_ICON_TEXT */
#define CHALLENGE_MACHINE_DUEL_LOST_ICON_TEXT ChallengeMachineDuelLostIconText
/* <<< part CHALLENGE_MACHINE_DUEL_LOST_ICON_TEXT */
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
		const uint8_t *text = rom_ptr(ChallengeMachine_DrMasonText_BANK, ChallengeMachine_DrMasonText_ADDR);
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
/* >>> factory ChallengeMachine_Start */
void ChallengeMachine_Start(void)
{
	wLineSeparation = DOUBLE_SPACED;
	wd317 = 0u;
	(void)ChallengeMachine_Initialize();

	EnableSRAM();
	uint8_t player_in_challenge = sPlayerInChallengeMachine;
	DisableSRAM();

	uint8_t b = 0u, c = 0u, d = 0u, e = 0u, f = 0u;
	uint16_t hl = 0u;
	int quit = 0, resume = player_in_challenge == 0xffu;

	if (!resume) {
		ChallengeMachine_PickOpponentSequence();
		ChallengeMachine_DrawScoreScreen();
		FlashWhiteScreen();
		HandleYesOrNoMenuResult play = YesOrNoMenuWithText_SetCursorToYes(PlayTheChallengeMachineText);
		if ((play.f & 0x10u) != 0u)
			goto end_challenge;

		(void)PrintScrollableText_NoTextBoxLabel(LetUsChooseYourOpponentText);
		FadeScreenToWhite();
		EnableSRAM();
		gb_write8(sPresentConsecutiveWinsBackup_ADDR, 0u);
		gb_write8((uint16_t)(sPresentConsecutiveWinsBackup_ADDR + 1u), 0u);
		DisableSRAM();

		ChallengeMachine_DrawOpponentList();
		FlashWhiteScreen();
		(void)PrintScrollableText_NoTextBoxLabel(YourOpponentsForThisGameText);
	}

	for (;;) {
		if (!resume) {
			ChallengeMachineOpponentResult opponent = ChallengeMachine_GetCurrentOpponent();
			ChallengeMachine_AreYouReadyResult ready = ChallengeMachine_AreYouReady(
				0u, f, b, c, opponent.d, opponent.e, opponent.hl);
			if ((ready.f & 0x10u) != 0u) {
				(void)PrintScrollableText_NoTextBoxLabel(IfYouQuitTheDuelText);
				HandleYesOrNoMenuResult stay = YesOrNoMenuWithText(WouldYouLikeToQuitTheDuelText);
				if ((stay.f & 0x10u) != 0u)
					continue;
				quit = 1;
				break;
			}

			EnableSRAM();
			sPlayerInChallengeMachine = 0xffu;
			DisableSRAM();
			ChallengeMachine_Duel(f, b, c, opponent.d, opponent.e, opponent.hl);
		}
		resume = 0;

		EnableSRAM();
		sPlayerInChallengeMachine = 0u;
		DiscardSavedDuelData();
		DisableSRAM();

		ChallengeMachineOpponentResult current = ChallengeMachine_GetCurrentOpponent();
		d = current.d;
		e = current.e;
		hl = current.hl;
		ChallengeMachine_RecordDuelResult();
		ChallengeMachine_DrawOpponentList();
		FlashWhiteScreen();
		if (gb_read8(wDuelResult_ADDR) != 0u)
			goto lost;

		ChallengeMachineDuelWonResult won = ChallengeMachine_DuelWon();
		f = won.f;
		EnableSRAM();
		if (sChallengeMachineOpponentNumber == NUM_CHALLENGE_MACHINE_OPPONENTS - 1u)
			break;
		sChallengeMachineOpponentNumber++;
		DisableSRAM();
	}

	if (!quit) {
		hl = ChallengeMachine_IncrementHLMax999(sTotalChallengeMachineWins_ADDR);
		FadeScreenToWhite();
		ChallengeMachineRecordResult record = ChallengeMachine_CheckForNewRecord(b, c, d, e);
		b = record.b;
		c = record.c;
		d = record.d;
		e = record.e;
		hl = record.hl;
		ChallengeMachine_DrawScoreScreen();
		FlashWhiteScreen();
		EnableSRAM();
		gb_write8(wTxRam3_ADDR, gb_read8(sTotalChallengeMachineWins_ADDR));
		gb_write8((uint16_t)(wTxRam3_ADDR + 1u),
		          gb_read8((uint16_t)(sTotalChallengeMachineWins_ADDR + 1u)));
		DisableSRAM();
		(void)PrintScrollableText_NoTextBoxLabel(SuccessfullyDefeated5OpponentsText);
		goto end_challenge;
	}
	goto quit_challenge;

lost:
	{
		ChallengeMachineOpponentResult opponent = ChallengeMachine_GetCurrentOpponent();
		EnableSRAM();
		gb_write8(wTxRam3_ADDR, (uint8_t)(sChallengeMachineOpponentNumber + 1u));
		gb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0u);
		DisableSRAM();
		ChallengeMachine_GetOpponentNameAndDeckResult named =
			ChallengeMachine_GetOpponentNameAndDeck(f, b, c, opponent.d, opponent.e, opponent.hl);
		b = named.b;
		c = named.c;
		d = named.d;
		e = named.e;
		gb_write8(wTxRam2_ADDR, gb_read8(wOpponentName_ADDR));
		gb_write8((uint16_t)(wTxRam2_ADDR + 1u), gb_read8((uint16_t)(wOpponentName_ADDR + 1u)));
		(void)PrintScrollableText_NoTextBoxLabel(LostToTheNthOpponentText);
	}

quit_challenge:
	hl = ChallengeMachine_PrintFinalConsecutiveWinStreak(hl).hl;
	FadeScreenToWhite();
	{
		ChallengeMachineRecordResult record = ChallengeMachine_CheckForNewRecord(b, c, d, e);
		b = record.b;
		c = record.c;
		d = record.d;
		e = record.e;
		hl = record.hl;
	}
	ChallengeMachine_DrawScoreScreen();
	FlashWhiteScreen();
	EnableSRAM();
	gb_write8(sPresentConsecutiveWins_ADDR, 0u);
	gb_write8((uint16_t)(sPresentConsecutiveWins_ADDR + 1u), 0u);
	DisableSRAM();

end_challenge:
	{
		ChallengeMachineRecordResult record = ChallengeMachine_CheckForNewRecord(b, c, d, e);
		hl = record.hl;
	}
	EnableSRAM();
	gb_write8(sPresentConsecutiveWinsBackup_ADDR, gb_read8(sPresentConsecutiveWins_ADDR));
	gb_write8((uint16_t)(sPresentConsecutiveWinsBackup_ADDR + 1u),
	          gb_read8((uint16_t)(sPresentConsecutiveWins_ADDR + 1u)));
	(void)ChallengeMachine_ShowNewRecord(hl);
	DisableSRAM();
	(void)PrintScrollableText_NoTextBoxLabel(WeAwaitYourNextChallengeText);
}
/* <<< factory ChallengeMachine_Start */
/* === factory ChallengeMachine_PrintOpponentClubStatus */
