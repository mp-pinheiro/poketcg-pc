#ifndef POKETCG_HOME_CARD_ID_H
#define POKETCG_HOME_CARD_ID_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part CardId */
typedef uint16_t CardId;
/* <<< part CardId */

/* >>> part CARD_ID_MAX */
#define CARD_ID_MAX ((CardId)0x01FFu)
#define CARD_ID_INVALID ((CardId)0x0200u)
/* <<< part CARD_ID_MAX */

#endif
