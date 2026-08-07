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
    "bg_map": ("WriteDataBlocksToBGMap0", "WriteDataBlockToBGMap0", "WriteByteToBGMap0",
               "HblankWriteByteToBGMap0", "CopyDataToBGMap0", "SafeCopyDataHLtoDE",
               "JPHblankCopyDataHLtoDE"),
    "empty_screen": ("EmptyScreen", "BCCoordToBGMap0Address"),
    "tiles": ("FillRectangle", "Copy1bppTiles"),
    "text_box": ("SafeCopyDataDEtoHL", "DECoordToBGMap0Address",
                 "AdjustCoordinatesForBGScroll", "CopyLine"),
    "process_text": ("InitTextFormat", "CaseHalfWidthLetter", "ClassifyTextCharacterPair",
                     "GetTextLengthInHalfTiles", "GetTextLengthInTiles",
                     "GetFullWidthFontTileOffset", "ConvertTileNumberToTileDataAddress",
                     "CopyHalfWidthCharacterToDE", "CreateHalfWidthFontTile",
                     "CreateFullWidthFontTile", "CreateFullWidthFontTile_ConvertToTileDataAddress",
                     "GenerateTextTile", "TwoByteNumberToTxSymbol_PadSpace"),
    "input": ("ReadJoypad", "SaveButtonsHeld", "ClearJoypad"),
    "menus": ("InitializeCardListParameters", "InitializeMenuParameters", "SetMenuItem",
              "OneByteNumberToTxSymbol", "OneByteNumberToTxSymbol_PadSpace",
              "OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign", "CardTypeToSymbolID",
              "GetCardSymbolData"),
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
