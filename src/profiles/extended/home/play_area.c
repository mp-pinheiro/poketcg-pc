/* >>> part includes */
#include "home/play_area.h"

#include "generated/constants.h"
/* <<< part includes */
/* --- part includes_2 */
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
#include "generated/rom.h"
#include "generated/text_ids.h"
#include "generated/wram.h"
#include "home/objects.h"
#include "mem.h"
/* <<< part includes_tail */
/* >>> part includes_B_PAD_UP */
#include "home/duel.h"
#include "home/random.h"
#include "home/sound.h"
#include "home/deck_check.h"
#include "home/objects.h"
#include "home/play_area.h"
#include "generated/wram.h"
#include "generated/hram.h"
/* <<< part includes_B_PAD_UP */
/* >>> part EMPTY_LINE_TEXT */
#define EMPTY_LINE_TEXT EmptyLineText
/* <<< part EMPTY_LINE_TEXT */
/* >>> part HAND_TEXT_2 */
#define HAND_TEXT_2 HandText_2
/* <<< part HAND_TEXT_2 */
/* === factory OpenInPlayAreaScreen_HandleInput */
