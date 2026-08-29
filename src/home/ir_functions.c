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

#include "home/ir_core.h"
#include "home/ir_functions.h"
#include "generated/wram.h"

#include "generated/wram.h"
#include "home/ir_core.h"
#include "home/ir_functions.h"
#include "home/sound.h"
#define IRPARAM_SEND_CARDS 0x02u
#define CardTransferWasntSuccessful2Text 0x019fu
#define ReceivingACardText 0x019bu

#include "home/sound.h"
#define IRPARAM_SEND_DECK 0x03u
#define DeckConfigurationTransferWasntSuccessful2Text 0x01a1u
#define ReceivingDeckConfigurationText 0x019du
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

/* >>> factory ExchangeIRCommunicationParameters */
ExchangeIRCommunicationParametersResult ExchangeIRCommunicationParameters(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)a;
	(void)c;
	(void)d;
	(void)e;
	(void)hl;
	RequestDataTransmissionThroughIRResult parameters = RequestDataTransmissionThroughIR(
		f, b, 4u, (uint8_t)(wOtherIRCommunicationParams_ADDR >> 8),
		(uint8_t)wOtherIRCommunicationParams_ADDR, wOwnIRCommunicationParams_ADDR);
	if ((parameters.f & 0x10u) != 0u)
		goto error;
	if (gb_read8((uint16_t)(wOtherIRCommunicationParams_ADDR + 1u)) != 0x50u)
		goto error;
	if (gb_read8((uint16_t)(wOtherIRCommunicationParams_ADDR + 2u)) != 0x4Bu)
		goto error;
	uint8_t parameter_sum = 0u;
	for (uint8_t i = 0u; i < 4u; i++)
		parameter_sum = (uint8_t)(parameter_sum + gb_read8((uint16_t)(wOtherIRCommunicationParams_ADDR + i)));
	uint8_t own_parameter = wOwnIRCommunicationParams;
	uint8_t other_parameter = wOtherIRCommunicationParams;
	if (own_parameter != other_parameter) {
		uint8_t compare_f = 0x40u;
		if ((own_parameter & 0x0Fu) < (other_parameter & 0x0Fu))
			compare_f = (uint8_t)(compare_f | 0x20u);
		if (own_parameter < other_parameter)
			compare_f = (uint8_t)(compare_f | 0x10u);
		SetIRCommunicationErrorCode_ErrorResult error_result =
			SetIRCommunicationErrorCode_Error(own_parameter, compare_f, parameter_sum);
		return (ExchangeIRCommunicationParametersResult){error_result.a, error_result.f};
	}
	RequestDataTransmissionThroughIRResult name_received =
		RequestDataTransmissionThroughIR(
			0xC0u, parameter_sum, NAME_BUFFER_LENGTH,
			(uint8_t)(wNameBuffer_ADDR >> 8), (uint8_t)wNameBuffer_ADDR,
			wDefaultText_ADDR);
	if ((name_received.f & 0x10u) != 0u)
		goto error;
	uint8_t name_sum = 0u;
	for (uint8_t i = 0u; i < NAME_BUFFER_LENGTH; i++)
		name_sum = (uint8_t)(name_sum + gb_read8((uint16_t)(wNameBuffer_ADDR + i)));
	RequestDataReceivalThroughIRResult name_sent =
		RequestDataReceivalThroughIR(
			name_received.a, name_received.f, name_sum, NAME_BUFFER_LENGTH,
			(uint8_t)(wNameBuffer_ADDR >> 8), (uint8_t)wNameBuffer_ADDR,
			wDefaultText_ADDR);
	if ((name_sent.f & 0x10u) != 0u)
		goto error;
	return (ExchangeIRCommunicationParametersResult){
		name_sent.a, (name_sent.a == 0u) ? 0x80u : 0x00u};
error:
	return (ExchangeIRCommunicationParametersResult){0u, 0x90u};
}
/* <<< factory ExchangeIRCommunicationParameters */

/* >>> factory _ReceiveCard */
/* ir_functions.asm:248-304 */
_ReceiveCardResult _ReceiveCard(void)
{
	for (;;) {
		StopMusic();
		LoadLinkConnectingScene(ReceivingACardText);
		TryReceiveCardOrDeckConfigurationThroughIRResult received =
			TryReceiveCardOrDeckConfigurationThroughIR(IRPARAM_SEND_CARDS);
		gb_write8((uint16_t)(wOwnIRCommunicationParams_ADDR + 1u), 0x4Fu);
		RequestDataReceivalThroughIRResult data =
			RequestDataReceivalThroughIR(0x4Fu, received.f, 0u, 4u, 0xC5u, 0xEBu,
				wOwnIRCommunicationParams_ADDR);
		if ((data.f & 0x10u) == 0u) {
			RequestCloseIRCommunicationResult closed = RequestCloseIRCommunication();
			if ((closed.f & 0x10u) == 0u) {
				PlayCardPopSong();
				ClearRPAndRestoreVBlankFunction();
				return (_ReceiveCardResult){0x08u, 0x00u};
			}
		}
		PlayCardPopSong();
		LoadLinkNotConnectedSceneAndAskWhetherToTryAgainResult retry =
			LoadLinkNotConnectedSceneAndAskWhetherToTryAgain(CardTransferWasntSuccessful2Text);
		if ((retry.f & 0x10u) != 0u)
			return (_ReceiveCardResult){retry.a, (uint8_t)((retry.f & 0x80u) | 0x10u)};
	}
}
/* <<< factory _ReceiveCard */

/* >>> factory _ReceiveDeckConfiguration */
_ReceiveDeckConfigurationResult _ReceiveDeckConfiguration(void)
{
	for (;;) {
		StopMusic();
		LoadLinkConnectingScene(ReceivingDeckConfigurationText);
		TryReceiveCardOrDeckConfigurationThroughIRResult received = TryReceiveCardOrDeckConfigurationThroughIR(IRPARAM_SEND_DECK);
		if ((received.f & 0x10u) == 0u) {
			PlayCardPopSong();
			ClearRPAndRestoreVBlankFunction();
			return (_ReceiveDeckConfigurationResult){0x08u, 0x00u};
		}
		PlayCardPopSong();
		LoadLinkNotConnectedSceneAndAskWhetherToTryAgainResult menu = LoadLinkNotConnectedSceneAndAskWhetherToTryAgain(DeckConfigurationTransferWasntSuccessful2Text);
		if ((menu.f & 0x10u) == 0u)
			continue;
		return (_ReceiveDeckConfigurationResult){menu.a, (uint8_t)((menu.f & 0x80u) | 0x10u)};
	}
}
/* <<< factory _ReceiveDeckConfiguration */
