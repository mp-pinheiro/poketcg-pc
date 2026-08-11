#ifndef POKETCG_HOME_DECK_MACHINE_ROOM_H
#define POKETCG_HOME_DECK_MACHINE_ROOM_H
#include <stdint.h>
typedef struct { uint8_t a; uint8_t b; uint8_t c; uint16_t hl; } FuncD96cResult;
FuncD96cResult Func_d96c(uint8_t a);
void Script_BeatAaron(void);
#endif
