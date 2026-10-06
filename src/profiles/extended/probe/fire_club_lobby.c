#include "home/fire_club_lobby.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory FindExtraInteractableObjects */
static void adapt_FindExtraInteractableObjects(ProbeState *s)
{
	FindExtraInteractableObjectsResult r = FindExtraInteractableObjects(s->hl);
	s->hl = r.hl;
	s->d = r.d;
	s->e = r.e;
	if (r.carry) {
		s->b = r.b;
		s->c = r.c;
	}
}
/* <<< factory FindExtraInteractableObjects */

/* >>> factory FireClubPressedA */
static void adapt_FireClubPressedA(ProbeState *s)
{
	FireClubPressedAResult r = FireClubPressedA();
	s->hl = r.hl;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory FireClubPressedA */

/* >>> factory FireClubLobbyAfterDuel */
static void adapt_FireClubLobbyAfterDuel(ProbeState *s)
{
	FireClubLobbyAfterDuelResult r = FireClubLobbyAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory FireClubLobbyAfterDuel */

/* >>> factory Preload_Lad2 */
static void adapt_Preload_Lad2(ProbeState *s)
{
	PreloadLad2Result r = Preload_Lad2();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Lad2 */

/* >>> factory Preload_JessicaInFireClubLobby */
static void adapt_Preload_JessicaInFireClubLobby(ProbeState *s)
{
	PreloadJessicaInFireClubLobbyResult r = Preload_JessicaInFireClubLobby();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_JessicaInFireClubLobby */

const ProbeEntry probe_entries_fire_club_lobby[] = {
	{ "FindExtraInteractableObjects", adapt_FindExtraInteractableObjects },
	{ "FireClubPressedA", adapt_FireClubPressedA },
	{ "FireClubLobbyAfterDuel", adapt_FireClubLobbyAfterDuel },
	{ "Preload_Lad2", adapt_Preload_Lad2 },
	{ "Preload_JessicaInFireClubLobby", adapt_Preload_JessicaInFireClubLobby },
	{ NULL, NULL },
};
