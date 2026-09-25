#include "debug_cheats.h"

static DebugCoinMode g_coin_mode = DEBUG_COIN_RANDOM;

void debug_cheats_set_coin_mode(DebugCoinMode mode)
{
	if (mode != DEBUG_COIN_HEADS && mode != DEBUG_COIN_TAILS)
		mode = DEBUG_COIN_RANDOM;
	g_coin_mode = mode;
}

DebugCoinMode debug_cheats_coin_mode(void)
{
	return g_coin_mode;
}
