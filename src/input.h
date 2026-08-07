#ifndef POKETCG_INPUT_H
#define POKETCG_INPUT_H

#include <stdint.h>

/* Joypad bits in the order the DMG/CGB P1 register exposes them: the low nibble is
 * the direction row and the high nibble the button row. Held low when pressed on
 * hardware; this struct stores them active-high and joypad_p1() does the inversion. */
enum {
	BTN_RIGHT = 1 << 0,
	BTN_LEFT = 1 << 1,
	BTN_UP = 1 << 2,
	BTN_DOWN = 1 << 3,
	BTN_A = 1 << 4,
	BTN_B = 1 << 5,
	BTN_SELECT = 1 << 6,
	BTN_START = 1 << 7,
};

/* One frame of input. Recording and replay are streams of these, so the on-disk
 * format is fixed by this type. */
typedef struct {
	uint8_t buttons;
} InputFrame;

/* Resolve P1 ($FF00) for the currently held buttons against the select bits the game
 * wrote. Bits 4/5 select which row is readable; a selected-and-pressed bit reads 0. */
uint8_t joypad_p1(uint8_t held, uint8_t select_bits);

#endif /* POKETCG_INPUT_H */
