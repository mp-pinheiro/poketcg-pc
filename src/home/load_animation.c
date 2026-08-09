#include "home/load_animation.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/objects.h"
#include "home/switch_rom.h"
#include "mem.h"

#define SPRITE_ANIM_BUFFER_CAPACITY 16u
#define SPRITE_ANIM_LENGTH 16u
#define SPRITE_ANIM_ENABLED 0u
#define SPRITE_ANIM_FLAGS 15u
#define SPRITE_ANIM_FLAG_CENTERED_F 2u
#define SPRITE_ANIM_FRAME_BANK 11u

#define OAM_PRIO    0x80u
#define OAM_YFLIP   0x40u
#define OAM_XFLIP   0x20u
#define OAM_PAL1    0x10u
#define OAM_PALETTE 0x07u

#define SPRITE_NULL_ANIMATION_POINTER_ADDR 0x4E5Au
#define SPRITE_NULL_ANIMATION_POINTER_BANK 0x20u

/* GB ADD/ADC/SUB/SBC, carry out included: load_animation.asm's edge-clipping
 * math depends on the exact 8-bit carry chain, not the mathematical result. */
static uint8_t gb_add(uint8_t a, uint8_t n, uint8_t *carry_out)
{
	unsigned r = (unsigned)a + n;
	*carry_out = (uint8_t)(r >> 8);
	return (uint8_t)r;
}

static uint8_t gb_adc(uint8_t a, uint8_t n, uint8_t carry_in, uint8_t *carry_out)
{
	unsigned r = (unsigned)a + n + carry_in;
	*carry_out = (uint8_t)(r >> 8);
	return (uint8_t)r;
}

static uint8_t gb_sub(uint8_t a, uint8_t n, uint8_t *carry_out)
{
	*carry_out = (uint8_t)(a < n);
	return (uint8_t)(a - n);
}

static uint8_t gb_sbc(uint8_t a, uint8_t n, uint8_t carry_in, uint8_t *carry_out)
{
	unsigned nn = (unsigned)n + carry_in;
	*carry_out = (uint8_t)(a < nn);
	return (uint8_t)((unsigned)a - nn);
}

uint16_t GetSpriteAnimBufferProperty_SpriteInA(uint8_t a, uint8_t c)
{
	if (a >= SPRITE_ANIM_BUFFER_CAPACITY)
		a = SPRITE_ANIM_BUFFER_CAPACITY - 1u;
	return (uint16_t)(wSpriteAnimBuffer_ADDR + (uint16_t)a * SPRITE_ANIM_LENGTH + c);
}

uint16_t GetSpriteAnimBufferProperty(uint8_t c)
{
	return GetSpriteAnimBufferProperty_SpriteInA(gb_read8(wWhichSprite_ADDR), c);
}

uint16_t GetFirstSpriteAnimBufferProperty(void)
{
	return GetSpriteAnimBufferProperty(SPRITE_ANIM_ENABLED);
}

void Func_3ddb(uint8_t a)
{
	uint16_t address = GetSpriteAnimBufferProperty_SpriteInA(a, SPRITE_ANIM_FLAGS);
	gb_write8(address, (uint8_t)(gb_read8(address) & (uint8_t)~(1u << SPRITE_ANIM_FLAG_CENTERED_F)));
}

void Func_3de7(uint8_t a)
{
	uint16_t address = GetSpriteAnimBufferProperty_SpriteInA(a, SPRITE_ANIM_FLAGS);
	gb_write8(address, (uint8_t)(gb_read8(address) | (uint8_t)(1u << SPRITE_ANIM_FLAG_CENTERED_F)));
}

