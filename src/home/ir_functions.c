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
#include "home/ir_core.h"
#define SCENE_GAMEBOY_LINK_CONNECTING 0x0eu

#define SCENE_GAMEBOY_LINK_NOT_CONNECTED 0x10u
#define WouldYouLikeToTryAgainText 0x0197u

#include "generated/wram.h"
#include "home/ir_core.h"

#include "home/ir_core.h"
#include "generated/wram.h"
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

/* >>> factory ClearRPAndRestoreVBlankFunction */
/* ir_functions.asm:31-36 */
void ClearRPAndRestoreVBlankFunction(void)
{
	ClearRP();
	RestoreVBlankFunction();
}
/* <<< factory ClearRPAndRestoreVBlankFunction */

/* >>> factory LoadLinkNotConnectedSceneAndAskWhetherToTryAgain */
LoadLinkNotConnectedSceneAndAskWhetherToTryAgainResult LoadLinkNotConnectedSceneAndAskWhetherToTryAgain(uint16_t hl)
{
	uint16_t saved_hl = hl;
	RestoreVBlankFunction();
	SetSpriteAnimationsAsVBlankFunction();
	(void)LoadScene(SCENE_GAMEBOY_LINK_NOT_CONNECTED, 0u, 0u, 0u, 0u, 0u, saved_hl);
	(void)DrawWideTextBox_WaitForInput(saved_hl);
	HandleYesOrNoMenuResult menu = YesOrNoMenuWithText_SetCursorToYes(WouldYouLikeToTryAgainText);
	ClearRPAndRestoreVBlankFunction();
	return (LoadLinkNotConnectedSceneAndAskWhetherToTryAgainResult){menu.a, menu.f};
}
/* <<< factory LoadLinkNotConnectedSceneAndAskWhetherToTryAgain */

/* >>> factory SetIRCommunicationErrorCode_NoError */
SetIRCommunicationErrorCode_NoErrorResult SetIRCommunicationErrorCode_NoError(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)hl;
	wOwnIRCommunicationParams = 0u;
	RequestDataReceivalThroughIRResult received = RequestDataReceivalThroughIR(a, f, b, 1u, 0xC5u, 0xEAu, wOwnIRCommunicationParams_ADDR);
	if ((received.f & 0x10u) != 0u)
		return (SetIRCommunicationErrorCode_NoErrorResult){received.a, received.f};
	RequestCloseIRCommunicationResult closed = RequestCloseIRCommunication();
	return (SetIRCommunicationErrorCode_NoErrorResult){closed.a, (closed.a == 0u) ? 0x80u : 0x00u};
}
/* <<< factory SetIRCommunicationErrorCode_NoError */

/* >>> factory SetIRCommunicationErrorCode_Error */
SetIRCommunicationErrorCode_ErrorResult SetIRCommunicationErrorCode_Error(uint8_t a, uint8_t f, uint8_t b)
{
	wIRCommunicationErrorCode = 0x01u;
	(void)RequestDataReceivalThroughIR(a, f, b, 1u, 0xC5u, 0xEAu, wIRCommunicationErrorCode_ADDR);
	RequestCloseIRCommunicationResult closed = RequestCloseIRCommunication();
	return (SetIRCommunicationErrorCode_ErrorResult){0x01u, (uint8_t)((closed.f & 0x80u) | 0x10u)};
}
/* <<< factory SetIRCommunicationErrorCode_Error */

/* >>> factory TryReceiveCardOrDeckConfigurationThroughIR */
TryReceiveCardOrDeckConfigurationThroughIRResult TryReceiveCardOrDeckConfigurationThroughIR(uint8_t a)
{
	InitIRCommunications(a);
	for (;;) {
		wDuelTempList = 0u;
		TryReceiveIRRequestResult request = TryReceiveIRRequest();
		if ((request.f & 0x10u) == 0u)
			break;
		if ((request.a & 0x02u) != 0u)
			return (TryReceiveCardOrDeckConfigurationThroughIRResult){1u, 0x10u};
	}
	(void)ExecuteReceivedIRCommands();
	if (wIRCommunicationErrorCode == 0u)
		return (TryReceiveCardOrDeckConfigurationThroughIRResult){0u, 0x80u};
	return (TryReceiveCardOrDeckConfigurationThroughIRResult){0u, 0x90u};
}
/* <<< factory TryReceiveCardOrDeckConfigurationThroughIR */
