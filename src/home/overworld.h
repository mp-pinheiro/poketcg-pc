#ifndef POKETCG_HOME_OVERWORLD_H
#define POKETCG_HOME_OVERWORLD_H

#include <stdint.h>

/* >>> factory Func_c6cc */
uint8_t Func_c6cc(uint8_t a);
/* <<< factory Func_c6cc */
/* >>> factory Func_c6d4 */
uint8_t Func_c6d4(uint8_t a);
/* <<< factory Func_c6d4 */
/* >>> factory Func_c6f7 */
uint8_t Func_c6f7(uint16_t *hl);
/* <<< factory Func_c6f7 */
/* >>> factory SetOverworldNPCFlags */
typedef struct {
	uint8_t a;
	uint8_t f;
} OverworldNPCFlagsResult;
OverworldNPCFlagsResult SetOverworldNPCFlags(uint8_t a);
/* <<< factory SetOverworldNPCFlags */
#endif /* POKETCG_HOME_OVERWORLD_H */
