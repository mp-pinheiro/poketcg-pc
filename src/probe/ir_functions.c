#include "home/ir_functions.h"
#include "probe.h"

static void adapt_PlayCardPopSong(ProbeState *s)
{
	PlayCardPopSong();
	(void)s;
}

/* >>> factory InitIRCommunications */
static void adapt_InitIRCommunications(ProbeState *s)
{
	InitIRCommunications(s->a);
}
/* <<< factory InitIRCommunications */


/* >>> factory LoadLinkConnectingScene */
static void adapt_LoadLinkConnectingScene(ProbeState *s)
{
	LoadLinkConnectingScene(s->hl);
}
/* <<< factory LoadLinkConnectingScene */

/* >>> factory ClearRPAndRestoreVBlankFunction */
static void adapt_ClearRPAndRestoreVBlankFunction(ProbeState *s)
{
	(void)s;
	ClearRPAndRestoreVBlankFunction();
}
/* <<< factory ClearRPAndRestoreVBlankFunction */

/* >>> factory LoadLinkNotConnectedSceneAndAskWhetherToTryAgain */
static void adapt_LoadLinkNotConnectedSceneAndAskWhetherToTryAgain(ProbeState *s)
{
	LoadLinkNotConnectedSceneAndAskWhetherToTryAgainResult result = LoadLinkNotConnectedSceneAndAskWhetherToTryAgain(s->hl);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory LoadLinkNotConnectedSceneAndAskWhetherToTryAgain */

/* >>> factory SetIRCommunicationErrorCode_NoError */
static void adapt_SetIRCommunicationErrorCode_NoError(ProbeState *s)
{
	SetIRCommunicationErrorCode_NoErrorResult result = SetIRCommunicationErrorCode_NoError(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory SetIRCommunicationErrorCode_NoError */

/* >>> factory SetIRCommunicationErrorCode_Error */
static void adapt_SetIRCommunicationErrorCode_Error(ProbeState *s)
{
	SetIRCommunicationErrorCode_ErrorResult result = SetIRCommunicationErrorCode_Error(s->a, s->f, s->b);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory SetIRCommunicationErrorCode_Error */

/* >>> factory TryReceiveCardOrDeckConfigurationThroughIR */
static void adapt_TryReceiveCardOrDeckConfigurationThroughIR(ProbeState *s)
{
	TryReceiveCardOrDeckConfigurationThroughIRResult result = TryReceiveCardOrDeckConfigurationThroughIR(s->a);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory TryReceiveCardOrDeckConfigurationThroughIR */

/* >>> factory ExchangeIRCommunicationParameters */
static void adapt_ExchangeIRCommunicationParameters(ProbeState *s)
{
	ExchangeIRCommunicationParametersResult result = ExchangeIRCommunicationParameters(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory ExchangeIRCommunicationParameters */

/* >>> factory _ReceiveCard */
static void adapt__ReceiveCard(ProbeState *s)
{
	_ReceiveCardResult result = _ReceiveCard();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory _ReceiveCard */

/* >>> factory _ReceiveDeckConfiguration */
static void adapt__ReceiveDeckConfiguration(ProbeState *s)
{
	_ReceiveDeckConfigurationResult result = _ReceiveDeckConfiguration();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory _ReceiveDeckConfiguration */

/* >>> factory PrepareSendCardOrDeckConfigurationThroughIR */
static void adapt_PrepareSendCardOrDeckConfigurationThroughIR(ProbeState *s)
{
	PrepareSendCardOrDeckConfigurationThroughIRResult result =
		PrepareSendCardOrDeckConfigurationThroughIR(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory PrepareSendCardOrDeckConfigurationThroughIR */

const ProbeEntry probe_entries_ir_functions[] = {
	{ "PlayCardPopSong", adapt_PlayCardPopSong },
	{ "InitIRCommunications", adapt_InitIRCommunications },
	{ "LoadLinkConnectingScene", adapt_LoadLinkConnectingScene },
	{ "ClearRPAndRestoreVBlankFunction", adapt_ClearRPAndRestoreVBlankFunction },
	{ "LoadLinkNotConnectedSceneAndAskWhetherToTryAgain", adapt_LoadLinkNotConnectedSceneAndAskWhetherToTryAgain },
	{ "SetIRCommunicationErrorCode_NoError", adapt_SetIRCommunicationErrorCode_NoError },
	{ "SetIRCommunicationErrorCode_Error", adapt_SetIRCommunicationErrorCode_Error },
	{ "TryReceiveCardOrDeckConfigurationThroughIR", adapt_TryReceiveCardOrDeckConfigurationThroughIR },
	{ "ExchangeIRCommunicationParameters", adapt_ExchangeIRCommunicationParameters },
	{ "_ReceiveCard", adapt__ReceiveCard },
	{ "_ReceiveDeckConfiguration", adapt__ReceiveDeckConfiguration },
	{ "PrepareSendCardOrDeckConfigurationThroughIR", adapt_PrepareSendCardOrDeckConfigurationThroughIR },
	{ NULL, NULL },
};
