# Phase 1 hardware transform

This record covers the bounded disposition of 12 `home/` hardware-coupling files. It is not a whole-disassembly inventory; engine and script callsites outside that set have their own translation and evidence. The table's assembly callsite counts refer to the pinned `poketcg/src/**/*.asm`, excluding definitions and counting macro uses at callsites.

## Disposition table

| Routine | Source | Disposition | Assembly callsites | Resolution |
|---|---|---|---:|---|
| `Bank1Call` | `farcall.asm` | delete | 528 | Bank-1 trampoline becomes a plain C call. |
| `Bank1Call_FarCall_Common` | `farcall.asm` | delete | 0 internal | Shared trampoline tail is removed with its callers. |
| `SwitchToBankAtSP` | `farcall.asm` | delete | 2 | Return-frame bank restore removed; banked readers explicitly save and restore `hBankROM`. |
| `FarCall` | `farcall.asm` | delete | 466 | Far-call trampoline becomes a plain C call. |
| `JumpToFunctionInTable` | `jumptable.asm` | delete | 36 | Resolve at the caller to a C function-pointer table. |
| `CallIndirect` | `jumptable.asm` | delete | 8 | Resolve non-null indirect call to a direct C function call. |
| `CallHL` | `jumptable.asm` | delete | 3 | Resolve `jp hl` at its caller. |
| `CallHL2` | `call_regs.asm` | delete | 8 | Resolve trampoline at its caller. |
| `CallBC` | `call_regs.asm` | delete | 2 | Resolve `push bc; ret` at its caller. |
| `EnableInt_Timer` | `interrupt.asm` | delete | 1 | Timer interrupt-controller setup has no native dispatch counterpart. |
| `EnableInt_VBlank` | `interrupt.asm` | delete | 1 | Frame boundary is `DoFrame`, not a VBlank ISR. |
| `EnableInt_HBlank` | `interrupt.asm` | delete | 1 | Software PPU has no STAT-mode interrupt. |
| `DisableInt_HBlank` | `interrupt.asm` | delete | 1 | HBlank interrupt configuration is removed. |
| `CopyDMAFunction` | `dma.asm` | delete | 2 | Native code does not execute an HRAM-copied DMA stub. |
| `DMA` | `dma.asm` | port | via `hDMAFunction` | Retain the real 160-byte `$CA00` to `$FE00` OAM copy in `src/home/dma.c`. |
| `VBlankHandler` | `vblank.asm` | delete | 1 vector | OAM copy is `DMA`; PPU flush is host work; counter update is main-loop work. |
| `HblankCopyDataHLtoDE` | `hblank.asm` | delete | 9 | Replace the VRAM-window busy wait with `SafeCopyDataHLtoDE`. |
| `HblankCopyDataDEtoHL` | `hblank.asm` | delete | 1 | Replace the VRAM-window busy wait with `SafeCopyDataDEtoHL`. |
| `SwitchToCGBNormalSpeed` | `double_speed.asm` | delete | 3 | Remove `stop`/KEY1 speed switching; timer rate-compensates. |
| `SwitchToCGBDoubleSpeed` | `double_speed.asm` | delete | 4 | Remove `stop`/KEY1 speed switching; timer rate-compensates. |
| `CGBSpeedSwitch` | `double_speed.asm` | delete | 1 internal | Shared speed-switch sequence is removed. |
| `BankswitchVRAM0` | `vram.asm` | dissolve | 25 | Inline bank-zero latch and `$FF4F` bus write at use sites. |
| `BankswitchVRAM1` | `vram.asm` | dissolve | 21 | Inline bank-one latch and `$FF4F` bus write at use sites. |
| `BankswitchVRAM` | `vram.asm` | dissolve | 5 | Inline selected bank latch and `$FF4F` bus write at use sites. |
| `BankswitchSRAM` | `sram.asm` | port | - | `switch_sram.c` selects the flat-memory SRAM slice and latch. |
| `EnableSRAM` | `sram.asm` | port | - | Preserve SRAM enable latch behavior in `switch_sram.c`. |
| `DisableSRAM` | `sram.asm` | port | - | Preserve SRAM disable latch behavior in `switch_sram.c`. |
| `UnsafeWriteDataBlockToBGMap0` | `unsafe_bg_map.asm` | port | 4 | Retain `{x,y,data…,$00}` decoding and BGMap0 writes; source scan reads VRAM through the address left in `hl`. |
| `DoFrameIfLCDEnabled` | `lcd_enable_frame.asm` | port | 53 | Call `DoFrame` only when LCD enable is set; preserve registers. |

These dispositions define the hardware-removal boundary; the port contract owns the general exclusion, dispatch and fallthrough rules.
