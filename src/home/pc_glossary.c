#include "home/pc_glossary.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "home/init_menu.h"
#include "home/glossary.h"
#include "home/process_text.h"
/* <<< factory statics */

/* >>> factory _PCMenu_Glossary */
void _PCMenu_Glossary(void)
{
	uint8_t saved_d291 = wd291;
	(void)InitMenuScreen();
	(void)SetupText(0x30u, 0xFFu);
	(void)FlashWhiteScreen();
	OpenGlossaryScreen();
	wd291 = saved_d291;
}
/* <<< factory _PCMenu_Glossary */
