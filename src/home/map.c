#include "home/map.h"

#include "generated/wram.h"
#include "mem.h"

static uint16_t permission_address(uint8_t b, uint8_t c)
{
	uint8_t x = (uint8_t)(b >> 1);
	uint8_t y = (uint8_t)(c >> 1);
	return (uint16_t)(wPermissionMap_ADDR + (uint16_t)((uint8_t)(y << 4) | x));
}

PermissionResult GetPermissionByteOfMapPosition(uint8_t b, uint8_t c)
{
	uint16_t hl = permission_address(b, c);
	return (PermissionResult){(uint8_t)(hl - wPermissionMap_ADDR), hl};
}

uint8_t GetPermissionOfMapPosition(uint8_t b, uint8_t c)
{
	return gb_read8(permission_address(b, c));
}

void SetPermissionOfMapPosition(uint8_t a, uint8_t b, uint8_t c)
{
	gb_write8(permission_address(b, c), a);
}

uint8_t UpdatePermissionOfMapPosition(uint8_t a, uint8_t b, uint8_t c)
{
	uint16_t address = permission_address(b, c);
	uint8_t result = (uint8_t)(gb_read8(address) & (uint8_t)~a);
	gb_write8(address, result);
	return result;
}

PermissionResult GetItemInLoadedNPCIndex(uint8_t a, uint8_t l)
{
	if (a >= 8u)
		a = 0;
	uint8_t offset = (uint8_t)(a * 12u + l);
	return (PermissionResult){offset, (uint16_t)(wLoadedNPCs_ADDR + offset)};
}

PermissionResult GetLoadedNPCID(uint8_t a)
{
	return GetItemInLoadedNPCIndex(a, 0);
}
