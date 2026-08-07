"""The routines this slice ports, grouped by their pret source file.

`oracle-diff-all` walks this list, so a routine here with no CASES entry is a
FAIL rather than a silent pass. Dead code (zero callsites in poketcg/src) and
trampolines that become direct C calls at their callsites are deliberately absent.
"""

ROUTINES: dict[str, tuple[str, ...]] = {
    "copy": ("CopyGfxData", "CopyDataHLtoDE_SaveRegisters", "CopyDataHLtoDE"),
    "math": ("ATimes10",),
    "division": ("DivideBCbyDE",),
    "list": ("SetListPointer", "SetNextElementOfList"),
    "memory": ("DecompressDataFromBank", "CopyBankedDataToDE", "FillMemoryWithA",
               "FillMemoryWithDE", "GetFarByte"),
    "random": ("HtimesL", "Random", "UpdateRNGSources"),
    "decompress": ("InitDataDecompression", "DecompressData", "DecompressData.Decompress"),
    "write_number": ("TwoByteNumberToText",),
    "clear_sram_bg_maps": ("ClearSRAMBGMaps",),
    "clear_saved_duel": ("ClearSavedDuel",),
    "card_collection": ("CreateTempCardCollection", "AddCardToCollection",
                        "GetCardAlbumProgress"),
    "save": ("CopyGeneralSaveDataToSRAM", "ValidateGeneralSaveDataFromDE",
             "LoadGeneralSaveDataFromDE", "WriteDataToBackup", "LoadDataFromBackup",
             "WriteBackupGeneralSaveData", "WriteBackupCardAndDeckSaveData",
             "LoadBackupGeneralSaveData", "LoadBackupCardAndDeckSaveData",
             "InvalidateSaveData", "UpdateAlbumProgress", "LoadAlbumProgressFromSRAM",
             "LoadBackupSaveData", "_LoadGeneralSaveData",
             "_AddCardToCollectionAndUpdateAlbumProgress",
             "ValidateBackupGeneralSaveData", "_ValidateGeneralSaveData"),
}

ALL = tuple(fn for group in ROUTINES.values() for fn in group)
