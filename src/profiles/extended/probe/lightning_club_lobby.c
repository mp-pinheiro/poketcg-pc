#include "home/lightning_club_lobby.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory LightningClubLobbyAfterDuel */
static void adapt_LightningClubLobbyAfterDuel(ProbeState *s)
{
	LightningClubLobbyAfterDuelResult r = LightningClubLobbyAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory LightningClubLobbyAfterDuel */

/* >>> factory Preload_ImakuniInLightningClubLobby */
static void adapt_Preload_ImakuniInLightningClubLobby(ProbeState *s)
{
	PreloadImakuniInLightningClubLobbyResult r = Preload_ImakuniInLightningClubLobby();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_ImakuniInLightningClubLobby */

const ProbeEntry probe_entries_lightning_club_lobby[] = {
	{ "LightningClubLobbyAfterDuel", adapt_LightningClubLobbyAfterDuel },
	{ "Preload_ImakuniInLightningClubLobby", adapt_Preload_ImakuniInLightningClubLobby },
	{ NULL, NULL },
};
