/* >>> part includes */
#include <stdint.h>
#include "home/card_id.h"
/* <<< part includes */
/* >>> factory LookForCardIDInPlayArea_Bank8 */
typedef struct { uint8_t a; uint8_t b; uint8_t f; } LookForCardIDInPlayAreaResult;
LookForCardIDInPlayAreaResult LookForCardIDInPlayArea_Bank8(CardId de, uint8_t b);
/* <<< factory LookForCardIDInPlayArea_Bank8 */
/* >>> factory CheckIfHasCardIDInHand */
typedef struct { uint8_t a; uint8_t f; } CheckIfHasCardIDInHandResult;
CheckIfHasCardIDInHandResult CheckIfHasCardIDInHand(CardId de);
/* <<< factory CheckIfHasCardIDInHand */
/* >>> factory LookForCardIDInLocation_Bank8 */
typedef struct { uint8_t a; uint8_t f; } LookForCardIDInLocationBank8Result;
LookForCardIDInLocationBank8Result LookForCardIDInLocation_Bank8(uint8_t location, CardId de);
/* <<< factory LookForCardIDInLocation_Bank8 */
/* >>> factory LookForCardIDInHandList_Bank8 */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } LookForCardIDInHandListResult;
LookForCardIDInHandListResult LookForCardIDInHandList_Bank8(CardId de);
/* <<< factory LookForCardIDInHandList_Bank8 */
/* >>> factory LookForCardIDInHandAndPlayArea */
typedef struct { uint8_t a; uint8_t f; } LookForCardIDInHandAndPlayAreaResult;
LookForCardIDInHandAndPlayAreaResult LookForCardIDInHandAndPlayArea(CardId de);
/* <<< factory LookForCardIDInHandAndPlayArea */
/* >>> factory LookForCardIDToTradeWithDifferentHandCard */
typedef struct { uint8_t a; uint8_t f; uint8_t e; uint8_t d; } LookForCardIDToTradeWithDifferentHandCardResult;
LookForCardIDToTradeWithDifferentHandCardResult LookForCardIDToTradeWithDifferentHandCard(CardId de, CardId bc);
/* <<< factory LookForCardIDToTradeWithDifferentHandCard */
/* >>> factory LookForCardIDInDeck_GivenCardIDInHand */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } LookForCardIDInDeck_GivenCardIDInHandResult;
LookForCardIDInDeck_GivenCardIDInHandResult LookForCardIDInDeck_GivenCardIDInHand(CardId de, CardId bc);
/* <<< factory LookForCardIDInDeck_GivenCardIDInHand */
/* >>> factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult;
LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(CardId de, CardId bc);
/* <<< factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */
/* --- factory PreparePrinterConnection */
/* --- factory PrintDeckConfiguration */
/* >>> factory ShowPromotionalCardScreen */
void ShowPromotionalCardScreen(CardId de);
/* <<< factory ShowPromotionalCardScreen */
/* --- factory RequestToPrintCard */
/* --- factory PrintCardList */
/* --- factory ReceiveCard */
/* --- factory ReceiveDeckConfiguration */
/* --- factory DoCardPop */
/* --- factory SendCard */
/* --- factory SendDeckConfiguration */
/* --- factory SetUpAndStartLinkDuel */
