#ifndef POKETCG_HOME_NAMING_H
#define POKETCG_HOME_NAMING_H

#include <stdint.h>

/* >>> factory DisplayPlayerNamingScreen */
/* naming.asm:1-40. Result is the asm's exit state: a is the second
 * UpdateRNGSources output, f that call's inc-[hl] flags, and hl/de/bc the
 * restored source, destination and length of the sPlayerName copy. */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } DisplayPlayerNamingScreenResult;
DisplayPlayerNamingScreenResult DisplayPlayerNamingScreen(void);
/* <<< factory DisplayPlayerNamingScreen */
#endif /* POKETCG_HOME_NAMING_H */
