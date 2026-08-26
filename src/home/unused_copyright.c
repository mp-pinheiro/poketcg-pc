#include "home/unused_copyright.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/hram.h"
#include "home/color.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/init_menu.h"
#include "home/load_animation.h"
#include "home/random.h"

#define PAD_START 0x08u
#define SCENE_COPYRIGHT 0x19u
/* <<< factory statics */

/* >>> factory UnusedCopyrightScreen */
void UnusedCopyrightScreen(void)
{
	DisableLCD();
	LoadConsolePaletteData();
	(void)InitMenuScreen();
	(void)LoadScene(SCENE_COPYRIGHT, 0u, 0u, 0u, 0u, 0u, 0u);
	(void)FadeScreenFromWhite();
	uint16_t frame_count = 300u;
	for (;;) {
		DoFrameIfLCDEnabled();
		(void)UpdateRNGSources();
		if ((hKeysPressed & PAD_START) != 0u)
			break;
		frame_count = (uint16_t)(frame_count - 1u);
		if (frame_count == 0u)
			break;
	}
	FadeScreenToWhite();
}
/* <<< factory UnusedCopyrightScreen */
