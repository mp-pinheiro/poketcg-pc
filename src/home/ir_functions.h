#ifndef POKETCG_HOME_IR_FUNCTIONS_H
#define POKETCG_HOME_IR_FUNCTIONS_H

#include <stdint.h>

void PlayCardPopSong(void);

/* >>> factory InitIRCommunications */
void InitIRCommunications(uint8_t a);
/* <<< factory InitIRCommunications */
/* >>> factory LoadLinkConnectingScene */
void LoadLinkConnectingScene(uint16_t hl);
/* <<< factory LoadLinkConnectingScene */
/* >>> factory ClearRPAndRestoreVBlankFunction */
void ClearRPAndRestoreVBlankFunction(void);
/* <<< factory ClearRPAndRestoreVBlankFunction */
/* >>> factory LoadLinkNotConnectedSceneAndAskWhetherToTryAgain */
/* >>> factory LoadLinkNotConnectedSceneAndAskWhetherToTryAgain */
typedef struct { uint8_t a; uint8_t f; } LoadLinkNotConnectedSceneAndAskWhetherToTryAgainResult;
LoadLinkNotConnectedSceneAndAskWhetherToTryAgainResult LoadLinkNotConnectedSceneAndAskWhetherToTryAgain(uint16_t hl);
/* <<< factory LoadLinkNotConnectedSceneAndAskWhetherToTryAgain */
/* >>> factory SetIRCommunicationErrorCode_NoError */
typedef struct { uint8_t a; uint8_t f; } SetIRCommunicationErrorCode_NoErrorResult;
SetIRCommunicationErrorCode_NoErrorResult SetIRCommunicationErrorCode_NoError(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory SetIRCommunicationErrorCode_NoError */
/* >>> factory SetIRCommunicationErrorCode_Error */
typedef struct { uint8_t a; uint8_t f; } SetIRCommunicationErrorCode_ErrorResult;
SetIRCommunicationErrorCode_ErrorResult SetIRCommunicationErrorCode_Error(uint8_t a, uint8_t f, uint8_t b);
/* <<< factory SetIRCommunicationErrorCode_Error */
/* >>> factory TryReceiveCardOrDeckConfigurationThroughIR */
typedef struct { uint8_t a; uint8_t f; } TryReceiveCardOrDeckConfigurationThroughIRResult;
TryReceiveCardOrDeckConfigurationThroughIRResult TryReceiveCardOrDeckConfigurationThroughIR(uint8_t a);
/* <<< factory TryReceiveCardOrDeckConfigurationThroughIR */
/* >>> factory ExchangeIRCommunicationParameters */
typedef struct { uint8_t a; uint8_t f; } ExchangeIRCommunicationParametersResult;
ExchangeIRCommunicationParametersResult ExchangeIRCommunicationParameters(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ExchangeIRCommunicationParameters */
/* >>> factory _ReceiveCard */
typedef struct { uint8_t a; uint8_t f; } _ReceiveCardResult;
_ReceiveCardResult _ReceiveCard(void);
/* <<< factory _ReceiveCard */
/* >>> factory _ReceiveDeckConfiguration */
typedef struct { uint8_t a; uint8_t f; } _ReceiveDeckConfigurationResult;
_ReceiveDeckConfigurationResult _ReceiveDeckConfiguration(void);
/* <<< factory _ReceiveDeckConfiguration */
/* >>> factory PrepareSendCardOrDeckConfigurationThroughIR */
typedef struct { uint8_t a; uint8_t f; } PrepareSendCardOrDeckConfigurationThroughIRResult;
PrepareSendCardOrDeckConfigurationThroughIRResult PrepareSendCardOrDeckConfigurationThroughIR(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PrepareSendCardOrDeckConfigurationThroughIR */
/* >>> factory _SendCard */
void _SendCard(void);
/* <<< factory _SendCard */
/* >>> factory _SendDeckConfiguration */
void _SendDeckConfiguration(void);
/* <<< factory _SendDeckConfiguration */
#endif
