#ifndef HOME_ANIMATION_H
#define HOME_ANIMATION_H

#include <stdint.h>

void ClearNumLoadedFramesetSubgroups(void);
void ClearOWFramesetSubgroups(void);
void GetOWFramesetSubgroupData(uint16_t hl, uint8_t c);
uint8_t LoadOWFramesetSubgroup(uint8_t c);
void StoreOWFramesetSubgroup(uint8_t c);


/* >>> factory LoadOWFrameTiles */
void LoadOWFrameTiles(void);
/* <<< factory LoadOWFrameTiles */
/* >>> factory DoLoadedFramesetSubgroupsFrame */
void DoLoadedFramesetSubgroupsFrame(void);
/* <<< factory DoLoadedFramesetSubgroupsFrame */
/* >>> factory ProcessOWFrameset */
void ProcessOWFrameset(uint16_t hl);
/* <<< factory ProcessOWFrameset */
/* >>> factory DoMapOWFrame */
void DoMapOWFrame(void);
/* <<< factory DoMapOWFrame */
#endif
