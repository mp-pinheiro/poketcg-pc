#ifndef POKETCG_HOME_COPY_CARD_NAME_H
#define POKETCG_HOME_COPY_CARD_NAME_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint16_t hl;
} CopyCardNameResult;

CopyCardNameResult _CopyCardNameAndLevel_HalfwidthText(void);

#endif /* POKETCG_HOME_COPY_CARD_NAME_H */
