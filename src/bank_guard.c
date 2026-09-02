#include "bank_guard.h"

#include <stdio.h>
#include <stdlib.h>

#include "home/switch_rom.h"
#include "mem.h"

/* Every function here must stay uninstrumented, or the entry hook recurses
 * into itself on the first call. */
#define NOTRACE __attribute__((no_instrument_function))

#define BANK_GUARD_DEPTH 512u

typedef struct {
	const void *function;
	uint8_t saved;
	uint8_t switched;
} BankGuardFrame;

static const BankGuardEntry *g_sorted;
static BankGuardFrame g_frames[BANK_GUARD_DEPTH];
static size_t g_depth;

NOTRACE static int compare_entries(const void *left, const void *right)
{
	const BankGuardEntry *a = left;
	const BankGuardEntry *b = right;

	if (a->function < b->function)
		return -1;
	return a->function > b->function;
}

NOTRACE static const BankGuardEntry *lookup(const void *function)
{
	if (g_sorted == NULL) {
		BankGuardEntry *sorted = malloc(kBankGuardCount * sizeof *sorted);

		if (sorted == NULL)
			return NULL;
		for (size_t i = 0; i < kBankGuardCount; i++)
			sorted[i] = kBankGuardEntries[i];
		qsort(sorted, kBankGuardCount, sizeof *sorted, compare_entries);
		g_sorted = sorted;
	}

	size_t low = 0;
	size_t high = kBankGuardCount;

	while (low < high) {
		size_t middle = low + (high - low) / 2u;

		if (g_sorted[middle].function < function)
			low = middle + 1u;
		else
			high = middle;
	}
	if (low < kBankGuardCount && g_sorted[low].function == function)
		return &g_sorted[low];
	return NULL;
}

NOTRACE void bank_guard_enter(const void *function)
{
	const BankGuardEntry *entry = lookup(function);

	if (entry == NULL)
		return;
	if (g_depth >= BANK_GUARD_DEPTH) {
		fprintf(stderr, "bank guard depth exceeded at %p\n", function);
		abort();
	}

	uint8_t saved = g_rom_bank;
	BankGuardFrame *frame = &g_frames[g_depth++];

	frame->function = function;
	frame->saved = saved;
	frame->switched = saved != entry->bank;
	if (frame->switched)
		BankswitchROM(entry->bank);
}

NOTRACE void bank_guard_exit(const void *function)
{
	size_t index = g_depth;

	while (index > 0u && g_frames[index - 1u].function != function)
		index--;
	if (index == 0u)
		return;

	BankGuardFrame *frame = &g_frames[index - 1u];

	g_depth = index - 1u;
	if (frame->switched)
		BankswitchROM(frame->saved);
}

NOTRACE void bank_guard_reset(void)
{
	/* Restore in LIFO order, exactly as the abandoned `ret` cascade would, so
	 * the caller resumes on the bank it had before the skipped frames. */
	while (g_depth > 0u) {
		BankGuardFrame *frame = &g_frames[--g_depth];

		if (frame->switched)
			BankswitchROM(frame->saved);
	}
}
