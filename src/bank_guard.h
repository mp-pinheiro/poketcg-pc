#ifndef POKETCG_BANK_GUARD_H
#define POKETCG_BANK_GUARD_H

#include <stddef.h>
#include <stdint.h>

/* `farcall` semantics for the ported call graph: a routine the asm only ever
 * reaches through farcall/bank1call runs with its own bank selected and leaves
 * the caller's bank restored (poketcg/src/home/farcall.asm). The C port calls
 * such a routine directly, so the entry/exit instrumentation supplies the
 * switch for every target in tools/gen_bank_guard.py's table.
 *
 * A routine entered with its own bank already selected is an ordinary same-bank
 * `call`; it is left alone on both sides, so a bank the asm deliberately leaks
 * out of a same-bank call still leaks. */
typedef struct {
	const void *function;
	uint8_t bank;
} BankGuardEntry;

extern const BankGuardEntry kBankGuardEntries[];
extern const size_t kBankGuardCount;

void bank_guard_enter(const void *function);
void bank_guard_exit(const void *function);
/* Unwinds the frame stack after a non-local exit (boot restart's longjmp, the
 * probe's frame budget), restoring banks LIFO because those exits skipped every
 * pending exit hook. */
void bank_guard_reset(void);

#endif /* POKETCG_BANK_GUARD_H */
