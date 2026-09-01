#ifndef POKETCG_INDIRECT_DISPATCH_H
#define POKETCG_INDIRECT_DISPATCH_H

#include <stdint.h>

/* Dispatch a GB address held in a RAM function pointer. A zero target is the
 * asm's "no function registered" state and is ignored. Any other target not
 * handled by the caller's switch aborts with the site name, so whole-game
 * runs fail loudly instead of silently skipping per-frame work. */
void DispatchIndirect(const char *site, uint16_t target);

#endif
