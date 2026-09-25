#ifndef POKETCG_DEBUG_CHEATS_H
#define POKETCG_DEBUG_CHEATS_H

typedef enum {
	DEBUG_COIN_RANDOM,
	DEBUG_COIN_HEADS,
	DEBUG_COIN_TAILS,
} DebugCoinMode;

void debug_cheats_set_coin_mode(DebugCoinMode mode);
DebugCoinMode debug_cheats_coin_mode(void);

#endif /* POKETCG_DEBUG_CHEATS_H */
