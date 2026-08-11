#ifndef HOME_CREDITS_SEQUENCE_COMMANDS_H
#define HOME_CREDITS_SEQUENCE_COMMANDS_H

#include <stdint.h>

void SetCreditsSequenceCmdPtr(void);
void ExecuteCreditsSequenceCmd(void);
void AdvanceCreditsSequenceCmdPtr(uint8_t a);

#endif
