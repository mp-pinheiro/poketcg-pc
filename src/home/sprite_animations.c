/* >>> part includes */
#include "home/sprite_animations.h"
#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/rom.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/copy.h"
#include "home/memory.h"
#include "home/load_animation.h"
#include "home/load_gfx.h"
#include "home/objects.h"
#include "home/switch_sram.h"
#include "home/switch_rom.h"
#include "mem.h"
/* <<< part includes */
/* >>> part SLOT_COUNT */
#define SLOT_COUNT 16u
/* <<< part SLOT_COUNT */
/* >>> part SLOT_SIZE */
#define SLOT_SIZE 16u
/* <<< part SLOT_SIZE */
/* >>> part CACHE_SIZE_BYTES */
#define CACHE_SIZE_BYTES 64u
/* <<< part CACHE_SIZE_BYTES */
/* >>> part ANIM_COUNTER */
#define ANIM_COUNTER 14u
/* <<< part ANIM_COUNTER */
/* >>> part ANIM_ID */
#define ANIM_ID 5u
/* <<< part ANIM_ID */
/* >>> part ANIM_BANK */
#define ANIM_BANK 6u
/* <<< part ANIM_BANK */
/* >>> part ANIM_POINTER */
#define ANIM_POINTER 7u
/* <<< part ANIM_POINTER */
/* >>> part ANIM_FRAME_POINTER */
#define ANIM_FRAME_POINTER 9u
/* <<< part ANIM_FRAME_POINTER */
/* >>> part ANIM_COORD_X */
#define ANIM_COORD_X 2u
/* <<< part ANIM_COORD_X */
/* >>> part ANIM_COORD_Y */
#define ANIM_COORD_Y 3u
/* <<< part ANIM_COORD_Y */
/* >>> part ANIM_FLAGS */
#define ANIM_FLAGS 15u
/* <<< part ANIM_FLAGS */
/* >>> part FLAG_CENTERED */
#define FLAG_CENTERED 2u
/* <<< part FLAG_CENTERED */
/* >>> part FLAG_X_INVERTED */
#define FLAG_X_INVERTED 0u
/* <<< part FLAG_X_INVERTED */
/* >>> part FLAG_Y_INVERTED */
#define FLAG_Y_INVERTED 1u
/* <<< part FLAG_Y_INVERTED */
/* >>> part FLAG_UNSKIPPABLE */
#define FLAG_UNSKIPPABLE 7u
/* <<< part FLAG_UNSKIPPABLE */

/* >>> part slot_addr */
static uint16_t slot_addr(uint8_t slot, uint8_t field)
{
	if (slot >= SLOT_COUNT)
		slot = SLOT_COUNT - 1u;
	return (uint16_t)(wSpriteAnimBuffer_ADDR + (uint16_t)slot * SLOT_SIZE + field);
}
/* <<< part slot_addr */

/* >>> part state16 */
static uint16_t state16(uint16_t addr)
{
	return (uint16_t)(gb_read8(addr) | ((uint16_t)gb_read8((uint16_t)(addr + 1u)) << 8));
}
/* <<< part state16 */

/* >>> part put16 */
static void put16(uint16_t addr, uint16_t value)
{
	gb_write8(addr, (uint8_t)value);
	gb_write8((uint16_t)(addr + 1u), (uint8_t)(value >> 8));
}
/* <<< part put16 */

/* >>> factory _ClearSpriteAnimations */
void _ClearSpriteAnimations(void)
{
	if (wAllSpriteAnimationsDisabled)
		return;
	wWhichSprite = 0;
	for (uint8_t i = 0; i < SLOT_COUNT; i++) {
		gb_write8(slot_addr(i, 0), 0);
		wWhichSprite++;
	}
	ClearSpriteVRAMBuffer();
	ZeroObjectPositions();
	wVBlankOAMCopyToggle++;
}
/* <<< factory _ClearSpriteAnimations */

/* >>> factory CreateSpriteAndAnimBufferEntry */
uint8_t CreateSpriteAndAnimBufferEntry(uint8_t a, uint8_t f)
{
	if (wAllSpriteAnimationsDisabled)
		return f;
	SpriteAnimLookupResult result = Func_12c05(a);
	wCurrSpriteTileID = result.a;
	wWhichSprite = 0;
	for (uint8_t i = 0; i < SLOT_COUNT; i++) {
		wWhichSprite = i;
		if (gb_read8(slot_addr(i, 0)) == 0) {
			gb_write8(slot_addr(i, 0), 1);
			FillNewSpriteAnimBufferEntry(slot_addr(i, 0));
			return 0;
		}
	}
	return 0x90;
}
/* <<< factory CreateSpriteAndAnimBufferEntry */

