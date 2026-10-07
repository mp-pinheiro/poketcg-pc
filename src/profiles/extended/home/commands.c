/* >>> factory PrintDamageText */
/* commands.asm:277 */
PrintDamageTextResult PrintDamageText(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t saved_b = b;
	uint8_t saved_c = c;
	uint8_t saved_d = d;
	uint8_t saved_e = e;
	uint16_t saved_hl = hl;
	uint8_t attack_animation = gb_read8(wLoadedAttackAnimation_ADDR);
	if (attack_animation == ATK_ANIM_HEAL || attack_animation == ATK_ANIM_HEALING_WIND_PLAY_AREA)
		return (PrintDamageTextResult){saved_b, saved_c, saved_d, saved_e, saved_hl};

	LoadCardDataToBuffer1_FromCardID(card_id_read_at(wTempNonTurnDuelistCardID_ADDR));
	CopyCardNameAndLevelResult copied = CopyCardNameAndLevel(18u, b, c, d, e);
	gb_write8(copied.hl, TX_END);
	gb_write8(wTxRam2_ADDR, 0u);
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), 0u);
	uint16_t damage = (uint16_t)(gb_read8(wDamageAnimAmount_ADDR) |
		(uint16_t)gb_read8((uint16_t)(wDamageAnimAmount_ADDR + 1u)) << 8);
	uint16_t text = GetDamageText(damage);
	if (text != 0u)
		(void)DrawWideTextBox_PrintText(text);
	return (PrintDamageTextResult){saved_b, saved_c, saved_d, saved_e, saved_hl};
}
/* <<< factory PrintDamageText */
/* === factory AnimationCommand_AnimNormal */
/* === factory UpdateDuelAnimationScreen */
