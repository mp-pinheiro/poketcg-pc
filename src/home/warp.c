#include "home/warp.h"
#include "generated/wram.h"
#include "mem.h"
#define WARP_DATA_BANK 0x07u
#define WARP_DATA_POINTERS 0x4099u
static uint8_t warp_rom_read(uint16_t address){uint8_t bank=address<0x4000u?0u:WARP_DATA_BANK;return *rom_ptr(bank,address);}
static uint8_t compare_flags(uint8_t lhs,uint8_t rhs){uint8_t flags=0x40u;if(lhs==rhs)flags|=0x80u;if((lhs&0x0fu)<(rhs&0x0fu))flags|=0x20u;if(lhs<rhs)flags|=0x10u;return flags;}
HandleMapWarpResult _HandleMapWarp(void){uint8_t map=gb_read8(wCurMap_ADDR);uint16_t p=(uint16_t)(WARP_DATA_POINTERS+(uint16_t)map*2u);uint16_t w=(uint16_t)(warp_rom_read(p)|(uint16_t)warp_rom_read((uint16_t)(p+1u))<<8);uint8_t x=gb_read8(wPlayerXCoord_ADDR),y=gb_read8(wPlayerYCoord_ADDR),flags=0x80u,result_a=0;for(;;){uint8_t wx=warp_rom_read(w),wy=warp_rom_read((uint16_t)(w+1u));if((uint8_t)(wx|wy)==0)break;if(wy==y){flags=compare_flags(wx,x);if(wx==x){uint16_t d=(uint16_t)(w+2u);gb_write8(wTempMap_ADDR,warp_rom_read(d));d++;gb_write8(wTempPlayerXCoord_ADDR,warp_rom_read(d));d++;gb_write8(wTempPlayerYCoord_ADDR,warp_rom_read(d));result_a=gb_read8(wPlayerDirection_ADDR);gb_write8(wTempPlayerDirection_ADDR,result_a);break;}}w=(uint16_t)(w+5u);}return (HandleMapWarpResult){result_a,flags};}