/* >>> factory FillNewSpriteAnimBufferEntry */
void FillNewSpriteAnimBufferEntry(uint16_t hl)
{
	for (uint8_t i = 1; i < SLOT_SIZE; i++)
		gb_write8((uint16_t)(hl + i), 0);
	gb_write8((uint16_t)(hl + 4u), wCurrSpriteTileID);
	gb_write8((uint16_t)(hl + 5u), 0xff);
	gb_write8((uint16_t)(hl + 14u), 0xff);
}
/* <<< factory FillNewSpriteAnimBufferEntry */

/* >>> factory DisableCurSpriteAnim */
void DisableCurSpriteAnim(void)
{
	DisableSpriteAnim(wWhichSprite);
}
/* <<< factory DisableCurSpriteAnim */

/* >>> factory DisableSpriteAnim */
void DisableSpriteAnim(uint8_t a)
{
	if (!wAllSpriteAnimationsDisabled)
		gb_write8(slot_addr(a, 0), 0);
}
/* <<< factory DisableSpriteAnim */

/* >>> factory GetSpriteAnimCounter */
uint8_t GetSpriteAnimCounter(void)
{
	return gb_read8(slot_addr(wWhichSprite, ANIM_COUNTER));
}
/* <<< factory GetSpriteAnimCounter */

/* >>> factory _HandleAllSpriteAnimations */
void _HandleAllSpriteAnimations(void)
{
	if (wAllSpriteAnimationsDisabled)
		return;
	ZeroObjectPositions();
	wWhichSprite = 0;
	for (uint8_t i = 0; i < SLOT_COUNT; i++) {
		uint16_t slot = slot_addr(i, 0);
		wWhichSprite = i;
		if (gb_read8(slot) != 0) {
			TryHandleSpriteAnimationFrame(slot);
			LoadSpriteDataForAnimationFrame(slot);
		}
	}
	wWhichSprite = SLOT_COUNT;
	wVBlankOAMCopyToggle++;
}
/* <<< factory _HandleAllSpriteAnimations */

/* >>> factory LoadSpriteDataForAnimationFrame */
void LoadSpriteDataForAnimationFrame(uint16_t hl)
{
	wCurrSpriteAttributes = gb_read8((uint16_t)(hl + 1u));
	wCurrSpriteXPos = gb_read8((uint16_t)(hl + 2u));
	wCurrSpriteYPos = gb_read8((uint16_t)(hl + 3u));
	wCurrSpriteTileID = gb_read8((uint16_t)(hl + 4u));
	if ((gb_read8((uint16_t)(hl + 15u)) & (1u << FLAG_UNSKIPPABLE)) != 0)
		return;
	wCurrSpriteFrameBank = gb_read8((uint16_t)(hl + 11u));
	if (wCurrSpriteFrameBank == 0)
		return;
	uint16_t frame = state16((uint16_t)(hl + 12u));
	DrawSpriteAnimationFrame(&frame);
}
/* <<< factory LoadSpriteDataForAnimationFrame */

/* >>> factory TryHandleSpriteAnimationFrame */
void TryHandleSpriteAnimationFrame(uint16_t hl)
{
	uint8_t flags = gb_read8((uint16_t)(hl + ANIM_FLAGS));
	uint8_t counter = gb_read8((uint16_t)(hl + ANIM_COUNTER));
	if (counter == 0xff)
		return;
	uint8_t decrement = (flags & (1u << FLAG_CENTERED)) ? 2u : 1u;
	counter = (uint8_t)(counter - decrement);
	gb_write8((uint16_t)(hl + ANIM_COUNTER), counter);
	if (counter == 0 || counter > (uint8_t)(0xffu - decrement))
		(void)HandleAnimationFrame(hl);
}
/* <<< factory TryHandleSpriteAnimationFrame */

/* >>> factory StartNewSpriteAnimation */
void StartNewSpriteAnimation(uint8_t a)
{
	uint16_t id = GetSpriteAnimBufferProperty(ANIM_ID);
	if (gb_read8(id) == a)
		return;
	StartSpriteAnimation(a);
}
/* <<< factory StartNewSpriteAnimation */

/* >>> factory StartSpriteAnimation */
uint8_t StartSpriteAnimation(uint8_t a)
{
	uint16_t slot = LoadSpriteAnimPointers(a);
	return HandleAnimationFrame(slot);
}
/* <<< factory StartSpriteAnimation */

