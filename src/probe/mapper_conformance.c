#include "mem.h"
#include "probe.h"

static void adapt_MBC5ConformanceVector(ProbeState *s)
{
	(void)s;

	gb_write8(0xC000, gb_read8(0x0150));
	gb_write8(0xC001, gb_read8(0x4000));

	gb_write8(0x2000, 0x00);
	gb_write8(0xC002, gb_read8(0x4000));
	gb_write8(0x2000, 0x45);
	gb_write8(0xC003, gb_read8(0x4000));
	gb_write8(0x3000, 0x01);
	gb_write8(0xC004, gb_read8(0x4000));
	gb_write8(0x0000, 0x0A);
	gb_write8(0x4000, 0x03);
	gb_write8(0xA123, 0x33);
	gb_write8(0x4000, 0x04);
	gb_write8(0xA123, 0x44);
	gb_write8(0x4000, 0x03);
	gb_write8(0xC005, gb_read8(0xA123));
	gb_write8(0x4000, 0x04);
	gb_write8(0xC006, gb_read8(0xA123));

	gb_write8(0x0000, 0x1A);
	gb_write8(0xA123, 0x55);
	gb_write8(0xC007, gb_read8(0xA123));

	gb_write8(0x0000, 0x0A);
	gb_write8(0x4000, 0x00);
	gb_write8(0xC008, gb_read8(0xA123));

	gb_write8(0x0000, 0x00);
}

const ProbeEntry probe_entries_mapper_conformance[] = {
	{ "MBC5ConformanceVector", adapt_MBC5ConformanceVector },
	{ NULL, NULL },
};
