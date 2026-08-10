#include "home/labels.h"

#include "generated/hram.h"
#include "home/print_text.h"
#include "home/text_box.h"
#include "mem.h"

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