/* >>> factory Func_12ac9 */
void Func_12ac9(uint8_t a, uint8_t c)
{
	if (c == 0) {
		StartSpriteAnimation(a);
		return;
	}
	uint16_t slot = LoadSpriteAnimPointers(a);
	GetAnimFramePointerFromOffset(0xff, slot);
	SetAnimationCounterAndLoop(c, slot);
}
/* <<< factory Func_12ac9 */

/* >>> factory LoadSpriteAnimPointers */
uint16_t LoadSpriteAnimPointers(uint8_t a)
{
	uint16_t slot = GetFirstSpriteAnimBufferProperty();
	gb_write8((uint16_t)(slot + ANIM_ID), a);
	MapDataPointerResult map = GetMapDataPointer(a, GFXTABLE_SPRITE_ANIMATIONS);
	uint16_t table = map.hl;
	LoadGraphicsPointerFromHL(&table);
	uint16_t pointer = state16(wTempPointer_ADDR);
	gb_write8((uint16_t)(slot + ANIM_BANK), wTempPointerBank);
	put16((uint16_t)(slot + ANIM_POINTER), pointer);
	put16((uint16_t)(slot + ANIM_FRAME_POINTER), (uint16_t)(pointer + 3u));
	return slot;
}
/* <<< factory LoadSpriteAnimPointers */

/* >>> factory HandleAnimationFrame */
uint8_t HandleAnimationFrame(uint16_t hl)
{
	for (;;) {
		uint16_t frame_ptr_addr = (uint16_t)(hl + ANIM_FRAME_POINTER);
		uint16_t frame_ptr = state16(frame_ptr_addr);
		gb_write8(wTempPointer_ADDR, (uint8_t)frame_ptr);
		gb_write8((uint16_t)(wTempPointer_ADDR + 1u), (uint8_t)(frame_ptr >> 8));
		wTempPointerBank = gb_read8((uint16_t)(hl + ANIM_BANK));
		put16(frame_ptr_addr, (uint16_t)(frame_ptr + 4u));
		CopyBankedDataToDE(4u, wLoadedFrameData_ADDR);
		GetAnimFramePointerFromOffset(gb_read8(wLoadedFrameData_ADDR), hl);
		uint8_t counter = gb_read8((uint16_t)(wLoadedFrameData_ADDR + 1u));
		uint8_t flags = gb_read8((uint16_t)(hl + ANIM_FLAGS));
		uint8_t frame_flags = SetAnimationCounterAndLoop(counter, hl);
		if (frame_flags & 0x10u)
			continue;
		uint8_t x = gb_read8((uint16_t)(wLoadedFrameData_ADDR + 2u));
		uint8_t y = gb_read8((uint16_t)(wLoadedFrameData_ADDR + 3u));
		if (flags & (1u << FLAG_X_INVERTED))
			x = (uint8_t)(0u - x);
		if (flags & (1u << FLAG_Y_INVERTED))
			y = (uint8_t)(0u - y);
		uint16_t xaddr = (uint16_t)(hl + ANIM_COORD_X);
		gb_write8(xaddr, (uint8_t)(gb_read8(xaddr) + x));
		uint16_t yaddr = (uint16_t)(hl + ANIM_COORD_Y);
		uint8_t out = (uint8_t)(gb_read8(yaddr) + y);
		gb_write8(yaddr, out);
		return out;
	}
}
/* <<< factory HandleAnimationFrame */

/* >>> factory GetAnimFramePointerFromOffset */
void GetAnimFramePointerFromOffset(uint8_t a, uint16_t hl)
{
	wWhichAnimationFrame = a;
	wTempPointerBank = gb_read8((uint16_t)(hl + ANIM_BANK));
	gb_write8(wTempPointer_ADDR, gb_read8((uint16_t)(hl + ANIM_POINTER)));
	gb_write8((uint16_t)(wTempPointer_ADDR + 1u),
	          gb_read8((uint16_t)(hl + ANIM_POINTER + 1u)));
	GetAnimationFramePointer(hl);
}
/* <<< factory GetAnimFramePointerFromOffset */

/* >>> factory SetAnimationCounterAndLoop */
uint8_t SetAnimationCounterAndLoop(uint8_t a, uint16_t hl)
{
	gb_write8((uint16_t)(hl + ANIM_COUNTER), a);
	if (a != 0)
		return 0;
	uint16_t base = state16((uint16_t)(hl + ANIM_POINTER));
	uint16_t pointer = (uint16_t)(base + 3u);
	put16((uint16_t)(hl + ANIM_FRAME_POINTER), pointer);
	return (uint8_t)((pointer >> 8) == 0 ? 0x90u : 0x10u);
}
/* <<< factory SetAnimationCounterAndLoop */

