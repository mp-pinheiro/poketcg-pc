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
