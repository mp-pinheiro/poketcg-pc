#include "home/labels.h"

#include "generated/hram.h"
#include "home/print_text.h"
#include "home/text_box.h"
#include "mem.h"
/* >>> factory statics */
#include "home/labels.h"
#include "home/text_box.h"
#include "home/overworld.h"
#include "home/lcd_enable_frame.h"
#include "home/menus.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< factory statics */

LabelsResult PrintLabels(uint16_t hl, uint8_t d, uint8_t e)
{
	uint8_t saved_hffb0 = hffb0;
	uint16_t start = hl;

	hffb0 = 0x02;
	for (;;) {
		d = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (d & 0x80u)
			break;
		hl = (uint16_t)(hl + 1u);
		uint8_t low = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint16_t text = (uint16_t)(low | ((uint16_t)gb_read8(hl) << 8));
		TextResult result = PrintTextNoDelay(text, d, e);
		d = result.d;
		e = result.e;
		hl = (uint16_t)(hl + 1u);
	}

	hl = start;
	hffb0 = saved_hffb0;
	for (;;) {
		d = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (d & 0x80u)
			return (LabelsResult){d, e, hl};
		e = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		AdjustCoordinatesForBGScroll(&d, &e);
		uint8_t low = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint16_t text = (uint16_t)(low | ((uint16_t)gb_read8(hl) << 8));
		InitTextPrinting(d, e);
		TextResult result = PrintTextNoDelay(text, d, e);
		d = result.d;
		e = result.e;
		hl = (uint16_t)(hl + 1u);
	}
}

/* >>> factory InitAndPrintMenu */
void InitAndPrintMenu(uint16_t hl, uint8_t a)
{
	uint8_t d = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	uint8_t e = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	uint8_t b = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	uint8_t c = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	uint16_t saved_hl = hl;

	AdjustCoordinatesForBGScroll(&d, &e);

	FuncC3caResult r_c3ca = Func_c3ca(b, c, d, e);

	uint16_t draw_hl = saved_hl;
	DrawRegularTextBox(&draw_hl, r_c3ca.a, b, c, d, e);
	DoFrameIfLCDEnabled();

	LabelsResult labels = PrintLabels(saved_hl, d, e);

	uint16_t menu_hl = labels.hl;
	InitializeMenuParameters(a, &menu_hl);
}
/* <<< factory InitAndPrintMenu */
