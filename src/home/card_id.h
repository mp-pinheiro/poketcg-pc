#ifndef POKETCG_HOME_CARD_ID_H
#define POKETCG_HOME_CARD_ID_H

#include <stdint.h>

typedef uint16_t CardId;

#define CARD_ID_MAX ((CardId)0x01FFu)
#define CARD_ID_INVALID ((CardId)0x0200u)

#endif
