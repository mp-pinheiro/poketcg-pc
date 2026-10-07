/* >>> part includes */
#include "home/load_deck.h"
#include "generated/hram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory LoadDeck */
/* Valid path ends `or a` on the restored bank (overwrites f: Z iff bank==0, C=0).
 * Null path: `pop af` restores entry f, then `scf` sets C/N=0/H=0 but keeps the
 * restored Z bit -> f = 0x10 | (entry_f & Z). */
static void adapt_LoadDeck(ProbeState *s)
{
	uint8_t carry = LoadDeck(s->a);
	if (carry)
		s->f = (uint8_t)(0x10u | (s->f & 0x80u));
	else
		s->f = (uint8_t)(hBankROM == 0 ? 0x80u : 0u);
}
/* <<< factory LoadDeck */

/* >>> factory CompressDeckToSRAM */
static void adapt_CompressDeckToSRAM(ProbeState *s)
{
	CompressDeckToSRAM((uint16_t)(((uint16_t)s->d << 8) | s->e), s->hl);
}
/* <<< factory CompressDeckToSRAM */

/* >>> factory DecompressSRAMDeck */
static void adapt_DecompressSRAMDeck(ProbeState *s)
{
	DecompressSRAMDeck((uint16_t)(((uint16_t)s->d << 8) | s->e), s->hl);
}
/* <<< factory DecompressSRAMDeck */

/* >>> part probe_entries_load_deck */
const ProbeEntry probe_entries_load_deck[] = {
	{ "LoadDeck", adapt_LoadDeck },
	{ "CompressDeckToSRAM", adapt_CompressDeckToSRAM },
	{ "DecompressSRAMDeck", adapt_DecompressSRAMDeck },
	{ NULL, NULL },
};
/* <<< part probe_entries_load_deck */
