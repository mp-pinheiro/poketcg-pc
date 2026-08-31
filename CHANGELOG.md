# Changelog

All notable changes to this project are documented here.
This changelog is generated automatically from [Conventional Commits](https://www.conventionalcommits.org) by [git-cliff](https://github.com/orhun/git-cliff).
## v0.217.0 - 2026-08-31

### Bug Fixes

- *(factory)* Reopen new game
- *(factory)* Reopen intro sequence
- *(factory)* Reopen continue duel
- *(factory)* Relocate intro routine
- *(factory)* Reopen enter script
- *(factory)* Bound credits event check
- *(oracle)* Preserve event completion spec
- *(factory)* Unblock Func_1f96
- *(factory)* Unblock AIDoAction_Turn
- *(factory)* Unblock StoneBarrage effect
- *(factory)* Unblock DebugDuelMode
- *(factory)* Unblock SuperPotion AI
- *(factory)* Unblock Chansey effect
- *(factory)* Unblock SuperEnergy retrieval
- *(factory)* Unblock ComputerSearch selection
- *(factory)* Unblock Jigglypuff effect
- *(factory)* Unblock EnergyConversion effect
- *(factory)* Unblock FriendshipSong effect
- *(factory)* Unblock Magneton recoil effect
- *(duel)* Skip disabled attack animations
- *(factory)* Unblock Golem selfdestruct
- *(factory)* Unblock Magnemite effect
- *(factory)* Unblock Magneton35 effect
- *(factory)* Unblock PayDay effect
- *(factory)* Unblock PokeBall selection
- *(factory)* Refresh changed context
- *(factory)* Unblock Prophecy selection
- *(factory)* Unblock Quickfreeze effect
- *(factory)* Retry corrected duel init blocker
- *(factory)* Retry animation effect blockers
- *(factory)* Retry interactive effect blockers
- *(factory)* Retry corrected interactive fixtures
- *(factory)* Diagnose interactive blockers
- *(factory)* Retry frame-safe solar power
- *(factory)* Diagnose solar animation boundary
- *(factory)* Retry chansey effect
- *(factory)* Retry duel setup state
- *(factory)* Retry link handshake fixture
- *(oracle)* Align captured entry stack pointers
- *(factory)* Support explicit entry stack frames
- *(oracle)* Normalize stack return frames
- *(oracle)* Unify synthetic call frames
- *(oracle)* Restore ROM bank request
- *(factory)* Reopen exhausted retries
- *(factory)* Reopen retired routines
- *(script)* Align bank oracle cases
- *(factory)* Preserve SCC packet members

### Features

- *(port)* GiftCenter_SendDeck
- *(port)* HandleGiftCenter
- *(port)* GameEvent_GiftCenter
- *(port)* MainMenu_NewGame
- *(port)* MainMenu_ContinueFromDiary
- *(port)* MainMenu_ContinueDuel
- *(port)* PlayIntroSequence
- *(port)* HandleTitleScreen
- *(port)* _GameLoop
- *(port)* Func_3b11
- *(port)* EnterScript
- *(port)* SetScriptData
- *(port)* Register credits sequence
- *(port)* DebugCredits
- *(port)* GameEvent_Credits
- *(port)* _DebugLookAtSprite
- *(port)* DebugLookAtSprite
- *(port)* Func_1f96
- *(port)* AIDecide_SuperPotion_Phase08
- *(port)* AIPlay_SuperEnergyRetrieval
- *(port)* SetUpAndStartLinkDuel
- *(port)* GameEvent_BattleCenter
- *(port)* SetLinkDuelTransmissionFrameFunction
- *(port)* UnreferencedSaveSerialReturnAddress
- *(port)* AIDoAction_Turn +1
- *(port)* Duel_Init
- *(port)* ComputerSearch_PlayerDeckSelection
- *(port)* JigglypuffDoubleEdgeEffect +1
- *(port)* Recycle_PlayerSelection
- *(port)* GolemSelfdestructEffect
- *(port)* ChanseyDoubleEdgeEffect
- *(port)* FriendshipSong_AddToBench50PercentEff~
- *(port)* SubmissionEffect
- *(port)* MagnemiteSelfdestructEffect
- *(port)* MagnetonLv28SelfdestructEffect +3
- *(port)* EnergyConversion_AddToHandEffect +3
- *(port)* PokemonTrader_PlayerDeckSelection +3
- *(port)* PokeBall_PlayerSelection
- *(port)* PokemonTrader_TradeCardsEffect
- *(script)* Dispatch overworld scripts
- *(port)* RST20
- *(port)* HandleDeckConfigurationMenu +1
- *(port)* DeckSelectionMenu +2
- *(port)* PauseMenu_Deck
- *(port)* PauseMenu
- *(port)* OpenPauseMenu
- *(port)* ScriptCommand_OpenMenu
- *(port)* HandlePlayerMoveMode
- *(port)* CallHandlePlayerMoveMode
- *(port)* HandleOverworldMode
- *(port)* LoadMap
- *(port)* OpenDuelCheckMenu +1
- *(port)* DuelCheckMenu_InPlayArea +5
- *(port)* DisplayPlayAreaScreen +7

