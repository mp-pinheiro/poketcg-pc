#ifndef POKETCG_DIGEST_H
#define POKETCG_DIGEST_H

#include <stdint.h>
#include <stdio.h>

/* Per-DoFrame state digest, the native half of the session comparator
 * (tools/completion/session.py). At every DoFrame anchor the four regions the
 * game reads back -- WRAM, HRAM, OAM and both VRAM banks -- are copied, the
 * masked bytes zeroed, and each CRC-32'd (zlib's polynomial, so Python's
 * zlib.crc32 over the same masked bytes is the reference side). One record
 * per ordinal: four little-endian uint32 in that order.
 *
 * The mask file is one range per line, `<region> <start> <end>` with end
 * exclusive and numbers in C syntax (0x... or decimal); regions are wram, hram,
 * oam and vram (0x4000, bank 0 then bank 1). Blank lines and lines opening
 * with # are ignored. It is written by session.py from the scenario ledger,
 * so both lanes zero exactly the same bytes. */
int digest_open(const char *sink_path, const char *mask_path);
void digest_anchor(uint32_t ordinal);
int digest_close(void);

#endif
