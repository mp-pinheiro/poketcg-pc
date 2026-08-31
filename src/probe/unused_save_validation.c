#include "home/unused_save_validation.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory StubbedUnusedSaveDataValidation */
static void adapt_StubbedUnusedSaveDataValidation(ProbeState *s)
{
	StubbedUnusedSaveDataValidation();
}
/* <<< factory StubbedUnusedSaveDataValidation */

/* >>> factory UnusedCalculateSaveDataValidationByte */
static void adapt_UnusedCalculateSaveDataValidationByte(ProbeState *s)
{
	UnusedCalculateSaveDataValidationByteResult r = UnusedCalculateSaveDataValidationByte();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory UnusedCalculateSaveDataValidationByte */

/* >>> factory UnusedSaveDataValidation */
static void adapt_UnusedSaveDataValidation(ProbeState *s)
{
	(void)s;
	UnusedSaveDataValidation();
}
/* <<< factory UnusedSaveDataValidation */

const ProbeEntry probe_entries_unused_save_validation[] = {
	{ "StubbedUnusedSaveDataValidation", adapt_StubbedUnusedSaveDataValidation },
	{ "UnusedCalculateSaveDataValidationByte", adapt_UnusedCalculateSaveDataValidationByte },
	{ "UnusedSaveDataValidation", adapt_UnusedSaveDataValidation },
	{ NULL, NULL },
};
