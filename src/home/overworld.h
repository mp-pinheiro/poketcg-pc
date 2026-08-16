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
/* >>> factory Func_c158 */
uint8_t Func_c158(void);
/* <<< factory Func_c158 */
/* >>> factory Func_c184 */
void Func_c184(void);
/* <<< factory Func_c184 */
/* >>> factory WhiteOutDMGPals */
void WhiteOutDMGPals(void);
/* <<< factory WhiteOutDMGPals */
/* >>> factory Func_c1f8 */
void Func_c1f8(void);
/* <<< factory Func_c1f8 */
/* >>> factory BackupPlayerPosition */
void BackupPlayerPosition(void);
/* <<< factory BackupPlayerPosition */
/* >>> factory Func_c469 */
void Func_c469(void);
/* <<< factory Func_c469 */
/* >>> factory SetScreenScrollWram */
uint8_t SetScreenScrollWram(void);
/* <<< factory SetScreenScrollWram */
/* >>> factory SetScreenScroll */
void SetScreenScroll(void);
/* <<< factory SetScreenScroll */
/* >>> factory Func_c70d */
typedef struct {
	uint8_t a;
	uint8_t f;
} FuncC70dResult;

FuncC70dResult Func_c70d(void);
/* <<< factory Func_c70d */
#endif /* POKETCG_HOME_OVERWORLD_H */
