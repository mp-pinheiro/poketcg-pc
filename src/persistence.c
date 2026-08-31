#define _GNU_SOURCE
#include "persistence.h"

#include "mem.h"

#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

#define SAVE_HEADER_SIZE 16u
#define SAVE_VERSION 1u
#define SAVE_PAYLOAD_SIZE 0x8000u

static void put_u32(uint8_t *dst, uint32_t value)
{
	dst[0] = (uint8_t)value;
	dst[1] = (uint8_t)(value >> 8);
	dst[2] = (uint8_t)(value >> 16);
	dst[3] = (uint8_t)(value >> 24);
}

static uint32_t get_u32(const uint8_t *src)
{
	return (uint32_t)src[0] | (uint32_t)src[1] << 8 |
	       (uint32_t)src[2] << 16 | (uint32_t)src[3] << 24;
}

static uint32_t checksum(const uint8_t *data, size_t length)
{
	uint32_t result = 2166136261u;
	for (size_t i = 0; i < length; i++) {
		result ^= data[i];
		result *= 16777619u;
	}
	return result;
}

static int write_all(int fd, const uint8_t *data, size_t length)
{
	while (length) {
		ssize_t written = write(fd, data, length);
		if (written < 0 && errno == EINTR)
			continue;
		if (written <= 0)
			return -1;
		data += written;
		length -= (size_t)written;
	}
	return 0;
}

static int read_all(int fd, uint8_t *data, size_t length)
{
	while (length) {
		ssize_t count = read(fd, data, length);
		if (count < 0 && errno == EINTR)
			continue;
		if (count <= 0) {
			if (!count)
				errno = EINVAL;
			return -1;
		}
		data += count;
		length -= (size_t)count;
	}
	return 0;
}

static int sync_parent(const char *path)
{
	char parent[PATH_MAX];
	const char *slash = strrchr(path, '/');
	if (!slash) {
		strcpy(parent, ".");
	} else if (slash == path) {
		strcpy(parent, "/");
	} else {
		size_t length = (size_t)(slash - path);
		if (length >= sizeof parent) {
			errno = ENAMETOOLONG;
			return -1;
		}
		memcpy(parent, path, length);
		parent[length] = '\0';
	}
	int fd = open(parent, O_RDONLY | O_DIRECTORY);
	if (fd < 0)
		return -1;
	int result = fsync(fd);
	int saved_errno = errno;
	close(fd);
	errno = saved_errno;
	return result;
}

int sram_save_atomic(const char *path)
{
	if (!path || !*path) {
		errno = EINVAL;
		return -1;
	}
	char temporary[PATH_MAX];
	int length = snprintf(temporary, sizeof temporary, "%s.tmp.XXXXXX", path);
	if (length < 0 || (size_t)length >= sizeof temporary) {
		errno = ENAMETOOLONG;
		return -1;
	}
	int fd = mkstemp(temporary);
	if (fd < 0)
		return -1;
	uint8_t header[SAVE_HEADER_SIZE] = {'P', 'K', 'S', 'R'};
	put_u32(header + 4, SAVE_VERSION);
	put_u32(header + 8, SAVE_PAYLOAD_SIZE);
	put_u32(header + 12, checksum(g_sram, sizeof g_sram));
	int result = write_all(fd, header, sizeof header);
	if (!result)
		result = write_all(fd, g_sram, sizeof g_sram);
	if (!result)
		result = fsync(fd);
	int saved_errno = errno;
	if (close(fd) != 0 && !result) {
		result = -1;
		saved_errno = errno;
	}
	if (!result && rename(temporary, path) != 0) {
		result = -1;
		saved_errno = errno;
	}
	if (result)
		unlink(temporary);
	else if (sync_parent(path) != 0) {
		result = -1;
		saved_errno = errno;
	}
	errno = saved_errno;
	return result;
}

int sram_load(const char *path)
{
	if (!path || !*path) {
		errno = EINVAL;
		return -1;
	}
	int fd = open(path, O_RDONLY);
	if (fd < 0)
		return -1;
	uint8_t header[SAVE_HEADER_SIZE];
	uint8_t payload[SAVE_PAYLOAD_SIZE];
	int result = read_all(fd, header, sizeof header);
	if (!result && (memcmp(header, "PKSR", 4) != 0 ||
	                get_u32(header + 4) != SAVE_VERSION ||
	                get_u32(header + 8) != SAVE_PAYLOAD_SIZE)) {
		errno = EINVAL;
		result = -1;
	}
	if (!result)
		result = read_all(fd, payload, sizeof payload);
	if (!result && checksum(payload, sizeof payload) != get_u32(header + 12)) {
		errno = EINVAL;
		result = -1;
	}
	int saved_errno = errno;
	if (close(fd) != 0 && !result) {
		result = -1;
		saved_errno = errno;
	}
	if (!result)
		memcpy(g_sram, payload, sizeof payload);
	errno = saved_errno;
	return result;
}
