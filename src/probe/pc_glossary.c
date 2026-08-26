#include "home/pc_glossary.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory _PCMenu_Glossary */
static void adapt__PCMenu_Glossary(ProbeState *s)
{
	(void)s;
	_PCMenu_Glossary();
}
/* <<< factory _PCMenu_Glossary */

const ProbeEntry probe_entries_pc_glossary[] = {
	{ "_PCMenu_Glossary", adapt__PCMenu_Glossary },
	{ NULL, NULL },
};
