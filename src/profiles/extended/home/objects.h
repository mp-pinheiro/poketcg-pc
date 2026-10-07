#ifndef POKETCG_HOME_OBJECTS_H
#define POKETCG_HOME_OBJECTS_H

#include <stdint.h>

/* poketcg/src/home/objects.asm */

void SetOneObjectAttributes(uint8_t e, uint8_t d, uint8_t c, uint8_t b);
void ZeroObjectPositions(void);

typedef struct { uint16_t hl; uint8_t carry; } SetManyObjResult;
SetManyObjResult SetManyObjectsAttributes(uint16_t hl, uint8_t d, uint8_t e);

#endif /* POKETCG_HOME_OBJECTS_H */
