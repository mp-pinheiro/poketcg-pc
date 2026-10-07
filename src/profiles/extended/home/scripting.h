/* --- factory GetScriptArgs5AfterPointer */
/* >>> factory ScriptCommand_JumpIfCardInCollection */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
} JumpIfCardInCollectionResult;

JumpIfCardInCollectionResult ScriptCommand_JumpIfCardInCollection(uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_JumpIfCardInCollection */
/* >>> factory ScriptCommand_GiveCard */
IncreaseScriptPointerResult ScriptCommand_GiveCard(uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_GiveCard */
/* >>> factory ScriptCommand_TakeCard */
IncreaseScriptPointerResult ScriptCommand_TakeCard(uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_TakeCard */
/* >>> factory ScriptCommand_SetSpriteAttributes */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t c;
} SetSpriteAttributesResult;

SetSpriteAttributesResult ScriptCommand_SetSpriteAttributes(uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_SetSpriteAttributes */
/* --- factory ScriptCommand_BattleCenter */
/* >>> factory SetNextScript */
uint16_t SetNextScript(uint8_t a, uint16_t bc);
/* <<< factory SetNextScript */
/* === factory ScriptCommand_JumpIfEnoughCardsOwned */
/* >>> part ScriptCommand_RemoveAllEnergyCardsResult */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
} ScriptCommand_RemoveAllEnergyCardsResult;
/* <<< part ScriptCommand_RemoveAllEnergyCardsResult */
/* >>> factory ScriptCommand_RemoveAllEnergyCardsFromCollection */
ScriptCommand_RemoveAllEnergyCardsResult ScriptCommand_RemoveAllEnergyCardsFromCollection(uint8_t b);
/* <<< factory ScriptCommand_RemoveAllEnergyCardsFromCollection */
/* >>> factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
} ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult;

ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult ScriptCommand_JumpIfAnyEnergyCardsInCollection(void);
/* <<< factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */
/* --- factory Func_c998 */
/* --- factory ScriptCommand_GiftCenter */
/* >>> factory ScriptCommand_ShowCardReceivedScreen */
/* scripting.asm:990. c on entry is the script argument that selects the card;
 * the routine tail-jumps to IncreaseScriptPointerBy2, so the shared
 * IncreaseScriptPointerResult (a, f, c) is the exit contract. b/d/e/hl are not
 * reported: the promotional card screen does not carry them out. */
IncreaseScriptPointerResult ScriptCommand_ShowCardReceivedScreen(uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_ShowCardReceivedScreen */
/* --- factory Script_GiftCenterClerk */
