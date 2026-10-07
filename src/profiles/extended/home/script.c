/* === part MAP_SCRIPTS */
/* >>> part OVERWORLD_SCRIPT_TABLE_BANK */
#define OVERWORLD_SCRIPT_TABLE_BANK OverworldScriptTable_BANK
/* <<< part OVERWORLD_SCRIPT_TABLE_BANK */
/* >>> part OVERWORLD_SCRIPT_TABLE_ADDR */
#define OVERWORLD_SCRIPT_TABLE_ADDR OverworldScriptTable_ADDR
/* <<< part OVERWORLD_SCRIPT_TABLE_ADDR */
/* >>> factory GetMapScriptPointer */
/* script.asm:62-95. Entry l = script selector; the entry is
 * MapScripts + wCurMap * 16 + l in bank 4. The pointer is read there and the
 * routine's bank is restored, so the returned value is a plain address.
 * Exit carry is set iff the pointer is non-zero (`scf / ccf` double-negation),
 * and a is lo | hi of the pointer. */
MapScriptResult GetMapScriptPointer(uint8_t l)
{
	uint16_t entry = (uint16_t)(MAP_SCRIPTS + (uint16_t)wCurMap * 24u + l);
	const uint8_t *p = rom_ptr(MAP_SCRIPTS_BANK, entry);
	uint16_t ptr = (uint16_t)(p[0] | (uint16_t)p[1] << 8);
	uint8_t found = (uint8_t)((uint8_t)ptr | (uint8_t)(ptr >> 8));
	uint8_t f = found == 0u ? 0x80u : 0x10u;
	return (MapScriptResult){p[2], f, ptr};
}
/* <<< factory GetMapScriptPointer */
/* --- factory GetNPCDuelConfigurations */
/* >>> factory HandleMoveModeAPress */
HandleMoveModeAPressResult HandleMoveModeAPress(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)a;
	(void)d;
	(void)hl;
	uint8_t saved_f = f;
	uint8_t saved_bank = hBankROM;
	MapScriptResult objects = GetMapScriptPointer(MAP_SCRIPT_OBJECTS);
	if ((objects.f & 0x10u) == 0u) {
		BankswitchROM(saved_bank);
		CallMapScriptResult second = CallMapScriptPointerIfExists(MAP_SCRIPT_PRESSED_A);
		uint8_t second_f = second.f;
		return (HandleMoveModeAPressResult){second.a, second_f, b, c, d, e, second.hl};
	}

	FindPlayerMovementWithOffsetResult movement = FindPlayerMovementFromDirection();
	uint8_t object_direction = wPlayerDirection;
	uint16_t cursor = objects.hl;
	for (;;) {
		const uint8_t *entry = rom_ptr(MAP_SCRIPTS_BANK, cursor);
		if ((entry[0] & 0x80u) != 0u)
			break;
		if (entry[0] == object_direction && entry[1] == movement.b && entry[2] == movement.c) {
			wNextScript = entry[3];
			gb_write8((uint16_t)(wNextScript_ADDR + 1u), entry[4]);
			wNextScriptBank = entry[5];
			wDefaultObjectText = entry[6];
			gb_write8((uint16_t)(wDefaultObjectText_ADDR + 1u), entry[7]);
			wCurrentNPCNameTx = entry[8];
			gb_write8((uint16_t)(wCurrentNPCNameTx_ADDR + 1u), entry[9]);
			BankswitchROM(saved_bank);
			return (HandleMoveModeAPressResult){saved_bank, (uint8_t)((saved_f & 0x80u) | 0x10u), movement.b, movement.c, object_direction, e, (uint16_t)(cursor + 1u)};
		}
		cursor = (uint16_t)(cursor + MAP_OBJECT_SIZE);
	}

	BankswitchROM(saved_bank);
	CallMapScriptResult second = CallMapScriptPointerIfExists(MAP_SCRIPT_PRESSED_A);
	uint8_t second_f = second.f;
	return (HandleMoveModeAPressResult){second.a, second_f, movement.b, movement.c, object_direction, e, second.hl};
}
/* <<< factory HandleMoveModeAPress */
/* --- factory Func_3b11 */
/* >>> factory RunOverworldScript */
/* script.asm:108-133. The command entry inherits the caller flags and d/e,
 * receives the two inline script arguments in b/c, and starts with the
 * command address in hl. */
RunOverworldScriptResult RunOverworldScript(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c,
	uint8_t d, uint8_t e, uint16_t hl)
{
	(void)a;
	(void)b;
	(void)c;
	(void)hl;
	uint8_t saved_bank = hBankROM;
	uint16_t script_pointer = (uint16_t)(
		gb_read8(wScriptPointer_ADDR)
		| ((uint16_t)gb_read8((uint16_t)(wScriptPointer_ADDR + 1u)) << 8));
	uint8_t opcode = gb_read8(script_pointer);
	uint16_t args = (uint16_t)(script_pointer + 1u);
	/* Both operand bytes are fetched before the command's length is known, so
	 * a one-byte command at the end of a blob reads past it. Every command
	 * that consumes an operand owns bytes inside its own blob, so a byte the
	 * pack does not carry is one the asm discards. */
	uint8_t command_c = script_operand(args);
	uint8_t command_b = script_operand((uint16_t)(args + 1u));
	const uint8_t *entry;

	BankswitchROM(OVERWORLD_SCRIPT_TABLE_BANK);
	entry = rom_ptr(OVERWORLD_SCRIPT_TABLE_BANK,
		(uint16_t)(OVERWORLD_SCRIPT_TABLE_ADDR + (uint16_t)opcode * 2u));
	uint16_t target = (uint16_t)(entry[0] | ((uint16_t)entry[1] << 8));
	BankswitchROM(saved_bank);

	ScriptDispatchFn dispatch = ScriptDispatchLookupOpcode(opcode);
	if (dispatch == NULL) {
		fprintf(stderr,
			"script opcode miss opcode=$%02X target=$%04X pointer=$%04X\n",
			(unsigned)opcode, (unsigned)target, (unsigned)script_pointer);
		abort();
	}
	ScriptDispatchState state = {
		.a = saved_bank,
		.f = f,
		.b = command_b,
		.c = command_c,
		.d = d,
		.e = e,
		.hl = target,
		.stack_count = 0u,
		.post_call_byte = 0u,
	};
	dispatch(&state);
	return (RunOverworldScriptResult){
		state.a, state.f, state.b, state.c, state.d, state.e, state.hl};
}
/* <<< factory RunOverworldScript */
/* === factory EnterFarScript */
