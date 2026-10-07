/* >>> part includes */
#include "home/link_duel.h"
#include "runtime.h"

#include "generated/text_ids.h"
#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "generated/wram.h"
#include "generated/hram.h"
#include "home/duel.h"
#include "home/core.h"
#include "home/frames.h"
#include "home/text_box.h"
#include "home/menus.h"
#include "home/credits_sequence_commands.h"
#include "home/lcd.h"
#include "home/serial.h"
#include "home/duel_core.h"
#include "home/process_text.h"
#include "home/load_animation.h"
#include "home/print_text.h"
#include "home/sprite_vblank.h"
#include "home/time.h"
#include "home/bg_map.h"
#include "mem.h"
/* <<< part includes_2 */

/* >>> part OPPONENT_TURN */
#define OPPONENT_TURN 0xc3u
/* <<< part OPPONENT_TURN */
/* >>> part PLAYER_TURN */
#define PLAYER_TURN 0xc2u
/* <<< part PLAYER_TURN */
/* >>> part SYM_0 */
#define SYM_0 0x20u
/* <<< part SYM_0 */
/* >>> part SYM_SPACE */
#define SYM_SPACE 0x00u
/* <<< part SYM_SPACE */
/* >>> part B_PAD_A */
#define B_PAD_A 0u
/* <<< part B_PAD_A */
/* >>> part B_PAD_RIGHT */
#define B_PAD_RIGHT 4u
/* <<< part B_PAD_RIGHT */
/* >>> part B_PAD_LEFT */
#define B_PAD_LEFT 5u
/* <<< part B_PAD_LEFT */
/* >>> part F_C */
#define F_C 0x10u
/* <<< part F_C */


/* >>> factory _SetUpAndStartLinkDuel */
void _SetUpAndStartLinkDuel(void)
{
	SetSpriteAnimationsAsVBlankFunction();
	(void)LoadScene(SCENE_GAMEBOY_LINK_TRANSMITTING, 0u, 0u, 0u, 0u, 0u, 0u);
	LoadPlayerDeck();
	SwitchToCGBNormalSpeed();
	uint8_t decision = DecideLinkDuelVariables();
	RestoreVBlankFunction();
	uint8_t failed = (uint8_t)(decision & F_C);

	if (!failed) {
		wPlayerDuelistType = DUELIST_TYPE_PLAYER;
		wOpponentDuelistType = DUELIST_TYPE_LINK_OPP;
		wDuelType = DUELTYPE_LINK;
		EmptyScreen();

		if (gb_read8(wSerialOp_ADDR) == 0x29u) {
			hWhoseTurn = PLAYER_TURN;
			(void)CopyPlayerName(wDefaultText_ADDR);
			SerialExchangeResult names = SerialExchangeBytes(
				NAME_BUFFER_LENGTH, wDefaultText_ADDR, wNameBuffer_ADDR);
			if (names.f & F_C) {
				failed = F_C;
			} else {
				wOpponentName = 0u;
				wOpponentName_PTR[1] = 0u;
				SerialExchangeResult deck = SerialExchangeBytes(
					DECK_SIZE, wPlayerDeck_ADDR, wOpponentDeck_ADDR);
				if (deck.f & F_C) {
					failed = F_C;
				} else {
					uint16_t box_hl = deck.hl;
					DrawRegularTextBox(&box_hl, deck.a, 8u, 6u, 6u, 2u);
					InitTextPrinting(7u, 4u);
					(void)ProcessTextFromID(PrizesCardsText);
					(void)DrawWideTextBox_PrintText(ChooseTheNumberOfPrizesText);
					EnableLCD();
					wNPCDuelPrizes = PRIZES_4;
					wPrizeCardSelectionFrameCounter = 0u;
					uint8_t symbol;
					uint8_t held;
					for (;;) {
						DoFrame();
						uint8_t prize = wNPCDuelPrizes;
						symbol = (uint8_t)(prize + SYM_0);
						uint8_t frame = wPrizeCardSelectionFrameCounter;
						wPrizeCardSelectionFrameCounter = (uint8_t)(frame + 1u);
						if ((frame & 0x10u) != 0u)
							symbol = SYM_SPACE;
						WriteByteToBGMap0(symbol, 9u, 6u);
						held = hDPadHeld;
						if ((held & (uint8_t)(1u << B_PAD_LEFT)) != 0u) {
							prize = (uint8_t)(prize - 1u);
							if (prize < PRIZES_2)
								prize = PRIZES_6;
							wNPCDuelPrizes = prize;
							wPrizeCardSelectionFrameCounter = 0u;
						} else if ((held & (uint8_t)(1u << B_PAD_RIGHT)) != 0u) {
							prize = (uint8_t)(prize + 1u);
							if (prize >= (uint8_t)(PRIZES_6 + 1u))
								prize = PRIZES_2;
							wNPCDuelPrizes = prize;
							wPrizeCardSelectionFrameCounter = 0u;
						}
						if ((held & (uint8_t)(1u << B_PAD_A)) != 0u)
							break;
					}
					SerialSend8Bytes((uint8_t)(SEND8_ALL & ~SEND8_D), wNPCDuelPrizes, 0x20u, held, 6u,
						symbol, wPrizeCardSelectionFrameCounter_ADDR);
				}
			}
		} else {
			hWhoseTurn = OPPONENT_TURN;
			(void)CopyPlayerName(wDefaultText_ADDR);
			SerialExchangeResult names = SerialExchangeBytes(
				NAME_BUFFER_LENGTH, wDefaultText_ADDR, wNameBuffer_ADDR);
			if (names.f & F_C) {
				failed = F_C;
			} else {
				wOpponentName = 0u;
				wOpponentName_PTR[1] = 0u;
				SerialExchangeResult deck = SerialExchangeBytes(
					DECK_SIZE, wPlayerDeck_ADDR, wOpponentDeck_ADDR);
				if (deck.f & F_C)
					failed = F_C;
				else {
					uint16_t box_hl = deck.hl;
					(void)box_hl;
					(void)DrawWideTextBox_PrintText(PleaseWaitDecidingNumberOfPrizesText);
					EnableLCD();
					SerialRecv8BytesResult received = SerialRecv8Bytes();
					wNPCDuelPrizes = received.a;
				}
			}
		}
	}

	if (failed) {
		wDuelResult = 0xFFu;
		SetSpriteAnimationsAsVBlankFunction();
		(void)LoadScene(SCENE_GAMEBOY_LINK_NOT_CONNECTED, 0u, 0u, 0u, 0u, 0u, 0u);
		(void)DrawWideTextBox_WaitForInput(TransmissionErrorText);
		RestoreVBlankFunction();
		ResetSerial();
		return;
	}

	(void)ExchangeRNG(0u, 0u, 0u, 0u);
	wOpponentPortrait = LINK_OPP_PIC;
	uint8_t saved_turn = hWhoseTurn;
	EmptyScreen();
	SetDefaultConsolePalettes();
	wDuelDisplayedScreen = SHUFFLE_DECK;
	DrawDuelistPortraitsAndNames();
	hWhoseTurn = OPPONENT_TURN;
	LoadTxRam3((uint16_t)wNPCDuelPrizes);
	(void)DrawWideTextBox_WaitForInput(BeginAPrizeDuelWithText);
	hWhoseTurn = saved_turn;
	(void)ExchangeRNG(0u, 0u, 0u, 0u);
	StartDuel_VSLinkOpp();
	SwitchToCGBDoubleSpeed();
	runtime_mark_event(RUNTIME_EVENT_LINK_SESSION_CLOSED);
}
/* <<< factory _SetUpAndStartLinkDuel */
