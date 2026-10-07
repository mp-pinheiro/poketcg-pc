/* >>> factory Func_1d705 */
void Func_1d705(void)
{
	DisableLCD();
	wd317 = 0u;
	EnableAndClearSpriteAnimations();
	(void)InitMenuScreen();
	Func_1d7ee();
	(void)SetDoFrameFunction(FUNC_3E31);

	wd647 = 0x91u;
	wd649 = 0x91u;
	wd648 = 0x01u;
	wd64a = 0x01u;
	Func_1d765();
	SetWindowOn();

	wd657 = 0x00u;
	gb_write8(wLCDCFunctionTrampoline_ADDR + 1u, (uint8_t)FUNC_3E44);
	gb_write8(wLCDCFunctionTrampoline_ADDR + 2u, (uint8_t)(FUNC_3E44 >> 8));
	gb_write8(R_STAT, (uint8_t)(gb_read8(R_STAT) | STAT_LYC_MASK));
	gb_write8(R_LYC, 0x00u);
	gb_write8(R_IE, (uint8_t)(gb_read8(R_IE) | IE_STAT_MASK));
}

/* <<< factory Func_1d705 */
