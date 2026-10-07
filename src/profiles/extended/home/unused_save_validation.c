/* >>> part includes */
#include "home/unused_save_validation.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> factory statics */
#include "generated/sram.h"

#define RRAMG_ADDR             0x0000u
#define RAMG_SRAM_ENABLE       0x0Au
#define SAVE_VALIDATION_RANGE  0x250u

#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/credits_sequence_commands.h"
#include "home/duel_core.h"
#include "home/input.h"
#include "home/process_text.h"
#include "home/tiles.h"
#include "mem.h"
/* <<< factory statics */

