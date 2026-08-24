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
/* >>> factory IntroSequenceCmd_WaitSFX */
typedef struct { uint8_t a; uint8_t f; } IntroSequenceCmdWaitSFXResult;
IntroSequenceCmdWaitSFXResult IntroSequenceCmd_WaitSFX(void);
/* <<< factory IntroSequenceCmd_WaitSFX */
/* >>> factory IntroSequenceCmd_WaitOrbsAnimation */
typedef struct { uint8_t a; uint8_t f; } IntroSequenceCmdWaitOrbsAnimationResult;
IntroSequenceCmdWaitOrbsAnimationResult IntroSequenceCmd_WaitOrbsAnimation(void);
/* <<< factory IntroSequenceCmd_WaitOrbsAnimation */
/* >>> factory IntroSequenceCmd_SetOrbsAnimations */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } IntroSequenceCmdSetOrbsAnimationsResult;
IntroSequenceCmdSetOrbsAnimationsResult IntroSequenceCmd_SetOrbsAnimations(uint8_t b, uint8_t c);
/* <<< factory IntroSequenceCmd_SetOrbsAnimations */
/* >>> factory IntroSequenceCmd_SetOrbsCoordinates */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } IntroSequenceCmdSetOrbsCoordinatesResult;
IntroSequenceCmdSetOrbsCoordinatesResult IntroSequenceCmd_SetOrbsCoordinates(uint8_t b, uint8_t c);
/* <<< factory IntroSequenceCmd_SetOrbsCoordinates */
/* >>> factory IntroSequenceCmd_PlayTitleScreenMusic */
typedef struct { uint8_t a; uint8_t f; } IntroSequenceCmd_PlayTitleScreenMusicResult;
IntroSequenceCmd_PlayTitleScreenMusicResult IntroSequenceCmd_PlayTitleScreenMusic(void);
/* <<< factory IntroSequenceCmd_PlayTitleScreenMusic */
/* >>> factory IntroSequenceCmd_FadeOut */
typedef struct { uint8_t a; uint8_t f; } IntroSequenceCmd_FadeOutResult;
IntroSequenceCmd_FadeOutResult IntroSequenceCmd_FadeOut(void);
/* <<< factory IntroSequenceCmd_FadeOut */
/* >>> factory AdvanceIntroSequenceCmdPtrBy3 */
void AdvanceIntroSequenceCmdPtrBy3(void);
/* <<< factory AdvanceIntroSequenceCmdPtrBy3 */
#endif /* POKETCG_HOME_INTRO_SEQUENCE_COMMANDS_H */
