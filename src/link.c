#define _POSIX_C_SOURCE 200809L
#include "link.h"

#include "mem.h"
#include "home/serial.h"

#include <fcntl.h>
#include <stddef.h>
#include <time.h>
#include <sys/socket.h>
#include <unistd.h>

#define LINK_SB 0xFF01u
#define LINK_SC 0xFF02u
#define LINK_FRAME_MAGIC 0x5Au
#define LINK_FRAME_SIZE 3u
#define LINK_POLL_MASK 0x3Fu
#define LINK_TIMEOUT_CHECK 0x3FFu
#define LINK_TIMEOUT_SECONDS 2.0
#define LINK_OPEN_BUS 0xFFu

static int g_fd = -1;
static uint8_t g_armed;
static uint8_t g_sent;
static uint8_t g_in_pump;
static uint8_t g_peer_valid;
static uint8_t g_peer_armed;
static uint8_t g_peer_byte;
static uint32_t g_polls;
static uint32_t g_attempts;
static uint32_t g_exchanges;
static uint32_t g_timeouts;
static uint32_t g_drain_timeouts;
static uint8_t g_draining;
static int g_first_received = -1;
static struct timespec g_armed_at;

static double link_elapsed(void)
{
	struct timespec now;

	if (clock_gettime(CLOCK_MONOTONIC, &now) != 0)
		return 0.0;
	return (double)(now.tv_sec - g_armed_at.tv_sec)
	       + 1e-9 * (double)(now.tv_nsec - g_armed_at.tv_nsec);
}

int link_open(int fd)
{
	int flags = fcntl(fd, F_GETFL, 0);

	if (flags < 0 || fcntl(fd, F_SETFL, flags | O_NONBLOCK) < 0)
		return -1;
	g_fd = fd;
	g_armed = 0;
	g_sent = 0;
	g_peer_valid = 0;
	g_polls = 0;
	g_attempts = 0;
	g_exchanges = 0;
	g_timeouts = 0;
	g_drain_timeouts = 0;
	g_first_received = -1;
	return 0;
}

void link_close(void)
{
	if (g_fd >= 0)
		close(g_fd);
	g_fd = -1;
}

int link_active(void)
{
	return g_fd >= 0;
}

uint32_t link_exchanges(void)
{
	return g_exchanges;
}

uint32_t link_timeouts(void)
{
	return g_timeouts;
}

uint32_t link_drain_timeouts(void)
{
	return g_drain_timeouts;
}

int link_first_received(void)
{
	return g_first_received;
}

void link_note_sc_write(uint8_t value)
{
	if (g_fd < 0 || !(value & 0x80u))
		return;
	g_armed = 1;
	g_sent = 0;
	g_attempts = 0;
	(void)clock_gettime(CLOCK_MONOTONIC, &g_armed_at);
}

static void link_send_frame(void)
{
	uint8_t frame[LINK_FRAME_SIZE] = {LINK_FRAME_MAGIC, 1u, gb_read8(LINK_SB)};
	ssize_t written = send(g_fd, frame, sizeof frame, MSG_NOSIGNAL);

	if (written == (ssize_t)sizeof frame)
		g_sent = 1;
}

static void link_recv_frame(void)
{
	uint8_t frame[LINK_FRAME_SIZE];
	ssize_t got = recv(g_fd, frame, sizeof frame, 0);

	if (got != (ssize_t)sizeof frame || frame[0] != LINK_FRAME_MAGIC)
		return;
	g_peer_valid = 1;
	g_peer_armed = frame[1];
	g_peer_byte = frame[2];
}

static void link_complete(uint8_t received)
{
	g_armed = 0;
	g_sent = 0;
	g_attempts = 0;
	if (g_first_received < 0)
		g_first_received = received;
	gb_write8(LINK_SB, received);
	gb_write8(LINK_SC, (uint8_t)(gb_read8(LINK_SC) & 0x7Fu));
	g_exchanges++;
	SerialHandler();
}

void link_drain(void)
{
	uint32_t settled = g_exchanges + g_timeouts + g_drain_timeouts;

	g_draining = 1;
	while (g_fd >= 0 && g_armed
	       && g_exchanges + g_timeouts + g_drain_timeouts == settled) {
		link_pump();
		if (g_exchanges + g_timeouts + g_drain_timeouts == settled
		    && link_elapsed() > LINK_TIMEOUT_SECONDS) {
			g_timeouts++;
			link_complete(LINK_OPEN_BUS);
		}
	}
}

void link_pump(void)
{
	if (g_fd < 0 || g_in_pump)
		return;
	g_polls++;
	if (!g_armed)
		return;
	g_in_pump = 1;
	if (!g_sent)
		link_send_frame();
	if (!g_peer_valid && (g_attempts == 0 || (g_polls & LINK_POLL_MASK) == 0)) {
		link_recv_frame();
		g_attempts++;
	}
	if (g_peer_valid) {
		uint8_t received = g_peer_armed ? g_peer_byte : LINK_OPEN_BUS;

		g_peer_valid = 0;
		link_complete(received);
	} else if (!g_draining && (gb_read8(LINK_SC) & 0x01u)
	           && (g_attempts & LINK_TIMEOUT_CHECK) == 0
	           && link_elapsed() > LINK_TIMEOUT_SECONDS) {
		g_timeouts++;
		link_complete(LINK_OPEN_BUS);
	}
	g_in_pump = 0;
}
