#ifndef POKETCG_HOME_MAP_EVENTS_H
#define POKETCG_HOME_MAP_EVENTS_H

#include <stdint.h>

void ClearOWMapEvents(void);

/* >>> factory SetOWMapEvent_SRAMOrVRAM */
uint8_t SetOWMapEvent_SRAMOrVRAM(uint8_t a);
/* <<< factory SetOWMapEvent_SRAMOrVRAM */
/* >>> factory ApplyOWMapEventChangeIfEventSet */
void ApplyOWMapEventChangeIfEventSet(uint8_t a);
/* <<< factory ApplyOWMapEventChangeIfEventSet */
/* >>> factory SetOWMapEvent */
uint8_t SetOWMapEvent(uint8_t a);
/* <<< factory SetOWMapEvent */
#endif
