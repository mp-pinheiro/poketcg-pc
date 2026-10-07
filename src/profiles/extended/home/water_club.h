#ifndef HOME_WATER_CLUB_H
#define HOME_WATER_CLUB_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
} PreloadAmyResult;

PreloadAmyResult Preload_Amy(void);

/* >>> factory WaterClubMovePlayer */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint16_t hl; } WaterClubMovePlayerResult;
WaterClubMovePlayerResult WaterClubMovePlayer(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory WaterClubMovePlayer */
/* >>> factory WaterClubAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } WaterClubAfterDuelResult;
WaterClubAfterDuelResult WaterClubAfterDuel(void);
/* <<< factory WaterClubAfterDuel */
#endif