/* >>> factory Func_12ba7 */
void Func_12ba7(void)
{
	uint16_t src = wSpriteAnimBuffer_ADDR;
	uint16_t dst = sGeneralSaveDataEnd_ADDR;
	EnableSRAM();
	CopyDataHLtoDE(&src, &dst, 0x100u);
	src = wSpriteVRAMBuffer_ADDR;
	CopyDataHLtoDE(&src, &dst, 0x40u);
	gb_write8(dst, wSpriteVRAMBufferSize);
	DisableSRAM();
}
/* <<< factory Func_12ba7 */

/* >>> factory Func_12bcd */
void Func_12bcd(void)
{
	uint16_t src = sGeneralSaveDataEnd_ADDR;
	uint16_t dst = wSpriteAnimBuffer_ADDR;
	EnableSRAM();
	CopyDataHLtoDE(&src, &dst, 0x100u);
	src = (uint16_t)(sGeneralSaveDataEnd_ADDR + 0x100u);
	dst = wSpriteVRAMBuffer_ADDR;
	CopyDataHLtoDE(&src, &dst, 0x40u);
	wSpriteVRAMBufferSize = gb_read8(src);
	DisableSRAM();
}
/* <<< factory Func_12bcd */

/* >>> factory ClearSpriteVRAMBuffer */
void ClearSpriteVRAMBuffer(void)
{
	wSpriteVRAMBufferSize = 0;
	for (uint8_t i = 0; i < CACHE_SIZE_BYTES; i++)
		gb_write8((uint16_t)(wSpriteVRAMBuffer_ADDR + i), 0);
}
/* <<< factory ClearSpriteVRAMBuffer */

/* >>> factory Func_12c05 */
SpriteAnimLookupResult Func_12c05(uint8_t a)
{
	SpriteAnimLookupResult result = {0, 0x90};
	uint8_t count = wSpriteVRAMBufferSize;
	uint8_t offset = 0;
	uint16_t entry = wSpriteVRAMBuffer_ADDR;
	for (uint16_t i = 0; i < count; i++) {
		if (gb_read8((uint16_t)(entry + 1u)) == a) {
			gb_write8(entry, (uint8_t)(gb_read8(entry) + 1u));
			uint8_t size = gb_read8((uint16_t)(entry + 3u));
			uint8_t end = (uint8_t)(offset + size);
			if (end >= 0x81u)
				return result;
			result.a = offset;
			result.f = offset ? 0 : 0x80;
			return result;
		}
		offset = (uint8_t)(offset + gb_read8((uint16_t)(entry + 3u)));
		entry = (uint16_t)(entry + 4u);
	}
	if (count >= SLOT_COUNT)
		return result;
	entry = (uint16_t)(wSpriteVRAMBuffer_ADDR + (uint16_t)count * 4u);
	gb_write8((uint16_t)(entry + 1u), a);
	uint8_t size = Func_12c4f(a, offset);
	gb_write8((uint16_t)(entry + 2u), offset);
	gb_write8((uint16_t)(entry + 3u), size);
	gb_write8(entry, (uint8_t)(gb_read8(entry) + 1u));
	wSpriteVRAMBufferSize = (uint8_t)(count + 1u);
	if ((uint8_t)(offset + size) >= 0x81u)
		return result;
	result.a = offset;
	result.f = offset ? 0 : 0x80;
	return result;
}
/* <<< factory Func_12c05 */

/* >>> factory Func_12c4f */
uint8_t Func_12c4f(uint8_t a, uint8_t d)
{
	wWhichVRAMBank = 0;
	wVRAMTileOffset = d;
	uint8_t saved = hBankROM;
	BankswitchROM(LoadSpriteGfx_BANK);
	uint8_t result = LoadSpriteGfx(a);
	BankswitchROM(saved);
	return result;
}
/* <<< factory Func_12c4f */

/* >>> factory Func_12c5e */
void Func_12c5e(void)
{
	for (uint8_t i = 0; i < SLOT_COUNT; i++) {
		uint16_t entry = (uint16_t)(wSpriteVRAMBuffer_ADDR + (uint16_t)i * 4u);
		if (gb_read8(entry) != 0)
			Func_12c4f(gb_read8((uint16_t)(entry + 1u)), gb_read8((uint16_t)(entry + 2u)));
	}
}
/* <<< factory Func_12c5e */
