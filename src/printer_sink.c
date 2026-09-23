#include "printer_sink.h"

#include "runtime.h"

#include <stdio.h>
#include <string.h>

#define PRINTER_MAGIC_0 0x88u
#define PRINTER_MAGIC_1 0x33u
#define PRINTER_CMD_INIT 0x01u
#define PRINTER_CMD_PRINT 0x02u
#define PRINTER_CMD_DATA 0x04u
#define PRINTER_CMD_STATUS 0x0Fu
#define PRINTER_DEVICE_ID 0x81u
#define PRINTER_STATUS_DATA 0x08u
#define PRINTER_STATUS_PRINTING 0x02u
#define PRINTER_BAND_TILES 40u
#define PRINTER_BAND_BYTES (PRINTER_BAND_TILES * 16u)
#define PRINTER_MAX_BANDS 64u
#define PRINTER_PAYLOAD_MAX 0x280u
#define PRINTER_WIDTH 160u
#define PRINTER_TILES_PER_ROW 20u

enum {
	STATE_MAGIC_0,
	STATE_MAGIC_1,
	STATE_COMMAND,
	STATE_COMPRESSION,
	STATE_LENGTH_LOW,
	STATE_LENGTH_HIGH,
	STATE_PAYLOAD,
	STATE_CHECKSUM_LOW,
	STATE_CHECKSUM_HIGH,
	STATE_REPLY_DEVICE,
	STATE_REPLY_STATUS,
};

static struct {
	int attached;
	char directory[512];
	char last_path[640];
	int state;
	uint8_t command;
	uint8_t compression;
	uint16_t length;
	uint16_t received;
	uint16_t checksum;
	uint16_t claimed;
	uint8_t payload[PRINTER_PAYLOAD_MAX];
	uint8_t bands[PRINTER_MAX_BANDS * PRINTER_BAND_BYTES];
	size_t band_bytes;
	uint8_t status;
	size_t pages;
} g_printer;

void printer_attach(const char *directory)
{
	memset(&g_printer, 0, sizeof g_printer);
	if (directory) {
		snprintf(g_printer.directory, sizeof g_printer.directory, "%s", directory);
		g_printer.attached = 1;
	}
}

int printer_attached(void)
{
	return g_printer.attached;
}

void printer_reset(void)
{
	g_printer.state = STATE_MAGIC_0;
	g_printer.band_bytes = 0;
	g_printer.status = 0;
}

size_t printer_pages(void)
{
	return g_printer.pages;
}

size_t printer_band_bytes(void)
{
	return g_printer.band_bytes;
}

const uint8_t *printer_band_data(void)
{
	return g_printer.bands;
}

const char *printer_last_path(void)
{
	return g_printer.last_path;
}

uint8_t printer_device_byte(void)
{
	return g_printer.attached ? PRINTER_DEVICE_ID : 0xFFu;
}

uint8_t printer_status_byte(void)
{
	return g_printer.attached ? g_printer.status : 0xFFu;
}

static void append_band_byte(uint8_t value)
{
	if (g_printer.band_bytes < sizeof g_printer.bands)
		g_printer.bands[g_printer.band_bytes++] = value;
}

static void decode_payload(void)
{
	if (!g_printer.compression) {
		for (uint16_t i = 0; i < g_printer.length; i++)
			append_band_byte(g_printer.payload[i]);
		return;
	}
	uint16_t index = 0;
	while (index < g_printer.length) {
		uint8_t control = g_printer.payload[index++];
		if (control & 0x80u) {
			unsigned run = (control & 0x7Fu) + 2u;
			if (index >= g_printer.length)
				break;
			uint8_t value = g_printer.payload[index++];
			while (run--)
				append_band_byte(value);
		} else {
			unsigned run = control + 1u;
			while (run-- && index < g_printer.length)
				append_band_byte(g_printer.payload[index++]);
		}
	}
}

static void finish_page(uint8_t palette)
{
	if (g_printer.band_bytes == 0u)
		return;
	g_printer.pages++;
	snprintf(g_printer.last_path, sizeof g_printer.last_path, "%s/print-%03zu.png",
	         g_printer.directory, g_printer.pages);
	if (printer_write_png(g_printer.last_path, g_printer.bands, g_printer.band_bytes, palette) != 0)
		g_printer.status |= 0x40u;
	else
		runtime_mark_event(RUNTIME_EVENT_PRINTER_PNG_CLOSED);
	g_printer.band_bytes = 0;
}

