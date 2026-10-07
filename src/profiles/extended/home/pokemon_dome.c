/* >>> part PokemonDomeAfterDuelTable */
#define PokemonDomeAfterDuelTable (PokemonDomeAfterDuel_ADDR + 0x06u)
/* <<< part PokemonDomeAfterDuelTable */
/* >>> factory PokemonDomeMovePlayer */
void PokemonDomeMovePlayer(void)
{
	if (gb_read8(wPlayerYCoord_ADDR) != 0x16u)
		return;
	uint8_t x = gb_read8(wPlayerXCoord_ADDR);
	if (x < 0x0Eu)
		return;
	if (x >= 0x11u)
		return;
	wTempNPC = NPC_ROD;
	(void)SetNextNPCAndScript(Script_f84c_ADDR, PokemonDomeMovePlayer_ADDR);
}
/* <<< factory PokemonDomeMovePlayer */
/* >>> factory PokemonDomeLoadMap */
void PokemonDomeLoadMap(void)
{
	TryGivePCPack(0x0Du);
	/* pokemon_dome.asm PokemonDomeLoadMap: `get_event_value` goes through
	 * GetEventVar, which leaves the event's mask in wLoadedEventBits. */
	if (GetEventValue(EVENT_POKEMON_DOME_IN_MENU) == 0u)
		return;
	SetNextScript(Script_f80b_BANK, Script_f80b_ADDR);
}
/* <<< factory PokemonDomeLoadMap */
