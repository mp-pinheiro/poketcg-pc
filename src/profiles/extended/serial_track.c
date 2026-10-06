#include "serial_track.h"

#include <errno.h>

uint8_t g_serial_track_watch[0x10000u >> 3];
int g_serial_track_on;

int serial_track_load(const char *path)
{
	(void)path;
	errno = ENOTSUP;
	return -1;
}

void serial_track_free(void)
{
}

void serial_track_begin_interval(uint32_t interval)
{
	(void)interval;
}

void serial_track_access(void)
{
}

void serial_track_anchor(void)
{
}

void serial_track_residue(uint8_t known, uint8_t bytes[8])
{
	(void)known;
	(void)bytes;
}

uint32_t serial_track_mismatches(void)
{
	return 0u;
}

uint32_t serial_track_first_mismatch(void)
{
	return 0u;
}
