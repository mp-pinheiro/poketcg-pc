/* >>> part includes_2 */
#include "home/switch_rom.h"
#include "home/time.h"
#include "home/music.h"
#include "generated/wram.h"
#include "generated/hram.h"
/* <<< part includes_2 */
/* >>> part BANK_SOUND_TIMER_HANDLER */
#define BANK_SOUND_TIMER_HANDLER 0x42u
/* <<< part BANK_SOUND_TIMER_HANDLER */
/* >>> factory TimerHandler */
void TimerHandler(void)
{
	uint8_t counter = wTimerCounter;
	wTimerCounter = (uint8_t)(counter + 1u);
	if ((counter & 0x3u) != 0u)
		return;
	IncrementPlayTimeCounter();
	if ((wReentrancyFlag & (1u << IN_TIMER)) != 0u)
		return;
	wReentrancyFlag = (uint8_t)(wReentrancyFlag | (1u << IN_TIMER));
	uint8_t saved_bank = hBankROM;
	BankswitchROM(BANK_SOUND_TIMER_HANDLER);
	SoundTimerHandler();
	BankswitchROM(saved_bank);
	wReentrancyFlag = (uint8_t)(wReentrancyFlag & (uint8_t)~(1u << IN_TIMER));
}
/* <<< factory TimerHandler */
/* === factory SwitchToCGBDoubleSpeed */
/* === factory SwitchToCGBNormalSpeed */