static void complete_packet(void)
{
	switch (g_printer.command) {
	case PRINTER_CMD_INIT:
		g_printer.band_bytes = 0;
		g_printer.status = 0;
		break;
	case PRINTER_CMD_DATA:
		if (g_printer.length) {
			decode_payload();
			g_printer.status |= PRINTER_STATUS_DATA;
		}
		break;
	case PRINTER_CMD_PRINT:
		finish_page(g_printer.length >= 3u ? g_printer.payload[2] : 0xE4u);
		g_printer.status = (uint8_t)((g_printer.status & 0x40u) | PRINTER_STATUS_PRINTING);
		break;
	case PRINTER_CMD_STATUS:
	default:
		g_printer.status &= (uint8_t)~PRINTER_STATUS_PRINTING;
		break;
	}
}

void printer_serial_byte(uint8_t value)
{
	if (!g_printer.attached)
		return;
	switch (g_printer.state) {
	case STATE_MAGIC_0:
		if (value == PRINTER_MAGIC_0)
			g_printer.state = STATE_MAGIC_1;
		break;
	case STATE_MAGIC_1:
		g_printer.state = value == PRINTER_MAGIC_1 ? STATE_COMMAND : STATE_MAGIC_0;
		break;
	case STATE_COMMAND:
		g_printer.command = value;
		g_printer.checksum = value;
		g_printer.state = STATE_COMPRESSION;
		break;
	case STATE_COMPRESSION:
		g_printer.compression = value & 1u;
		g_printer.checksum = (uint16_t)(g_printer.checksum + value);
		g_printer.state = STATE_LENGTH_LOW;
		break;
	case STATE_LENGTH_LOW:
		g_printer.length = value;
		g_printer.checksum = (uint16_t)(g_printer.checksum + value);
		g_printer.state = STATE_LENGTH_HIGH;
		break;
	case STATE_LENGTH_HIGH:
		g_printer.length |= (uint16_t)(value << 8);
		g_printer.checksum = (uint16_t)(g_printer.checksum + value);
		g_printer.received = 0;
		if (g_printer.length > PRINTER_PAYLOAD_MAX)
			g_printer.length = PRINTER_PAYLOAD_MAX;
		g_printer.state = g_printer.length ? STATE_PAYLOAD : STATE_CHECKSUM_LOW;
		break;
	case STATE_PAYLOAD:
		g_printer.payload[g_printer.received++] = value;
		g_printer.checksum = (uint16_t)(g_printer.checksum + value);
		if (g_printer.received >= g_printer.length)
			g_printer.state = STATE_CHECKSUM_LOW;
		break;
	case STATE_CHECKSUM_LOW:
		g_printer.claimed = value;
		g_printer.state = STATE_CHECKSUM_HIGH;
		break;
	case STATE_CHECKSUM_HIGH:
		g_printer.claimed |= (uint16_t)(value << 8);
		if (g_printer.claimed != g_printer.checksum)
			g_printer.status |= 0x01u;
		else
			complete_packet();
		g_printer.state = STATE_REPLY_DEVICE;
		break;
	case STATE_REPLY_DEVICE:
		g_printer.state = STATE_REPLY_STATUS;
		break;
	case STATE_REPLY_STATUS:
	default:
		g_printer.state = STATE_MAGIC_0;
		break;
	}
}

static uint32_t crc_table[256];

static void crc_init(void)
{
	if (crc_table[1])
		return;
	for (uint32_t n = 0; n < 256; n++) {
		uint32_t c = n;
		for (int k = 0; k < 8; k++)
			c = (c & 1u) ? 0xEDB88320u ^ (c >> 1) : c >> 1;
		crc_table[n] = c;
	}
}

static uint32_t crc_update(uint32_t crc, const uint8_t *data, size_t length)
{
	crc ^= 0xFFFFFFFFu;
	for (size_t i = 0; i < length; i++)
		crc = crc_table[(crc ^ data[i]) & 0xFFu] ^ (crc >> 8);
	return crc ^ 0xFFFFFFFFu;
}

static void put32(uint8_t *out, uint32_t value)
{
	out[0] = (uint8_t)(value >> 24);
	out[1] = (uint8_t)(value >> 16);
	out[2] = (uint8_t)(value >> 8);
	out[3] = (uint8_t)value;
}

