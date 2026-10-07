/* --- factory HblankWriteByteToBGMap0 */
/* >>> part probe_entries_bg_map */
const ProbeEntry probe_entries_bg_map[] = {
	{ "WriteDataBlocksToBGMap0", adapt_WriteDataBlocksToBGMap0 },
	{ "WriteDataBlockToBGMap0", adapt_WriteDataBlockToBGMap0 },
	{ "WriteByteToBGMap0", adapt_WriteByteToBGMap0 },
	{ "CopyDataToBGMap0", adapt_CopyDataToBGMap0 },
	{ "SafeCopyDataHLtoDE", adapt_SafeCopyDataHLtoDE },
	{ "JPHblankCopyDataHLtoDE", adapt_SafeCopyDataHLtoDE },
	{ NULL, NULL },
};
/* <<< part probe_entries_bg_map */
