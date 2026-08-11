#include "home/unused_save_validation.h"
#include "probe.h"

static void adapt_StubbedUnusedSaveDataValidation(ProbeState *s)
{
	StubbedUnusedSaveDataValidation();
	(void)s;
}

static void adapt_UnusedCalculateSaveDataValidationByte(ProbeState *s)
{
	UnusedSaveValidationResult result = UnusedCalculateSaveDataValidationByte();
	s->a = result.a;
	s->f = result.f;
}

const ProbeEntry probe_entries_unused_save_validation[] = {
	{"StubbedUnusedSaveDataValidation", adapt_StubbedUnusedSaveDataValidation},
	{"UnusedCalculateSaveDataValidationByte", adapt_UnusedCalculateSaveDataValidationByte},
	{NULL, NULL},
};
