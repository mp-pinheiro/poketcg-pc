"""Extended oracle-diff cases for effect_functions: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import STACK_CANARY, STACK_TOP, WRAMX_START, const, sym, sym_bank
from tests.cases._inherit import inherit
from tests.cases._fixtures import lass_hand_fixture
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
_COIN_FIXTURE = {
    "keys": [0x00, 0x01],
    "wram": {
        sym("wDamage"): b"\x00\x00",
        sym("wAIMinDamage"): b"\x00",
        sym("wAIMaxDamage"): b"\x00",
        sym("wLoadedAttackAnimation"): b"\x00",
        sym("wEffectFailed"): b"\x00",
        sym("hWhoseTurn"): b"\xc2",
        sym("wDeckToBuild") + 0xE7: b"\x00",
        sym("wPlayerArenaCardSubstatus1"): b"\x00",
        sym("wPlayerArenaCardSubstatus2"): b"\x00",
        sym("wPlayerArenaCardLastTurnSubstatus2"): b"\x00",
        sym("wPlayerDuelistType"): b"\x00",
        sym("wDuelType"): b"\x00",
        sym("wDuelDisplayedScreen"): b"\x06",
        sym("wLCDC"): b"\x00",
        sym("wRNG1"): b"\x00\x00\x00",
        sym("wCoinTossTotalNum"): b"\xff",
        sym("wCoinTossNumHeads"): b"\xff",
        sym("wCoinTossDuelistType"): b"\xff",
        sym("wCoinTossNumTossed"): b"\x01",
        sym("wCoinTossScreenTextID"): b"4\x12",
    },
    "read": {sym("wLoadedAttackAnimation"): 0x01, sym("wEffectFailed"): 0x01, sym("wDuelDisplayedScreen"): 0x01, sym("hWhoseTurn"): 0x01, sym("wDeckToBuild") + 0xE7: 0x01, sym("wPlayerArenaCardSubstatus1"): 0x01, sym("wPlayerArenaCardSubstatus2"): 0x01, sym("wPlayerArenaCardLastTurnSubstatus2"): 0x01},
    "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
    "instruction_budget": 0x1312D00,
    "cycle_budget": 0x4C4B400,
}
_ENERGY_SELECTION_FIXTURE = {
    "keys": [0x00, 0x01],
    "wram": {sym("hWhoseTurn"): b"\xc2", sym("wLCDC"): b"\x00", sym("wDuelTempList"): b"\xff"},
    "read": {sym("hCurSelectionItem"): 0x01, sym("wDuelTempList"): 0x02},
    "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
    "instruction_budget": 0x1312D00,
    "cycle_budget": 0x4C4B400,
}
_DAMAGE_CASE = {
    "wram": {sym("wDamage"): b"\x00\x00", sym("wAIMinDamage"): b"\x00", sym("wAIMaxDamage"): b"\x00"},
    "read": {sym("wDamage"): 0x02, sym("wAIMinDamage"): 0x01, sym("wAIMaxDamage"): 0x01},
}
_CARD_DAMAGE_CASE = {
    "e": 0x00,
    "wram": {sym("hWhoseTurn"): b"\xc2", sym("wPlayerArenaCard"): b"\x00", sym("wPlayerArenaCardHP"): b"\x05", sym("wBoosterCardsDrawn"): b"\x01",
             sym("wDamage"): b"\x00\x00", sym("wAIMinDamage"): b"\x00", sym("wAIMaxDamage"): b"\x00"},
    "read": {sym("wDamage"): 0x02, sym("wAIMinDamage"): 0x01, sym("wAIMaxDamage"): 0x01},
}
_ENERGY_CASE = {
    "wram": {sym("wAttachedEnergies"): b"\x00\x00\x00\x00\x00\x00\x00\x00"},
    "read": {sym("wAttachedEnergies"): 0x08},
}
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('effect_functions', remove=(
    'ArcanineFlamethrower_AISelectEffect',
    'ArcanineFlamethrower_CheckEnergy',
    'ArcanineFlamethrower_DiscardEffect',
    'ArcanineFlamethrower_PlayerSelectEffect',
    'ArcanineQuickAttack_AIEffect',
    'ArcanineQuickAttack_DamageBoostEffect',
    'ButterfreeWhirlwind_CheckBench',
    'ButterfreeWhirlwind_SwitchEffect',
    'CharmeleonFlamethrower_AISelectEffect',
    'CharmeleonFlamethrower_CheckEnergy',
    'CharmeleonFlamethrower_DiscardEffect',
    'CharmeleonFlamethrower_PlayerSelectEffect',
    'ClefableMinimizeEffect',
    'CommentedOut_2c086',
    'CopyPlayAreaHPFromBackup_Unreferenced',
    'CopyPlayAreaHPToBackup_Unreferenced',
    'CuboneRage_AIEffect',
    'CuboneRage_DamageBoostEffect',
    'DodrioRage_AIEffect',
    'DodrioRage_DamageBoostEffect',
    'DragonairHyperBeam_AISelectEffect',
    'DragonairHyperBeam_DiscardEffect',
    'DragonairHyperBeam_PlayerSelectEffect',
    'DuelistSelectForcedSwitch',
    'EeveeQuickAttack_AIEffect',
    'EeveeQuickAttack_DamageBoostEffect',
    'ElectabuzzQuickAttack_AIEffect',
    'ElectabuzzQuickAttack_DamageBoostEffect',
    'ElectrodeSonicboom_NullEffect',
    'ElectrodeSonicboom_UnaffectedByColorEffect',
    'EnergyBurnCheck_Unreferenced',
    'FearowAgilityEffect',
    'FlareonFlamethrower_AISelectEffect',
    'FlareonFlamethrower_CheckEnergy',
    'FlareonFlamethrower_DiscardEffect',
    'FlareonFlamethrower_PlayerSelectEffect',
    'FlareonQuickAttack_AIEffect',
    'FlareonQuickAttack_DamageBoostEffect',
    'FlareonRage_AIEffect',
    'FlareonRage_DamageBoostEffect',
    'Func_2c0a8',
    'Func_2c6d9',
    'GengarDarkMind_AISelectEffect',
    'GengarDarkMind_DamageBenchEffect',
    'GengarDarkMind_PlayerSelectEffect',
    'GolduckHyperBeam_AISelectEffect',
    'GolduckHyperBeam_DiscardEffect',
    'GolduckHyperBeam_PlayerSelectEffect',
    'GravelerHardenEffect',
    'GrimerMinimizeEffect',
    'HorseaSmokescreenEffect',
    'HypnoDarkMind_AISelectEffect',
    'HypnoDarkMind_DamageBenchEffect',
    'HypnoDarkMind_PlayerSelectEffect',
    'JolteonQuickAttack_AIEffect',
    'JolteonQuickAttack_DamageBoostEffect',
    'JynxMeditate_AIEffect',
    'JynxMeditate_DamageBoostEffect',
    'KakunaStiffenEffect',
    'KinglerFlail_AIEffect',
    'KinglerFlail_HPCheck',
    'LickitungSupersonicEffect',
    'MagikarpFlail_AIEffect',
    'MagikarpFlail_HPCheck',
    'MagmarFlamethrower_AISelectEffect',
    'MagmarFlamethrower_CheckEnergy',
    'MagmarFlamethrower_DiscardEffect',
    'MagmarFlamethrower_PlayerSelectEffect',
    'MagmarSmokescreenEffect',
    'MagnetonSonicboom_NullEffect',
    'MagnetonSonicboom_UnaffectedByColorEffect',
    'MetapodStiffenEffect',
    'MewtwoAltEnergyAbsorption_AISelectEffect',
    'MewtwoAltEnergyAbsorption_AddToHandEffect',
    'MewtwoAltEnergyAbsorption_CheckDiscardPile',
    'MewtwoAltEnergyAbsorption_PlayerSelectEffect',
    'MewtwoEnergyAbsorption_AISelectEffect',
    'MewtwoEnergyAbsorption_AddToHandEffect',
    'MewtwoEnergyAbsorption_CheckDiscardPile',
    'MewtwoEnergyAbsorption_PlayerSelectEffect',
    'MrMimeMeditate_AIEffect',
    'MrMimeMeditate_DamageBoostEffect',
    'NidoranFFurySwipes_AIEffect',
    'NidoranFFurySwipes_MultiplierEffect',
    'NidorinaDoubleKick_AIEffect',
    'NidorinaDoubleKick_MultiplierEffect',
    'NidorinaSupersonicEffect',
    'NidorinoDoubleKick_AIEffect',
    'NidorinoDoubleKick_MultiplierEffect',
    'OnixHardenEffect',
    'PidgeottoMirrorMove_AIEffect',
    'PidgeottoMirrorMove_AISelection',
    'PidgeottoMirrorMove_AfterDamage',
    'PidgeottoMirrorMove_BeforeDamage',
    'PidgeottoMirrorMove_InitialEffect1',
    'PidgeottoMirrorMove_InitialEffect2',
    'PidgeottoMirrorMove_PlayerSelection',
    'PidgeottoWhirlwind_SelectEffect',
    'PidgeottoWhirlwind_SwitchEffect',
    'PidgeyWhirlwind_SelectEffect',
    'PidgeyWhirlwind_SwitchEffect',
    'PikachuAltLv16GrowlEffect',
    'PikachuLv16GrowlEffect',
    'PoliwhirlAmnesia_AISelectEffect',
    'PoliwhirlAmnesia_CheckAttacks',
    'PoliwhirlAmnesia_DisableEffect',
    'PoliwhirlAmnesia_PlayerSelectEffect',
    'PrimeapeFurySwipes_AIEffect',
    'PrimeapeFurySwipes_MultiplierEffect',
    'PsyduckFurySwipes_AIEffect',
    'PsyduckFurySwipes_MultiplierEffect',
    'RaichuAgilityEffect',
    'RaichuThunder_Recoil50PercentEffect',
    'RaichuThunder_RecoilEffect',
    'RapidashAgilityEffect',
    'SandslashFurySwipes_AIEffect',
    'SandslashFurySwipes_MultiplierEffect',
    'SeadraAgilityEffect',
    'Serial_TossCoin',
    'Serial_TossCoinATimes',
    'Serial_TossZeroCoins',
    'ShellderSupersonicEffect',
    'SlowpokeAmnesia_AISelectEffect',
    'SlowpokeAmnesia_CheckAttacks',
    'SlowpokeAmnesia_DisableEffect',
    'SlowpokeAmnesia_PlayerSelectEffect',
    'SpearowMirrorMove_AIEffect',
    'SpearowMirrorMove_AISelection',
    'SpearowMirrorMove_AfterDamage',
    'SpearowMirrorMove_BeforeDamage',
    'SpearowMirrorMove_InitialEffect1',
    'SpearowMirrorMove_InitialEffect2',
    'SpearowMirrorMove_PlayerSelection',
    'SquirtleWithdrawEffect',
    'TentacruelSupersonicEffect',
    'TossCoinATimes_BankB',
    'TossCoin_BankB',
    'VaporeonQuickAttack_AIEffect',
    'VaporeonQuickAttack_DamageBoostEffect',
    'WartortleWithdrawEffect',
    'Whirlpool_AISelectEffect',
    'Whirlpool_DiscardEffect',
    'Whirlpool_PlayerSelectEffect',
    'ZapdosThunder_Recoil50PercentEffect',
    'ZapdosThunder_RecoilEffect',
    'ZubatSupersonicEffect',
))
OWN = (
    'AgilityEffect',
    'Amnesia_AISelectEffect',
    'Amnesia_CheckAttacks',
    'Amnesia_DisableEffect',
    'Amnesia_PlayerSelectEffect',
    'CheckIfDefendingPokemonHasAnyAttack',
    'DarkMind_AISelectEffect',
    'DarkMind_DamageBenchEffect',
    'DarkMind_PlayerSelectEffect',
    'DevolutionSpray_PlayerSelection',
    'DoubleKick30_AIEffect',
    'DoubleKick30_MultiplierEffect',
    'DuelistSelectForcedSwitch',
    'EnergyAbsorption_AISelectEffect',
    'EnergyAbsorption_AddToHandEffect',
    'EnergyAbsorption_CheckDiscardPile',
    'EnergyAbsorption_PlayerSelectEffect',
    'EnergySpike_PlayerSelectEffect',
    'Flail_AIEffect',
    'Flail_HPCheck',
    'Flamethrower_AISelectEffect',
    'Flamethrower_CheckEnergy',
    'Flamethrower_DiscardEffect',
    'Flamethrower_PlayerSelectEffect',
    'FoulGas_PoisonOrConfusionEffect',
    'FurySwipes10_AIEffect',
    'FurySwipes10_MultiplierEffect',
    'FurySwipes20_AIEffect',
    'FurySwipes20_MultiplierEffect',
    'GrowlEffect',
    'GustOfWind_SwitchEffect',
    'HardenEffect',
    'HyperBeam_AISelectEffect',
    'HyperBeam_DiscardEffect',
    'HyperBeam_PlayerSelectEffect',
    'LassEffect',
    'Meditate_AIEffect',
    'Meditate_DamageBoostEffect',
    'MinimizeEffect',
    'PealOfThunder_RandomlyDamageEffect',
    'PokeBall_PlayerSelection',
    'QuickAttack_AIEffect',
    'QuickAttack_DamageBoostEffect',
    'Rage_AIEffect',
    'Rage_DamageBoostEffect',
    'Recycle_PlayerSelection',
    'SmokescreenEffect',
    'Sonicboom_NullEffect',
    'Sonicboom_UnaffectedByColorEffect',
    'StiffenEffect',
    'SupersonicEffect',
    'Thunder_Recoil50PercentEffect',
    'Thunder_RecoilEffect',
    'Whirlwind_SelectEffect',
    'Whirlwind_SwitchEffect',
    'WithdrawEffect',
)
CONTRACT.update({
    'CheckIfDefendingPokemonHasAnyAttack': {'compare': ('f',), 'preserve': ()},
    'GustOfWind_SwitchEffect': {'compare': (), 'preserve': ()},
    'FoulGas_PoisonOrConfusionEffect': {'compare': ('f',), 'preserve': ()},
    'LassEffect': {'compare': (), 'preserve': ()},
    'Recycle_PlayerSelection': {'compare': ('a', 'f'), 'preserve': ()},
    'PokeBall_PlayerSelection': {'compare': ('a', 'f'), 'preserve': ()},
    'DuelistSelectForcedSwitch': {'compare': ('a', 'f'), 'preserve': ()},
    'PealOfThunder_RandomlyDamageEffect': {'compare': ('a', 'f'), 'preserve': ()},
    'DevolutionSpray_PlayerSelection': {'compare': ('f',), 'preserve': ()},
    'EnergySpike_PlayerSelectEffect': {'compare': (), 'preserve': ()},
    'StiffenEffect': {'compare': ('f',), 'preserve': ()},
    'SupersonicEffect': {'compare': ('f',), 'preserve': ()},
    'FurySwipes10_AIEffect': {'compare': (), 'preserve': ()},
    'FurySwipes10_MultiplierEffect': {'compare': (), 'preserve': ()},
    'DoubleKick30_AIEffect': {'compare': (), 'preserve': ()},
    'DoubleKick30_MultiplierEffect': {'compare': (), 'preserve': ()},
    'Whirlwind_SelectEffect': {'compare': ('a', 'f'), 'preserve': ()},
    'Whirlwind_SwitchEffect': {'compare': ('a', 'f'), 'preserve': ()},
    'MinimizeEffect': {'compare': ('hl',), 'preserve': ()},
    'WithdrawEffect': {'compare': ('f',), 'preserve': ()},
    'Flail_AIEffect': {'compare': (), 'preserve': ()},
    'Flail_HPCheck': {'compare': (), 'preserve': ()},
    'AgilityEffect': {'compare': ('f',), 'preserve': ()},
    'QuickAttack_AIEffect': {'compare': (), 'preserve': ()},
    'QuickAttack_DamageBoostEffect': {'compare': (), 'preserve': ()},
    'SmokescreenEffect': {'compare': ('hl',), 'preserve': ()},
    'Flamethrower_CheckEnergy': {'compare': ('a', 'f', 'hl'), 'preserve': ('b', 'c', 'd')},
    'Flamethrower_PlayerSelectEffect': {'compare': ('a', 'f'), 'preserve': ()},
    'Flamethrower_AISelectEffect': {'compare': (), 'preserve': ()},
    'Flamethrower_DiscardEffect': {'compare': (), 'preserve': ()},
    'Rage_AIEffect': {'compare': (), 'preserve': ()},
    'Rage_DamageBoostEffect': {'compare': (), 'preserve': ()},
    'DarkMind_PlayerSelectEffect': {'compare': (), 'preserve': ()},
    'DarkMind_AISelectEffect': {'compare': ('a',), 'preserve': ()},
    'DarkMind_DamageBenchEffect': {'compare': (), 'preserve': ()},
    'EnergyAbsorption_CheckDiscardPile': {'compare': ('f', 'hl'), 'preserve': ()},
    'EnergyAbsorption_PlayerSelectEffect': {'compare': ('a', 'f', 'hl'), 'preserve': ()},
    'EnergyAbsorption_AISelectEffect': {'compare': (), 'preserve': ()},
    'EnergyAbsorption_AddToHandEffect': {'compare': (), 'preserve': ()},
    'Amnesia_CheckAttacks': {'compare': ('f', 'hl'), 'preserve': ()},
    'Amnesia_PlayerSelectEffect': {'compare': ('a', 'f'), 'preserve': ()},
    'Amnesia_AISelectEffect': {'compare': ('a',), 'preserve': ()},
    'Amnesia_DisableEffect': {'compare': (), 'preserve': ()},
    'Meditate_AIEffect': {'compare': (), 'preserve': ()},
    'Meditate_DamageBoostEffect': {'compare': (), 'preserve': ()},
    'HardenEffect': {'compare': ('hl',), 'preserve': ()},
    'FurySwipes20_AIEffect': {'compare': (), 'preserve': ()},
    'FurySwipes20_MultiplierEffect': {'compare': (), 'preserve': ()},
    'Thunder_Recoil50PercentEffect': {'compare': ('a', 'f', 'b', 'hl'), 'preserve': ()},
    'Thunder_RecoilEffect': {'compare': ('a', 'f'), 'preserve': ()},
    'GrowlEffect': {'compare': ('hl',), 'preserve': ()},
    'Sonicboom_UnaffectedByColorEffect': {'compare': ('f', 'hl'), 'preserve': ()},
    'Sonicboom_NullEffect': {'compare': (), 'preserve': ()},
    'HyperBeam_PlayerSelectEffect': {'compare': (), 'preserve': ()},
    'HyperBeam_AISelectEffect': {'compare': (), 'preserve': ()},
    'HyperBeam_DiscardEffect': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
})
CASES.update({
    'CheckIfDefendingPokemonHasAnyAttack': [
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCard"): b'\x00', sym("wLoadedCard2Atk1Category"): b'\x08'}, 'read': {sym("hWhoseTurn"): 0x01}},
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCard"): b'\x00', sym("wLoadedCard2Atk1Category"): b'\x11'}, 'read': {sym("hWhoseTurn"): 0x01}},
        {'wram': {sym("hWhoseTurn"): b'\xc3', sym("wPlayerArenaCard"): b'\x00', sym("wBoosterCardsDrawn"): b'\xbe'}, 'read': {sym("hWhoseTurn"): 0x01}},
        {   'wram': {sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCard"): b'\x00', sym("wLoadedCard2Atk1Category"): b'\xcb', sym("wLoadedCard2Atk2Name"): b'\x10'},
            'read': {sym("hWhoseTurn"): 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCard"): b'\x00', sym("wLoadedCard2Atk1Category"): b'\xcc', sym("wLoadedCard2Atk2Name"): b'\x10'},
            'read': {sym("hWhoseTurn"): 0x01}},
    ],
    'GustOfWind_SwitchEffect': [
        {   'wram': {sym("wDuelDisplayedScreen"): b'\x05', sym("wLCDC"): b'\x80', 0xFF40: b'\x80'},
            'read': {sym("wDamageAnimAmount"): 0x02, sym("wDuelDisplayedScreen"): 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'wram': {sym("wDuelDisplayedScreen"): b'\xff', sym("wLCDC"): b'\x80', 0xFF40: b'\x80'},
            'read': {sym("wDamageAnimAmount"): 0x02, sym("wDuelDisplayedScreen"): 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x1234,
            'wram': {sym("wDuelDisplayedScreen"): b'\x03', sym("wLCDC"): b'\x80', 0xFF40: b'\x80'},
            'read': {sym("wDamageAnimAmount"): 0x02, sym("wDuelDisplayedScreen"): 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0x0B,
            'f': 0x12,
            'b': 0x03,
            'c': 0x01,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x7E90,
            'wram': {sym("wDuelDisplayedScreen"): b'\x00', sym("wLCDC"): b'\x80', 0xFF40: b'\x80'},
            'read': {sym("wDamageAnimAmount"): 0x02, sym("wDuelDisplayedScreen"): 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'FoulGas_PoisonOrConfusionEffect': [
        {   'keys': [0x00, 0x01, 0x00, 0x01, 0x00, 0x01],
            'wram': {   sym("wPlayerDuelistType"): b'\x00',
                        sym("wDoFrameFunction"): b'\xc9\x32',
                        sym("wDuelType"): b'\x00',
                        sym("wDuelDisplayedScreen"): b'\x06',
                        sym("wLCDC"): b'\x00',
                        sym("wRNG1"): b'\x00\x00\x00',
                        sym("wStatusConditionQueueIndex"): b'\x00',
                        sym("wCoinTossTotalNum"): b'\xff',
                        sym("wCoinTossNumHeads"): b'\xff',
                        sym("wCoinTossDuelistType"): b'\xff',
                        sym("wCoinTossNumTossed"): b'\x01',
                        sym("wCoinTossScreenTextID"): b'4\x12'},
            'read': {   sym("wCoinTossTotalNum"): 0x01,
                        sym("wCoinTossNumHeads"): 0x01,
                        sym("wCoinTossDuelistType"): 0x01,
                        sym("wCoinTossNumTossed"): 0x01,
                        sym("wStatusConditionQueueIndex"): 0x01,
                        sym("wStatusConditionQueue"): 0x03,
                        sym("wCoinTossScreenTextID"): 0x02,
                        sym("wDuelDisplayedScreen"): 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': [0x00, 0x01, 0x00, 0x01, 0x00, 0x01],
            'wram': {   sym("wPlayerDuelistType"): b'\x00',
                        sym("wDoFrameFunction"): b'\xc9\x32',
                        sym("wDuelType"): b'\x00',
                        sym("wDuelDisplayedScreen"): b'\x06',
                        sym("wLCDC"): b'\x00',
                        sym("wRNG1"): b'\x00\x00\x00',
                        sym("wStatusConditionQueueIndex"): b'\x00',
                        sym("wCoinTossTotalNum"): b'\xff',
                        sym("wCoinTossNumHeads"): b'\xff',
                        sym("wCoinTossDuelistType"): b'\xff',
                        sym("wCoinTossNumTossed"): b'\x01',
                        sym("wCoinTossScreenTextID"): b'\xee\xdd'},
            'read': {   sym("wCoinTossTotalNum"): 0x01,
                        sym("wCoinTossNumHeads"): 0x01,
                        sym("wCoinTossDuelistType"): 0x01,
                        sym("wCoinTossNumTossed"): 0x01,
                        sym("wStatusConditionQueueIndex"): 0x01,
                        sym("wStatusConditionQueue"): 0x03,
                        sym("wCoinTossScreenTextID"): 0x02,
                        sym("wDuelDisplayedScreen"): 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'wram': {   sym("wDeckToBuild"): b'\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0'
                                b'\xc1\xc2\xc3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0'
                                b'\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x01\x08\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00'
                                b'\x00\x08\x08\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x01\x00\x00\x00\x00'
                                b'\x00\x00\x00\x08\x01\x01\x00\x00\x00\x00\x00\x003\x12\x03\x11'
                                b'\x00\x00\t\x04\x17\x025+\x1c4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00&\t\x04\x17\x025+3\x12\x03'
                                b"\x11\x1c4\x152-1,!\x1e.\x078\x1d\x0e\x18$\x05\x0c\x1a';\x196"
                                b'\x08/\x10#\x01\n\x16\x1b\x0b"\x067:(\x14 \x0f0\x1f\x13\x00*\r9)%\r&'
                                b'\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00(\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x0f\x00\x08\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x10\x08\x00\x00\x00\x00'
                                b'\x00\x01\x00\x08\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01'
                                b'\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x11\x00\x00\x01\x00\x00'
                                b'\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x01\x00'
                                b'\x078\x0f/\x00\x00)\r:\x16\x1b\x06&\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00)\x01\r:\x16 '
                                b'\x1b\x078\x0f/&\x06#\x1f\x13,\x12\x14\x1e3\x15\x0e\x17*.4\x11\x0c\x18'
                                b'70\x00\x08\x029\x0b\n\x05%-!(\t\x0356;\x1a\x19\'$2\x1d"1\x04+'
                                b'\x10\x1c\r &\xff\xff\xff\xff\xff\x80\x80\x00\x00\x00\x002(\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x0f\x00\x05\x02\x00\xa6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x04\x04'
                                b'\x04\x04\x04\x04\x04\x04\x05\x05\x05\x05\x05\x05001266899;``giikuyyz'
                                b'}~\xa7\xa7\xa8\xb1\xc3\xc5\xc5\xd2\xd6\xd8\xdd\xdd\xdf\xdf'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01\x01\x01\x04\x04\x04\x04'
                                b'\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x05\x05\x05\x05\x05\x05'
                                b'\x05\x05****+++jjjjkkll\x80\x80\x80\x80\x81\x81\x81\x82\x82\xc3\xc3'
                                b'\xcf\xcf\xd9\xd9\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x030\x030\x030\x030\x030\x030'
                                b'\x00\x00\x00\x00\x1b\x16:\r)\xff\xff\xff8\x1a\xff$5\xff\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x06Koffing Lv13\x00                       \x00                      '
                                b'     \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x000SHBSAP,LF.LEG  HK EFS.CTLPA DDMIFG@'
                                b'EOFO (AR)OSIO KNDR IUNWROVO ITIEO;OIG LRWFI1 CO EKWOH N3ORTA.ADN NAS'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00LGTI'
                                b"GCU \x03UC AE SIFLU RYET TNO'GE FI FA EW  KHCNT!DMASRIDPNP EU.OOMOE"
                                b'FLDW IFRSDNKNMODAEN S YUDCEMSKG1KTATNHNIGERS\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000123456m^\x86\x8e'
                                b'Z\x95r@\x97\x94;t\x9fDEW\x82_=|I\x93p\x9aU\x7fQR}\x98\\\x92\x90dCh'
                                b'Pw]F<cz\x87aYi\x9d\x80\x8fJf9vl>XjkqM\x9cs~y?L\x91oK\x88Hge:8'
                                b'\x83VG\x84xSN\x8a\x81\x8c\x8b[\x00Obun{\x8dT\x89B\x99A'
                                b'\x9b\x85\x96\x9e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x0012345678\x83l\x82B`Joy?\x9b\x99ZEF_\x86\x7fLj}'
                                b'zt\x8a\x91\\RS\x89\x97P\x85Gpe<\x8fV^9I\x90d\x92aY\x81k\x80[fqr'
                                b'n8\x94|Ns>vC\x93m]\x88xb\x95KTwQh\x8cH\x84\x87\x9d:c~\x98\x8b\x8e'
                                b'\x8d\x96;iX{WMA=\x9e@U\x9aO\x9cug\x9fD\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x01\x00\x00\x00\x03\x00\x00\x00\x03 \x00\x00\x04\x00'
                                b'\x00\x00\x05\x00\x00\x00\x06\x00\x00\x00\x07\x00\x00\x00\x08\x00'
                                b'\x00\x00\x03 \x00\x00\x03\x00\x00\x00\x03 \x00\x00\x00\x00'
                                b'\x00\x00\x01\x00\x00\x00\x03\x00\x00\x00\x03 \x00\x00B\x02'
                                b'\x00\x00C\x02\x00\x00C"\x00\x00B"\x00\x00\t\x00\x00\x00\x08\x00'
                                b'\x00\x00\x18\x00\x00\x00\x19\x00\x00\x00\x04\x00\x00\x00\x14\x00'
                                b'\x00\x00$\x00\x00\x00\x05\x00\x00\x00\x15\x00\x00\x00%\x00'
                                b'\x00\x005\x00\x00\x004\x00\x00\x00(\x00\x00\x00&\x00\x00\x00\x16\x00'
                                b"\x00\x00\x06\x00\x00\x00\x07\x00\x00\x00\x17\x00\x00\x00'\x00"
                                b'\x00\x00)\x00\x00\x00\x00! \x00las\x00\x030\x00\x00\x00\x00'
                                b'\x00\x00\x00\x11\x02\x00\x00',
                        sym("wVBlankCounter"): b'',
                        sym("wVBlankCounter") + 1: b'\x00\x00\xc3\xe4\xe6\xe4',
                        sym("wVBlankOAMCopyToggle"): b'',
                        sym("wTempByte"): b'\x1d\x00=\x01\x17+\x1c\x01\x00\xea\x10?\xc3\x00\x00\xc3"\x03\x00\x00\x00\x13t\x05\x00\x00\x00\x00\xc0\x00\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9cc\xb5BJ!\x00\x00\x9cc\xbe\x03~\x00\x00\x00\x9cc@\x02lQ\x00\x00\x9cc\x16X\xfb\x0c\x00\x00\x9ccZ\x01\x1c\x00\x00\x00\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff3\x9aU\x10@\x04\x10\xffk\x84U\x840\x00\x00\x9cc\xb5BJ!\x00\x00\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\x00\x00\x11\xc5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x03\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x08\x02\x00\x00o\x00\xa7\x00\x01\x00\x00\x00\x00\x00\x00\xe8\xdf\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\x08\x00\x0e;S\x00\x00\xc3\x03\x00\x04\xa6\x00\x01\x00\xa6&\xff\xff\xff0\x00$\x18\xc1\x03\x04&\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x94\x0f\xb9\x08\x000*2\x00\x00\x00\x02\x00\x00\x00\xba\x08\xbb\x08\x00\x00\n\x00wG\t\x00\x00\x005\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00\xbc\x08m\x00\r\x02\x00\x14\x00\xbd\x08\x10\x02\x94\'\xd1\t\x00\x00i(\x00\x00\x00\x00\x10\x00\x00\xd2\t"\x08\x00\x00\n\x00cL\x04\x00\x00\x00o\x00\x10\x00\x10\xc0\x08\xd3\t\x00\x00(\x00gL@\x00\x00(V\x01\x08\x00\xd4\tQ\x00\r\x01\x00\x82\x00\xd5\t\x13\x02\x00\x00\x00\xba\x08\xbb\x08\x00\x00\n\x00wG\t\x00\x00\x005\n\x00\n\x14\x00\x00\x00\x00\x00**i\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc2\xf0\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x06\x02\x00\x00\x00!\x00\x00\x00\x00\x04\x00\x00@@@@@@@@@@\x00\x00@@\x9f`\x88\x80\x00\x02\x01\x00\n\x01\x00',
                        sym("wCurMenuItem"): b'\x00\x12\x11\x01\x01/\x1d\x00\x00\x00\x04\x06\x0e\x19W\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x01\x06\x00\x00\x12\x01\x01\x00\x01'
                                b'\x00\x00\x00\x00\x00\xff\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x01\x02\x01\x016\x08\x00\x00\x00\x00T'
                                b'\x8c\x80\x84\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 '
                                b'\x08\x00\x04\x04\x04\x00\x00\x00\x00\x00\x81\x01\x00P\x85\x80'
                                b'\x84\x00\x00}\x80\x80\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00)\x00\x00\x00\x00\x00y\x00\x01\x01\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x0e\x00\x1a\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\xff\xd8\x0e\x18\t\x00\x00\x00\x00\x00'
                                b'\x00\x00\x0b\xff3\x9aU\x10@\x04\x10\x0f\x01\r\xe0e\x0f\x01\x16\xde'
                                b'Y\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xba\x08\x01'
                                b'\x00\x00\x00\x02\x00\x02\x00\x00\xc1\x03\x00\x00\xc3\xc2\x01['
                                b'K\xcf\x01\x00\x00\x00\xa2\xff\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b"\x00\x00\x00\x00\x00\x00\x00\x00'\x00\x00\x14\x00\x00\x80\xc3"
                                b'0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        sym("wCardListCursorPos"): b'\x05\x00\x00\x00\x00\x06\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x1b\x16:\r)\xff\xff\xff\xff\xff+$5\xff'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x1b\x16:\r)\xff\xff\xff\xff\xff+$5\xff\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x030\x030\x030\x030\x03',
                        sym("wNamingScreenBufferLength"): b'\x00\xc5^g\x0c\t\x06\x0c\x01\x02\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00@\x01\x00 \x00\x00\x00\x0f\x06\x0c\x00\x01'
                                b'\x01\x00\x01\x01$\x02/d\xc1\x03\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x0c\x00\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x81\x82'
                                b'\x83\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06'
                                b'\x06c\x05\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x00\x00\x00\x80\x80\x80\x80\x80\x80\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x80\x00\x00\x00@\x00\x00\x00\x00\x80\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x80\x00\x00\x00\x00\x80\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x80\x00\x00\x00\x00\x80\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x80\x00\x00@\x00\x80\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x80\x00\x00\x00\x00\x80\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x80\x00\x00\x00\x00\x80\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x00\x00\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x00\x00\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x00\x04\x00 \x08\x0eE\x00\x00\x00!*\xff\x00\x00R\x9c'
                                b'c\x8cQ\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00)m\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x10\x00\x00\x00'
                                b'\x00\x00\x00\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
                                b'\x7f\xff\x7f\x00ZJ\x83\x05\xff\xff\xff\xff\xff\xff\x01\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x0f\x06\x0c0`'
                                b'\x00\x00\x00\x1e\x00\x01\x04\x028\x04\x02]f\x00\x00\xaa'
                                b'\x00\x00\x01\xf0\x00\x04#\x01\x0e\x12\x02\x00\x0e\x02\x00\x00'
                                b'\x00\x00$\x02\x06\n\x02\x00\x1e\x02\x00\x00\x00\x00%\x03'
                                b'\x16\x0c\x00\x00\x1e\x00\x00\x00\x00\x00&\x04\x0c\x04\x00\x00'
                                b'\x16\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x01#\x12\x06\x02\x02\x00\x16\x00\t'
                                b'\x00\x00\x01\x00\x00\xc1\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00<\x03\x01\x00\x00\x00\x06\x00.\xe2\x00\x00\xf0\x00\x10'
                                b'\x00\x10\x00\x00\x10\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00'
                                b'\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00p\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01E'
                                b'd\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00W\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\x8cS\x00\xc2\x00\x14\x00\x00\x01'
                                b'S\x00\xc2\x00\x14\x00\x00\x01\n\x00\xc2\x00\x14\x00\x01\x06'
                                b'\x07\x00\xc2\x00\x14\x00\x01\x06c\x00\xc2\x00\x14\x00\x01\x06'
                                b'\x97\x00\xc2\x00\x14\x00\x01\x06\x8c\x00\xc2\x00\x14\x00\x00\x06'
                                b'\x02\x00\xc2\x00\x14\x00\x00\x06\x98\x02\xc2\x00\x14\x00\x00\x06'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc2\x00\x14\x00\x00'
                                b'\x00QO\x03\x12\xbcL\x00aM\x01W\xff\x00\x00\x80\xbat,\x10\x05\x00*\x00'
                                b'\x00\x00\x00\x10\x00\x00XX\x00\xa5,\xbat\xd9t,\xe2s\xff\x00'
                                b'\x00\x00x\x80\x14\x10*\xc1Q\xd4Q*nQ\x0c\x00\x00\x008@( *\xe9U\xfcU*'
                                b'\x96U\x0e\x00\x00\x00\xb8P(\x1e*\x05U\x18U*AU\x10\x00\x00\x00h\x10'
                                b'<\x16*\xf1R\x04S*-S\x06\x00\x00\x00\x88`(\x11*\xd8Q\xdfQ*'
                                b'\x90Q\x07\x00\x00\x00(`(\x0f*\xb2Q\xbdQ*LQ\x01\x00\x00\x00\x08\xd0'
                                b'(\x10*\xc1Q\xd4Q*nQ\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00XX\x00\x00\x00,\x00\x01c\x00\x05'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'
                                b'\x08\x10\x18\x003{\x00\x00\x00\x00\x00\x00\x02\x01\x02\x03'
                                b'\x04\x05\x06\x07\x00\xe1U\x06\x00m\x00\x00\x0e\x04\x02\x02'
                                b'l\x03\xff\x01\x02\x02\x01\x0f\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00',
                        sym("wCurDeckCards") + 0x38: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        sym("hBankROM"): b'\x0b\x00\x00>\xca\xe0F>(= \xfd\xc9',
                        sym("hKeysReleased"): b'',
                        sym("hDPadHeld"): b'',
                        sym("hKeysHeld"): b'',
                        sym("hKeysPressed"): b'',
                        sym("hSCX"): b'\x00\x00\x00\x00\x00\xc3\x06\x14\xc5\xc3\x00\x00\n \x00\x00'
                                b'\xff\xff\x00\x00\x00\x00\x9f`\x06\x9a\x05\x01\x13\x0f\x00\x00'
                                b'\x00\x00\x00\x00\x1f\x03',
                        0x8000: b'\x1f\x1f\x10\x1f\x10\x1f\x10\x1f\x11\x1e\x13\x1c\x13\x1d\x11\x1e'
                                b'\xf8\xf8\x08\xf8\x08\xf8\x08\xf8\x88x\xc88\xc88\x88x\x10\x1f\x10\x1f'
                                b'\x10\x1f\x1f\x1f\x1f\x10\x1f\x1f\x1f\x10\x1f\x1f\x10\x1f\x10\x1f'
                                b'\x10\x1f\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x11\x1e\x13\x1c'
                                b'\x13\x1d\x11\x1e\x10\x1f\x10\x1f\x10\x1f\x1f\x1fc:!}!=1\x1d'
                                b'\x11\x1d1\x1dy\r\xf3\nB^b.".\x11\x16\x08\t\x06\x06\x03\x01\x00\x00'
                                b'\x00\x00\x00\x00\x01\x00\x00\x00B\x81\x00~\x81\x81\xff~\x12\nf\x14'
                                b'\xe4\x14\x88h\x10\x90``\xc0\x80\x00\x00\x00\x00\x03\x01\x06\x06\x08\t'
                                b'\x10\x17 /`/@_\xff~\x81\x81\x00~\x00\xff\x00\xff\x00\xff'
                                b'\x00\xff\x00\xff\xc0_\x80\xbf\x80\xbf\x80\xbf\x80\xbf\x80\xbf'
                                b'\x80\xbf\xc0_\x00\xff\x00\xff\x00\xff\x00\xff\x00\xff\x00\xff'
                                b"\x00\xff\x00\xff\x00\x00\x07\x07\x18\x18 '@X\x80\xa7\x97\xc8\x9f\xa0"
                                b'\xff\xff\x00\x00\x00\xff\x00\x00\x00\xff\xff\x00\xff\x00\xff\x00'
                                b'\x9f\xa0\x9f\xa0\x8f\xb0PO$#\x18\x18\x07\x07\x00\x00\xff\x00\xff\x00'
                                b'\xff\x00\xff\x00\x00\xff\x00\xff\x00\x00\xff\xff\x00\x00\x07\x07'
                                b'\x18\x18$#PN\x80\xb0\x90\xa0\x80\xa0\xff\xff\x00\x00\x00\xff\x00\x81'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x80\xb0\xd4\xc8\xe0\xa7x@? \x1f\x18'
                                b'\x07\x07\x00\x00\x00\x00\x00\x00\x81\x00\x00\xff\x00\x00\xff\x00'
                                b'\xff\x00\xff\xff\x00\x00\x00\x00\xff\xff\x80\x80\xff\x80\xff\xff'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\xff\x00\xff\xff'
                                b'\x00\x00\x00\x00\x00\x00\xe0\xe0\x10\xf0\x08\xf8\x08\xf8\xfc\x1c'
                                b'\xfc\xfc\xfe\x1e\xff\xe2\xff\xf2\x7fx\x1f\x17\x1f\x13\x0c\x0f'
                                b'\x07\x07\x00\x00\xffG\xffO\xfe\x1e\xe8\xf8\x10\xf0\xf0\xf0'
                                b'\x10\xf0\xe0\xe0\x07\x07\x08\x0f\x10\x1f\x10\x1f0?8?\x7f\x7f\xff\xff'
                                b"\xff\xff\x7f\x7f\x1f\x17<'\x1b\x1f\x08\x0f\t\x0f\x06\x06"
                                b'\x00\x00\x07\x07\x08\x0f\x10\x1f\x10\x1f0?8?\x7f\x7f\x00\x00\xe0\xe0'
                                b'\x10\xf0\x08\xf8\x08\xf8\x0c\xfc\x1c\xfc\xfe\xfe\xff\xff\xff\xff'
                                b'\x7f\x7f\x1f\x17\x1f\x13\x0c\x0f\x07\x07\x00\x00\xff\xff\xff\xff'
                                b'\xfe\xfe\xe8\xf8\x10\xf0\xf0\xf0\x10\xf0\xe0\xe0\x07\x07\x08\x0f'
                                b'\x10\x1f\x10\x1f\x10\x1f\x1f\x1f????\xe0\xe0\x10\xf08\xc8<\xcc'
                                b'\x02\xfe\xfc\x8c\xf8(\xf8(\x7f|\x7f~??\x07\x06\x07\x04\x07\x07'
                                b'\x04\x07\x03\x03\xf8\x08\xf0\x10\xe0\xe0\xc0\xc0\xc0\xc0\xc0\xc0'
                                b' \xe0\xc0\xc0\x00\x00\x07\x07\x08\x0f\x10\x1f\x10\x1f\x10\x1f'
                                b'\x1f\x1f??\x00\x00\xe0\xe0\x10\xf08\xc8<\xcc\x02\xfe\xfc\x8c\xf8('
                                b'??\x7f|\x7f~??\x1f\x1d\x1f\x19\x17\x1f\x1e\x1e\xf8(\xf8\x08'
                                b'\xf0\x10\xe0\xe0\xf8\xf8$\xfc\xc8\xf8pp\x12\x12\x1f\x1f\x1f\x1f?/?#?!'
                                b'\x7f@\x7fB?2?8\x7fO\x7fO??\x17\x1f\x11\x1f\x0e\x0e\x00\x00\x12\x12'
                                b'\x1f\x1f\x1f\x1f?/?#?!\x7f@\x00\x00HH\xf8\xf8\xf8\xf8\xfc\xf4\xfc\xc4'
                                b"\xfc\x84\xfe\x02\x7fB?2?8?'?'\x19\x1f\x0e\x0e\x00\x00\xfeB\xfeN"
                                b'\xfe\x1a\xfc\xfc\xf8\xf8\xe8\xf8\x88\xf8pp\x12\x12\x1f\x1f\x1f\x1f?/'
                                b'?#? \x7f@\x7f@?0?8\x7fO\x7f_??\x17\x1f\x11\x1f\x0e\x0e'
                                b'\x00\x00\x12\x12\x1f\x1f\x1f\x1f?/?#? \x7f@\x00\x00HH\xf8\xf8\xf8\xf8'
                                b'\xfc\xf4\xfc\xc4\xfc\x04\xfe\x02\x7f@\x7fp\x7fX??\x1f\x1f\x17\x1f'
                                b'\x13\x1f\x0e\x0e\xfe\x02\xfc\x0c\xfc\x1c\xfe\xf2\xfe\xf2\xec\xfc'
                                b'\xf0\xf0\x00\x00\x12\x12\x1f\x1f\x1f\x1f\x1f\x18\x1f\x10\x1f\x10'
                                b'\x1f\x16\x1f\x19HH\xf8\xf8\xf8\xf8\xf8\x18\xf8\x08\xf8\x08\xf8(\xf8('
                                b'\x1f\x18\x0f\x0e\x07\x07\x07\x04\x07\x04\x07\x07\x04\x07\x03\x03'
                                b'\xf8\x08\xf0\x10\xe0\xe0\xc0\xc0\xc0\xc0 \xe0 \xe0\xc0\xc0'
                                b'\x00\x00\x12\x12\x1f\x1f\x1f\x1f\x1f\x18\x1f\x10\x1f\x10\x1f\x16'
                                b'\x00\x00HH\xf8\xf8\xf8\xf8\xf8\x18\xf8\x08\xf8\x08\xf8('
                                b"\x1f\x19\x1f\x18\x0f\x0e\x07\x07\x1f\x19/9'?\x18\x18\xf8(\xf8\x08"
                                b'\xf0\x10\xe0\xe0\xf8\xf8\xe4\xfc\xc8\xf8pp\x03\x03\x0c\x0f'
                                b'\x10\x1f\x17\x1f/8/8/8?2\x1f\x12?8\x7fO\x7fO9?\x16\x1f'
                                b'\x11\x1f\x0e\x0e\x00\x00\x03\x03\x0c\x0f\x10\x1f\x17\x1f/8/8/8'
                                b"\x00\x00\xc0\xc00\xf0\x08\xf8\xe8\xf8\xf4\x1c\xf4\x1c\xf4\x1c?2?2?8?'"
                                b"?'\x19\x1f\x0e\x0e\x00\x00\xfcL\xfeJ\xfe\x1a\xfc\xfc\x98\xf8h\xf8"
                                b'\x88\xf8pp\x03\x03\x0c\x0f\x10\x1f\x10\x1f ? ?0?8/\x1c\x17?;'
                                b'\x7fO\x7f_??\x17\x1f\x11\x1f\x0e\x0e\x00\x00\x03\x03\x0c\x0f\x10\x1f'
                                b'\x10\x1f ? ?0?\x00\x00\xc0\xc00\xf0\x08\xf8\x08\xf8\x04\xfc'
                                b'\x04\xfc\x0c\xfcxo|W\x7f[??\x1f\x1f\x17\x1f\x13\x1f\x0e\x0e'
                                b'\x1c\xf48\xe8\xfc\xdc\xfe\xf2\xfe\xf2\xec\xfc\xf0\xf0\x00\x00'
                                b'\x07\x07\x08\x0f\x10\x1f\x11\x1f!?!?#>\x13\x1e\xf0\xf0\x08\xf8'
                                b'\xfc\xfc\xf8\x08\xf8\x08\xf8\x08\xf8(\xf8(\x17\x1c\x0f\x0e'
                                b'\x07\x07\x07\x04\x07\x04\x07\x07\x04\x07\x03\x03\xf8\x08\xf0\x10'
                                b'\xe0\xe0\xc0\xc0\xc0\xc0 \xe0 \xe0\xc0\xc0\x00\x00\x07\x07'
                                b'\x08\x0f\x10\x1f\x11\x1f!?!?#>\x00\x00\xf0\xf0\x08\xf8\xfc\xfc'
                                b'\xf8\x08\xf8\x08\xf8\x08\xf8(\x13\x1e\x17\x1c\x0f\x0e\x07\x07'
                                b"\x1f\x19/9'?\x18\x18\xf8(\xf8\x08\xf0\x10\xe0\xe0\xf8\xf8$\xfc"
                                b'\xc8\xf8pp\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\xae\xae\xa8\xa8\xe8\xe8\xea\xea\xea\xea'
                                b'\xaa\xaa\xae\xae\x00\x00\xa0\xa0\xe0\xe0\xe0\xe0\xa0\xa0\xa0\xa0'
                                b'\xa0\xa0\xa0\xa0\x00\x00HH\xa8\xa8\xa8\xa8\xa8\xa8\xa8\xa8\xa8\xa8NN'
                                b'\x00\x00\xcc\xcc\xaa\xaa\xaa\xaa\xaa\xaa\xae\xae\xac\xac\xca\xca'
                                b'\x00\x00JJ\xaa\xaa\xaa\xaa\xea\xea\xaa\xaa\xae\xae\xaa\xaa'
                                b'\x00\x00\xee\xee\x88\x88\x88\x88\xce\xce\x88\x88\x88\x88\xe8\xe8'
                                b'\x00\x00\xae\xae\xa4\xa4\xe4\xe4\xe4\xe4\xe4\xe4\xa4\xa4\xae\xae'
                                b'\x00\x00\x04\x04\x0c\x0c\x04\x04\x04\x04\x04\x04\x04\x04\x0e\x0e'
                                b'\x00\x00``\x80\x80\x80\x80\xe0\xe0    \xc0\xc0\x00\x00\x06\x06'
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x06\x06\x00\x00\xa4\xa4'
                                b'\xaa\xaa\xaa\xaa\xaa\xaaJJJJDD\x00\x00\xa0\xa0\xa0\xa0\xa0\xa0'
                                b'\xa0\xa0\xa0\xa0\xa0\xa0\xe0\xe0\x00\x00\xce\xce\xa8\xa8\xa8\xa8'
                                b'\xac\xac\xa8\xa8\xa8\xa8\xce\xce\x00\x00jj\x8a\x8a\x8a\x8a'
                                b'\x8c\x8c\x8a\x8a\x8a\x8ajj\x00\x00\xea\xea\x8a\x8a\x8a\x8a'
                                b'\xca\xca\x8a\x8a\x8e\x8e\xea\xea\x00\x00\xa4\xa4\xea\xea\xea\xea'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xa4\xa4\x00\x00jj\x8a\x8a\x8a\x8a\xee\xee**'
                                b'**\xca\xca\x00\x00\xa0\xa0\xa0\xa0\xa0\xa0\xc0\xc0\xa0\xa0'
                                b'\xa0\xa0\xa0\xa0\x00\x00\xea\xea\x8a\x8a\x8e\x8e\xae\xae\xae\xae'
                                b'\xaa\xaa\xea\xea\x00\x00NN\xc2\xc2BBNNBBBB\xee\xee\x00\x00\xa4\xa4'
                                b'\xaa\xaa\xaa\xaa\xca\xca\xaa\xaa\xaa\xaa\xa4\xa4\x00\x00\xec\xecJJJJ'
                                b'JJNNLLJJ\x00\x00NN\xa4\xa4\xa4\xa4\xe4\xe4\xa4\xa4\xa4\xa4\xa4\xa4'
                                b'\x00\x00\xe4\xe4JJJJNNJJJJJJ\x00\x00\xa0\xa0\xa0\xa0\xe0\xe0'
                                b'\xe0\xe0\xe0\xe0\xac\xac\xac\xac\x00\x00\xa4\xa4\xaa\xaa\xaa\xaa'
                                b'\xee\xee\xaa\xaa\xaa\xaa\xaa\xaa\x00\x00\xac\xac\xaa\xaa\xea\xea'
                                b'\xea\xea\xea\xea\xaa\xaa\xac\xac\x00\x00\xea\xeaJJNNNNNNJJ\xea\xea'
                                b'\x00\x00\xe0\xe0\x80\x80\x80\x80\xa0\xa0\xa0\xa0\xa0\xa0\xe0\xe0'
                                b'\x00\x00\xea\xea\x8a\x8a\x8e\x8e\xce\xce\x8e\x8e\x8a\x8a\xea\xea'
                                b'\x00\x00\xc4\xc4\xaa\xaa\xaa\xaa\xae\xae\xea\xea\xca\xca\xaa\xaa'
                                b'\x00\x00ff\x88\x88\x88\x88\xee\xee""""\xcc\xcc\xff\xff\xd0\x80'
                                b'\x81\x80\x82\x80\xd5\x80\xab\x80\xfe\x81\xbc\x83\xde\x81\xaf\x80'
                                b'\xff\x80\xd6\x81\xfe\x81\xe8\x87\xfa\x84\x91\x8d\xf1\x81\xae\x8e'
                                b'\xd1\x91\xa3\xac\xa0\xaf\xa5\xaa\xd3\x94\x95\x92\x8b\x88\x89\x8a'
                                b'\x93\x94\xd7\x90\xdf\x90\xd7\x90\x9b\x90\x91\x90\x89\x88\xa9\x88'
                                b'\xe8\x88\x95\x90\xab\xa0\xaf\xa0\xd5\x92\xcd\xac\xf2\x82\xa9\x81'
                                b'\xc5\x81\xaa\x80\x80\x80\xac\x80\xa2\xdd\xff\xff\xff\xff\x8b`'
                                b'\x9f`\x15b\xbe@)\xc1\xf2\x02J\x82\x12\xc2*\xc2$\xc5X\x9b \xa7EZ'
                                b'\x8b\xb4\x17o)Z\x17\xf0?\xd0]\xaa\xff\x08\xbdJ\xff\x10\xff\x00'
                                b'\xff\x00\xfd\x00\xef\x00\xb5\x00\xea\x00U\x00\xaa\x00A\x01'
                                b'\x82\x02\x03\x02\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00'
                                b'\x80\x00\xc0\x00`\x00\xb0\x80\\@\xaa \xd3\x10\xff\xff\xff\xff\x0ep'
                                b'\xbf@;\x00\xc2\xc100\x0f\xcf\x00\xf0 \xdfZ\xa5?\xc0W\xac\xbcDo\x97'
                                b'\xfe\x82\xdf#\xff\x00\xff\x00\xff\x00\xff\x00\xff\x00\xff\x00'
                                b'\xff\x00\xff\x01\xffb\xd6\x9e\xd6R{I\xeb*}%\xb5\x14\x9e\x92'
                                b'\xfaz\x03\x01\xf1\xe0>\x1c\x07\x02\x03\x01\x01\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00U\x00\xff\xff'
                                b'\xff\xff\xa9\x00]\x00\xac\x00\x08\x00\xf0\xf0\x0f\x0f\x00\xff'
                                b'\xff\x1e\xa7a\xf1\x11\xf8\x08|\x04\x8e\x82\xf3\xf1\x8d\xfc'
                                b'\xc3\x7f\xf8\x7f\xe6?\xf1\x1f\xf8\x0f\xfe\x07\xff\xf1\x9f\x0c'
                                b'\x07\x039p~L\x7f"?\x11\x9f\x8c\xc7\x83\xf0p_\x16/\t\xc1\xc0\x7f?'
                                b'\x00\x00\xbf?\xa5\xa0\xd2\x90\xedLb"g">\x1c\x15\x00\xaa\x00'
                                b'W\x00\xff\xff\xff\xff\xf7\x00A\x00\xa3\x00\x1d\x1c\xa2:Rj\x92\xea'
                                b'\xa2Z\xd1\xad\xf8\x86\xfcC_@o@W@\xbf\xc0\x7f\x03\xdc\xc4>\xf2\x8f\xf9'
                                b'G\xfc"\xfe\x11\xff\xc8\xff\xe4?\xfe\x9f\xffC\x7f \xbf \xbf\x90'
                                b'\x1f\x90?\x10\xff`\xff\x80\x7f\x00\xff\xe0?\x10\xdf\xc8\x7f(\xbf\x10'
                                b'o\x00\xbf\x00]\x02\xfe\x01U*\xfa\x05T\xab\xff\xff\xff\xff\xa5_'
                                b'\xcc37\xc8\x9ae\x8d2\xc6\x19S\x0c\xe1\x1e\x14"\xa0\x81HA)\xa0\x90P'
                                b'\xcf/\xce \xf8\x87\xfcc~q\x9c\x12\xdc\x8a\xccKn)\xbc\x93Z\xc5i\xe6'
                                b'\xd6\xd1\xfd~\xfa\x05\xfd\x02\xfa\x07\xfd\x03\xfe\x01\xff\x00'
                                b"\xfc\x00\xfb\x03\xdc'\xe8\x1e@\xbe\xe1\x1dI\xbd\xa2ZB\xb2\x85d"
                                b'\x0b\xc8\x16\xd0\xb7\xb0\xff\xff\xff\xff\x86\xff\xc7\xffN\xff'
                                b'\xb8\x7fT\xbb\x89\x7fR\xaf\xd5\x03\xe8\x03B\x01\x81\x00\x07\x00Y\x80'
                                b'\x01\x00\xb2\x81MB[DKD\xad\x82\x83\x84_DCDAB \xa1"\xa1 \xa3\'\xa2'
                                b'$\xa3\x11\x92T\xd3\t\xe8\xd5\xf4\x84\xf4\xd4\xf4\n\xe8\x08\x08tp'
                                b'\x83\x8c,\x11u\x00(\x00u\x00\xca\x00\xd5\x00\xaa\x00\xd5\x00\xff\xff'
                                b'\xff\xff\xeb\xff\xf7\xff\xb9\xf7S\xff\xaf\xffU\xff\xab\xfdS\xfd3\xed'
                                b'=\xc1\xd9\x01\xff\x01\x879;\xc5\xed\x03\xdf\x01\xab\x01'
                                b'\xd5\x01\xab\x01U\x01\xab\x01\xff\x01\xf5\x01\xf5\x01\xab\x01'
                                b'\xd5\x01k\x01\xd1\x01\x871\xc1\x07-\x01\x05\x01\xc1\x01'
                                b'\xc3\x01\xb1\x0f\x01\x01\t\x07\x07\x01\x0b\x81\x11\xc1\x83}'
                                b'\x7f\x01\xd3\x01U\x01\xab\x01U\x01\xff\xff\x00\x00\x00\x00'
                                b'\x1f\x1f\x10\x10\x10\x10\x11\x10\x13\x10\x13\x10\x00\x00\x00\x00'
                                b'\xf8\xf8\x08\x08\x08\x08\x88\x08\xc8\x08\xc8\x08\x13\x10\x13\x10'
                                b'\x11\x10\x10\x10\x10\x10\x1f\x1f\x00\x00\x00\x00\xc8\x08\xc8\x08'
                                b'\x88\x08\x08\x08\x08\x08\xf8\xf8\x00\x00\x00\x00\x00\x00\x7f\x7f@@@F'
                                b'@N@N@F@F\x00\x00\xe0\xe0      <<$$$$@F@F@O@@\x7f\x7f\x08\x08'
                                b'\x08\x08\x0f\x0f$$$$$$$$\xe4\xe4\x04\x04\x04\x04\xfc\xfc'
                                b'\xff\xff\x80\x80\x80\x9e\x80\xbf\x80\xb3\x80\xb3\x80\x86\x80\x8c'
                                b'\xc0\xc0@@ppPP\\\\TTTTTT\x80\x98\x80\xbf\x80\x80\xff\xff  ??'
                                b'\x08\x08\x0f\x0fTTTTTT\xd4\xd4\x14\x14\xf4\xf4\x04\x04\xfc\xfc'
                                b'\x00\x00\xff\xff\x80\x80\x80\x9e\x80\xbf\x80\xb3\x80\xb3\x80\x86'
                                b'\x00\x00\xc0\xc0@@@@||DDDDDD\x80\x8c\x80\x98\x80\xbf\x80\x80'
                                b'\xff\xff\x08\x08\x08\x08\x0f\x0fDDDDDDDD\xc4\xc4\x04\x04'
                                b'\x04\x04\xfc\xfc\x00\x00\xff\xff\x80\xff\x83\xff\x81\xff\x93\xff'
                                b'\xa7\xff\xbf\xff\x00\x00\xfe\xfe\x02\xfe\x82\xfe\x82\xfe\x82\xfe'
                                b'\x8a\xfe\xf2\xfe\xbf\xff\x9e\xff\xad\xff\xbc\xff\x9c\xff\x8f\xff'
                                b'\x80\xff\xff\xff\xf2\xfe\xe2\xfe\xca\xfe\xfa\xfe\xf2\xfe\xc2\xfe'
                                b'\x02\xfe\xfe\xfe\x00\x00\xff\xff\xff\x80\xff\x81\xff\x87\xff\x88'
                                b'\xff\x9e\xff\xa2\x00\x00\xfe\xfe\xfe\x02\xfe\xc2\xfeb\xfe"'
                                b'\xfe\xf2\xfe\x8a\xff\xbc\xff\xa2\xff\x98\xff\x8e\xff\x82\xff\x83'
                                b'\xff\x80\xff\xff\xfez\xfe\x8a\xfe2\xfe\xe2\xfe\x82\xfe\x82'
                                b'\xfe\x02\xfe\xfe\x00\x00\xff\xff\xff\x80\xff\x80\xff\x80\xff\x81'
                                b'\xff\x83\xff\x87\x00\x00\xfe\xfe\xfe\x02\xfeB\xfe\x82\xfe\x82'
                                b'\xfe\x02\xfe\xf2\xff\x8f\xff\x80\xff\x81\xff\x81\xff\x82\xff\x84'
                                b'\xff\x80\xff\xff\xfe\xe2\xfe\xc2\xfe\x82\xfe\x02\xfe\x02\xfe\x02'
                                b'\xfe\x02\xfe\xfe\x00\x00\xff\xff\x80\xff\x81\xff\x87\xff\x8f\xff'
                                b'\x9f\xff\xbf\xff\x00\x00\xfe\xfe\x02\xfe\xf2\xfe\xe2\xfe\xc2\xfe'
                                b'\xc2\xfe\xe2\xfe\xbf\xff\xbf\xff\xb9\xff\x98\xff\x9f\xff\x8f\xff'
                                b'\x80\xff\xff\xff\xe2\xfe\xf2\xfe\xf2\xfe\xf2\xfe\xe2\xfe\xc2\xfe'
                                b'\x02\xfe\xfe\xfe\x00\x00\xff\xff\x80\xff\xb6\xff\xb6\xff\xb6\xff'
                                b'\xb6\xff\x80\xff\x00\x00\xfe\xfe\x02\xfe\xda\xfe\xda\xfe\xda\xfe'
                                b'\xda\xfe\x02\xfe\xbe\xff\xbe\xff\xb8\xff\xbb\xff\x83\xff\x8f\xff'
                                b'\x80\xff\xff\xff\xfa\xfe\xfa\xfe\xfa\xfe\xfa\xfe\xe2\xfe\xe2\xfe'
                                b'\x02\xfe\xfe\xfe\x00\x00\xff\xff\xff\x80\xff\x80\xff\x83\xfc\x8c'
                                b'\xf3\x93\xe7\xa7\x00\x00\xfe\xfe\xfe\x02\xfe\x02\xfe\x82~b\x9e\x92NJ'
                                b'\xc7\xc7\xe7\xa4\xf3\x93\xfc\x8c\xff\x83\xff\x80\xff\x80\xff\xff'
                                b'FF\xceJ\x9e\x92~b\xfe\x82\xfe\x02\xfe\x02\xfe\xfe\x00\x00\xff\xff'
                                b'\x81\x80\x80\x81\x81\x81\xb3\x81\x8d\x9b\x87\x8f\x00\x00\xfe\xfe'
                                b'\x02\x02\x02\x02\x02\x02\x9a\x02b\xb2\xc2\xe2\x8b\x87\x87\x8f'
                                b'\x8d\x9b\xb3\x81\x81\x81\x80\x81\x81\x80\xff\xff\xa2\xc2\xc2\xe2'
                                b'b\xb2\x9a\x02\x02\x02\x02\x02\x02\x02\xfe\xfe\x00\x00\xff\xff'
                                b'\xff\x80\xff\xbf\xe0\xa0\xe0\xaf\xe7\xaf\xe0\xaf\x00\x00\xfe\xfe'
                                b'\xfe\x02\xfe\xfa\x0e\x1a\x0e\xfa\xfe\xfa\x0e\xfa\xe0\xa0\xe0\xaf'
                                b'\xe7\xaf\xe0\xaf\xe0\xa0\xff\xbf\xff\x80\xff\xff\x0e\x1a\x0e\xfa'
                                b'\xfe\xfa\x0e\xfa\x0e\x1a\xfe\xfa\xfe\x02\xfe\xfe\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10 \x08\x10'
                                b'\xb2\x18\\\xba.|\xbd,j\xc7Z<\x0c\x0c44nn\xee\xee\xde\xde\\\\0000'
                                b'\x08\x08\x10\x1000~~\xfc\xfc\x18\x18\x10\x10  \x0f\x0f\x1c<xxx\xf8'
                                b'\xfc\xfe\xfe\xfeL\xce<x(\xaa\xaa\xaa\xaa\xaa\x00\x00\xf6\xf6\xc6\xc6'
                                b'\xde\xde<<\x00\x00<<ZZ\xb5\xb5\xa5\xa5ZZ<<\x00\x00\x00\x00\x10\x10'
                                b'\x92\x92||88||\x92\x92\x10\x10\x00\x0088||\xd6\xd6\x92\x92ll8888'
                                b'\xf0\xf0  @@\xf0\xf0\x0f\x0f\x02\x02\x04\x04\x0f\x0f\x00\x00<<'
                                b'\xc2B\x9c\x9c\xa2\xa2\x9a\x9a\xc6D|8\x11\x00*\x11U;;\x7fn\x7fDn'
                                b'\x00D\x00\x00\x14\x08\x18\x1c.,D.GF\x82G\x83\x83\xfe\xfe'
                                b'\xfe\xfe\x82\xba\xaa\x92\xc6\x82\xaa\xaa\x82\xaa\x82\xc6\xfe\xfe'
                                b'\x00\x00\x92\x92DD((\x92\x92((DD\x92\x92\xe0\xc0\x98\xb0'
                                b'\x84\x8c\x83\x82\x86\x8f\x9d\xbe\xf4\xf8P`\x00\x00\xae\xac'
                                b'\xaa\xaa\xaa\xaa\xee\xec\xa8\xa8\xa8\xa8\xa8\xa8\x00\x00\x80\x80'
                                b'\xa2\xa2\xb6\xa2\x94\x94\x9c\x94\x88\x88\xe8\xe8\x00\x00\xfc\xfc'
                                b'\x80\x80\x80\x80\xfc\xfc\x80\x80\x80\x80\xfc\xfc\x00\x00\x00\x00'
                                b'\x90\x90\xd0\xd0\xf6\xd6\xf9\xb9\xb9\xb9\x96\x96\x00\x00\x10\x1088LD'
                                b'\xd6\xd6LD\\\\||\x00\x00||\xce\xce\xd6\xd6\xd6\xd6\xd6\xd6LL88'
                                b'\x00\x0088DD\x82\x82\x82\x82\x82\x82DD88\x00\x0088,\\\xde\x8e'
                                b'\xae\xde\xfe\xfe||88\x00\x00\x1f\x1f? p@hGgOdLdL\x00\x00\xf8\xf8'
                                b'\xf4\x0c\n\x06\x12\xe6\xf2\xe62&2&dLdLgOo@P` ?\x1f\x1f\x00\x002&2&'
                                b'\xf2\xe6\xf2\x06\x02\x0e\x04\xfc\xf8\xf8\x00\x00\x00\x00\xff\xff'
                                b'\xff\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\x00\x00dLdLdLdLdLdLdLdL2&2&'
                                b'2&2&2&2&2&2&\x00\x00<<BBBBBBBBBB<<\x00\x00\x08\x08\x18\x18(('
                                b'\x08\x08\x08\x08\x08\x08>>\x00\x00<<BB\x02\x02\x0c\x0c00@@~~'
                                b'\x00\x00<<BB\x02\x02\x1c\x1c\x02\x02BB<<\x00\x00\x0c\x0c\x14\x14$$'
                                b'DDDD~~\x04\x04\x00\x00~~@@||\x02\x02\x02\x02BB<<\x00\x00<<@@@@||BB'
                                b'BB<<\x00\x00~~\x02\x02\x04\x04\x08\x08\x10\x10\x10\x10\x10\x10'
                                b'\x00\x00<<BBBB<<BBBB<<\x00\x00<<BBBB>>\x02\x02\x02\x02<<'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000000\x00\x00\x00\x00'
                                b'\x00\x00\x10\x10\x10\x10||\x10\x10\x10\x10\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00||\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00DD'
                                b'((\x10\x10((DD\x00\x00\x03\x03\x06\x06\x0c\x0c\x18\x1800``\xc0\xc0'
                                b'\xfe\xfe\x83\x83\x82GGFD..,\x18\x1c\x14\x08~~B~Zf~BRRBfB~~~'
                                b'\x00\x00\x00\x00\xff\xff\xfe\x01\xff\x00\xfd\xfe\x03\x02\x03\x02'
                                b'\x00\x00\x00\x00\x00\x00\x80\x80@\xc0\xc0@\xc0@\xc0@\x03\x02\x03\x02'
                                b'\x03\x02\x03\x02\x03\x02\x03\x02\x03\x02\x03\x02\xc0@\xc0@\xc0@\xc0@'
                                b'\xc0@\xc0@\xc0@\xc0@\x03\x02\x03\x02\x03\x02\x02\x03\x01\x01\x00\x00'
                                b'\x00\x00\x00\x00\xc0@\xc0@\xbf\x7f\xff\x00\x7f\x80\xff\xff'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\xff\x00\xff\xff'
                                b'\x00\x00\x00\x00\x00\x00\x18\x18~~BBBB\x00\x00\xa6\xa6'
                                b'\xa8\xa8\xa8\xa8\xae\xae\xa2\xa2\xa2\xa2\xec\xec\x00\x00jj'
                                b'\x8a\x8a\x8a\x8a\x8e\x8e\x8a\x8a\x8a\x8ajj\x00\x00\x0c\x0c\n\n\n\n'
                                b'\x0c\x0c\n\n\n\n\x0c\x0c\x00\x00FF\xa8\xa8\xa8\xa8\xee\xee\xa2\xa2'
                                b'\xa2\xa2\xac\xac\x00\x00\xe4\xe4\x8a\x8a\x8a\x8a\xce\xce\x8a\x8a'
                                b'\x8a\x8a\xea\xea\x00\x00\x0e\x0e\n\n\n\n\n\n\x0e\x0e\x08\x08\x08\x08'
                                b'\x00\x00``\x80\x80\x80\x80\xe0\xe0  ,,\xc4\xc4\x00\x00\xe8\xe8HHHH'
                                b'HHHHHH\xee\xee\x00\x00\xee\xee\x88\x88\x88\x88\xee\xee\x88\x88'
                                b'\x88\x88\x88\x88\x00\x00\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x8c\x8c\xec\xec\x00\x00\xa8\xa8\xa8\xa8\xa8\xa8\xa8\xa8\xa8\xa8'
                                b'\xa8\xa8\xee\xee\x00\x00\x0e\x0e\x08\x08\x08\x08\x0c\x0c\x08\x08'
                                b'\x08\x08\x0e\x0e\x00\x00\xce\xce\xa8\xa8\xa8\xa8\xaa\xaa\xea\xea'
                                b'\xca\xca\xae\xae\x00\x00\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0@@@@@@'
                                b'\x00\x00\xe0\xe0\x80\x80\x80\x80\xc0\xc0\x80\x80\x80\x80\xe0\xe0'
                                b'\x00\x00\xea\xeaJJJJNNJJJJJJ\x00\x00\n\n\n\n\n\n\x0c\x0c\n\n\n\n\n\n'
                                b'\x00\x00\xe0\xe0@@@@@@@@@@@@\x00\x00\xae\xae\xa8\xa8\xe8\xe8'
                                b'\xec\xec\xe8\xe8\xa8\xa8\xae\xae\x00\x00NN\xa8\xa8\xa8\xa8'
                                b'\xae\xae\xa8\xa8\xa8\xa8HH\x00\x00ff((((NN\x02\x02\x02\x02\x0c\x0c'
                                b'\x00\x00\xe0\xe0\x80\x80\x80\x80\xa0\xa0\xa0\xa0\xac\xac\xec\xec'
                                b'\x00\x00\xe6\xe6\x88\x88\x88\x88\xc8\xc8\x88\x88\x88\x88\xe6\xe6'
                                b'\x00\x00\x0e\x0e\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04'
                                b'\x00\x00\xe8\xe8\x88\x88\x88\x88\xe8\xe8\x88\x88\x88\x88\x8e\x8e'
                                b'\x00\x00\xee\xeeJJJJJJNNHH\xe8\xe8\x00\x00\x04\x04\n\n\n\n'
                                b'\x0e\x0e\n\n\n\n\n\n\x00\x00\xe0\xe0\x80\x80\x80\x80\xe0\xe0\x80\x80'
                                b'\x80\x80\x80\x80\x00\x00LL\xaa\xaa\xaa\xaa\xea\xea\xaa\xaa'
                                b'\xaa\xaa\xac\xac\x00\x00\x0c\x0c\n\n\n\n\n\n\n\n\n\n\x0c\x0c'
                                b'\x00\x00\xea\xea\x8e\x8e\x8e\x8e\xca\xca\x8a\x8a\x8a\x8a\xea\xea'
                                b'\x00\x00\xae\xae\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xe4\xe4\xae\xae'
                                b'\x00\x00\x0e\x0e\x08\x08\x08\x08\x0e\x0e\x08\x08\x08\x08\x08\x08'
                                b'\x00\x00\x0e\x0e\x08\x08\x08\x08\n\n\n\n\n\n\x0e\x0e\x00\x00\xa6\xa6'
                                b'\xa0\xa0\xae\xae\xc8\xc8\xae\xae\xa8\xa8\xae\xae\x00\x00\xae\xae'
                                b'\xa8\xa8\xa8\xa8\xec\xec\xa8\xa8\xa8\xa8\xae\xae\x00\x00dd'
                                b'\x8a\x8a\x8a\x8a\x8a\x8a\x8a\x8a\x8a\x8add\x00\x00\xae\xae'
                                b'\xa8\xa8\xe8\xe8\xee\xee\xe8\xe8\xa8\xa8\xa8\xa8\x00\x00\xe4\xe4JJJJ'
                                b'JJJJJJDD\x00\x00@@@@@@@@@@\x00\x00@@\x00\x00\xc2\xc2\xa4\xa4\xa4\xa4'
                                b'\xa4\xa4\xa4\xa4\xa4\xa4\xc2\xc2\x00\x00\xa4\xa4\xea\xea\xea\xea'
                                b'\xae\xae\xaa\xaa\xaa\xaa\xaa\xaa\x00\x00LL\xaa\xaa\xaa\xaa'
                                b'\xea\xea\xae\xae\xac\xac\xaa\xaa\x00\x00dd\x82\x82\x82\x82\xe2\xe2""'
                                b'""\xc4\xc4\x00\x00\xc4\xc4\xaa\xaa\xaa\xaa\xaa\xaa\xea\xea'
                                b'\xca\xca\xa4\xa4\x00\x00\xe6\xe6HHHHNNBBBB\xec\xec\x00\x00\xce\xce'
                                b'\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xce\xce\x00\x00\xe4\xe4'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xea\xea\x8a\x8a\x84\x84\x00\x00\xa0\xa0'
                                b'\xa0\xa0\xe0\xe0\xe0\xe0\xe0\xe0\xa0\xa0\xa0\xa0\x00\x00\xea\xea'
                                b'\xaa\xaa\xaa\xaa\xac\xac\xea\xea\x8a\x8a\x8a\x8a\x00\x00\n\n'
                                b'\n\n\x0e\x0e\x0e\x0e\x0e\x0e\n\n\n\n\x00\x00\xec\xec\x8a\x8a\x8a\x8a'
                                b'\xca\xca\x8a\x8a\x8a\x8a\xec\xec\x00\x00\xac\xac\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xae\xae\xac\xac\xea\xea\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\xc0\xc0\xc0\xc0\x00\x00NN\xa4\xa4\xa4\xa4'
                                b'\xa4\xa4\xa4\xa4\xa4\xa4NN\x00\x00JJ\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaaNN\x00\x00\xaa\xaa\xea\xea\xee\xee\xae\xae\xae\xae'
                                b'\xaa\xaa\xaa\xaa\x00\x00JJ\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xae\xaeJJ'
                                b'\x00\x00\xec\xec\x8a\x8a\x8a\x8a\xca\xca\x8e\x8e\x8c\x8c\xea\xea'
                                b'\x00\x00\xe4\xe4\x8a\x8a\x8a\x8a\xea\xea\x8a\x8a\x8a\x8a\x84\x84'
                                b'\x00\x00\x8a\x8a\x8a\x8a\x8a\x8a\x8a\x8a\x8a\x8a\x8a\x8a\xe4\xe4'
                                b'\x00\x00\xc4\xc4\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xc4\xc4'
                                b'\x00\x00\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xe0\xe0\xa0\xa0'
                                b'\x00\x00\x0e\x0e\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x0e\x0e'
                                b'\x00\x00\xee\xeeDDDDDDDDDD\xe4\xe4\x00\x00\xee\xee\x84\x84\x84\x84'
                                b'\xe4\xe4\x84\x84\x84\x84\x8e\x8e\x00\x00\xce\xce\xa8\xa8\xa8\xa8'
                                b'\xac\xac\xe8\xe8\xc8\xc8\xae\xae\x00\x00dd\x8a\x8a\x8a\x8a\xea\xea**'
                                b'**\xc4\xc4\x00\x00\xc0\xc0\xa0\xa0\xa4\xa4\xa0\xa0\xa0\xa0'
                                b'\xa4\xa4\xc8\xc8\x00\x00\xa4\xa4\xaa\xaa\xea\xea\xea\xea\xea\xea'
                                b'\xaa\xaa\xa4\xa4\x00\x00\xae\xae\xa4\xa4\xa4\xa4\xc4\xc4\xa4\xa4'
                                b'\xa4\xa4\xae\xae\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x02\x02\x00\x00\x00tCZ<\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'! \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00QRS\x89o\x98xT\\U?P\\V\x85\x9dg\x80\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00h[\x8fifkr>o|K}xT\x97@?\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00yx\x88~w]^9ln\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x18\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c'
                                b'\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x19\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x1e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x1e\x94A\x9b\x9cu\x93M\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x1e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x1etCZ<`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x1a\x1d\x1d\x1d\x1d\x1d\x1d\x1d\x1d\x1d\x1d\x1d\x1d\x1d\x1d\x1d'
                                b'\x1d\x1d\x1d\x1b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        sym("wDoFrameFunction"): b'\xc9\x32',
                        sym("wLCDC"): b'\x00',
                        sym("wPlayerDuelistType"): b'\x00',
                        sym("wAnimationQueue"): b'\xff\xff\xff\xff\xff\xff\xff',
                        sym("wActiveScreenAnim"): b'\xff',
                        sym("wd4c0"): b'\xff',
                        sym("wDuelAnimBufferCurPos"): b'\x00',
                        sym("wDuelAnimBufferSize"): b'\x00',
                        0xFF40: b'\xc3'},
            'oracle': False,
            'why': 'The full seeded VRAM/text case enters the frame-driven Foul Gas coin animation path without an isolated ROM return; the Extended asm tail only dispatches PoisonEffect or ConfusionEffect after TossCoin.',
            'expect': {},
            'keys': [0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01,
                     0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01],
            'rom_bank': 0x0B,
            'read': {sym("wStatusConditionQueueIndex"): 0x01, sym("wStatusConditionQueue"): 0x03, sym("wRNG1"): 0x03, sym("wCoinTossTotalNum"): 0x04},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400,
            'vread': {0x00: {0x9800: 0x0400}},
            'a': 0x0B,
            'b': 0x12,
            'c': 0x03,
            'd': 0x12,
            'e': 0x01,
            'f': 0x00,
            'hl': 0x482A},
    ],
    'LassEffect': [
        {   'keys': [0x00, 0x01],
            'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("wDoFrameFunction"): b'\x22\x03',
                        sym("wDuelType"): b'\x00',
                        sym("wPlayerNumberOfCardsInDiscardPile"): b'\x00',
                        sym("wOpponentNumberOfCardsInDiscardPile"): b'\x00',
                        sym("hTempCardIndex_ff9f"): b'\x00',
                        sym("wLCDC"): b'\x00'},
            'read': {sym("hCurSelectionItem"): 0x01},
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': [0x00, 0x01],
            'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("wDoFrameFunction"): b'\x22\x03',
                        sym("wDuelType"): b'\x00',
                        sym("wPlayerNumberOfCardsInDiscardPile"): b'\x00',
                        sym("wOpponentNumberOfCardsInDiscardPile"): b'\x00',
                        sym("hTempCardIndex_ff9f"): b'\x00',
                        sym("wLCDC"): b'\x00'},
            'read': {sym("hCurSelectionItem"): 0x01},
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'Recycle_PlayerSelection': [
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'keys': [0x00, 0x01],
            'wram': {   sym("wPlayerDuelistType"): b'\x00',
                        sym("wDuelType"): b'\x00',
                        sym("wLCDC"): b'\x00',
                        sym("wRNG1"): b'\x00\x00\x80',
                        sym("wCoinTossTotalNum"): b'\xff',
                        sym("wCoinTossNumHeads"): b'\xff',
                        sym("wCoinTossDuelistType"): b'\xff',
                        sym("wCoinTossNumTossed"): b'\x01',
                        sym("wCoinTossScreenTextID"): b'\x00\x00',
                        sym("hTempCardIndex_ff98"): b'\xe1',
                        sym("hTempList"): b'\x00'},
            'read': {sym("hTempList"): 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': [0x00, 0x01],
            'wram': {   sym("wPlayerDuelistType"): b'\x00',
                        sym("wDuelType"): b'\x00',
                        sym("wLCDC"): b'\x00',
                        sym("wRNG1"): b'\x00\x00\x80',
                        sym("wCoinTossTotalNum"): b'\xff',
                        sym("wCoinTossNumHeads"): b'\xff',
                        sym("wCoinTossDuelistType"): b'\xff',
                        sym("wCoinTossScreenTextID"): b'4\x12',
                        sym("hTempCardIndex_ff98"): b'\xe1',
                        sym("hTempList"): b'\x00'},
            'read': {sym("hTempList"): 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'PokeBall_PlayerSelection': [
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'entry_sp': STACK_TOP,
            'keys': [0x00, 0x01, 0x00, 0x01, 0x00, 0x01],
            'wram': {   sym("wPlayerNumberOfCardsNotInDeck"): b'<',
                        sym("wPlayerDuelistType"): b'\x00',
                        sym("wDuelType"): b'\x00',
                        sym("wLCDC"): b'\x00',
                        sym("wRNG1"): b'\x00\x00\x80',
                        sym("wCoinTossTotalNum"): b'\xff',
                        sym("wCoinTossNumHeads"): b'\xff',
                        sym("wCoinTossDuelistType"): b'\xff',
                        sym("wCoinTossNumTossed"): b'\x01',
                        sym("wCoinTossScreenTextID"): b'\xef\x00',
                        sym("hTempCardIndex_ff98"): b'\x01',
                        sym("hTempList"): b'\x00'},
            'read': {sym("hTempList"): 0x02},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'entry_sp': STACK_TOP,
            'keys': [0x00, 0x01, 0x00, 0x01, 0x00, 0x01],
            'wram': {   sym("wPlayerNumberOfCardsNotInDeck"): b'<',
                        sym("wPlayerDuelistType"): b'\x00',
                        sym("wDuelType"): b'\x00',
                        sym("wLCDC"): b'\x00',
                        sym("wRNG1"): b'\x00\x00\x80',
                        sym("wCoinTossTotalNum"): b'\xff',
                        sym("wCoinTossNumHeads"): b'\xff',
                        sym("wCoinTossDuelistType"): b'\xff',
                        sym("wCoinTossNumTossed"): b'\x01',
                        sym("wCoinTossScreenTextID"): b'\xef\x00',
                        sym("hTempCardIndex_ff98"): b'\x01',
                        sym("hTempList"): b'\x00'},
            'read': {sym("hTempList"): 0x02},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'DuelistSelectForcedSwitch': [
        {   'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("wPlayerDuelistType"): b'\x00',
                        sym("wOpponentDuelistType"): b'\x80',
                        sym("wOpponentDeckID"): b'\x01',
                        sym("wPlayerAttackingAttackIndex"): b'\x00\x00\x08',
                        sym("wPlayerArenaCard"): b'\x00',
                        sym("wOpponentArenaCard"): b'\x00',
                        sym("wBoosterCardsDrawn"): b'\x08',
                        sym("wNameBuffer"): b'\x08'},
            'read': {sym("hTempPlayAreaLocation_ff9d"): 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("wPlayerDuelistType"): b'\x00',
                        sym("wOpponentDuelistType"): b'\x80',
                        sym("wOpponentDeckID"): b'\x01',
                        sym("wPlayerAttackingAttackIndex"): b'\x00\x00\x08',
                        sym("wPlayerArenaCard"): b'\x00',
                        sym("wOpponentArenaCard"): b'\x00',
                        sym("wBoosterCardsDrawn"): b'\x08',
                        sym("wNameBuffer"): b'\x08'},
            'read': {sym("hTempPlayAreaLocation_ff9d"): 0x01}},
        {   'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("wPlayerDuelistType"): b'\x00',
                        sym("wOpponentDuelistType"): b'\x01',
                        sym("wDuelType"): b'\x01',
                        sym("wCardPageNumber"): b'\x00',
                        sym("wNumCardsBeingDrawn") + 0xB: b'\x04',
                        sym("wSkipDuelistIsThinkingDelay"): b'\x00',
                        sym("wEnergyDiscardMenuNumerator"): b'\x00\x00\x00\x01',
                        sym("wSelectedDuelSubMenuScrollOffset"): b'\x00',
                        sym("wCardPageType"): b'\x00',
                        sym("wExcludeArenaPokemon"): b'\x00'},
            'read': {sym("hTempPlayAreaLocation_ff9d"): 0x01}},
    ],
    'PealOfThunder_RandomlyDamageEffect': [
        {'d': 0x00, 'e': 0x14,
         'wram': {sym("hWhoseTurn"): b'\xc2', sym("hTempPlayAreaLocation_ff9d"): b'\x01',
                  sym("wPlayerNumberOfPokemonInPlayArea"): b'\x01', sym("wOpponentNumberOfPokemonInPlayArea"): b'\x01',
                  sym("wPlayerArenaCard"): b'\x00', sym("wOpponentArenaCard"): b'\x00',
                  sym("wPlayerArenaCardHP"): b'P', sym("wOpponentArenaCardHP"): b'P',
                  sym("wBoosterCardsDrawn"): b'\x01', sym("wOpponentDeck"): b'\x01',
                  sym("wLCDC"): b'\x00', sym("wRNG1"): b'\x00\x00\x00', sym("wDuelFinished"): b'\x00',
                  sym("wDuelFinishParam"): b'\x00', sym("wPlayerArenaCardSubstatus1"): b'\x00', sym("wOpponentArenaCardSubstatus1"): b'\x00',
                  sym("wPlayerArenaCardStatus"): b'\x00', sym("wOpponentArenaCardStatus"): b'\x00',
                  sym("wAttackAnimationIsPlaying"): b'\x01', sym("wAnimationQueue"): b'\xff\xff\xff\xff\xff\xff\xff',
                  sym("wActiveScreenAnim"): b'\xff', sym("wd4c0"): b'\xff',
                  sym("wDuelAnimBufferCurPos"): b'\x08', sym("wDuelAnimBufferSize"): b'\x00'},
         'read': {sym("wNoDamageOrEffect"): 0x01, sym("wIsDamageToSelf"): 0x01, sym("wLoadedAttackAnimation"): 0x01},
         'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
         'instruction_budget': 0x1312D00, 'cycle_budget': 0x4C4B400,
         'oracle': False,
         'why': 'Extended asm calls HandleDestinyBondAndBetweenTurnKnockOuts after frame-driven thunder damage; the isolated oracle exceeds its frame budget.',
         'expect_regs': {'a': 0x00, 'f': 0x80}},
        {'d': 0xDD, 'e': 0xEE,
         'wram': {sym("hWhoseTurn"): b'\xc2', sym("hTempPlayAreaLocation_ff9d"): b'\x01',
                  sym("wPlayerNumberOfPokemonInPlayArea"): b'\x01', sym("wOpponentNumberOfPokemonInPlayArea"): b'\x01',
                  sym("wPlayerArenaCard"): b'\x00', sym("wOpponentArenaCard"): b'\x00',
                  sym("wPlayerArenaCardHP"): b'P', sym("wOpponentArenaCardHP"): b'P',
                  sym("wBoosterCardsDrawn"): b'\x01', sym("wOpponentDeck"): b'\x01',
                  sym("wLCDC"): b'\x00', sym("wRNG1"): b'\x00\x00\x00', sym("wDuelFinished"): b'\x00',
                  sym("wDuelFinishParam"): b'\x00', sym("wPlayerArenaCardSubstatus1"): b'\x00', sym("wOpponentArenaCardSubstatus1"): b'\x00',
                  sym("wPlayerArenaCardStatus"): b'\x00', sym("wOpponentArenaCardStatus"): b'\x00',
                  sym("wAttackAnimationIsPlaying"): b'\x01', sym("wAnimationQueue"): b'\xff\xff\xff\xff\xff\xff\xff',
                  sym("wActiveScreenAnim"): b'\xff', sym("wd4c0"): b'\xff',
                  sym("wDuelAnimBufferCurPos"): b'\x08', sym("wDuelAnimBufferSize"): b'\x00'},
         'read': {sym("wNoDamageOrEffect"): 0x01, sym("wIsDamageToSelf"): 0x01, sym("wLoadedAttackAnimation"): 0x01},
         'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
         'instruction_budget': 0x1312D00, 'cycle_budget': 0x4C4B400,
         'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'hl': 0x1234,
         'oracle': False,
         'why': 'Extended asm calls HandleDestinyBondAndBetweenTurnKnockOuts after frame-driven thunder damage; the isolated oracle exceeds its frame budget.',
         'expect_regs': {'a': 0x00, 'f': 0x80}},
    ],
    'DevolutionSpray_PlayerSelection': [
        {   'keys': [0x00, 0x02],
            'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("hTempPlayAreaLocation_ff9d"): b'\x00',
                        sym("hTempList"): b'\x00',
                        sym("wPlayerCardLocations"): b'\x10\x10',
                        sym("wPlayerArenaCard"): b'\x00',
                        sym("wPlayerArenaCardHP"): b'(',
                        sym("wPlayerArenaCardStage"): b'\x01',
                        sym("wPlayerNumberOfPokemonInPlayArea"): b'\x01',
                        sym("wBoosterCardsDrawn"): b'\t\x08',
                        sym("wLCDC"): b'\x80',
                        0xFF40: b'\x80'},
            'read': {sym("hTempList"): 0x03},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'entry_sp': WRAMX_START + 0xFE4,
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'keys': [0x00, 0x01, 0x00, 0x02, 0x00, 0x01, 0x00, 0x02],
            'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("hTempPlayAreaLocation_ff9d"): b'\x00',
                        sym("hTempList"): b'\x00',
                        sym("wPlayerCardLocations"): b'\x10\x10',
                        sym("wPlayerArenaCard"): b'\x00',
                        sym("wPlayerArenaCardHP"): b'(',
                        sym("wPlayerArenaCardStage"): b'\x01',
                        sym("wPlayerNumberOfPokemonInPlayArea"): b'\x01',
                        sym("wBoosterCardsDrawn"): b'\t\x08',
                        sym("wLCDC"): b'\x80',
                        0xFF40: b'\x80'},
            'read': {sym("hTempList"): 0x03, sym("hTempPlayAreaLocation_ff9d"): 0x01, sym("wCurPlayAreaSlot"): 0x02},
            'expect': {sym("hTempList"): b'\x00\x00\xff', sym("hTempPlayAreaLocation_ff9d"): b'\x00', sym("wCurPlayAreaSlot"): b'\x00\x00'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'entry_sp': WRAMX_START + 0xFE4,
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': [0x00, 0x01, 0x00, 0x02, 0x00, 0x01, 0x00, 0x02],
            'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("hTempPlayAreaLocation_ff9d"): b'\x00',
                        sym("hTempList"): b'\x00',
                        sym("wPlayerCardLocations"): b'\x10\x10',
                        sym("wPlayerArenaCard"): b'\x00',
                        sym("wPlayerArenaCardHP"): b'(',
                        sym("wPlayerArenaCardStage"): b'\x01',
                        sym("wPlayerNumberOfPokemonInPlayArea"): b'\x01',
                        sym("wBoosterCardsDrawn"): b'\t\x08',
                        sym("wLCDC"): b'\x80',
                        0xFF40: b'\x80'},
            'read': {sym("hTempList"): 0x03, sym("hTempPlayAreaLocation_ff9d"): 0x01, sym("wCurPlayAreaSlot"): 0x02},
            'expect': {sym("hTempList"): b'\x00\x00\xff', sym("hTempPlayAreaLocation_ff9d"): b'\x00', sym("wCurPlayAreaSlot"): b'\x00\x00'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'entry_sp': WRAMX_START + 0xFE4,
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'EnergySpike_PlayerSelectEffect': [
        {'keys': [0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x02, 0x00, 0x01],
         'oracle': False,
         'why': 'Extended asm enters the nested deck-card and play-area selection screens; the isolated oracle does not return within its frame budget with this probe-only deck state.',
         'expect': {sym("hTempList"): b'\xff'}},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD,
         'e': 0xEE, 'hl': 0x1234,
         'keys': [0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x02, 0x00, 0x01],
         'oracle': False,
         'why': 'Extended asm enters the nested deck-card and play-area selection screens; the isolated oracle does not return within its frame budget with this probe-only deck state.',
         'expect': {sym("hTempList"): b'\xff'}},
        {'keys': [0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x02, 0x00, 0x01],
         'oracle': False,
         'why': 'Extended asm enters the nested deck-card and play-area selection screens; the isolated oracle does not return within its frame budget with this probe-only deck state.',
         'expect': {sym("hTempList"): b'\xff'}},
    ],
    'StiffenEffect': [
        dict(_COIN_FIXTURE),
        dict(POISON, **_COIN_FIXTURE),
    ],
    'SupersonicEffect': [
        dict(_COIN_FIXTURE),
        dict(POISON, **_COIN_FIXTURE),
    ],
    'FurySwipes10_AIEffect': [
        dict(_DAMAGE_CASE),
        dict(POISON, **_DAMAGE_CASE),
    ],
    'FurySwipes10_MultiplierEffect': [
        dict(_COIN_FIXTURE),
        dict(POISON, **_COIN_FIXTURE),
    ],
    'DoubleKick30_AIEffect': [
        dict(_DAMAGE_CASE),
        dict(POISON, **_DAMAGE_CASE),
    ],
    'DoubleKick30_MultiplierEffect': [
        dict(_COIN_FIXTURE),
        dict(POISON, **_COIN_FIXTURE),
    ],
    'Whirlwind_SelectEffect': [
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("wOpponentNumberOfPokemonInPlayArea"): b'\x01', sym("hTempList"): b'\x00'}, 'read': {sym("hTempList"): 0x01}},
        dict(POISON, wram={sym("hWhoseTurn"): b'\xc2', sym("wOpponentNumberOfPokemonInPlayArea"): b'\x01', sym("hTempList"): b'\x55'}, read={sym("hTempList"): 0x01}),
    ],
    'Whirlwind_SwitchEffect': [
        {'wram': {sym("hTempList"): b'\xff'}},
        dict(POISON, wram={sym("hTempList"): b'\xff'}),
    ],
    'MinimizeEffect': [
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("wPlayerArenaCardSubstatus1"): b'\x00'}, 'read': {sym("wPlayerArenaCardSubstatus1"): 0x01}},
        dict(POISON, wram={sym("hWhoseTurn"): b'\xc2', sym("wPlayerArenaCardSubstatus1"): b'\x00'}, read={sym("wPlayerArenaCardSubstatus1"): 0x01}),
    ],
    'WithdrawEffect': [
        dict(_COIN_FIXTURE),
        dict(POISON, **_COIN_FIXTURE),
    ],
    'Flail_AIEffect': [
        dict(_CARD_DAMAGE_CASE),
        dict(POISON, **_CARD_DAMAGE_CASE),
    ],
    'Flail_HPCheck': [
        dict(_CARD_DAMAGE_CASE),
        dict(POISON, **_CARD_DAMAGE_CASE),
    ],
    'AgilityEffect': [
        dict(_COIN_FIXTURE),
        dict(POISON, **_COIN_FIXTURE),
    ],
    'QuickAttack_AIEffect': [
        dict(_DAMAGE_CASE),
        dict(POISON, **_DAMAGE_CASE),
    ],
    'QuickAttack_DamageBoostEffect': [
        dict(_COIN_FIXTURE),
        dict(POISON, **_COIN_FIXTURE),
    ],
    'SmokescreenEffect': [
        {'hl': sym("wPlayerCardLocations"), 'wram': {sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCardSubstatus2"): b'\x00', sym("wOpponentArenaCardLastTurnSubstatus2"): b'\x00'}, 'read': {sym("wOpponentArenaCardSubstatus2"): 0x01, sym("wOpponentArenaCardLastTurnSubstatus2"): 0x01}},
        dict(POISON, hl=sym("wPlayerCardLocations"), wram={sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCardSubstatus2"): b'\x00', sym("wOpponentArenaCardLastTurnSubstatus2"): b'\x00'}, read={sym("wOpponentArenaCardSubstatus2"): 0x01, sym("wOpponentArenaCardLastTurnSubstatus2"): 0x01}),
    ],
    'Flamethrower_CheckEnergy': [
        dict(_ENERGY_CASE),
        {'wram': {sym("wAttachedEnergies"): b'\x01\x00\x00\x00\x00\x00\x00\x00'}, 'read': {sym("wAttachedEnergies"): 0x08}},
        dict(POISON, **_ENERGY_CASE),
    ],
    'Flamethrower_PlayerSelectEffect': [
        dict(_ENERGY_SELECTION_FIXTURE),
        dict(POISON, **_ENERGY_SELECTION_FIXTURE),
    ],
    'Flamethrower_AISelectEffect': [
        {'wram': {sym("wDuelTempList"): b'\xff', sym("hTempList"): b'\x00'}, 'read': {sym("wDuelTempList"): 0x08, sym("hTempList"): 0x01}},
        dict(POISON, wram={sym("wDuelTempList"): b'\xff', sym("hTempList"): b'\x55'}, read={sym("wDuelTempList"): 0x08, sym("hTempList"): 0x01}),
        {'wram': {sym("wDuelTempList"): b'\x03\xff', sym("hTempList"): b'\x00'}, 'read': {sym("hTempList"): 0x01}},
    ],
    'Flamethrower_DiscardEffect': [
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("hTempList"): b'\x00', sym("wPlayerNumberOfCardsInDiscardPile"): b'\x00'}, 'read': {sym("hTempList"): 0x01, sym("wPlayerNumberOfCardsInDiscardPile"): 0x01, sym("wPlayerDeckCards"): 0x02}},
        dict(POISON, wram={sym("hWhoseTurn"): b'\xc2', sym("hTempList"): b'\x05', sym("wPlayerNumberOfCardsInDiscardPile"): b'\x00'}, read={sym("hTempList"): 0x01, sym("wPlayerNumberOfCardsInDiscardPile"): 0x01, sym("wPlayerDeckCards"): 0x02}),
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("hTempList"): b'\x05', sym("wPlayerNumberOfCardsInDiscardPile"): b'\x01', sym("wPlayerDeckCards"): b'\x00', sym("wPlayerArenaCardLastTurnEffect"): b'\x00'}, 'read': {sym("hTempList"): 0x01, sym("wPlayerNumberOfCardsInDiscardPile"): 0x01, sym("wPlayerDeckCards"): 0x02, sym("wPlayerArenaCardLastTurnEffect"): 0x01}},
    ],
    'Rage_AIEffect': [
        dict(_CARD_DAMAGE_CASE),
        dict(POISON, **_CARD_DAMAGE_CASE),
    ],
    'Rage_DamageBoostEffect': [
        dict(_CARD_DAMAGE_CASE),
        dict(POISON, **_CARD_DAMAGE_CASE),
    ],
    'DarkMind_PlayerSelectEffect': [
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("wOpponentNumberOfPokemonInPlayArea"): b'\x01', sym("hTempList"): b'\x00'}, 'read': {sym("hTempList"): 0x01}},
        dict(POISON, wram={sym("hWhoseTurn"): b'\xc2', sym("wOpponentNumberOfPokemonInPlayArea"): b'\x01', sym("hTempList"): b'\x55'}, read={sym("hTempList"): 0x01}),
    ],
    'DarkMind_AISelectEffect': [
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("wOpponentNumberOfPokemonInPlayArea"): b'\x01', sym("hTempList"): b'\x00'}, 'read': {sym("hTempList"): 0x01}},
        dict(POISON, wram={sym("hWhoseTurn"): b'\xc2', sym("wOpponentNumberOfPokemonInPlayArea"): b'\x01', sym("hTempList"): b'\x55'}, read={sym("hTempList"): 0x01}),
    ],
    'DarkMind_DamageBenchEffect': [
        {'wram': {sym("hTempList"): b'\xff'}},
        {'wram': {sym("hTempList"): b'\x00', sym("wNoDamageOrEffect"): b'\x01', sym("wTempPlayAreaLocation_cceb"): b'\xaa'}, 'read': {sym("wTempPlayAreaLocation_cceb"): 0x01}},
        dict(POISON, wram={sym("hTempList"): b'\x00', sym("wNoDamageOrEffect"): b'\x01', sym("wTempPlayAreaLocation_cceb"): b'\xaa'}, read={sym("wTempPlayAreaLocation_cceb"): 0x01}),
    ],
    'EnergyAbsorption_CheckDiscardPile': [
        {},
        dict(POISON),
    ],
    'EnergyAbsorption_PlayerSelectEffect': [
        dict(_ENERGY_SELECTION_FIXTURE),
        dict(POISON, **_ENERGY_SELECTION_FIXTURE),
    ],
    'EnergyAbsorption_AISelectEffect': [
        {'wram': {sym("wDuelTempList"): b'\xff', sym("hTempList"): b'\x00\x00\x00'}, 'read': {sym("hTempList"): 0x03}},
        dict(POISON, wram={sym("wDuelTempList"): b'\xff', sym("hTempList"): b'\x55\x55\x55'}, read={sym("hTempList"): 0x03}),
        {'wram': {sym("wDuelTempList"): b'\x01\x02\xff', sym("hTempList"): b'\x00\x00\x00'}, 'read': {sym("hTempList"): 0x03}},
        dict(POISON, wram={sym("wDuelTempList"): b'\x01\x02\xff', sym("hTempList"): b'\x55\x55\x55'}, read={sym("hTempList"): 0x03}),
    ],
    'EnergyAbsorption_AddToHandEffect': [
        {'wram': {sym("hTempList"): b'\xff'}, 'read': {sym("hTempList"): 0x01}},
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("hTempList"): b'\x03\xff', sym("wPlayerCardLocations") + 3: b'\x01', sym("wPlayerNumberOfCardsInDiscardPile"): b'\x01', sym("wPlayerNumberOfCardsInHand"): b'\x01', sym("wPlayerDeckCards"): b'\x00', sym("wDuelTempList"): b'\x00\x00'}, 'read': {sym("hTempList"): 0x02, sym("wPlayerCardLocations") + 3: 0x01}},
        dict(POISON, wram={sym("hWhoseTurn"): b'\xc2', sym("hTempList"): b'\x03\xff', sym("wPlayerCardLocations") + 3: b'\x22', sym("wPlayerNumberOfCardsInDiscardPile"): b'\x01', sym("wPlayerNumberOfCardsInHand"): b'\x01', sym("wPlayerDeckCards"): b'\x00', sym("wDuelTempList"): b'\x00\x00'}, read={sym("hTempList"): 0x02, sym("wPlayerCardLocations") + 3: 0x01}),
    ],
    'Amnesia_CheckAttacks': [
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCard"): b'\x00', sym("wOpponentDeck"): b'\x08'}, 'read': {sym("hWhoseTurn"): 0x01}},
        dict(POISON, wram={sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCard"): b'\x00', sym("wOpponentDeck"): b'\x08'}, read={sym("hWhoseTurn"): 0x01}),
    ],
    'Amnesia_PlayerSelectEffect': [
        dict(_ENERGY_SELECTION_FIXTURE, wram={**_ENERGY_SELECTION_FIXTURE['wram'], sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCard"): b'\x00', sym("wOpponentDeck"): b'\x08'}),
        dict(POISON, **dict(_ENERGY_SELECTION_FIXTURE, wram={**_ENERGY_SELECTION_FIXTURE['wram'], sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCard"): b'\x00', sym("wOpponentDeck"): b'\x08'})),
    ],
    'Amnesia_AISelectEffect': [
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCard"): b'\x00', sym("wOpponentDeck"): b'\x08'}, 'read': {sym("hTempList"): 0x01}},
        dict(POISON, wram={sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCard"): b'\x00', sym("wOpponentDeck"): b'\x08'}, read={sym("hTempList"): 0x01}),
    ],
    'Amnesia_DisableEffect': [
        {'a': 0x01, 'f': 0x00, 'b': 0x02, 'c': 0x03, 'd': 0x04, 'e': 0x05, 'hl': 0x00,
         'wram': {sym("hWhoseTurn"): b'\xc2', sym("wNoDamageOrEffect"): b'\x00', sym("wOpponentArenaCardSubstatus2"): b'\x00', sym("wOpponentArenaCardLastTurnSubstatus2"): b'\x00', sym("wOpponentArenaCardDisabledAttackIndex"): b'\x00', sym("wOpponentArenaCardLastTurnEffect"): b'\x00', sym("hTempList"): b'\x02'},
         'read': {sym("wOpponentArenaCardSubstatus2"): 0x01, sym("wOpponentArenaCardLastTurnSubstatus2"): 0x01, sym("wOpponentArenaCardDisabledAttackIndex"): 0x01, sym("wOpponentArenaCardLastTurnEffect"): 0x01}},
        dict(POISON, hl=0x00,
             wram={sym("hWhoseTurn"): b'\xc2', sym("wNoDamageOrEffect"): b'\x00', sym("wOpponentArenaCardSubstatus2"): b'\x11', sym("wOpponentArenaCardLastTurnSubstatus2"): b'"', sym("wOpponentArenaCardDisabledAttackIndex"): b'3', sym("wOpponentArenaCardLastTurnEffect"): b'D', sym("hTempList"): b'\x03'},
             read={sym("wOpponentArenaCardSubstatus2"): 0x01, sym("wOpponentArenaCardLastTurnSubstatus2"): 0x01, sym("wOpponentArenaCardDisabledAttackIndex"): 0x01, sym("wOpponentArenaCardLastTurnEffect"): 0x01}),
    ],
    'Meditate_AIEffect': [
        dict(_CARD_DAMAGE_CASE),
        dict(POISON, **_CARD_DAMAGE_CASE),
    ],
    'Meditate_DamageBoostEffect': [
        dict(_CARD_DAMAGE_CASE),
        dict(POISON, **_CARD_DAMAGE_CASE),
    ],
    'HardenEffect': [
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("wPlayerArenaCardSubstatus1"): b'\x00'}, 'read': {sym("wPlayerArenaCardSubstatus1"): 0x01}},
        dict(POISON, wram={sym("hWhoseTurn"): b'\xc2', sym("wPlayerArenaCardSubstatus1"): b'\x00'}, read={sym("wPlayerArenaCardSubstatus1"): 0x01}),
    ],
    'FurySwipes20_AIEffect': [
        dict(_DAMAGE_CASE),
        dict(POISON, **_DAMAGE_CASE),
    ],
    'FurySwipes20_MultiplierEffect': [
        dict(_COIN_FIXTURE),
        dict(POISON, **_COIN_FIXTURE),
    ],
    'Thunder_Recoil50PercentEffect': [
        dict(_COIN_FIXTURE),
        dict(POISON, **_COIN_FIXTURE),
    ],
    'Thunder_RecoilEffect': [
        {'f': 0x00, 'wram': {sym("hTempList"): b'\x01'}},
        dict(POISON, f=0x00, wram={sym("hTempList"): b'\x01'}),
    ],
    'GrowlEffect': [
        {'hl': sym("wPlayerCardLocations"), 'wram': {sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCardSubstatus2"): b'\x00', sym("wOpponentArenaCardLastTurnSubstatus2"): b'\x00'}, 'read': {sym("wOpponentArenaCardSubstatus2"): 0x01, sym("wOpponentArenaCardLastTurnSubstatus2"): 0x01}},
        dict(POISON, hl=sym("wPlayerCardLocations"), wram={sym("hWhoseTurn"): b'\xc2', sym("wOpponentArenaCardSubstatus2"): b'\x00', sym("wOpponentArenaCardLastTurnSubstatus2"): b'\x00'}, read={sym("wOpponentArenaCardSubstatus2"): 0x01, sym("wOpponentArenaCardLastTurnSubstatus2"): 0x01}),
    ],
    'Sonicboom_UnaffectedByColorEffect': [
        {'wram': {sym("wDamage"): b'\x00\x00'}, 'read': {sym("wDamage"): 0x02}},
        dict(POISON, wram={sym("wDamage"): b'\x00\x00'}, read={sym("wDamage"): 0x02}),
    ],
    'Sonicboom_NullEffect': [
        {'wram': {sym("wDecompressionSecondaryBufferStart") + 0x11: b'\x00'}, 'read': {sym("wDecompressionSecondaryBufferStart") + 0x11: 0x01}},
        dict(POISON, wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b'\x00'}, read={sym("wDecompressionSecondaryBufferStart") + 0x11: 0x01}),
    ],
    'HyperBeam_PlayerSelectEffect': [
        dict(_ENERGY_SELECTION_FIXTURE),
        dict(_ENERGY_SELECTION_FIXTURE, read={**_ENERGY_SELECTION_FIXTURE['read'], sym("hTempList"): 0x01}),
        dict(POISON, **dict(_ENERGY_SELECTION_FIXTURE, read={**_ENERGY_SELECTION_FIXTURE['read'], sym("hTempList"): 0x01})),
    ],
    'HyperBeam_AISelectEffect': [
        {'wram': {sym("wDuelTempList"): b'\xff', sym("hTempList"): b'\x00'}, 'read': {sym("hTempList"): 0x01}},
        dict(POISON, wram={sym("wDuelTempList"): b'\xff', sym("hTempList"): b'\x55'}, read={sym("hTempList"): 0x01}),
        {'wram': {sym("wDuelTempList"): b'\x03\xff', sym("hTempList"): b'\x00'}, 'read': {sym("hTempList"): 0x01}},
    ],
    'HyperBeam_DiscardEffect': [
        {'hl': sym("wDecompressionSecondaryBufferStart") + 0x11, 'wram': {sym("hWhoseTurn"): b'\xc2', sym("hTempList"): b'\xff', sym("wDecompressionSecondaryBufferStart") + 0x11: b'\x00'}, 'read': {sym("wDecompressionSecondaryBufferStart") + 0x11: 0x01}},
        dict(POISON, hl=sym("wDecompressionSecondaryBufferStart") + 0x11, wram={sym("hWhoseTurn"): b'\xc2', sym("hTempList"): b'\xff', sym("wDecompressionSecondaryBufferStart") + 0x11: b'\x00'}, read={sym("wDecompressionSecondaryBufferStart") + 0x11: 0x01}),
        {'hl': sym("wDecompressionSecondaryBufferStart") + 0x11, 'wram': {sym("hWhoseTurn"): b'\xc2', sym("hTempList"): b'\x05', sym("wNoDamageOrEffect"): b'\x00', sym("wPlayerNumberOfCardsInDiscardPile"): b'\x01', sym("wPlayerDeckCards"): b'\x00', sym("wPlayerArenaCardLastTurnEffect"): b'\x00'}, 'read': {sym("wDecompressionSecondaryBufferStart") + 0x11: 0x01, sym("wPlayerArenaCardLastTurnEffect"): 0x01}},
    ],
})
MUTATIONS.update({
    'SetNoEffectFromStatus': {   'source_symbol': 'SetNoEffectFromStatus',
        'before': 'wEffectFailed = EFFECT_FAILED_NO_EFFECT;',
        'after': 'wEffectFailed = EFFECT_FAILED_UNSUCCESSFUL;',
        'case_ids': ['SetNoEffectFromStatus-0', 'SetNoEffectFromStatus-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'SetDefiniteAIDamage': {   'source_symbol': 'SetDefiniteAIDamage',
        'before': 'wAIMinDamage = wDamage;',
        'after': 'wAIMinDamage = (uint8_t)(wDamage + 1u);',
        'case_ids': ['SetDefiniteAIDamage-1', 'SetDefiniteAIDamage-0', 'SetDefiniteAIDamage-2'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'CheckIfDefendingPokemonHasAnyAttack': {   'source_symbol': 'CheckIfDefendingPokemonHasAnyAttack',
        'before': 'f = (uint8_t)(category == 0u ? 0x80u : 0x00u);',
        'after': 'f = (uint8_t)(category == 0u ? 0x80u : 0x01u);',
        'case_ids': [   'CheckIfDefendingPokemonHasAnyAttack-0',
                        'CheckIfDefendingPokemonHasAnyAttack-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'KrabbyCallForFamily_AISelectEffect': {'source_symbol': 'KrabbyCallForFamily_AISelectEffect', 'before': 'if (card_id == KRABBY)', 'after': 'if (card_id != KRABBY)', 'case_ids': ['KrabbyCallForFamily_AISelectEffect-0', 'KrabbyCallForFamily_AISelectEffect-1'], 'source': 'src/home/effect_functions.c'},
    'SolarPower_CheckUse': {   'source_symbol': 'SolarPower_CheckUse',
        'before': 'return (SolarPowerCheckUseResult){0x10u, OnlyOncePerTurnText};',
        'after': 'return (SolarPowerCheckUseResult){0x90u, OnlyOncePerTurnText};',
        'case_ids': ['SolarPower_CheckUse-0'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'MirrorMove_InitialEffect1': {'source_symbol': 'MirrorMove_InitialEffect1', 'before': 'return (MirrorMoveInitialEffect1Result){0x90u, YouDidNotReceiveAnAttackToMirrorMoveText};', 'after': 'return (MirrorMoveInitialEffect1Result){0x90u, (uint16_t)(YouDidNotReceiveAnAttackToMirrorMoveText + 1u)};', 'case_ids': ['MirrorMove_InitialEffect1-0', 'MirrorMove_InitialEffect1-5'], 'source': 'src/profiles/extended/home/effect_functions.c'},
    'SwordsDanceEffect': {   'source_symbol': 'SwordsDanceEffect',
        'before': 'if (card_id != SCYTHER)',
        'after': 'if (card_id == SCYTHER)',
        'case_ids': ['SwordsDanceEffect-0', 'SwordsDanceEffect-1', 'SwordsDanceEffect-2'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'FocusEnergyEffect': {   'source_symbol': 'FocusEnergyEffect',
        'before': 'if (card_id != VAPOREON_LV29)',
        'after': 'if (card_id == VAPOREON_LV29)',
        'case_ids': ['FocusEnergyEffect-0', 'FocusEnergyEffect-1', 'FocusEnergyEffect-2'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'ClefairyMetronome_CheckAttacks': {   'source_symbol': 'ClefairyMetronome_CheckAttacks',
        'before': '\treturn (ClefairyMetronomeCheckAttacksResult){r.f, NoAttackMayBeChosenText};',
        'after': '\treturn (ClefairyMetronomeCheckAttacksResult){r.f, 0};',
        'case_ids': ['ClefairyMetronome_CheckAttacks-0', 'ClefairyMetronome_CheckAttacks-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'ClefableMetronome_CheckAttacks': {   'source_symbol': 'ClefableMetronome_CheckAttacks',
        'before': '\treturn (ClefableMetronomeCheckAttacksResult){r.f, NoAttackMayBeChosenText};',
        'after': '\treturn (ClefableMetronomeCheckAttacksResult){r.f, '
                 '(uint16_t)(NoAttackMayBeChosenText + 1u)};',
        'case_ids': ['ClefableMetronome_CheckAttacks-0', 'ClefableMetronome_CheckAttacks-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Heal_OncePerTurnCheck': {   'source_symbol': 'Heal_OncePerTurnCheck',
        'before': '\tif (flags.a & USED_PKMN_POWER_THIS_TURN)\n'
                  '\t\treturn (HealOncePerTurnCheckResult){0x10u, OnlyOncePerTurnText};',
        'after': '\tif (!(flags.a & USED_PKMN_POWER_THIS_TURN))\n'
                 '\t\treturn (HealOncePerTurnCheckResult){0x10u, OnlyOncePerTurnText};',
        'case_ids': ['Heal_OncePerTurnCheck-0', 'Heal_OncePerTurnCheck-2'],
        'source': 'src/home/effect_functions.c'},
    'StrangeBehavior_CheckDamage': {   'source_symbol': 'StrangeBehavior_CheckDamage',
        'before': 'if (hp.a < 20u)',
        'after': 'if (hp.a < 0u)',
        'case_ids': ['StrangeBehavior_CheckDamage-0', 'StrangeBehavior_CheckDamage-1'],
        'source': 'src/home/effect_functions.c'},
    'JolteonDoubleKick_MultiplierEffect': {   'source_symbol': 'JolteonDoubleKick_MultiplierEffect',
        'before': 'void JolteonDoubleKick_MultiplierEffect(void)\n'
                  '{\n'
                  '\tLoadTxRam3(20u);\n'
                  '\tTossCoinATimesResult result = TossCoinATimes(2u, 0u, 0u, 0u, 0u, '
                  'DamageCheckIfHeadsXDamageText, 10u);',
        'after': 'void JolteonDoubleKick_MultiplierEffect(void)\n'
                 '{\n'
                 '\tLoadTxRam3(20u);\n'
                 '\tTossCoinATimesResult result = TossCoinATimes(3u, 0u, 0u, 0u, 0u, '
                 'DamageCheckIfHeadsXDamageText, 10u);',
        'case_ids': [   'JolteonDoubleKick_MultiplierEffect-0',
                        'JolteonDoubleKick_MultiplierEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'CometPunch_MultiplierEffect': {   'source_symbol': 'CometPunch_MultiplierEffect',
        'before': 'void CometPunch_MultiplierEffect(void)\n'
                  '{\n'
                  '\tLoadTxRam3(20u);\n'
                  '\tTossCoinATimesResult result = TossCoinATimes(4u, 0u, 0u, 0u, 0u, '
                  'DamageCheckIfHeadsXDamageText, 20u);',
        'after': 'void CometPunch_MultiplierEffect(void)\n'
                 '{\n'
                 '\tLoadTxRam3(20u);\n'
                 '\tTossCoinATimesResult result = TossCoinATimes(5u, 0u, 0u, 0u, 0u, '
                 'DamageCheckIfHeadsXDamageText, 20u);',
        'case_ids': ['CometPunch_MultiplierEffect-0'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'PinMissile_MultiplierEffect': {   'source_symbol': 'PinMissile_MultiplierEffect',
        'before': 'void PinMissile_MultiplierEffect(void)\n'
                  '{\n'
                  '\tLoadTxRam3(20u);\n'
                  '\tTossCoinATimesResult result = TossCoinATimes(4u, 0u, 0u, 0u, '
                  '0x00u, DamageCheckIfHeadsXDamageText, 0u);\n'
                  '\tuint8_t damage = ATimes10((uint8_t)(result.a + result.a));\n'
                  '\tSetDefiniteDamage(damage);\n'
                  '}',
        'after': 'void PinMissile_MultiplierEffect(void)\n'
                 '{\n'
                 '\tLoadTxRam3(20u);\n'
                 '\tTossCoinATimesResult result = TossCoinATimes(4u, 0u, 0u, 0u, '
                 '0x00u, DamageCheckIfHeadsXDamageText, 0u);\n'
                 '\tuint8_t damage = ATimes10((uint8_t)(result.a + result.a + 1u));\n'
                 '\tSetDefiniteDamage(damage);\n'
                 '}',
        'case_ids': ['PinMissile_MultiplierEffect-0', 'PinMissile_MultiplierEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'FuryAttack_MultiplierEffect': {   'source_symbol': 'FuryAttack_MultiplierEffect',
        'before': 'void FuryAttack_MultiplierEffect(void)\n'
                  '{\n'
                  '\tLoadTxRam3(10u);\n'
                  '\tTossCoinATimesResult result = TossCoinATimes(2u, 0u, 0u, 0u, '
                  '0x00u, DamageCheckIfHeadsXDamageText, 0u);',
        'after': 'void FuryAttack_MultiplierEffect(void)\n'
                 '{\n'
                 '\tLoadTxRam3(10u);\n'
                 '\tTossCoinATimesResult result = TossCoinATimes(3u, 0u, 0u, 0u, '
                 '0x00u, DamageCheckIfHeadsXDamageText, 0u);',
        'case_ids': ['FuryAttack_MultiplierEffect-0', 'FuryAttack_MultiplierEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Bonemerang_MultiplierEffect': {   'source_symbol': 'Bonemerang_MultiplierEffect',
        'before': 'void Bonemerang_MultiplierEffect(void)\n'
                  '{\n'
                  '\tLoadTxRam3(30u);\n'
                  '\tTossCoinATimesResult result = TossCoinATimes(2u, 0u, 0u, 0u, 0u, '
                  'DamageCheckIfHeadsXDamageText, 0u);',
        'after': 'void Bonemerang_MultiplierEffect(void)\n'
                 '{\n'
                 '\tLoadTxRam3(30u);\n'
                 '\tTossCoinATimesResult result = TossCoinATimes(1u, 0u, 0u, 0u, 0u, '
                 'DamageCheckIfHeadsXDamageText, 0u);',
        'case_ids': ['Bonemerang_MultiplierEffect-0', 'Bonemerang_MultiplierEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'CloysterSpikeCannon_MultiplierEffect': {   'source_symbol': 'CloysterSpikeCannon_MultiplierEffect',
        'before': 'void CloysterSpikeCannon_MultiplierEffect(void)\n'
                  '{\n'
                  '\tLoadTxRam3(30u);\n'
                  '\tTossCoinATimesResult result = TossCoinATimes(2u, 0u, 0u, 0u, '
                  '0x00u, DamageCheckIfHeadsXDamageText, 0u);\n'
                  '\tuint8_t damage = result.a;\n'
                  '\tdamage = (uint8_t)(damage + damage);\n'
                  '\tdamage = (uint8_t)(damage + result.a);\n'
                  '\tSetDefiniteDamage(ATimes10(damage));\n'
                  '}',
        'after': 'void CloysterSpikeCannon_MultiplierEffect(void)\n'
                 '{\n'
                 '\tLoadTxRam3(30u);\n'
                 '\tTossCoinATimesResult result = TossCoinATimes(2u, 0u, 0u, 0u, '
                 '0x00u, DamageCheckIfHeadsXDamageText, 0u);\n'
                 '\tuint8_t damage = result.a;\n'
                 '\tdamage = (uint8_t)(damage + damage);\n'
                 '\tdamage = (uint8_t)(damage + result.a);\n'
                 '\tSetDefiniteDamage(ATimes10((uint8_t)(damage + 1u)));\n'
                 '}',
        'case_ids': [   'CloysterSpikeCannon_MultiplierEffect-0',
                        'CloysterSpikeCannon_MultiplierEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'DragoniteLv41Slam_MultiplierEffect': {   'source_symbol': 'DragoniteLv41Slam_MultiplierEffect',
        'before': 'void DragoniteLv41Slam_MultiplierEffect(void)\n'
                  '{\n'
                  '\tLoadTxRam3(30u);\n'
                  '\tTossCoinATimesResult result = TossCoinATimes(2u, 0u, 0u, 0u, '
                  '0x00u, DamageCheckIfHeadsXDamageText, 0u);',
        'after': 'void DragoniteLv41Slam_MultiplierEffect(void)\n'
                 '{\n'
                 '\tLoadTxRam3(30u);\n'
                 '\tTossCoinATimesResult result = TossCoinATimes(3u, 0u, 0u, 0u, '
                 '0x00u, DamageCheckIfHeadsXDamageText, 0u);',
        'case_ids': [   'DragoniteLv41Slam_MultiplierEffect-0',
                        'DragoniteLv41Slam_MultiplierEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'OmastarSpikeCannon_MultiplierEffect': {   'source_symbol': 'OmastarSpikeCannon_MultiplierEffect',
        'before': 'void OmastarSpikeCannon_MultiplierEffect(void)\n'
                  '{\n'
                  '\tLoadTxRam3(30u);\n'
                  '\tTossCoinATimesResult result = TossCoinATimes(2u, 0u, 0u, 0u, '
                  '0x00u, DamageCheckIfHeadsXDamageText, 0u);\n'
                  '\tuint8_t damage = result.a;\n'
                  '\tdamage = (uint8_t)(damage + damage);\n'
                  '\tdamage = (uint8_t)(damage + result.a);\n'
                  '\tSetDefiniteDamage(ATimes10(damage));\n'
                  '}',
        'after': 'void OmastarSpikeCannon_MultiplierEffect(void)\n'
                 '{\n'
                 '\tLoadTxRam3(30u);\n'
                 '\tTossCoinATimesResult result = TossCoinATimes(1u, 0u, 0u, 0u, '
                 '0x00u, DamageCheckIfHeadsXDamageText, 0u);\n'
                 '\tuint8_t damage = result.a;\n'
                 '\tdamage = (uint8_t)(damage + damage);\n'
                 '\tdamage = (uint8_t)(damage + result.a);\n'
                 '\tSetDefiniteDamage(ATimes10(damage));\n'
                 '}',
        'case_ids': [   'OmastarSpikeCannon_MultiplierEffect-0',
                        'OmastarSpikeCannon_MultiplierEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'DragonairSlam_MultiplierEffect': {   'source_symbol': 'DragonairSlam_MultiplierEffect',
        'before': 'void DragonairSlam_MultiplierEffect(void)\n'
                  '{\n'
                  '\tLoadTxRam3(30u);\n'
                  '\tTossCoinATimesResult result = TossCoinATimes(2u, 0u, 0u, 0u, '
                  '0x00u, DamageCheckIfHeadsXDamageText, 0u);\n'
                  '\tuint8_t damage = (uint8_t)(result.a + result.a);\n'
                  '\tdamage = (uint8_t)(damage + result.a);\n'
                  '\tSetDefiniteDamage(ATimes10(damage));',
        'after': 'void DragonairSlam_MultiplierEffect(void)\n'
                 '{\n'
                 '\tLoadTxRam3(30u);\n'
                 '\tTossCoinATimesResult result = TossCoinATimes(2u, 0u, 0u, 0u, '
                 '0x00u, DamageCheckIfHeadsXDamageText, 0u);\n'
                 '\tuint8_t damage = (uint8_t)(result.a + result.a);\n'
                 '\tdamage = (uint8_t)(damage + result.a);\n'
                 '\tSetDefiniteDamage(ATimes10((uint8_t)(damage + 1u)));',
        'case_ids': ['DragonairSlam_MultiplierEffect-0', 'DragonairSlam_MultiplierEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'GustOfWind_SwitchEffect': {'source_symbol': 'GustOfWind_SwitchEffect', 'before': '\tgb_write8(wDuelDisplayedScreen_ADDR, 0u);', 'after': '\tgb_write8(wDuelDisplayedScreen_ADDR, (uint8_t)((0u) ^ 1u));', 'case_ids': ['GustOfWind_SwitchEffect-0'], 'source': 'src/profiles/extended/home/effect_functions.c'},
    'Confusion50PercentEffect': {   'source_symbol': 'Confusion50PercentEffect',
        'before': 'uint8_t Confusion50PercentEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = TossCoin(ConfusionCheckText, 0u);\n'
                  '\tif ((toss.f & 0x10u) == 0u)\n'
                  '\t\treturn toss.f;\n'
                  '\treturn ConfusionEffect().f;',
        'after': 'uint8_t Confusion50PercentEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = TossCoin(ConfusionCheckText, 0u);\n'
                 '\tif ((toss.f & 0x10u) == 0u)\n'
                 '\t\treturn toss.f;\n'
                 '\treturn (uint8_t)(ConfusionEffect().f ^ 0x10u);',
        'case_ids': ['Confusion50PercentEffect-0', 'Confusion50PercentEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Poison50PercentEffect': {   'source_symbol': 'Poison50PercentEffect',
        'before': 'uint8_t Poison50PercentEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = TossCoin(PoisonCheckText, 0u);\n'
                  '\tif ((toss.f & 0x10u) == 0u)\n'
                  '\t\treturn toss.f;\n'
                  '\treturn PoisonEffect().f;',
        'after': 'uint8_t Poison50PercentEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = TossCoin(PoisonCheckText, 0u);\n'
                 '\tif ((toss.f & 0x10u) == 0u)\n'
                 '\t\treturn toss.f;\n'
                 '\treturn (uint8_t)(PoisonEffect().f ^ 0x10u);',
        'case_ids': ['Poison50PercentEffect-0', 'Poison50PercentEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Paralysis50PercentEffect': {   'source_symbol': 'Paralysis50PercentEffect',
        'before': 'uint8_t Paralysis50PercentEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = TossCoin(ParalysisCheckText, 0u);\n'
                  '\tif ((toss.f & 0x10u) == 0u)\n'
                  '\t\treturn toss.f;\n'
                  '\treturn ParalysisEffect().f;',
        'after': 'uint8_t Paralysis50PercentEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = TossCoin(ParalysisCheckText, 0u);\n'
                 '\tif ((toss.f & 0x10u) == 0u)\n'
                 '\t\treturn toss.f;\n'
                 '\treturn (uint8_t)(ParalysisEffect().f ^ 0x10u);',
        'case_ids': ['Paralysis50PercentEffect-0', 'Paralysis50PercentEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Sleep50PercentEffect': {   'source_symbol': 'Sleep50PercentEffect',
        'before': 'uint8_t Sleep50PercentEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = TossCoin(SleepCheckText, 0u);\n'
                  '\tif ((toss.f & 0x10u) == 0u)\n'
                  '\t\treturn toss.f;\n'
                  '\treturn SleepEffect().f;',
        'after': 'uint8_t Sleep50PercentEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = TossCoin(SleepCheckText, 0u);\n'
                 '\tif ((toss.f & 0x10u) == 0u)\n'
                 '\t\treturn toss.f;\n'
                 '\treturn (uint8_t)(SleepEffect().f ^ 0x10u);',
        'case_ids': ['Sleep50PercentEffect-0', 'Sleep50PercentEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'MoltresLv35DiveBomb_Success50PercentEffect': {   'source_symbol': 'MoltresLv35DiveBomb_Success50PercentEffect',
        'before': 'uint8_t MoltresLv35DiveBomb_Success50PercentEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = '
                  'TossCoin(SuccessCheckIfHeadsAttackIsSuccessfulText, 0u);\n'
                  '\tif ((toss.f & 0x10u) != 0u) {\n'
                  '\t\twLoadedAttackAnimation = ATK_ANIM_DIVE_BOMB;',
        'after': 'uint8_t MoltresLv35DiveBomb_Success50PercentEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = '
                 'TossCoin(SuccessCheckIfHeadsAttackIsSuccessfulText, 0u);\n'
                 '\tif ((toss.f & 0x10u) != 0u) {\n'
                 '\t\twLoadedAttackAnimation = 0x12u;',
        'case_ids': ['MoltresLv35DiveBomb_Success50PercentEffect-0'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'MoltresLv37DiveBomb_Success50PercentEffect': {   'source_symbol': 'MoltresLv37DiveBomb_Success50PercentEffect',
        'before': 'uint8_t MoltresLv37DiveBomb_Success50PercentEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = '
                  'TossCoin(SuccessCheckIfHeadsAttackIsSuccessfulText, 0u);\n'
                  '\tif ((toss.f & 0x10u) != 0u) {\n'
                  '\t\twLoadedAttackAnimation = ATK_ANIM_DIVE_BOMB;',
        'after': 'uint8_t MoltresLv37DiveBomb_Success50PercentEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = '
                 'TossCoin(SuccessCheckIfHeadsAttackIsSuccessfulText, 0u);\n'
                 '\tif ((toss.f & 0x10u) != 0u) {\n'
                 '\t\twLoadedAttackAnimation = 0x12u;',
        'case_ids': ['MoltresLv37DiveBomb_Success50PercentEffect-0'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'HornHazard_NoDamage50PercentEffect': {   'source_symbol': 'HornHazard_NoDamage50PercentEffect',
        'before': 'uint8_t HornHazard_NoDamage50PercentEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = TossCoin(DamageCheckIfTailsNoDamageText, '
                  '0u);\n'
                  '\tif ((toss.f & 0x10u) != 0u) {\n'
                  '\t\twLoadedAttackAnimation = ATK_ANIM_HIT;',
        'after': 'uint8_t HornHazard_NoDamage50PercentEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = TossCoin(DamageCheckIfTailsNoDamageText, '
                 '0u);\n'
                 '\tif ((toss.f & 0x10u) != 0u) {\n'
                 '\t\twLoadedAttackAnimation = 0x00u;',
        'case_ids': ['HornHazard_NoDamage50PercentEffect-0'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'RapidashStomp_DamageBoostEffect': {   'source_symbol': 'RapidashStomp_DamageBoostEffect',
        'before': 'void RapidashStomp_DamageBoostEffect(void)\n'
                  '{\n'
                  '\tLoadTxRam3(10u);\n'
                  '\tTossCoinRoutineResult toss = TossCoin(DamageCheckIfHeadsPlusDamageText, '
                  '0u);\n'
                  '\tif ((toss.f & 0x10u) == 0u)\n'
                  '\t\treturn;\n'
                  '\tAddToDamage(10u);',
        'after': 'void RapidashStomp_DamageBoostEffect(void)\n'
                 '{\n'
                 '\tLoadTxRam3(10u);\n'
                 '\tTossCoinRoutineResult toss = TossCoin(DamageCheckIfHeadsPlusDamageText, '
                 '0u);\n'
                 '\tif ((toss.f & 0x10u) == 0u)\n'
                 '\t\treturn;\n'
                 '\tAddToDamage(11u);',
        'case_ids': ['RapidashStomp_DamageBoostEffect-0'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'ScrunchEffect': {   'source_symbol': 'ScrunchEffect',
        'before': 'uint8_t ScrunchEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = TossCoin(IfHeadsNoDamageNextTurnText, 0u);\n'
                  '\tif ((toss.f & 0x10u) == 0u) {\n'
                  '\t\tSetWasUnsuccessful();\n'
                  '\t\treturn toss.f;\n'
                  '\t}\n'
                  '\twLoadedAttackAnimation = ATK_ANIM_SCRUNCH;',
        'after': 'uint8_t ScrunchEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = TossCoin(IfHeadsNoDamageNextTurnText, 0u);\n'
                 '\tif ((toss.f & 0x10u) == 0u) {\n'
                 '\t\tSetWasUnsuccessful();\n'
                 '\t\treturn toss.f;\n'
                 '\t}\n'
                 '\twLoadedAttackAnimation = 0x6cu;',
        'case_ids': ['ScrunchEffect-0'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'TailWagEffect': {   'source_symbol': 'TailWagEffect',
        'before': '\twLoadedAttackAnimation = ATK_ANIM_TAIL_WHIP;\n'
                  '\tApplySubstatus2ToDefendingCard(SUBSTATUS2_TAIL_WAG, hl);',
        'after': '\twLoadedAttackAnimation = 0x71u;\n'
                 '\tApplySubstatus2ToDefendingCard(SUBSTATUS2_TAIL_WAG, hl);',
        'case_ids': ['TailWagEffect-0'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'TantrumEffect': {   'source_symbol': 'TantrumEffect',
        'before': 'uint8_t TantrumEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = '
                  'TossCoin(IfTailsYourPokemonBecomesConfusedText, 0u);\n'
                  '\tif ((toss.f & 0x10u) != 0u)\n'
                  '\t\treturn toss.f;\n'
                  '\twLoadedAttackAnimation = ATK_ANIM_MULTIPLE_SLASH;',
        'after': 'uint8_t TantrumEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = '
                 'TossCoin(IfTailsYourPokemonBecomesConfusedText, 0u);\n'
                 '\tif ((toss.f & 0x10u) != 0u)\n'
                 '\t\treturn toss.f;\n'
                 '\twLoadedAttackAnimation = 0x2au;',
        'case_ids': ['TantrumEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Thunderpunch_ModifierEffect': {   'source_symbol': 'Thunderpunch_ModifierEffect',
        'before': 'void Thunderpunch_ModifierEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = '
                  'TossCoin(IfHeadPlus10IfTails10ToYourselfText, 0u);\n'
                  '\thTemp_ffa0 = toss.a;\n'
                  '\tif ((toss.f & 0x10u) == 0u)\n'
                  '\t\treturn;\n'
                  '\tAddToDamage(10u);',
        'after': 'void Thunderpunch_ModifierEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = '
                 'TossCoin(IfHeadPlus10IfTails10ToYourselfText, 0u);\n'
                 '\thTemp_ffa0 = toss.a;\n'
                 '\tif ((toss.f & 0x10u) == 0u)\n'
                 '\t\treturn;\n'
                 '\tAddToDamage(11u);',
        'case_ids': ['Thunderpunch_ModifierEffect-0', 'Thunderpunch_ModifierEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'SpacingOut_Success50PercentEffect': {   'source_symbol': 'SpacingOut_Success50PercentEffect',
        'before': 'void SpacingOut_Success50PercentEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = '
                  'TossCoin(SuccessCheckIfHeadsAttackIsSuccessfulText, 0u);\n'
                  '\thTemp_ffa0 = toss.a;\n'
                  '\tif ((toss.f & 0x10u) == 0u) {',
        'after': 'void SpacingOut_Success50PercentEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = '
                 'TossCoin(SuccessCheckIfHeadsAttackIsSuccessfulText, 0u);\n'
                 '\thTemp_ffa0 = toss.a;\n'
                 '\tif ((toss.f & 0x10u) != 0u) {',
        'case_ids': ['SpacingOut_Success50PercentEffect-0', 'SpacingOut_Success50PercentEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Thrash_ModifierEffect': {   'source_symbol': 'Thrash_ModifierEffect',
        'before': 'void Thrash_ModifierEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = '
                  'TossCoin(IfHeadPlus10IfTails10ToYourselfText, 0u);\n'
                  '\thTemp_ffa0 = toss.a;\n'
                  '\tif ((toss.f & 0x10u) == 0u)\n'
                  '\t\treturn;\n'
                  '\tAddToDamage(10u);',
        'after': 'void Thrash_ModifierEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = '
                 'TossCoin(IfHeadPlus10IfTails10ToYourselfText, 0u);\n'
                 '\thTemp_ffa0 = toss.a;\n'
                 '\tif ((toss.f & 0x10u) == 0u)\n'
                 '\t\treturn;\n'
                 '\tAddToDamage(0u);',
        'case_ids': ['Thrash_ModifierEffect-0', 'Thrash_ModifierEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'TaurosStomp_DamageBoostEffect': {   'source_symbol': 'TaurosStomp_DamageBoostEffect',
        'before': 'void TaurosStomp_DamageBoostEffect(void)\n'
                  '{\n'
                  '\tLoadTxRam3(10u);\n'
                  '\tTossCoinRoutineResult toss = TossCoin(DamageCheckIfHeadsPlusDamageText, '
                  '0u);\n'
                  '\tif ((toss.f & 0x10u) == 0u)\n'
                  '\t\treturn;\n'
                  '\tAddToDamage(10u);',
        'after': 'void TaurosStomp_DamageBoostEffect(void)\n'
                 '{\n'
                 '\tLoadTxRam3(10u);\n'
                 '\tTossCoinRoutineResult toss = TossCoin(DamageCheckIfHeadsPlusDamageText, '
                 '0u);\n'
                 '\tif ((toss.f & 0x10u) == 0u)\n'
                 '\t\treturn;\n'
                 '\tAddToDamage(11u);',
        'case_ids': ['TaurosStomp_DamageBoostEffect-0'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'ThunderJolt_Recoil50PercentEffect': {   'source_symbol': 'ThunderJolt_Recoil50PercentEffect',
        'before': 'ThunderJolt_Recoil50PercentEffectResult '
                  'ThunderJolt_Recoil50PercentEffect(void)\n'
                  '{\n'
                  '\tLoadTxRam3(10u);\n'
                  '\tTossCoinRoutineResult toss = TossCoin(IfTailsDamageToYourselfTooText, '
                  '10u);\n'
                  '\thTemp_ffa0 = toss.a;',
        'after': 'ThunderJolt_Recoil50PercentEffectResult ThunderJolt_Recoil50PercentEffect(void)\n'
                 '{\n'
                 '\tLoadTxRam3(10u);\n'
                 '\tTossCoinRoutineResult toss = TossCoin(IfTailsDamageToYourselfTooText, '
                 '10u);\n'
                 '\thTemp_ffa0 = (uint8_t)(toss.a + 1u);',
        'case_ids': [   'ThunderJolt_Recoil50PercentEffect-0',
                        'ThunderJolt_Recoil50PercentEffect-1',
                        'ThunderJolt_Recoil50PercentEffect-2'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'LeekSlap_NoDamage50PercentEffect': {   'source_symbol': 'LeekSlap_NoDamage50PercentEffect',
        'before': 'uint8_t LeekSlap_NoDamage50PercentEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = TossCoin(DamageCheckIfTailsNoDamageText, '
                  '0u);\n'
                  '\tif ((toss.f & 0x10u) != 0u)\n'
                  '\t\treturn toss.f;\n'
                  '\tSetDefiniteDamage(0u);',
        'after': 'uint8_t LeekSlap_NoDamage50PercentEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = TossCoin(DamageCheckIfTailsNoDamageText, '
                 '0u);\n'
                 '\tif ((toss.f & 0x10u) != 0u)\n'
                 '\t\treturn toss.f;\n'
                 '\tSetDefiniteDamage(1u);',
        'case_ids': ['LeekSlap_NoDamage50PercentEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Blizzard_BenchDamage50PercentEffect': {   'source_symbol': 'Blizzard_BenchDamage50PercentEffect',
        'before': 'void Blizzard_BenchDamage50PercentEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = '
                  'TossCoin(DamageToOppBenchIfHeadsDamageToYoursIfTailsText, 0u);\n'
                  '\thTemp_ffa0 = toss.a;',
        'after': 'void Blizzard_BenchDamage50PercentEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = '
                 'TossCoin(DamageToOppBenchIfHeadsDamageToYoursIfTailsText, 0u);\n'
                 '\thTemp_ffa0 = (uint8_t)(toss.a ^ 0x01u);',
        'case_ids': [   'Blizzard_BenchDamage50PercentEffect-0',
                        'Blizzard_BenchDamage50PercentEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'VenomPowder_PoisonConfusion50PercentEffect': {   'source_symbol': 'VenomPowder_PoisonConfusion50PercentEffect',
        'before': 'uint8_t VenomPowder_PoisonConfusion50PercentEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = TossCoin(VenomPowderCheckText, 0u);\n'
                  '\tif ((toss.f & 0x10u) == 0u)\n'
                  '\t\treturn toss.f;',
        'after': 'uint8_t VenomPowder_PoisonConfusion50PercentEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = TossCoin(VenomPowderCheckText, 0u);\n'
                 '\tif ((toss.f & 0x10u) != 0u)\n'
                 '\t\treturn toss.f;',
        'case_ids': [   'VenomPowder_PoisonConfusion50PercentEffect-0',
                        'VenomPowder_PoisonConfusion50PercentEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'FoulGas_PoisonOrConfusionEffect': {   'source_symbol': 'FoulGas_PoisonOrConfusionEffect',
        'before': 'uint8_t FoulGas_PoisonOrConfusionEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = '
                  'TossCoin(PoisonedIfHeadsConfusedIfTailsText, 0u);\n'
                  '\tif ((toss.f & 0x10u) == 0u)',
        'after': 'uint8_t FoulGas_PoisonOrConfusionEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = TossCoin(PoisonedIfHeadsConfusedIfTailsText, '
                 '0u);\n'
                 '\tif ((toss.f & 0x10u) != 0u)',
        'case_ids': [   'FoulGas_PoisonOrConfusionEffect-0',
                        'FoulGas_PoisonOrConfusionEffect-1',
                        'FoulGas_PoisonOrConfusionEffect-2'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'GamblerEffect': {'source_symbol': 'GamblerEffect', 'before': '\thTemp_ffa0 = toss.a;', 'after': '\thTemp_ffa0 = (uint8_t)((toss.a) ^ 1u);', 'case_ids': ['GamblerEffect-0'], 'source': 'src/profiles/extended/home/effect_functions.c'},
    'SpitPoison_Poison50PercentEffect': {   'source_symbol': 'SpitPoison_Poison50PercentEffect',
        'before': 'SpitPoison_Poison50PercentEffectResult '
                  'SpitPoison_Poison50PercentEffect(uint16_t hl)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = TossCoin(PoisonCheckText, hl);\n'
                  '\tif ((toss.f & 0x10u) != 0u) {',
        'after': 'SpitPoison_Poison50PercentEffectResult SpitPoison_Poison50PercentEffect(uint16_t '
                 'hl)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = TossCoin(PoisonCheckText, hl);\n'
                 '\tif ((toss.f & 0x10u) == 0u) {',
        'case_ids': ['SpitPoison_Poison50PercentEffect-0', 'SpitPoison_Poison50PercentEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'BigThunderEffect': {   'source_symbol': 'BigThunderEffect',
        'before': 'RandomlyDamagePlayAreaPokemonResult BigThunderEffect(uint8_t b, uint8_t c, '
                  'uint16_t de, uint16_t hl)\n'
                  '{\n'
                  '\treturn RandomlyDamagePlayAreaPokemon(70u);',
        'after': 'RandomlyDamagePlayAreaPokemonResult BigThunderEffect(uint8_t b, uint8_t c, '
                 'uint16_t de, uint16_t hl)\n'
                 '{\n'
                 '\treturn RandomlyDamagePlayAreaPokemon(0u);',
        'case_ids': ['BigThunderEffect-0', 'BigThunderEffect-1', 'BigThunderEffect-2'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'LassEffect': {'source_symbol': 'LassEffect', 'before': 'if (PROFILE_FEATURE_LINK_DUEL && wDuelType != 0u) {', 'after': 'if (wDuelType != 0u) {', 'case_ids': ['LassEffect-3'], 'source': 'src/home/effect_functions.c'},
    'TakeDownEffect': {   'source_symbol': 'TakeDownEffect',
        'before': 'DealRecoilDamageToSelf(30u, f, d, e)',
        'after': 'DealRecoilDamageToSelf(40u, f, d, e)',
        'case_ids': ['TakeDownEffect-0', 'TakeDownEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'JigglypuffDoubleEdgeEffect': {   'source_symbol': 'JigglypuffDoubleEdgeEffect',
        'before': 'DealRecoilDamageToSelf(20u, f, d, e)',
        'after': 'DealRecoilDamageToSelf(30u, f, d, e)',
        'case_ids': ['JigglypuffDoubleEdgeEffect-0', 'JigglypuffDoubleEdgeEffect-1'],
        'source': 'src/home/effect_functions.c'},
    'Recycle_PlayerSelection': {   'source_symbol': 'Recycle_PlayerSelection',
        'before': 'hTempList = 0xFFu;\n\treturn (RecyclePlayerSelectionResult){0xFFu, 0x00u};',
        'after': 'hTempList = 0x00u;\n\treturn (RecyclePlayerSelectionResult){0xFFu, 0x00u};',
        'case_ids': ['Recycle_PlayerSelection-0'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'GolemSelfdestructEffect': {   'source_symbol': 'GolemSelfdestructEffect',
        'before': 'DealDamageToAllBenchedPokemon(20u, recoil.f, 0u, 0u, 0u, 0u, 0u)',
        'after': 'DealDamageToAllBenchedPokemon(10u, recoil.f, 0u, 0u, 0u, 0u, 0u)',
        'case_ids': ['GolemSelfdestructEffect-0', 'GolemSelfdestructEffect-1'],
        'source': 'src/home/effect_functions.c'},
    'ChanseyDoubleEdgeEffect': {   'source_symbol': 'ChanseyDoubleEdgeEffect',
        'before': 'DealRecoilDamageToSelf(80u, f, d, e)',
        'after': 'DealRecoilDamageToSelf(70u, f, d, e)',
        'case_ids': ['ChanseyDoubleEdgeEffect-0', 'ChanseyDoubleEdgeEffect-1'],
        'source': 'src/home/effect_functions.c'},
    'SubmissionEffect': {   'source_symbol': 'SubmissionEffect',
        'before': 'DealRecoilDamageToSelf(20u, f, d, e)',
        'after': 'DealRecoilDamageToSelf(30u, f, d, e)',
        'case_ids': ['SubmissionEffect-0', 'SubmissionEffect-1'],
        'source': 'src/home/effect_functions.c'},
    'MagnemiteSelfdestructEffect': {   'source_symbol': 'MagnemiteSelfdestructEffect',
        'before': 'DealRecoilDamageToSelf(40u, f, d, e)',
        'after': 'DealRecoilDamageToSelf(50u, f, d, e)',
        'case_ids': ['MagnemiteSelfdestructEffect-0', 'MagnemiteSelfdestructEffect-1'],
        'source': 'src/home/effect_functions.c'},
    'Ram_RecoilSwitchEffect': {   'source_symbol': 'Ram_RecoilSwitchEffect',
        'before': 'DealRecoilDamageToSelf(20u, f, d, e)',
        'after': 'DealRecoilDamageToSelf(30u, f, d, e)',
        'case_ids': ['Ram_RecoilSwitchEffect-0', 'Ram_RecoilSwitchEffect-1'],
        'source': 'src/home/effect_functions.c'},
    'MagnetonLv35SelfdestructEffect': {   'source_symbol': 'MagnetonLv35SelfdestructEffect',
        'before': 'DealRecoilDamageToSelf(100u, f, d, e)',
        'after': 'DealRecoilDamageToSelf(90u, f, d, e)',
        'case_ids': ['MagnetonLv35SelfdestructEffect-0', 'MagnetonLv35SelfdestructEffect-1'],
        'source': 'src/home/effect_functions.c'},
    'MagnetonLv28SelfdestructEffect': {   'source_symbol': 'MagnetonLv28SelfdestructEffect',
        'before': 'DealRecoilDamageToSelf(80u, f, d, e)',
        'after': 'DealRecoilDamageToSelf(90u, f, d, e)',
        'case_ids': ['MagnetonLv28SelfdestructEffect-0', 'MagnetonLv28SelfdestructEffect-1'],
        'source': 'src/home/effect_functions.c'},
    'WeezingSelfdestructEffect': {   'source_symbol': 'WeezingSelfdestructEffect',
        'before': 'DealDamageToAllBenchedPokemon(10u, recoil.f, 0u, 0u, 0u, 0u, 0u)',
        'after': 'DealDamageToAllBenchedPokemon(20u, recoil.f, 0u, 0u, 0u, 0u, 0u)',
        'case_ids': ['WeezingSelfdestructEffect-0', 'WeezingSelfdestructEffect-1'],
        'source': 'src/home/effect_functions.c'},
    'PayDayEffect': {   'source_symbol': 'PayDayEffect',
        'before': 'void PayDayEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = TossCoin(IfHeadsDraw1CardFromDeckText, '
                  '0u);\n'
                  '\tif ((toss.f & 0x10u) != 0u) {',
        'after': 'void PayDayEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = TossCoin(IfHeadsDraw1CardFromDeckText, 0u);\n'
                 '\tif ((toss.f & 0x10u) == 0u) {',
        'case_ids': ['PayDayEffect-0', 'PayDayEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'StoneBarrage_MultiplierEffect': {'source_symbol': 'StoneBarrage_MultiplierEffect', 'before': '*gb_ptr(wCoinTossScreenTextID_ADDR) = 0x00u;', 'after': '*gb_ptr(wCoinTossScreenTextID_ADDR) = 0x01u;', 'case_ids': ['StoneBarrage_MultiplierEffect-0', 'StoneBarrage_MultiplierEffect-1'], 'source': 'src/profiles/extended/home/effect_functions.c'},
    'EnergyConversion_AddToHandEffect': {   'source_symbol': 'EnergyConversion_AddToHandEffect',
        'before': 'DealRecoilDamageToSelf(10u, f, d, e)',
        'after': 'DealRecoilDamageToSelf(20u, f, d, e)',
        'case_ids': ['EnergyConversion_AddToHandEffect-0', 'EnergyConversion_AddToHandEffect-1'],
        'source': 'src/home/effect_functions.c'},
    'Quickfreeze_Paralysis50PercentEffect': {   'source_symbol': 'Quickfreeze_Paralysis50PercentEffect',
        'before': 'uint8_t Quickfreeze_Paralysis50PercentEffect(void)\n'
                  '{\n'
                  '\tTossCoinRoutineResult toss = TossCoin(ParalysisCheckText, 0u);\n'
                  '\tuint8_t result_f;\n'
                  '\tif ((toss.f & 0x10u) == 0u) {\n'
                  '\t\tSetWasUnsuccessful();\n'
                  '\t\tDrawDuelMainScene();\n'
                  '\t\t(void)PrintFailedEffectText();\n'
                  '\t\tresult_f = WaitForWideTextBoxInput().f;\n'
                  '\t} else {\n'
                  '\t\tQueueStatusConditionResult paralysis = ParalysisEffect();\n'
                  '\t\tuint8_t location = hTempPlayAreaLocation_ff9d;\n'
                  '\t\tuint8_t turn = hWhoseTurn;\n'
                  '\t\tuint16_t animation_hl = (uint16_t)(((uint16_t)turn << 8) | '
                  '(wStatusConditionQueueIndex_ADDR & 0xffu));\n'
                  '\t\tPlayAttackAnimation(turn, paralysis.f, location, 0u, 0u, 0u, '
                  'animation_hl);\n'
                  '\t\tPlayStatusConditionQueueAnimations();\n'
                  '\t\tWaitAttackAnimation();\n'
                  '\t\t(void)ApplyStatusConditionQueue();\n'
                  '\t\tDrawDuelHUDs();\n'
                  '\t\tPrintFailedEffectTextResult failed = PrintFailedEffectText();\n'
                  '\t\tresult_f = failed.f;\n'
                  '\t\tif ((failed.f & 0x10u) != 0u)\n'
                  '\t\t\tresult_f = WaitForWideTextBoxInput().f;\n'
                  '\t}\n'
                  '\treturn result_f;\n'
                  '}',
        'after': 'uint8_t Quickfreeze_Paralysis50PercentEffect(void)\n'
                 '{\n'
                 '\tTossCoinRoutineResult toss = TossCoin(ParalysisCheckText, 0u);\n'
                 '\tuint8_t result_f;\n'
                 '\tif ((toss.f & 0x10u) == 0u) {\n'
                 '\t\tSetWasUnsuccessful();\n'
                 '\t\tDrawDuelMainScene();\n'
                 '\t\t(void)PrintFailedEffectText();\n'
                 '\t\tresult_f = WaitForWideTextBoxInput().f;\n'
                 '\t} else {\n'
                 '\t\tQueueStatusConditionResult paralysis = ParalysisEffect();\n'
                 '\t\tuint8_t location = hTempPlayAreaLocation_ff9d;\n'
                 '\t\tuint8_t turn = hWhoseTurn;\n'
                 '\t\tuint16_t animation_hl = (uint16_t)(((uint16_t)turn << 8) | '
                 '(wStatusConditionQueueIndex_ADDR & 0xffu));\n'
                 '\t\tPlayAttackAnimation(turn, paralysis.f, location, 0u, 0u, 0u, animation_hl);\n'
                 '\t\tPlayStatusConditionQueueAnimations();\n'
                 '\t\tWaitAttackAnimation();\n'
                 '\t\t(void)ApplyStatusConditionQueue();\n'
                 '\t\tDrawDuelHUDs();\n'
                 '\t\tPrintFailedEffectTextResult failed = PrintFailedEffectText();\n'
                 '\t\tresult_f = failed.f;\n'
                 '\t\tif ((failed.f & 0x10u) != 0u)\n'
                 '\t\t\tresult_f = WaitForWideTextBoxInput().f;\n'
                 '\t}\n'
                 '\treturn 0x00u;\n'
                 '}',
        'case_ids': [   'Quickfreeze_Paralysis50PercentEffect-0',
                        'Quickfreeze_Paralysis50PercentEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'PokeBall_PlayerSelection': {   'source_symbol': 'PokeBall_PlayerSelection',
        'before': 'PokeBallPlayerSelectionResult PokeBall_PlayerSelection(void)\n'
                  '{\n'
                  '\tTossCoinATimesResult toss = TossCoinATimes(1u, 0u, 0u, 0u, 0u, '
                  'TrainerCardSuccessCheckText, 0u);\n'
                  '\thTempList = toss.a;',
        'after': 'PokeBallPlayerSelectionResult PokeBall_PlayerSelection(void)\n'
                 '{\n'
                 '\tTossCoinATimesResult toss = TossCoinATimes(1u, 0u, 0u, 0u, 0u, '
                 'TrainerCardSuccessCheckText, 0u);\n'
                 '\thTempList = (uint8_t)(toss.a ^ 1u);',
        'case_ids': ['PokeBall_PlayerSelection-0'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'DuelistSelectForcedSwitch': {   'source_symbol': 'DuelistSelectForcedSwitch',
        'before': '\tuint8_t selected = AIDoAction_ForcedSwitch();\n'
                  '\thTempPlayAreaLocation_ff9d = selected;',
        'after': '\tuint8_t selected = AIDoAction_ForcedSwitch();\n'
                 '\thTempPlayAreaLocation_ff9d = (uint8_t)(selected + 1u);',
        'case_ids': ['DuelistSelectForcedSwitch-0', 'DuelistSelectForcedSwitch-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'PealOfThunder_RandomlyDamageEffect': {'source_symbol': 'PealOfThunder_RandomlyDamageEffect', 'before': 'PealOfThunderRandomlyDamageEffectResult PealOfThunder_RandomlyDamageEffect(uint8_t b, uint8_t c, uint16_t de, uint16_t hl)\n{', 'after': 'PealOfThunderRandomlyDamageEffectResult PealOfThunder_RandomlyDamageEffect(uint8_t b, uint8_t c, uint16_t de, uint16_t hl)\n{\n\tgb_write8(0xdff0u, 0xFFu);', 'case_ids': ['PealOfThunder_RandomlyDamageEffect-0'], 'source': 'src/profiles/extended/home/effect_functions.c'},
    'DevolutionSpray_PlayerSelection': {   'source_symbol': 'DevolutionSpray_PlayerSelection',
        'before': 'return (DevolutionSpray_PlayerSelectionResult){screen.a, (uint8_t)((entry_f & '
                  '0x80u) | 0x10u)};',
        'after': 'return (DevolutionSpray_PlayerSelectionResult){screen.a, (uint8_t)(entry_f & '
                 '0x80u)};',
        'case_ids': ['DevolutionSpray_PlayerSelection-0'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'EnergySpike_PlayerSelectEffect': {   'source_symbol': 'EnergySpike_PlayerSelectEffect',
        'before': '\t\t\thTemp_ffa0 = hTempCardIndex_ff98;',
        'after': '\t\t\thTemp_ffa0 = 0xffu;',
        'case_ids': ['EnergySpike_PlayerSelectEffect-0'],
        'source': 'src/home/effect_functions.c'},
    'StiffenEffect': {'source_symbol': 'StiffenEffect',
        'before': 'ApplySubstatus1ToAttackingCard(SUBSTATUS1_NO_DAMAGE_STIFFEN);',
        'after': 'ApplySubstatus1ToAttackingCard(SUBSTATUS1_NO_DAMAGE_WITHDRAW);',
        'case_ids': ['StiffenEffect-0', 'StiffenEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'SupersonicEffect': {'source_symbol': 'SupersonicEffect', 'before': '\tif ((f & 0x10u) == 0u)', 'after': '\tif (!((f & 0x10u) == 0u))', 'case_ids': ['SupersonicEffect-0'], 'source': 'src/profiles/extended/home/effect_functions.c'},
    'FurySwipes10_AIEffect': {'source_symbol': 'FurySwipes10_AIEffect',
        'before': 'SetExpectedAIDamage(15u, 0u, 30u);',
        'after': 'SetExpectedAIDamage(16u, 0u, 30u);',
        'case_ids': ['FurySwipes10_AIEffect-0', 'FurySwipes10_AIEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'FurySwipes10_MultiplierEffect': {'source_symbol': 'FurySwipes10_MultiplierEffect',
        'before': 'TossCoinATimes(3u, 0u, 0u, 0u, 0u, DamageCheckIfHeadsXDamageText, 0u);',
        'after': 'TossCoinATimes(2u, 0u, 0u, 0u, 0u, DamageCheckIfHeadsXDamageText, 0u);',
        'case_ids': ['FurySwipes10_MultiplierEffect-0', 'FurySwipes10_MultiplierEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'DoubleKick30_AIEffect': {'source_symbol': 'DoubleKick30_AIEffect',
        'before': 'SetExpectedAIDamage(30u, 0u, 60u);',
        'after': 'SetExpectedAIDamage(31u, 0u, 60u);',
        'case_ids': ['DoubleKick30_AIEffect-0', 'DoubleKick30_AIEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'DoubleKick30_MultiplierEffect': {'source_symbol': 'DoubleKick30_MultiplierEffect',
        'before': 'damage = (uint8_t)(damage + result.a);\n\tSetDefiniteDamage(ATimes10(damage));',
        'after': 'damage = 0u;\n\tSetDefiniteDamage(ATimes10(damage));',
        'case_ids': ['DoubleKick30_MultiplierEffect-0', 'DoubleKick30_MultiplierEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Whirlwind_SelectEffect': {'source_symbol': 'Whirlwind_SelectEffect',
        'before': 'hTemp_ffa0 = 0xffu;\n\t\treturn (WhirlwindSelectEffectResult){0xffu, 0x70u};',
        'after': 'hTemp_ffa0 = 0xfeu;\n\t\treturn (WhirlwindSelectEffectResult){0xffu, 0x70u};',
        'case_ids': ['Whirlwind_SelectEffect-0', 'Whirlwind_SelectEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Whirlwind_SwitchEffect': {'source_symbol': 'Whirlwind_SwitchEffect',
        'before': 'return HandleSwitchDefendingPokemonEffect(hTemp_ffa0);',
        'after': 'return HandleSwitchDefendingPokemonEffect((uint8_t)(hTemp_ffa0 + 1u));',
        'case_ids': ['Whirlwind_SwitchEffect-0', 'Whirlwind_SwitchEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'MinimizeEffect': {'source_symbol': 'MinimizeEffect',
        'before': 'SUBSTATUS1_REDUCE_BY_20',
        'after': 'SUBSTATUS1_REDUCE_BY_10',
        'case_ids': ['MinimizeEffect-0', 'MinimizeEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'WithdrawEffect': {'source_symbol': 'WithdrawEffect',
        'before': 'ApplySubstatus1ToAttackingCard(SUBSTATUS1_NO_DAMAGE_WITHDRAW);',
        'after': 'ApplySubstatus1ToAttackingCard(SUBSTATUS1_NO_DAMAGE_STIFFEN);',
        'case_ids': ['WithdrawEffect-0', 'WithdrawEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Flail_AIEffect': {'source_symbol': 'Flail_AIEffect',
        'before': 'Flail_HPCheck();\n\tSetDefiniteAIDamage();',
        'after': 'Flail_HPCheck();\n\tSetDefiniteDamage(1u);',
        'case_ids': ['Flail_AIEffect-0', 'Flail_AIEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Flail_HPCheck': {'source_symbol': 'Flail_HPCheck',
        'before': 'CardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tSetDefiniteDamage(damage.a);',
        'after': 'CardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);\n\tSetDefiniteDamage(1u);',
        'case_ids': ['Flail_HPCheck-0', 'Flail_HPCheck-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'AgilityEffect': {'source_symbol': 'AgilityEffect',
        'before': 'ApplySubstatus1ToAttackingCard(SUBSTATUS1_AGILITY);',
        'after': 'ApplySubstatus1ToAttackingCard(SUBSTATUS1_FLY);',
        'case_ids': ['AgilityEffect-0', 'AgilityEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'QuickAttack_AIEffect': {'source_symbol': 'QuickAttack_AIEffect',
        'before': 'SetExpectedAIDamage(20u, 10u, 30u);',
        'after': 'SetExpectedAIDamage(21u, 10u, 30u);',
        'case_ids': ['QuickAttack_AIEffect-0', 'QuickAttack_AIEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'QuickAttack_DamageBoostEffect': {'source_symbol': 'QuickAttack_DamageBoostEffect',
        'before': 'AddToDamage(20u);',
        'after': 'AddToDamage(21u);',
        'case_ids': ['QuickAttack_DamageBoostEffect-0', 'QuickAttack_DamageBoostEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'SmokescreenEffect': {'source_symbol': 'SmokescreenEffect',
        'before': 'SUBSTATUS2_SMOKESCREEN',
        'after': 'SUBSTATUS2_GROWL',
        'case_ids': ['SmokescreenEffect-0', 'SmokescreenEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Flamethrower_CheckEnergy': {'source_symbol': 'Flamethrower_CheckEnergy', 'before': '\t\tenergy, effect_compare(energy, 1u), NotEnoughFireEnergyText};', 'after': '\t\tenergy, effect_compare(energy, 0x0u), NotEnoughFireEnergyText};', 'case_ids': ['Flamethrower_CheckEnergy-0'], 'source': 'src/profiles/extended/home/effect_functions.c'},
    'Flamethrower_PlayerSelectEffect': {'source_symbol': 'Flamethrower_PlayerSelectEffect',
        'before': 'return PlayerPickFireEnergyCardToDiscard();',
        'after': 'return (PlayerPickFireEnergyCardToDiscardResult){0u, 0u};',
        'case_ids': ['Flamethrower_PlayerSelectEffect-0', 'Flamethrower_PlayerSelectEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Flamethrower_AISelectEffect': {'source_symbol': 'Flamethrower_AISelectEffect',
        'before': 'void Flamethrower_AISelectEffect(void)\n{\n\tAIPickFireEnergyCardToDiscard();',
        'after': 'void Flamethrower_AISelectEffect(void)\n{\n\thTemp_ffa0 = 0xffu;',
        'case_ids': ['Flamethrower_AISelectEffect-0', 'Flamethrower_AISelectEffect-1', 'Flamethrower_AISelectEffect-2'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Flamethrower_DiscardEffect': {'source_symbol': 'Flamethrower_DiscardEffect',
        'before': 'PutCardInDiscardPile(hTemp_ffa0);',
        'after': 'PutCardInDiscardPile(0u);',
        'case_ids': ['Flamethrower_DiscardEffect-0', 'Flamethrower_DiscardEffect-1', 'Flamethrower_DiscardEffect-2'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Rage_AIEffect': {'source_symbol': 'Rage_AIEffect',
        'before': 'Rage_DamageBoostEffect();\n\tSetDefiniteAIDamage();',
        'after': 'Rage_DamageBoostEffect();\n\tSetDefiniteDamage(1u);',
        'case_ids': ['Rage_AIEffect-0', 'Rage_AIEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Rage_DamageBoostEffect': {'source_symbol': 'Rage_DamageBoostEffect',
        'before': 'AddToDamage(damage.a);',
        'after': 'AddToDamage(1u);',
        'case_ids': ['Rage_DamageBoostEffect-0', 'Rage_DamageBoostEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'DarkMind_PlayerSelectEffect': {'source_symbol': 'DarkMind_PlayerSelectEffect',
        'before': 'hTemp_ffa0 = 0xffu;',
        'after': 'hTemp_ffa0 = 0xfeu;',
        'case_ids': ['DarkMind_PlayerSelectEffect-0', 'DarkMind_PlayerSelectEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'DarkMind_AISelectEffect': {'source_symbol': 'DarkMind_AISelectEffect',
        'before': 'hTemp_ffa0 = 0xffu;\n\tDuelistVarResult count =',
        'after': 'hTemp_ffa0 = 0xfeu;\n\tDuelistVarResult count =',
        'case_ids': ['DarkMind_AISelectEffect-0', 'DarkMind_AISelectEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'DarkMind_DamageBenchEffect': {'source_symbol': 'DarkMind_DamageBenchEffect',
        'before': 'uint8_t target = hTemp_ffa0;',
        'after': 'uint8_t target = hTemp_ffa0;\n\thTemp_ffa0 = 0xfeu;',
        'case_ids': ['DarkMind_DamageBenchEffect-0', 'DarkMind_DamageBenchEffect-1', 'DarkMind_DamageBenchEffect-2'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'EnergyAbsorption_CheckDiscardPile': {'source_symbol': 'EnergyAbsorption_CheckDiscardPile',
        'before': 'ThereAreNoEnergyCardsInDiscardPileText, list.f',
        'after': 'NoCardsLeftInTheDeckText, list.f',
        'case_ids': ['EnergyAbsorption_CheckDiscardPile-0', 'EnergyAbsorption_CheckDiscardPile-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'EnergyAbsorption_PlayerSelectEffect': {'source_symbol': 'EnergyAbsorption_PlayerSelectEffect',
        'before': 'return HandleEnergyCardsInDiscardPileSelection(\n\t\tChoose2EnergyCardsFromDiscardPileToAttachText);',
        'after': 'return (HandleEnergyCardsInDiscardPileSelectionResult){0u, 0u, 0u};',
        'case_ids': ['EnergyAbsorption_PlayerSelectEffect-0', 'EnergyAbsorption_PlayerSelectEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'EnergyAbsorption_AISelectEffect': {'source_symbol': 'EnergyAbsorption_AISelectEffect',
        'before': 'gb_write8(dst, 0xffu);\n\t\t\treturn;',
        'after': 'gb_write8(dst, 0xfeu);\n\t\t\treturn;',
        'case_ids': ['EnergyAbsorption_AISelectEffect-0', 'EnergyAbsorption_AISelectEffect-1', 'EnergyAbsorption_AISelectEffect-2', 'EnergyAbsorption_AISelectEffect-3'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'EnergyAbsorption_AddToHandEffect': {'source_symbol': 'EnergyAbsorption_AddToHandEffect',
        'before': 'gb_write8(location.hl, CARD_LOCATION_ARENA);',
        'after': 'gb_write8(location.hl, CARD_LOCATION_HAND);',
        'case_ids': ['EnergyAbsorption_AddToHandEffect-1', 'EnergyAbsorption_AddToHandEffect-2'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Amnesia_CheckAttacks': {'source_symbol': 'Amnesia_CheckAttacks',
        'before': 'return (ClefableMetronomeCheckAttacksResult){attacks.f, NoAttackMayBeChosenText};',
        'after': 'return (ClefableMetronomeCheckAttacksResult){attacks.f, 0u};',
        'case_ids': ['Amnesia_CheckAttacks-0', 'Amnesia_CheckAttacks-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Amnesia_PlayerSelectEffect': {'source_symbol': 'Amnesia_PlayerSelectEffect',
        'before': 'return PlayerPickAttackForAmnesia();',
        'after': 'return (PlayerPickAttackForAmnesiaResult){0u, 0u};',
        'case_ids': ['Amnesia_PlayerSelectEffect-0', 'Amnesia_PlayerSelectEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Amnesia_AISelectEffect': {'source_symbol': 'Amnesia_AISelectEffect',
        'before': 'hTemp_ffa0 = attack;',
        'after': 'hTemp_ffa0 = 0xffu;',
        'case_ids': ['Amnesia_AISelectEffect-0', 'Amnesia_AISelectEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Amnesia_DisableEffect': {'source_symbol': 'Amnesia_DisableEffect',
        'before': 'ApplyAmnesiaToAttack(a, f, b, c, d, e, hl);',
        'after': '(void)hl;',
        'case_ids': ['Amnesia_DisableEffect-0', 'Amnesia_DisableEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Meditate_AIEffect': {'source_symbol': 'Meditate_AIEffect',
        'before': 'Meditate_DamageBoostEffect();\n\tSetDefiniteAIDamage();',
        'after': 'Meditate_DamageBoostEffect();\n\tSetDefiniteDamage(1u);',
        'case_ids': ['Meditate_AIEffect-0', 'Meditate_AIEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Meditate_DamageBoostEffect': {'source_symbol': 'Meditate_DamageBoostEffect',
        'before': 'AddToDamage(damage.a);',
        'after': 'AddToDamage(1u);',
        'case_ids': ['Meditate_DamageBoostEffect-0', 'Meditate_DamageBoostEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'HardenEffect': {'source_symbol': 'HardenEffect',
        'before': 'SUBSTATUS1_PREVENT_LESS_THAN_40',
        'after': 'SUBSTATUS1_REDUCE_BY_20',
        'case_ids': ['HardenEffect-0', 'HardenEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'FurySwipes20_AIEffect': {'source_symbol': 'FurySwipes20_AIEffect',
        'before': 'SetExpectedAIDamage(30u, 0u, 60u);',
        'after': 'SetExpectedAIDamage(31u, 0u, 60u);',
        'case_ids': ['FurySwipes20_AIEffect-0', 'FurySwipes20_AIEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'FurySwipes20_MultiplierEffect': {'source_symbol': 'FurySwipes20_MultiplierEffect',
        'before': 'uint8_t damage = (uint8_t)(result.a + result.a);\n\tSetDefiniteDamage(ATimes10(damage));',
        'after': 'uint8_t damage = 0u;\n\tSetDefiniteDamage(ATimes10(damage));',
        'case_ids': ['FurySwipes20_MultiplierEffect-0', 'FurySwipes20_MultiplierEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Thunder_Recoil50PercentEffect': {'source_symbol': 'Thunder_Recoil50PercentEffect',
        'before': 'TossCoin(IfTailsDamageToYourselfTooText, 30u);',
        'after': 'TossCoin(IfTailsDamageToYourselfTooText, 31u);',
        'case_ids': ['Thunder_Recoil50PercentEffect-0', 'Thunder_Recoil50PercentEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Thunder_RecoilEffect': {'source_symbol': 'Thunder_RecoilEffect', 'before': '\t\treturn (ThunderRecoilEffectResult){coin, 0x00u};', 'after': '\t\treturn (ThunderRecoilEffectResult){(uint8_t)((coin) ^ 1u), 0x00u};', 'case_ids': ['Thunder_RecoilEffect-0'], 'source': 'src/profiles/extended/home/effect_functions.c'},
    'GrowlEffect': {'source_symbol': 'GrowlEffect',
        'before': 'SUBSTATUS2_GROWL',
        'after': 'SUBSTATUS2_SMOKESCREEN',
        'case_ids': ['GrowlEffect-0', 'GrowlEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Sonicboom_UnaffectedByColorEffect': {'source_symbol': 'Sonicboom_UnaffectedByColorEffect',
        'before': '1u << UNAFFECTED_BY_WEAKNESS_RESISTANCE_F',
        'after': '1u << RESISTANCE',
        'case_ids': ['Sonicboom_UnaffectedByColorEffect-0', 'Sonicboom_UnaffectedByColorEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'Sonicboom_NullEffect': {'source_symbol': 'Sonicboom_NullEffect',
        'before': 'void Sonicboom_NullEffect(void)\n{\n\treturn;',
        'after': 'void Sonicboom_NullEffect(void)\n{\n\tgb_write8(0xC100u, 0xFFu);',
        'case_ids': ['Sonicboom_NullEffect-0', 'Sonicboom_NullEffect-1'],
        'source': 'src/profiles/extended/home/effect_functions.c'},
    'HyperBeam_PlayerSelectEffect': {'source_symbol': 'HyperBeam_PlayerSelectEffect', 'before': 'hTemp_ffa0 = 0xffu;', 'after': 'hTemp_ffa0 = 0x00u;', 'case_ids': ['HyperBeam_PlayerSelectEffect-0', 'HyperBeam_PlayerSelectEffect-1', 'HyperBeam_PlayerSelectEffect-2'], 'source': 'src/profiles/extended/home/effect_functions.c'},
    'HyperBeam_AISelectEffect': {'source_symbol': 'HyperBeam_AISelectEffect', 'before': '\thTemp_ffa0 = selected.a;', 'after': '\thTemp_ffa0 = (uint8_t)((selected.a) ^ 1u);', 'case_ids': ['HyperBeam_AISelectEffect-0'], 'source': 'src/profiles/extended/home/effect_functions.c'},
    'HyperBeam_DiscardEffect': {'source_symbol': 'HyperBeam_DiscardEffect', 'before': '\tif (no_effect.f & 0x10u)', 'after': '\tif (!(no_effect.f & 0x10u))', 'case_ids': ['HyperBeam_DiscardEffect-2'], 'source': 'src/profiles/extended/home/effect_functions.c'},
})
CASES['LassEffect'] = [
    *CASES['LassEffect'],
    lass_hand_fixture((const("LASS"),), (const("POTION"),)),
    lass_hand_fixture((const("GRASS_ENERGY"),) * 7, (const("LASS"),), ai_turn=True, duel_type=0x81),
]
MUTATIONS['LassEffect'] = {
    'source': 'src/home/effect_functions.c', 'source_symbol': 'LassEffect',
    'before': 'if (PROFILE_FEATURE_LINK_DUEL && wDuelType != 0u)',
    'after': 'if (wDuelType != 0u)',
    'case_ids': ['LassEffect-3'],
}
MUTATIONS['NidoranFCallForFamily_PlayerSelectEffect'] = {
    'source': 'src/profiles/extended/home/effect_functions.c',
    'source_symbol': 'NIDORAN_F_CANCEL_CHECK_M',
    'before': '#define NIDORAN_F_CANCEL_CHECK_M 1',
    'after': '#define NIDORAN_F_CANCEL_CHECK_M 0',
    'case_ids': ['NidoranFCallForFamily_PlayerSelectEffect-2'],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
for _name in (
    "ChanseyDoubleEdgeEffect",
    "JigglypuffDoubleEdgeEffect",
    "TakeDownEffect",
    "SubmissionEffect",
    "GolemSelfdestructEffect",
    "MagnemiteSelfdestructEffect",
    "MagnetonLv28SelfdestructEffect",
    "MagnetonLv35SelfdestructEffect",
    "Ram_RecoilSwitchEffect",
    "WeezingSelfdestructEffect",
    "EnergyConversion_AddToHandEffect",
):
    for _index, _record in enumerate(SCHEMA2_CASES[_name]):
        _completion = {
            "mode": "entry",
            "pc": sym("PlayAttackAnimation_DealAttackDamageSimple"),
            "bank": sym_bank("PlayAttackAnimation_DealAttackDamageSimple"),
            "routine": "PlayAttackAnimation_DealAttackDamageSimple",
        }
        _record["completion"] = _completion
        _record["compare"] = ()
        CASES[_name][_index]["completion"] = dict(_completion)
        CASES[_name][_index]["compare"] = ()
for _record in SCHEMA2_CASES["EnergySpike_PlayerSelectEffect"][:1]:
    _record.pop("oracle", None)
    _record.pop("why", None)
    _record.pop("expect", None)
    _record["completion"] = {
        "mode": "entry",
        "pc": sym("LookForCardsInDeck"),
        "bank": sym_bank("LookForCardsInDeck"),
        "routine": "LookForCardsInDeck",
    }
    _record["compare"] = ()
for _record in SCHEMA2_CASES["PealOfThunder_RandomlyDamageEffect"][:1]:
    _record.pop("oracle", None)
    _record.pop("why", None)
    _record.pop("expect_regs", None)
    _record["completion"] = {
        "mode": "entry",
        "pc": sym("PlayAttackAnimation_DealAttackDamageSimple"),
        "bank": sym_bank("PlayAttackAnimation_DealAttackDamageSimple"),
        "routine": "PlayAttackAnimation_DealAttackDamageSimple",
    }
    _record["compare"] = ()
for _record in CASES["EnergySpike_PlayerSelectEffect"][:1]:
    _record.pop("oracle", None)
    _record.pop("why", None)
    _record.pop("expect", None)
for _record in CASES["PealOfThunder_RandomlyDamageEffect"][:1]:
    _record.pop("oracle", None)
    _record.pop("why", None)
    _record.pop("expect_regs", None)
    _record["compare"] = ()
SCHEMA2_CASES["EnergySpike_PlayerSelectEffect"][0]["evidence"] = "primary"
SCHEMA2_CASES["PealOfThunder_RandomlyDamageEffect"][0]["evidence"] = "primary"
SCHEMA2_CASES["EnergySpike_PlayerSelectEffect"][0].pop("reason", None)
SCHEMA2_CASES["PealOfThunder_RandomlyDamageEffect"][0].pop("reason", None)
for _name, _records in ((_fn, SCHEMA2_CASES[_fn]) for _fn in OWN):
    for _index, _record in enumerate(_records):
        if isinstance(_record.get("completion"), dict) and _record["completion"].get("mode") == "entry":
            CASES[_name][_index]["completion"] = _record["completion"]
        if "compare" in _record and _record["compare"] != CONTRACT[_name]["compare"]:
            CASES[_name][_index]["compare"] = _record["compare"]
SCHEMA2_CASES["PealOfThunder_RandomlyDamageEffect"][0].setdefault("bus", {}).update(
    {sym("wPlayerDuelVariables"): 0x100, sym("wOpponentDuelVariables"): 0x100, STACK_CANARY: 1})
