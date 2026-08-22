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
#endif /* POKETCG_HOME_INTRO_SEQUENCE_COMMANDS_H */
