#include "home/intro_sequence_commands.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/load_animation.h"
#include "home/random.h"
#include "home/sprite_animations.h"

#define CONSOLE_CGB                     0x02u
#define SPRITE_ANIM_215                 0xd7u
#define SPRITE_ANIM_216                 0xd8u
#define SPRITE_ANIM_ATTRIBUTES          0x01u
#define SPRITE_ANIM_COORD_X             0x02u
#define SPRITE_ANIM_FLAG_UNSKIPPABLE_F  0x07u
#define ORB_COUNTER_MASK                0x3fu
#define NUM_TITLE_SCREEN_ORBS           0x07u

/* intro_sequence_commands.asm:392-408 (.UpdateSpriteAttributes) */
static void UpdateSpriteAttributes(void)
{
	uint16_t de = wTitleScreenSprites_ADDR;
	for (uint8_t c = NUM_TITLE_SCREEN_ORBS; c != 0u; c--) {
		wWhichSprite = gb_read8(de);
		uint16_t hl = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
		uint8_t x = gb_read8(hl);
		hl--;
		if (x == 152u)
			gb_write8(hl, (uint8_t)(gb_read8(hl) & (uint8_t)~(1u << SPRITE_ANIM_FLAG_UNSKIPPABLE_F)));
		de = (uint16_t)(de + 1u);
	}
}

#include "generated/wram.h"
#include "mem.h"
/* <<< factory statics */

/* >>> factory AnimateRandomTitleScreenOrb */
/* intro_sequence_commands.asm:331-390 */
uint8_t AnimateRandomTitleScreenOrb(void)
{
	if (wConsole == CONSOLE_CGB)
		UpdateSpriteAttributes();
	uint8_t a = (uint8_t)(wTitleScreenOrbCounter & ORB_COUNTER_MASK);
	if (a != 0u)
		return a;

	do {
		uint8_t c = Random(NUM_TITLE_SCREEN_ORBS);
		wWhichSprite = gb_read8((uint16_t)(wTitleScreenSprites_ADDR + c));
		a = GetSpriteAnimCounter();
	} while (a != 0xffu);

	uint16_t hl = GetSpriteAnimBufferProperty(SPRITE_ANIM_ATTRIBUTES);
	if (wConsole == CONSOLE_CGB)
		gb_write8(hl, (uint8_t)(gb_read8(hl) | (uint8_t)(1u << SPRITE_ANIM_FLAG_UNSKIPPABLE_F)));
	hl++;
	gb_write8(hl, 248u);
	hl++;
	gb_write8(hl, 14u);
	a = (wConsole == CONSOLE_CGB) ? SPRITE_ANIM_216 : SPRITE_ANIM_215;
	StartSpriteAnimation(a);
	return a;
}
/* <<< factory AnimateRandomTitleScreenOrb */

/* >>> factory AdvanceIntroSequenceCmdPtr */
AdvanceIntroSequenceCmdPtrResult AdvanceIntroSequenceCmdPtr(uint8_t a)
{
	uint8_t low = gb_read8(wSequenceCmdPtr_ADDR);
	uint16_t low_sum = (uint16_t)a + (uint16_t)low;
	uint8_t carry = (uint8_t)(low_sum > 0xFFu);
	gb_write8(wSequenceCmdPtr_ADDR, (uint8_t)low_sum);
	uint8_t high_before = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));
	uint16_t high_sum = (uint16_t)high_before + (uint16_t)carry;
	uint8_t high = (uint8_t)high_sum;
	gb_write8((uint16_t)(wSequenceCmdPtr_ADDR + 1u), high);
	uint8_t f = (uint8_t)((high == 0u ? 0x80u : 0u) |
		((uint8_t)((high_before & 0x0Fu) + carry) > 0x0Fu ? 0x20u : 0u) |
		(high_sum > 0xFFu ? 0x10u : 0u));
	return (AdvanceIntroSequenceCmdPtrResult){high, f};
}
/* <<< factory AdvanceIntroSequenceCmdPtr */

/* >>> factory AdvanceIntroSequenceCmdPtrBy2 */
void AdvanceIntroSequenceCmdPtrBy2(void)
{
	AdvanceIntroSequenceCmdPtr(2u);
}
/* <<< factory AdvanceIntroSequenceCmdPtrBy2 */
