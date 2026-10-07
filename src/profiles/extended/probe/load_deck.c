/* === factory LoadDeck */
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
	{ "CompressDeckToSRAM", adapt_CompressDeckToSRAM },
	{ "DecompressSRAMDeck", adapt_DecompressSRAMDeck },
/* <<< part probe_entries_load_deck */
