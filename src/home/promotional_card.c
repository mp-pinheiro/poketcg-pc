#include "home/promotional_card.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/sound.h"
#include "home/card_data.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "home/core.h"
#include "home/music1.h"

#define ARTICUNO_LV37 0x5fu
#define BLASTOISE 0x43u
#define DRAGONITE_LV41 0xc1u
#define FLYING_PIKACHU 0x64u
#define MOLTRES_LV37 0x40u
#define MUSIC_MEDAL 0x1du
#define PLAYER_TURN 0xc2u
#define SURFING_PIKACHU_ALT_LV13 0x66u
#define SURFING_PIKACHU_LV13 0x65u
#define VILEPLUME 0x1eu
#define ZAPDOS_LV68 0x76u

#define ReceivedCardText 0x018fu
#define ReceivedLegendaryCardText 0x0191u
#define ReceivedPromotionalCardText 0x0190u
#define ReceivedPromotionalFlyingPikachuText 0x0192u
#define ReceivedPromotionalSurfingPikachuText 0x0193u
/* <<< factory statics */

/* >>> factory _ShowPromotionalCardScreen */
void _ShowPromotionalCardScreen(uint8_t a)
{
	/* promotional_card.asm:5. `.legendary_card_text` is not a helper label:
	 * with a == 0 the routine `call`s its own tail three times -- Moltres,
	 * Articuno, Zapdos -- and then falls into it a fourth time for Dragonite,
	 * so only that last pass's `ret` reaches the caller. Any other `a` is a
	 * card id and runs the tail exactly once. */
	const uint8_t legendary_cards[4] = {MOLTRES_LV37, ARTICUNO_LV37,
					    ZAPDOS_LV68, DRAGONITE_LV41};
	uint8_t pass = 0u;

	(void)SetupText(0x38u, 0x9Fu);

	for (;;) {
		uint8_t card;
		uint16_t text;
		uint16_t name;

		if (a == 0u) {
			card = legendary_cards[pass];
			text = ReceivedLegendaryCardText;
		} else {
			card = a;
			text = ReceivedCardText;
			if (card != VILEPLUME && card != BLASTOISE) {
				text = ReceivedPromotionalFlyingPikachuText;
				if (card != FLYING_PIKACHU) {
					text = ReceivedPromotionalSurfingPikachuText;
					if (card != SURFING_PIKACHU_LV13
					    && card != SURFING_PIKACHU_ALT_LV13)
						text = ReceivedPromotionalCardText;
				}
			}
		}

		LoadCardDataToBuffer1_FromCardID(card);
		PauseSong();
		PlaySong(MUSIC_MEDAL);
		name = (uint16_t)(gb_read8(wLoadedCard1Name_ADDR)
				  | ((uint16_t)gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)) << 8));
		LoadTxRam2(name);
		hWhoseTurn = PLAYER_TURN;
		(void)_DisplayCardDetailScreen(text);

		/* `.loop`: the ROM waits here until the medal jingle has run out, and
		 * only the timer ISR brings that about -- SoundTimerHandler is what
		 * walks each channel to its `music_end` so CheckForEndOfSong can mark
		 * wCurSongID finished. The port has no interrupt source, so the wait
		 * drives that same handler itself; nothing else on this thread can
		 * ever clear the flag. */
		while (AssertSongFinished() != 0u)
			SoundTimerHandler();

		ResumeSong();
		/* Everything but `a` is callee residue by this point, and
		 * OpenCardPage_FromHand overwrites `a` with its own page type. */
		OpenCardPage_FromHand(0u, 0u, 0u, 0u, 0u, 0u, 0u);

		if (a != 0u || pass == 3u)
			return;
		pass++;
	}
}
/* <<< factory _ShowPromotionalCardScreen */
