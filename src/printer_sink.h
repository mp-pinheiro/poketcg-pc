#ifndef POKETCG_PRINTER_SINK_H
#define POKETCG_PRINTER_SINK_H

#include <stddef.h>
#include <stdint.h>

void printer_attach(const char *directory);
int printer_attached(void);
void printer_reset(void);
void printer_serial_byte(uint8_t value);
uint8_t printer_device_byte(void);
uint8_t printer_status_byte(void);
size_t printer_pages(void);
size_t printer_band_bytes(void);
const uint8_t *printer_band_data(void);
const char *printer_last_path(void);
int printer_write_png(const char *path, const uint8_t *tiles, size_t tile_bytes, uint8_t palette);

#endif
