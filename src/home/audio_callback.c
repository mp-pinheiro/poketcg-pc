#include "home/audio_callback.h"

#include "home/switch_rom.h"

/* audio_callback.asm:4-22. The banked callback executes in bank $3f and
 * returns through the local tail, which restores the normal audio bank $3d. */
void Bankswitch3dTo3f(void)
{
	BankswitchROM(0x3Fu);
	BankswitchROM(0x3Du);
}
