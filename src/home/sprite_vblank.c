#include "home/sprite_vblank.h"

#include "mem.h"
/* >>> factory statics */
#include "home/empty_screen.h"
#include "home/lcd.h"
#include "home/load_animation.h"
#include "home/process_text.h"
#include "home/core.h"

/* poketcg.sym bank 00: home HandleAllSpriteAnimations trampoline entry,
 * the address baked into wVBlankFunctionTrampoline by
 * SetSpriteAnimationsAsVBlankFunction. */
#define HANDLEALLSPRITEANIMATIONS_ADDR 0x3CB4u

#include "generated/wram.h"
/* <<< factory statics */

uint8_t BackupVBlankFunctionTrampoline(uint16_t *hl, uint16_t *de)
{
	const uint8_t first = gb_read8(*hl);
	*hl = (uint16_t)(*hl + 1u);
	gb_write8(*de, first);
	*de = (uint16_t)(*de + 1u);

	const uint8_t second = gb_read8(*hl);
	*hl = (uint16_t)(*hl - 1u);
	gb_write8(*de, second);
	return second;
}

/* >>> factory SetSpriteAnimationsAsVBlankFunction */
/* sprite_vblank.asm:1-17 */
void SetSpriteAnimationsAsVBlankFunction(void)
{
	EmptyScreen();
	Set_OBJ_8x8();
	ClearSpriteAnimations();
	SetupText(0x38u, 0x7Fu);

	uint16_t hl = (uint16_t)(wVBlankFunctionTrampoline_ADDR + 1u);
	uint16_t de = wVBlankFunctionTrampolineBackup_ADDR;
	BackupVBlankFunctionTrampoline(&hl, &de);

	gb_write8(hl, (uint8_t)(HANDLEALLSPRITEANIMATIONS_ADDR & 0xFFu));
	hl = (uint16_t)(hl + 1u);
	gb_write8(hl, (uint8_t)(HANDLEALLSPRITEANIMATIONS_ADDR >> 8));
}
/* <<< factory SetSpriteAnimationsAsVBlankFunction */

/* >>> factory RestoreVBlankFunction */
/* sprite_vblank.asm:19-26 */
void RestoreVBlankFunction(void)
{
	uint16_t hl = wVBlankFunctionTrampolineBackup_ADDR;
	uint16_t de = (uint16_t)(wVBlankFunctionTrampoline_ADDR + 1u);
	BackupVBlankFunctionTrampoline(&hl, &de);
	ClearSpriteAnimations();
	ZeroObjectPositionsAndToggleOAMCopy();
}
/* <<< factory RestoreVBlankFunction */
