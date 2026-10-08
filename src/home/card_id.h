#ifndef POKETCG_HOME_CARD_ID_H
#define POKETCG_HOME_CARD_ID_H

/* >>> part includes */
#include <stdint.h>
#include "generated/profile_features.h"
/* <<< part includes */
/* >>> part CardId */

typedef PROFILE_CARD_ID_TYPE CardId;
/* <<< part CardId */

/* >>> part CARD_ID_MAX */
#define CARD_ID_MAX ((CardId)(PROFILE_FEATURE_NINE_BIT_CARD_IDS ? 0x01FFu : 0x00FFu))
/* <<< part CARD_ID_MAX */
/* >>> part CARD_ID_INVALID */
#define CARD_ID_INVALID ((CardId)(PROFILE_FEATURE_NINE_BIT_CARD_IDS ? 0x0200u : 0x00FFu))
/* <<< part CARD_ID_INVALID */

#endif
