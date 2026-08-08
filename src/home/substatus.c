#include "home/substatus.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "mem.h"

#define DUELVARS_ARENA_CARD_SUBSTATUS2 0xe8u
#define SUBSTATUS2_SMOKESCREEN 0x01u
#define SUBSTATUS2_SAND_ATTACK 0x02u
#define SAND_ATTACK_CHECK_TEXT 0x00deu
#define SMOKESCREEN_CHECK_TEXT 0x00dfu
#define DUELVARS_ARENA_CARD 0xbbu
#define DUELVARS_BENCH 0xbcu
#define DUELVARS_ARENA_CARD_STATUS 0xf0u
#define CNF_SLP_PRZ 0x0fu
#define wTempPokemonID_ADDR 0xce7cu

/* substatus.asm:544-590. Counts arena (if not status-incapable) plus bench
 * slots matching the target id. The bench walk ends at its $FF terminator. */
PkmnPowerCountResult CountTurnDuelistPokemonWithActivePkmnPower(uint8_t a)
{
	gb_write8(wTempPokemonID_ADDR, a);
	uint8_t count = 0;
	uint8_t arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	if (arena != 0xFF) {
		uint16_t arena_id = GetCardIDFromDeckIndex(arena);
		if ((uint8_t)arena_id == gb_read8(wTempPokemonID_ADDR)) {
			uint8_t status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
			if (!(status & CNF_SLP_PRZ))
				count++;
		}
	}
	uint16_t bench = GetTurnDuelistVariable(DUELVARS_BENCH).hl;
	while (gb_read8(bench) != 0xFF) {
		uint16_t slot_id = GetCardIDFromDeckIndex(gb_read8(bench));
		if ((uint8_t)slot_id == gb_read8(wTempPokemonID_ADDR))
			count++;
		bench++;
	}
	/* `or a / scf / jr nz / or a`: found = Z clear + C set. */
	return (PkmnPowerCountResult){count, count ? 0x10u : 0x80u};
}

/* substatus.asm:522-543: both duelists' play areas. */
PkmnPowerCountResult CountPokemonWithActivePkmnPowerInBothPlayAreas(uint8_t a)
{
	gb_write8(wTempPokemonID_ADDR, a);
	uint8_t count = CountTurnDuelistPokemonWithActivePkmnPower(a).a;
	SwapTurn();
	count = (uint8_t)(count + CountTurnDuelistPokemonWithActivePkmnPower(a).a);
	SwapTurn();
	return (PkmnPowerCountResult){count, count ? 0x10u : 0x80u};
}

/* substatus.asm:346-366. Returns carry iff the turn holder's arena card has the
 * sand-attack or smokescreen substatus active AND the coin toss came up tails.
 *
 * The ldtx flow is fall-through, not branch-scoped: `ldtx de, SandAttackCheckText`
 * runs for ANY non-zero substatus, then `ldtx de, SmokescreenCheckText` replaces it
 * whenever the value is not sand attack. So the unrelated-value exit carries
 * de = $00DF. GetTurnDuelistVariable leaves hl = the duelvar address and nothing
 * restores it, so exit hl is $C2E8/$C3E8 on every path. */
SandAttackCheckResult CheckSandAttackOrSmokescreenSubstatus(uint16_t de)
{
	DuelistVarResult status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS2);
	if (status.a == 0)
		return (SandAttackCheckResult){0, 0x80u, de, status.hl};

	de = SAND_ATTACK_CHECK_TEXT;
	if (status.a != SUBSTATUS2_SAND_ATTACK) {
		de = SMOKESCREEN_CHECK_TEXT;
		if (status.a != SUBSTATUS2_SMOKESCREEN)
			return (SandAttackCheckResult){status.a, 0x00u, de, status.hl};
	}

	uint8_t heads = gb_read8(wGotHeadsFromSandAttackOrSmokescreenCheck_ADDR);
	if (heads != 0)
		return (SandAttackCheckResult){heads, 0x00u, de, status.hl};
	/* `or a` set Z, then `scf` keeps it: the tails exit is Z+C. */
	return (SandAttackCheckResult){0, 0x90u, de, status.hl};
}
