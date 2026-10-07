/* >>> part kSetOWMapEventTilemapPointers */
static const uint8_t kSetOWMapEventTilemapPointers[33] = {
	0x16u, 0x00u, TILEMAP_POKEMON_DOME_DOOR_MAP_EVENT,
	0x0eu, 0x00u, TILEMAP_HALL_OF_HONOR_DOOR_MAP_EVENT,
	0x06u, 0x02u, TILEMAP_DECK_MACHINE_MAP_EVENT,
	0x0au, 0x02u, TILEMAP_DECK_MACHINE_MAP_EVENT,
	0x0eu, 0x02u, TILEMAP_DECK_MACHINE_MAP_EVENT,
	0x12u, 0x02u, TILEMAP_DECK_MACHINE_MAP_EVENT,
	0x0eu, 0x0au, TILEMAP_DECK_MACHINE_MAP_EVENT,
	0x12u, 0x0au, TILEMAP_DECK_MACHINE_MAP_EVENT,
	0x0eu, 0x12u, TILEMAP_DECK_MACHINE_MAP_EVENT,
	0x12u, 0x12u, TILEMAP_DECK_MACHINE_MAP_EVENT,
	0x0au, 0x00u, TILEMAP_CHALLENGE_MACHINE_MAP_EVENT,
};
/* <<< part kSetOWMapEventTilemapPointers */
/* >>> factory SetOWMapEvent_SRAMOrVRAM */
uint8_t SetOWMapEvent_SRAMOrVRAM(uint8_t a)
{
	/* rebuild after map_events.h stdint.h fix */
	uint8_t event_index = a;
	uint8_t saved_tilemap = wCurTilemap;
	uint8_t saved_bank = wBGMapBank;
	uint8_t saved_width = wBGMapWidth;
	uint8_t saved_height = wBGMapHeight;
	uint8_t saved_ptr_lo = gb_read8(wBGMapPermissionDataPtr_ADDR);
	uint8_t saved_ptr_hi = gb_read8((uint16_t)(wBGMapPermissionDataPtr_ADDR + 1u));

	gb_write8((uint16_t)(wOWMapEvents_ADDR + event_index), TRUE);

	uint8_t idx4 = (uint8_t)(event_index * 3u);
	uint8_t x = kSetOWMapEventTilemapPointers[idx4];
	uint8_t y = kSetOWMapEventTilemapPointers[(uint8_t)(idx4 + 1u)];
	uint8_t tilemap = kSetOWMapEventTilemapPointers[(uint8_t)(idx4 + 2u)];
	wCurTilemap = tilemap;

	LoadTilemap(x, y);

	uint8_t bx = (uint8_t)(x >> 1);
	uint8_t rrca_y = (uint8_t)((y >> 1) | ((y & 1u) << 7));
	uint8_t masked = (uint8_t)(rrca_y & 0x0Fu);
	uint8_t swapped = (uint8_t)(masked << 4);
	uint8_t offset = (uint8_t)(swapped + bx);
	DecompressPermissionMap((uint16_t)(wPermissionMap_ADDR + offset));

	gb_write8((uint16_t)(wBGMapPermissionDataPtr_ADDR + 1u), saved_ptr_hi);
	gb_write8(wBGMapPermissionDataPtr_ADDR, saved_ptr_lo);
	wBGMapHeight = saved_height;
	wBGMapWidth = saved_width;
	wBGMapBank = saved_bank;
	wCurTilemap = saved_tilemap;
	return saved_tilemap;
}
/* <<< factory SetOWMapEvent_SRAMOrVRAM */
/* === factory ApplyOWMapEventChangeIfEventSet */
