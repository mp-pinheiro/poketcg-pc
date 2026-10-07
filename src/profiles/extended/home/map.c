/* --- factory GameEvent_GiftCenter */
/* --- factory GameEvent_BattleCenter */
/* >>> factory _ExecuteGameEvent */
uint8_t _ExecuteGameEvent(void)
{
	uint8_t event = wGameEvent;
	if (event >= NUM_GAME_EVENTS)
		event = GAME_EVENT_CHALLENGE_MACHINE;
	switch (event) {
	case 0u:
		return GameEvent_Overworld(0u);
	case 1u:
		return GameEvent_Duel();
	case 2u:
		GameEvent_Credits();
		return 0x80u;
	case 3u: {
		SongResult result = GameEvent_ContinueDuel();
		return result.f;
	}
	case GAME_EVENT_CHALLENGE_MACHINE:
		return GameEvent_ChallengeMachine();
	default:
		return GameEvent_Overworld(0u);
	}
}
/* <<< factory _ExecuteGameEvent */
