#ifndef POKETCG_HOME_INTRO_SEQUENCE_COMMANDS_H
#define POKETCG_HOME_INTRO_SEQUENCE_COMMANDS_H

#include <stdint.h>

/* >>> factory AnimateRandomTitleScreenOrb */
uint8_t AnimateRandomTitleScreenOrb(void);
/* <<< factory AnimateRandomTitleScreenOrb */
/* >>> factory AdvanceIntroSequenceCmdPtr */
typedef struct {
	uint8_t a;
	uint8_t f;
} AdvanceIntroSequenceCmdPtrResult;

AdvanceIntroSequenceCmdPtrResult AdvanceIntroSequenceCmdPtr(uint8_t a);
/* <<< factory AdvanceIntroSequenceCmdPtr */
/* >>> factory AdvanceIntroSequenceCmdPtrBy2 */
void AdvanceIntroSequenceCmdPtrBy2(void);
/* <<< factory AdvanceIntroSequenceCmdPtrBy2 */
/* >>> factory AdvanceIntroSequenceCmdPtrBy4 */
void AdvanceIntroSequenceCmdPtrBy4(void);
/* <<< factory AdvanceIntroSequenceCmdPtrBy4 */
/* >>> factory IntroSequenceEmptyFunc */
void IntroSequenceEmptyFunc(void);
/* <<< factory IntroSequenceEmptyFunc */
/* >>> factory IntroSequenceCmd_FadeIn */
typedef struct { uint8_t a; uint8_t f; } IntroSequenceCmd_FadeInResult;
IntroSequenceCmd_FadeInResult IntroSequenceCmd_FadeIn(void);
/* <<< factory IntroSequenceCmd_FadeIn */
#endif /* POKETCG_HOME_INTRO_SEQUENCE_COMMANDS_H */
