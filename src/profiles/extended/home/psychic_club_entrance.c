/* --- factory TryFirstRonaldEncounter */
/* >>> factory LoadClubEntrance */
void LoadClubEntrance(void)
{
	TryFirstRonaldDuelResult r1 = TryFirstRonaldDuel(0u, 0u, 0u);
	TrySecondRonaldDuelResult r2 = TrySecondRonaldDuel(r1.b, r1.c, r1.hl);
	wTempNPC = NPC_RONALD1;
	NPCSearchResult found = FindLoadedNPC();
	if (found.f & 0x10u)
		return;
	(void)SetNextNPCAndScript(Script_FirstRonaldEncounter_ADDR, r2.hl);
}
/* <<< factory LoadClubEntrance */
