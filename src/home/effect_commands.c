#include "home/effect_commands.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/switch_rom.h"
#include "mem.h"

#define BANK_EFFECT_COMMANDS 0x06u
#define BANK_EFFECT_FUNCTIONS 0x0Bu

/* engine/duel/effect_commands.asm:37-85. hl walks a command list (2 bytes/entry:
 * type, function pointer; 0 terminates) under BANK_EFFECT_COMMANDS. NULL hl
 * short-circuits before any bank switch or wEffectFunctionsBank write. Only the
 * lookup ports -- TryExecuteEffectCommandFunction's `jp hl` dispatch into bank
 * $0b stays unported. */
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
