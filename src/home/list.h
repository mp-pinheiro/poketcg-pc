#ifndef POKETCG_HOME_LIST_H
#define POKETCG_HOME_LIST_H

#include <stdint.h>

/* poketcg/src/home/list.asm:2 — store `de` to wListPointer. Preserves a/b/c/d/e/hl
 * and the flags. */
void SetListPointer(uint16_t de);

/* poketcg/src/home/list.asm:34 — write `a` through wListPointer, then advance
 * wListPointer past it. Preserves a/b/c/d/e/hl and the flags. */
void SetNextElementOfList(uint8_t a);

#endif /* POKETCG_HOME_LIST_H */
