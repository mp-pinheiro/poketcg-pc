#include "link.h"

#include <errno.h>

int link_open(int fd)
{
	(void)fd;
	errno = ENOTSUP;
	return -1;
}

void link_close(void)
{
}

int link_active(void)
{
	return 0;
}

void link_note_sc_write(uint8_t value)
{
	(void)value;
}

void link_pump(void)
{
}

void link_drain(void)
{
}

uint32_t link_exchanges(void)
{
	return 0u;
}

uint32_t link_timeouts(void)
{
	return 0u;
}

uint32_t link_drain_timeouts(void)
{
	return 0u;
}

int link_first_received(void)
{
	return -1;
}

void link_replay_serial(uint8_t received)
{
	(void)received;
}

uint32_t link_transport_exchanges(void)
{
	return 0u;
}

uint32_t link_transport_crc(void)
{
	return 0u;
}
