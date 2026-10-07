/* >>> part includes */
#include "home/ishiharas_house.h"

#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "home/scripting.h"
/* <<< part includes_2 */
/* >>> part TRUE */
#define TRUE 0x01u
/* <<< part TRUE */

/* >>> part cp_flags */
static uint8_t cp_flags(uint8_t a, uint8_t n)
{
	return (uint8_t)(0x40u | ((a == n) ? 0x80u : 0u)
		| (((a & 0x0Fu) < (n & 0x0Fu)) ? 0x20u : 0u)
		| ((a < n) ? 0x10u : 0u));
}
/* <<< part cp_flags */

/* >>> part ccf_cp_flags */
static uint8_t ccf_cp_flags(uint8_t a, uint8_t n)
{
	uint8_t f = cp_flags(a, n);
	return (uint8_t)((f & 0x80u) | ((f & 0x10u) ? 0u : 0x10u));
}
/* <<< part ccf_cp_flags */

/* >>> factory Preload_NikkiInIshiharasHouse */
PreloadNikkiInIshiharasHouseResult Preload_NikkiInIshiharasHouse(void)
{
	uint8_t a = GetEventValue(0x35u);
	uint8_t f = (a == NIKKI_IN_ISHIHARAS_HOUSE) ? 0x90u : ((a == 0u) ? 0x80u : 0u);
	return (PreloadNikkiInIshiharasHouseResult){a, f};
}
/* <<< factory Preload_NikkiInIshiharasHouse */

/* >>> factory Preload_IshiharaInIshiharasHouse */
PreloadIshiharaInIshiharasHouseResult Preload_IshiharaInIshiharasHouse(void)
{
	uint8_t mentioned = GetEventValue(0x1Cu);
	if (mentioned == 0u)
		return (PreloadIshiharaInIshiharasHouseResult){mentioned, 0x80u};
	uint8_t a = GetEventValue(0x1Fu);
	return (PreloadIshiharaInIshiharasHouseResult){a, cp_flags(a, ISHIHARA_LEFT)};
}
/* <<< factory Preload_IshiharaInIshiharasHouse */

/* >>> factory Preload_Ronald1InIshiharasHouse */
PreloadRonald1InIshiharasHouseResult Preload_Ronald1InIshiharasHouse(void)
{
	uint8_t a = GetEventValue(0x22u);
	return (PreloadRonald1InIshiharasHouseResult){a, ccf_cp_flags(a, TRUE)};
}
/* <<< factory Preload_Ronald1InIshiharasHouse */