static int write_chunk(FILE *file, const char *type, const uint8_t *data, size_t length)
{
	uint8_t head[8];
	uint8_t tail[4];
	put32(head, (uint32_t)length);
	memcpy(head + 4, type, 4);
	uint32_t crc = crc_update(0, head + 4, 4);
	if (length)
		crc = crc_update(crc, data, length);
	put32(tail, crc);
	return fwrite(head, 1, 8, file) == 8 && (length == 0 || fwrite(data, 1, length, file) == length)
	               && fwrite(tail, 1, 4, file) == 4
	           ? 0
	           : -1;
}

int printer_write_png(const char *path, const uint8_t *tiles, size_t tile_bytes, uint8_t palette)
{
	size_t tile_count = tile_bytes / 16u;
	size_t rows = tile_count / PRINTER_TILES_PER_ROW;
	if (rows == 0u)
		return -1;
	size_t height = rows * 8u;
	size_t stride = 1u + PRINTER_WIDTH;
	size_t raw_size = height * stride;
	static uint8_t raw[1u + PRINTER_WIDTH * 8u * PRINTER_MAX_BANDS * 2u + 8u * PRINTER_MAX_BANDS * 2u];
	if (raw_size > sizeof raw)
		return -1;
	static const uint8_t grey[4] = {0xFFu, 0xAAu, 0x55u, 0x00u};
	for (size_t y = 0; y < height; y++) {
		raw[y * stride] = 0u;
		for (size_t x = 0; x < PRINTER_WIDTH; x++) {
			size_t tile = (y / 8u) * PRINTER_TILES_PER_ROW + x / 8u;
			size_t line = y % 8u;
			const uint8_t *data = tiles + tile * 16u + line * 2u;
			unsigned bit = 7u - (x % 8u);
			unsigned index = (unsigned)(((data[0] >> bit) & 1u) | (((data[1] >> bit) & 1u) << 1));
			unsigned shade = (palette >> (index * 2u)) & 3u;
			raw[y * stride + 1u + x] = grey[shade];
		}
	}
	FILE *file = fopen(path, "wb");
	if (!file)
		return -1;
	crc_init();
	static const uint8_t signature[8] = {0x89u, 'P', 'N', 'G', 0x0Du, 0x0Au, 0x1Au, 0x0Au};
	uint8_t header[13];
	put32(header, PRINTER_WIDTH);
	put32(header + 4, (uint32_t)height);
	header[8] = 8u;
	header[9] = 0u;
	header[10] = 0u;
	header[11] = 0u;
	header[12] = 0u;
	int ok = fwrite(signature, 1, 8, file) == 8 && write_chunk(file, "IHDR", header, 13) == 0;
	size_t blocks = (raw_size + 65534u) / 65535u;
	size_t deflate_size = 2u + raw_size + blocks * 5u + 4u;
	static uint8_t deflate[2u + sizeof raw + (sizeof raw / 65535u + 1u) * 5u + 4u];
	size_t cursor = 0;
	deflate[cursor++] = 0x78u;
	deflate[cursor++] = 0x01u;
	uint32_t a = 1u;
	uint32_t b = 0u;
	for (size_t i = 0; i < raw_size; i++) {
		a = (a + raw[i]) % 65521u;
		b = (b + a) % 65521u;
	}
	size_t offset = 0;
	for (size_t block = 0; block < blocks; block++) {
		size_t length = raw_size - offset > 65535u ? 65535u : raw_size - offset;
		deflate[cursor++] = block + 1u == blocks ? 1u : 0u;
		deflate[cursor++] = (uint8_t)length;
		deflate[cursor++] = (uint8_t)(length >> 8);
		deflate[cursor++] = (uint8_t)~length;
		deflate[cursor++] = (uint8_t)(~length >> 8);
		memcpy(deflate + cursor, raw + offset, length);
		cursor += length;
		offset += length;
	}
	put32(deflate + cursor, (b << 16) | a);
	cursor += 4;
	ok = ok && cursor == deflate_size && write_chunk(file, "IDAT", deflate, cursor) == 0
	     && write_chunk(file, "IEND", NULL, 0) == 0;
	if (fclose(file) != 0)
		ok = 0;
	return ok ? 0 : -1;
}
