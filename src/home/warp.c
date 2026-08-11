#include "home/warp.h"
#include "generated/wram.h"
#include "mem.h"
#define WARP_DATA_BANK 0x07u
#define WARP_DATA_POINTERS 0x4099u
static uint8_t warp_rom_read(uint16_t address){uint8_t bank=address<0x4000u?0u:WARP_DATA_BANK;return *rom_ptr(bank,address);}
static uint8_t compare_flags(uint8_t lhs,uint8_t rhs){uint8_t flags=0x40u;if(lhs==rhs)flags|=0x80u;if((lhs&0x0fu)<(rhs&0x0fu))flags|=0x20u;if(lhs<rhs)flags|=0x10u;return flags;}
HandleMapWarpResult _HandleMapWarp(void){
 uint8_t map=gb_read8(wCurMap_ADDR); uint16_t pointer_address=(uint16_t)(WARP_DATA_POINTERS+(uint16_t)map*2u); uint16_t warp_address=(uint16_t)(warp_rom_read(pointer_address)|(uint16_t)warp_rom_read((uint16_t)(pointer_address+1u))<<8); uint8_t player_x=gb_read8(wPlayerXCoord_ADDR); uint8_t player_y=gb_read8(wPlayerYCoord_ADDR); uint8_t flags=0x80u; uint8_t result_a=0;
 for(;;){uint8_t warp_x=warp_rom_read(warp_address);uint8_t warp_y=warp_rom_read((uint16_t)(warp_address+1u));if((uint8_t)(warp_x|warp_y)==0)break;if(warp_y==player_y){flags=compare_flags(warp_x,player_x);if(warp_x==player_x){uint16_t destination=(uint16_t)(warp_address+2u);gb_write8(wTempMap_ADDR,warp_rom_read(destination));destination++;gb_write8(wTempPlayerXCoord_ADDR,warp_rom_read(destination));destination++;gb_write8(wTempPlayerYCoord_ADDR,warp_rom_read(destination));result_a=gb_read8(wPlayerDirection_ADDR);gb_write8(wTempPlayerDirection_ADDR,result_a);break;}}warp_address=(uint16_t)(warp_address+5u);}
 return (HandleMapWarpResult){result_a,flags};
}
