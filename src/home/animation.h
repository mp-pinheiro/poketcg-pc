#ifndef HOME_ANIMATION_H
#define HOME_ANIMATION_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory ClearNumLoadedFramesetSubgroups */
void ClearNumLoadedFramesetSubgroups(void);
/* <<< factory ClearNumLoadedFramesetSubgroups */
/* >>> factory ClearOWFramesetSubgroups */
void ClearOWFramesetSubgroups(void);
/* <<< factory ClearOWFramesetSubgroups */
/* >>> factory GetOWFramesetSubgroupData */
void GetOWFramesetSubgroupData(uint16_t hl, uint8_t c);
/* <<< factory GetOWFramesetSubgroupData */
/* >>> factory LoadOWFramesetSubgroup */
uint8_t LoadOWFramesetSubgroup(uint8_t c);
/* <<< factory LoadOWFramesetSubgroup */
/* >>> factory StoreOWFramesetSubgroup */
void StoreOWFramesetSubgroup(uint8_t c);
/* <<< factory StoreOWFramesetSubgroup */


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
