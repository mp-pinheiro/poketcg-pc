#include "home/give_booster_pack.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "home/credits_sequence_commands.h"
#include "home/init_menu.h"
#include "home/lcd.h"
#include "home/sound.h"
#include "mem.h"

#define NUM_BOOSTERS 0x1du
#define MUSIC_BOOSTER_PACK 0x1cu

#define BOOSTER_COLOSSEUM 0x00u
#define BOOSTER_EVOLUTION 0x01u
#define BOOSTER_MYSTERY 0x02u
#define BOOSTER_LABORATORY 0x03u

#define SCENE_COLOSSEUM_BOOSTER 0x01u
#define SCENE_EVOLUTION_BOOSTER 0x02u
#define SCENE_MYSTERY_BOOSTER 0x03u
#define SCENE_LABORATORY_BOOSTER 0x04u

#define AndAnotherBoosterPackText 0x0388u
#define CheckedCardsInBoosterPackText 0x0389u
#define ReceivedBoosterPackText 0x0387u

/* BoosterScenesAndNameTexts' four `tx` entries (give_booster_pack.asm:90-101),
 * resolved through poketcg/src/text/text_offsets.asm:940-943. */
#define ColosseumBoosterText 0x03a8u
#define EvolutionBoosterText 0x03a9u
#define MysteryBoosterText 0x03aau
#define LaboratoryBoosterText 0x03abu
/* <<< factory statics */

/* engine/menus/give_booster_pack.asm:113. _PauseMenu_Exit is a bare ret. */
void _PauseMenu_Exit(void)
{
}

/* >>> factory GiveBoosterPack */
/* engine/menus/give_booster_pack.asm:1-38, the prefix that ends immediately
 * before asm:49 `call WaitForSongToFinish`, which is where the reference stops:
 * that wait only ends when the timer ISR has walked the booster jingle to its
 * `music_end`, and the call-level oracle arms VBlank alone, so the cases pin
 * this routine with a pre-ret cutpoint at AssertSongFinished (00:378A) and
 * nothing past it is measurable here.
 *
 * `a` is one of the 29 booster ids. BoosterTypes (asm:58-88) folds it to one of
 * the four pack types, and BoosterScenesAndNameTexts (asm:90-101) is that
 * type's 4-byte row: (scene, scene, name text id low, name text id high). Both
 * tables are this file's own data, inlined here the way medal.c inlines
 * MasterMedalNames.
 *
 * The exit registers are the `pop af` of the wd291 save: a is the byte wd291
 * held on entry, and f is the caller's own flags, because neither `ld c, a`
 * nor `ld a, [wd291]` touches them before the matching `push af`. */
GiveBoosterPackResult GiveBoosterPack(uint8_t a, uint8_t f)
{
	static const uint8_t booster_types[NUM_BOOSTERS] = {
		BOOSTER_COLOSSEUM, BOOSTER_COLOSSEUM, BOOSTER_COLOSSEUM,
		BOOSTER_COLOSSEUM, BOOSTER_COLOSSEUM, BOOSTER_COLOSSEUM,
		BOOSTER_COLOSSEUM,
		BOOSTER_EVOLUTION, BOOSTER_EVOLUTION, BOOSTER_EVOLUTION,
		BOOSTER_EVOLUTION, BOOSTER_EVOLUTION, BOOSTER_EVOLUTION,
		BOOSTER_EVOLUTION,
		BOOSTER_MYSTERY, BOOSTER_MYSTERY, BOOSTER_MYSTERY,
		BOOSTER_MYSTERY, BOOSTER_MYSTERY, BOOSTER_MYSTERY,
		BOOSTER_LABORATORY, BOOSTER_LABORATORY, BOOSTER_LABORATORY,
		BOOSTER_LABORATORY, BOOSTER_LABORATORY,
		BOOSTER_COLOSSEUM, BOOSTER_COLOSSEUM, BOOSTER_COLOSSEUM,
		BOOSTER_COLOSSEUM,
	};
	static const uint8_t booster_scenes[4] = {
		SCENE_COLOSSEUM_BOOSTER, SCENE_EVOLUTION_BOOSTER,
		SCENE_MYSTERY_BOOSTER, SCENE_LABORATORY_BOOSTER,
	};
	static const uint16_t booster_name_texts[4] = {
		ColosseumBoosterText, EvolutionBoosterText,
		MysteryBoosterText, LaboratoryBoosterText,
	};
	uint8_t saved_d291 = wd291;
	uint8_t type = booster_types[a];
	uint8_t scene = booster_scenes[type];
	uint16_t name_text = booster_name_texts[type];

	DisableLCD();
	(void)InitMenuScreen();
	wTextBoxFrameType = 0u;
	/* `lb bc, 6, 0` ahead of the call: b = 6, c = 0, a = the row's scene. */
	(void)LoadBoosterGfx(scene, 6u, 0u);
	wTxRam3 = scene;
	gb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0u);
	wTxRam2 = (uint8_t)name_text;
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), (uint8_t)(name_text >> 8));
	(void)FlashWhiteScreen();
	PauseSong();
	PlaySong(MUSIC_BOOSTER_PACK);
	return (GiveBoosterPackResult){saved_d291, f};
}
/* <<< factory GiveBoosterPack */
