#include "home/ir_functions.h"

#include "home/music1.h"
/* >>> factory statics */
#include "generated/hram.h"
#include "generated/wram.h"
#include "generated/sram.h"
#include "home/switch_sram.h"
#include "mem.h"

#define NAME_BUFFER_LENGTH 0x10u
#define PLAYER_TURN 0xC2u

#include "generated/wram.h"
#include "home/menus.h"
#include "home/lcd.h"
#include "home/load_animation.h"
#include "home/sprite_vblank.h"
#define SCENE_GAMEBOY_LINK_CONNECTING 0x0eu
/* <<< factory statics */

#define MUSIC_CARD_POP 0x08u

void PlayCardPopSong(void)
{
	Music1_PlaySong(MUSIC_CARD_POP);
}


/* >>> factory InitIRCommunications */
/* ir_functions.asm:40-72 */
void InitIRCommunications(uint8_t a)
{
	gb_write8(wOwnIRCommunicationParams_ADDR, a);
	gb_write8((uint16_t)(wOwnIRCommunicationParams_ADDR + 1u), 0x50u);
	gb_write8((uint16_t)(wOwnIRCommunicationParams_ADDR + 2u), 0x4Bu);
	gb_write8((uint16_t)(wOwnIRCommunicationParams_ADDR + 3u), 0x31u);
	gb_write8(wIRCommunicationErrorCode_ADDR, 0xFFu);
	hWhoseTurn = PLAYER_TURN;
	gb_write8(wNameBuffer_ADDR, 0u);
	gb_write8(wOpponentName_ADDR, 0u);
	gb_write8((uint16_t)(wOpponentName_ADDR + 1u), 0u);

	EnableSRAM();
	for (uint8_t i = 0; i < NAME_BUFFER_LENGTH; i++)
		gb_write8((uint16_t)(wDefaultText_ADDR + i), gb_read8((uint16_t)(sPlayerName_ADDR + i)));
	DisableSRAM();
}
/* <<< factory InitIRCommunications */

/* >>> factory LoadLinkConnectingScene */
void LoadLinkConnectingScene(uint16_t hl)
{
	uint16_t saved_hl = hl;
	SetSpriteAnimationsAsVBlankFunction();
	LoadScene(SCENE_GAMEBOY_LINK_CONNECTING, 0u, 0u, 0u, 0u, 0u, saved_hl);
	DrawWideTextBox_PrintText(saved_hl);
	EnableLCD();
}
/* <<< factory LoadLinkConnectingScene */
