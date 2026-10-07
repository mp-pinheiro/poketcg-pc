/* >>> factory Script_Specs2 */
/* science_club_lobby.asm:68-81 -- the routine's entire CODE portion, 24 bytes,
 * straight-line with a single exit. The `start_script` macro assembles to
 * `rst $20` at $6BDD, where the code ends and the script bytecode begins, so
 * the cases declare completion pre-ret there.
 *
 * `and %11` keeps the low two bits of UpdateRNGSources' return, indexing a
 * four-entry card-id table at Data_ebe7 (03:6BE7). GetCardName returns the new
 * `de`, which is stored little-endian to wTxRam2 by `ld [hli],a` / `ld [hl],d`,
 * leaving hl at wTxRam2+1. `d` is zeroed before the call, so only `e` carries
 * the table byte in. */
ScriptSpecs2Result Script_Specs2(void)
{
	uint8_t rng = UpdateRNGSources();
	uint8_t c = (uint8_t)(rng & 0x06u);
	uint16_t hl = (uint16_t)(DATA_EBE7 + c);
	const uint8_t *entry = rom_ptr(DATA_EBE7_BANK, hl);
	uint16_t card = (uint16_t)(entry[0] | ((uint16_t)entry[1] << 8));
	uint16_t text = GetCardName(card);
	hl = wTxRam2_ADDR;
	gb_write8(hl, (uint8_t)text);
	hl = (uint16_t)(hl + 1u);
	gb_write8(hl, (uint8_t)(text >> 8));
	return (ScriptSpecs2Result){(uint8_t)text, 0u, c,
	                            (uint8_t)(text >> 8), (uint8_t)text, hl};
}
/* <<< factory Script_Specs2 */
