#ifndef POKETCG_HOME_OBJECTS_H
#define POKETCG_HOME_OBJECTS_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory SetOneObjectAttributes */
/* poketcg/src/home/objects.asm */

void SetOneObjectAttributes(uint8_t e, uint8_t d, uint8_t c, uint8_t b);
/* <<< factory SetOneObjectAttributes */
/* >>> factory ZeroObjectPositions */
void ZeroObjectPositions(void);
/* <<< factory ZeroObjectPositions */

/* >>> part SetManyObjResult */
typedef struct { uint16_t hl; uint8_t carry; } SetManyObjResult;
/* <<< part SetManyObjResult */
/* >>> part SetManyObjectsAttributes */
SetManyObjResult SetManyObjectsAttributes(uint16_t hl, uint8_t d, uint8_t e);
/* <<< part SetManyObjectsAttributes */

#endif /* POKETCG_HOME_OBJECTS_H */
