#include "home/effect_commands.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/switch_rom.h"
#include "mem.h"
#include <stdio.h>
#include <stdlib.h>
/* >>> factory statics */
#include "home/effect_commands.h"
#include "home/switch_rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< factory statics */

#define BANK_EFFECT_COMMANDS 0x06u
#define BANK_EFFECT_FUNCTIONS 0x0Bu

/* engine/duel/effect_commands.asm:37-85. hl walks a command list (2 bytes/entry:
 * type, function pointer; 0 terminates) under BANK_EFFECT_COMMANDS. NULL hl
 * short-circuits before any bank switch or wEffectFunctionsBank write. The
 * matched function pointer resolves through the generated bank-$0b dispatch
 * table (tools/gen_effect_dispatch.py over the probe adapters); a pointer
 * with no adapter fails loud. */
EffectCmdLookup CheckMatchingCommand(uint8_t a, uint16_t hl)
{
	if (hl == 0)
		return (EffectCmdLookup){0, 1};

	uint8_t saved = hBankROM;
	BankswitchROM(BANK_EFFECT_COMMANDS);
	wEffectFunctionsBank = BANK_EFFECT_FUNCTIONS;
	for (;;) {
		uint8_t type = gb_read8(hl++);
		if (type == 0) {
			BankswitchROM(saved);
			return (EffectCmdLookup){hl, 1};
		}
		if (type == a) {
			uint16_t lo = gb_read8(hl++);
			uint16_t hi = gb_read8(hl);
			BankswitchROM(saved);
			return (EffectCmdLookup){(uint16_t)(lo | hi << 8), 0};
		}
		hl = (uint16_t)(hl + 2u);
	}
}

/* >>> factory TryExecuteEffectCommandFunction */
TryExecuteEffectCommandFunctionResult TryExecuteEffectCommandFunction(
	uint8_t command, uint8_t b, uint8_t d, uint8_t e)
{
	uint16_t list = (uint16_t)(gb_read8(wLoadedAttackEffectCommands_ADDR) |
		((uint16_t)gb_read8((uint16_t)(wLoadedAttackEffectCommands_ADDR + 1u)) << 8));
	EffectCmdLookup lookup = CheckMatchingCommand(command, list);
	if (lookup.carry != 0u) {
		uint8_t a = lookup.hl == 0u ? 0u : hBankROM;
		uint8_t f = (uint8_t)(a == 0u ? 0x80u : 0u);
		return (TryExecuteEffectCommandFunctionResult){
			.a = a, .f = f, .b = b, .c = command, .d = d, .e = e, .hl = lookup.hl,
		};
	}

	uint8_t saved_bank = hBankROM;
	uint8_t effect_bank = wEffectFunctionsBank;
	EffectDispatchFn function = EffectDispatchLookupAddress(lookup.hl);
	if (function == NULL) {
		fprintf(stderr,
		        "indirect dispatch miss site=TryExecuteEffectCommandFunction target=$%04X\n",
		        (unsigned)lookup.hl);
		abort();
	}
	BankswitchROM(effect_bank);
	TryExecuteEffectCommandFunctionResult state = {
		.a = effect_bank,
		.f = (uint8_t)(effect_bank == 0u ? 0x80u : 0u),
		.b = b,
		.c = command,
		.d = d,
		.e = e,
		.hl = lookup.hl,
	};
	function(&state);
	BankswitchROM(saved_bank);
	state.b = state.a;
	state.c = state.f;
	return state;
}
/* <<< factory TryExecuteEffectCommandFunction */
