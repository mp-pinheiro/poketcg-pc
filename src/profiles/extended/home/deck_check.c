/* >>> part includes */
#include "home/deck_check.h"

#include "generated/constants.h"
/* <<< part includes */
/* >>> part MENU_CONFIRM */
#define MENU_CONFIRM 0x01u
/* <<< part MENU_CONFIRM */
/* >>> part CURSOR_BLINK_PERIOD_MASK */
#define CURSOR_BLINK_PERIOD_MASK 0x0Fu
/* <<< part CURSOR_BLINK_PERIOD_MASK */
/* >>> part B_CURSOR_BLINK_PERIOD */
#define B_CURSOR_BLINK_PERIOD 4u
/* <<< part B_CURSOR_BLINK_PERIOD */
/* >>> part includes_tail */
#include "generated/wram.h"
#include "home/bg_map.h"
#include "home/random.h"
#include "home/sound.h"
/* <<< part includes_tail */
/* === factory HandleCheckMenuInput */