void DrawSpriteAnimationFrame(uint16_t *hl_io)
{
	uint8_t saved = hBankROM;
	uint16_t hl = *hl_io;
	uint8_t count;

	BankswitchROM(wCurrSpriteFrameBank);

	wCurrSpriteRightEdgeCheck = (wCurrSpriteXPos >= 0xF0u) ? 0xFFu : 0x00u;
	wCurrSpriteBottomEdgeCheck = (wCurrSpriteYPos >= 0xF0u) ? 0xFFu : 0x00u;

	count = gb_read8(hl++);
	for (uint8_t remaining = count; remaining != 0; remaining--) {
		uint16_t rec = hl;
		uint8_t y_off = gb_read8(rec);
		uint8_t y_ext = (y_off & 0x80u) ? 0xFFu : 0x00u;
		uint8_t e_val, y_check, c1, c2;

		if (wCurrSpriteAttributes & OAM_YFLIP) {
			uint8_t low = gb_add(y_off, 8u, &c1);
			uint8_t hi = gb_adc(0u, y_ext, c1, &c2);
			e_val = gb_sub(wCurrSpriteYPos, low, &c1);
			y_check = gb_sbc(wCurrSpriteBottomEdgeCheck, hi, c1, &c2);
		} else {
			e_val = gb_add(wCurrSpriteYPos, y_off, &c1);
			y_check = gb_adc(wCurrSpriteBottomEdgeCheck, y_ext, c1, &c2);
		}

		if (y_check == 0) {
			uint16_t xrec = (uint16_t)(rec + 1u);
			uint8_t x_off = gb_read8(xrec);
			uint8_t x_ext = (x_off & 0x80u) ? 0xFFu : 0x00u;
			uint8_t d_val, x_check;

			if (wCurrSpriteAttributes & OAM_XFLIP) {
				uint8_t low = gb_add(x_off, 8u, &c1);
				uint8_t hi = gb_adc(0u, x_ext, c1, &c2);
				d_val = gb_sub(wCurrSpriteXPos, low, &c1);
				x_check = gb_sbc(wCurrSpriteRightEdgeCheck, hi, c1, &c2);
			} else {
				d_val = gb_add(wCurrSpriteXPos, x_off, &c1);
				x_check = gb_adc(wCurrSpriteRightEdgeCheck, x_ext, c1, &c2);
			}

			if (x_check == 0) {
				uint8_t tile_delta = gb_read8((uint16_t)(rec + 2u));
				uint8_t attr_delta = gb_read8((uint16_t)(rec + 3u));
				uint8_t attrs = wCurrSpriteAttributes;
				uint8_t c_val = (uint8_t)(wCurrSpriteTileID + tile_delta);
				uint8_t pal_bits = (uint8_t)(((unsigned)attrs + attr_delta) & (OAM_PALETTE | OAM_PAL1));
				uint8_t flip_bits = (uint8_t)((attrs ^ attr_delta) & (OAM_XFLIP | OAM_YFLIP | OAM_PRIO));
				uint8_t b_val = (uint8_t)(pal_bits | flip_bits);

				SetOneObjectAttributes(e_val, d_val, c_val, b_val);
			}
		}

		hl = (uint16_t)(rec + 4u);
	}

	*hl_io = hl;
	BankswitchROM(saved);
}

/* GetAnimationFramePointer:: poketcg/src/home/load_animation.asm:144-191. hl
 * is only ever a write base (`+SPRITE_ANIM_FRAME_BANK`); it is popped back
 * unchanged, never advanced. bc always ends up clobbered to the constant
 * SPRITE_ANIM_FRAME_BANK offset (never restored) and d/e end up holding
 * whichever table address was last dereferenced -- both are incidental to the
 * register allocation the asm happened to use, not part of the callable
 * contract, so CONTRACT leaves them out. */
void GetAnimationFramePointer(uint16_t hl)
{
	uint8_t saved = hBankROM;
	uint16_t de;
	uint8_t bank;

	if (wWhichAnimationFrame == 0xFFu) {
		de = SPRITE_NULL_ANIMATION_POINTER_ADDR;
		bank = 0;
	} else {
		uint16_t table = (uint16_t)(wTempPointer_PTR[0] | (uint16_t)wTempPointer_PTR[1] << 8);
		uint8_t table_byte0, frame, rotated, c1, c2, e_val, d_val;

		BankswitchROM(wTempPointerBank);
		table_byte0 = gb_read8(table++);
		frame = wWhichAnimationFrame;
		rotated = (uint8_t)((frame << 1) | (frame >> 7));
		e_val = gb_add(rotated, gb_read8(table), &c1);
		d_val = gb_adc(gb_read8((uint16_t)(table + 1u)), 0u, c1, &c2);
		de = (uint16_t)(d_val << 8 | e_val);
		bank = table_byte0;
	}
	bank = (uint8_t)(bank + SPRITE_NULL_ANIMATION_POINTER_BANK);

	uint16_t dst = (uint16_t)(hl + SPRITE_ANIM_FRAME_BANK);
	gb_write8(dst, bank);
	BankswitchROM(bank);
	gb_write8((uint16_t)(dst + 1u), gb_read8(de));
	gb_write8((uint16_t)(dst + 2u), gb_read8((uint16_t)(de + 1u)));

	BankswitchROM(saved);
}
