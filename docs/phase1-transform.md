# Phase 1 — hardware-removal transform (audit record)

Resolution of the 12 `home/` hardware-coupling files named in epic #2. For each
routine the transform either **ports** it (it has real semantics over flat memory)
or **deletes/dissolves** it (it is pure GB-hardware plumbing the transform strips).
Neither verdict is silent: every routine is listed below with its callsite count in
`poketcg/src/` and confirmation that no ported file under `src/` depends on a deleted
one (verified by grep — the only `src/` hits are a `bg_map.c` comment and the already-
resolved `JPHblankCopyDataHLtoDE` trampoline, which adapts `SafeCopyDataHLtoDE`).

Callsite counts are over `poketcg/src/**/*.asm`, excluding definition lines; macro
expansions (`farcall`/`bank1call`) are counted at their use sites.

## Verdict table

| routine | src | verdict | asm callsites | justification |
|---|---|---|---|---|
| `Bank1Call` | farcall.asm | delete | 528 (`bank1call`) | rst $18 trampoline rewrites the return frame to load bank 1. Plain C call at the callsite. |
| `Bank1Call_FarCall_Common` | farcall.asm | delete | 0 (internal) | shared trampoline tail; folded into the dissolved `FarCall`/`Bank1Call`. |
| `SwitchToBankAtSP` | farcall.asm | delete | 2 (in farcall.asm) | bank-restore-on-return shim popped by the rewritten frame; banked readers save/restore `hBankROM` explicitly instead. |
| `FarCall` | farcall.asm | delete | 466 (`farcall`) | rst $28 trampoline. Plain C call at the callsite. |
| `JumpToFunctionInTable` | jumptable.asm | delete | 36 | `jp hl` after indexing a pointer table — unportable as a standalone (no GB address to jump to in C). Resolves to a C function-pointer table at each callsite (port-contract L238). |
| `CallIndirect` | jumptable.asm | delete | 8 | `call [hl]` if non-NULL → direct C function-pointer call. |
| `CallHL` | jumptable.asm | delete | 3 | `jp hl` → direct C call. |
| `CallHL2` | call_regs.asm | delete | 8 | `jp hl` trampoline → direct C call. |
| `CallBC` | call_regs.asm | delete | 2 | `retbc` (`push bc; ret`) trampoline → direct C call. |
| `EnableInt_Timer` | interrupt.asm | delete | 1 | sets IE_TIMER in `rIE`; no interrupt dispatch exists in the port. |
| `EnableInt_VBlank` | interrupt.asm | delete | 1 | sets IE_VBLANK; the frame boundary is `DoFrame`, not a VBlank ISR. |
| `EnableInt_HBlank` | interrupt.asm | delete | 1 | configures `rSTAT`+`rIE` for HBlank IRQ; a software PPU has no STAT mode. |
| `DisableInt_HBlank` | interrupt.asm | delete | 1 | clears the HBlank IRQ config. |
| `CopyDMAFunction` | dma.asm | delete | 2 | copies the DMA stub into HRAM (`hDMAFunction`) to run with IRQs off; C has no HRAM-resident code. |
| `DMA` | dma.asm | **port** | (via `hDMAFunction`) | OAM DMA: 160-byte copy `$CA00`→`$FE00`. `src/home/dma.c`; oracle-tested (2 cases). |
| `VBlankHandler` | vblank.asm | delete | 1 (IRQ vector) | the VBlank ISR. Its work is dissolved: OAM copy = `DMA`; scroll/LCDC flush = PPU-host concern; `wVBlankCounter++` = main loop. The frame boundary is `DoFrame` (`src/home/frames.c`). |
| `HblankCopyDataHLtoDE` | hblank.asm | delete | 9 | busy-waits on `rSTAT` for the VRAM window; a software PPU has none. Superseded by `SafeCopyDataHLtoDE` (`src/home/bg_map.c`). |
| `HblankCopyDataDEtoHL` | hblank.asm | delete | 1 | same; superseded by `SafeCopyDataDEtoHL` (`src/home/text_box.c`). |
| `SwitchToCGBNormalSpeed` | double_speed.asm | delete | 3 | `stop` + KEY1 double-speed; the timer rate-compensates. |
| `SwitchToCGBDoubleSpeed` | double_speed.asm | delete | 4 | same. |
| `CGBSpeedSwitch` | double_speed.asm | delete | 1 (internal) | the `stop` + KEY1 sequence the two above fall through to. |
| `BankswitchVRAM0` | vram.asm | dissolve | 25 | VRAM bank-0 latch. Inlined at callsites as `hBankVRAM=0; gb_write8($FF4F,0)` — the established C convention (`empty_screen.c:19-20`, `text_box.c:113-118`). A standalone helper would be dead code; adding one would be a second convention beside an existing one. |
| `BankswitchVRAM1` | vram.asm | dissolve | 21 | VRAM bank-1 latch; inlined as above. |
| `BankswitchVRAM` | vram.asm | dissolve | 5 | VRAM bank-N latch; inlined as `hBankVRAM=a; gb_write8($FF4F,a)`. |
| `BankswitchSRAM` | sram.asm | **port** (impl in `switch_sram.c`) | — | SRAM bank latch + enable; real flat-memory effect (selects the `g_sram` slice). Already ported by the MBC5 substrate; oracle coverage added here (`src/probe/sram.c`, 3 cases). |
| `EnableSRAM` | sram.asm | port (impl in `switch_sram.c`) | — | SRAM enable latch. Used by `card_collection`/`save`; its latch effect is masked by the span reader (`gb_ptr` bypasses `g_sram_enabled`), so it is not standalone-observable and is covered indirectly by the save/card suites. |
| `DisableSRAM` | sram.asm | port (impl in `switch_sram.c`) | — | SRAM disable latch; same. |
| `UnsafeWriteDataBlockToBGMap0` | unsafe_bg_map.asm | **port** | 4 | reads `{x,y,data…,$00}`, writes to BGMap0 at `(x,y)`. `src/home/unsafe_bg_map.c`; oracle-tested (3 cases). NB: `BCCoordToBGMap0Address` leaves the address in `hl`, so the asm's scan reads VRAM, not the WRAM struct — reproduced faithfully. |
| `DoFrameIfLCDEnabled` | lcd_enable_frame.asm | **port** | 53 | calls `DoFrame` only while `rLCDC` bit 7 is set; all registers preserved. `src/home/lcd_enable_frame.c`; oracle-tested (3 cases). |

Totals: 29 routines — 4 ported with new oracle coverage (`DMA`, `UnsafeWriteDataBlockToBGMap0`, `DoFrameIfLCDEnabled`, `BankswitchSRAM`), 2 already-ported (`EnableSRAM`, `DisableSRAM`), 3 dissolved into inline latch writes (VRAM), 20 deleted.

## Mutation tests

Each newly registered routine was given a shape-preserving mutation (structure
unchanged, meaning corrupted) and confirmed to flip the diff RED, then reverted.

| routine | mutation | result |
|---|---|---|
| `DMA` | copy count `0xA0`→`0x9F` (159 bytes) | RED — 2/2 cases differ (last OAM byte un-copied) |
| `UnsafeWriteDataBlockToBGMap0` | swap `x`/`y` args to `BCCoordToBGMap0Address` | RED — 1/3 cases differ (the `x≠y` case; `x==y` cases are swap-invariant) |
| `DoFrameIfLCDEnabled` | invert gate `if (lcd) DoFrame`→`if (!lcd) DoFrame` | RED — 2/3 cases differ (LCD-off non-zero + LCD-on C-only) |
| `BankswitchSRAM` | selected bank `bank`→`bank^1` | RED — 3/3 cases differ (wrong `g_sram` slice + `hBankSRAM`) |

## Epic #2 acceptance

Epic #2's two criteria, for the ported surface this slice owns:

1. **Clean compile with banking/HBlank/interrupt machinery removed.** Holds. The
   ported surface compiles clean under `-Wall -Wextra` (zero warnings). On the 12
   files the banking trampolines (`FarCall`/`Bank1Call`/`SwitchToBankAtSP`), the
   HBlank busy-waits, the interrupt-controller config, `CopyDMAFunction` (HRAM code
   copy), the double-speed `stop`, and the `VBlankHandler` ISR are all deleted or
   dissolved; `hBankROM` survives only as the explicit save/restore shadow used by
   banked-ROM readers (`memory.c`, `print_text.c`, `process_text.c`), never by a
   farcall return path.
2. **The Phase-0 leaf still diffs clean.** Holds. `just oracle-diff-all` is
   142/142 routines clean (was 138; +4 new) in ~5.6 s, and `just lint-adapters`
   exits 0.

Scope note: epic #2's full sweep (994 `farcall`/`bank1call` sites, 33 jump tables,
24 SGB branches) spans the whole disassembly, most of it still unported `engine/`/
`scripts/` asm. Those sites are resolved mechanically **as the surrounding routine
ports** — each `farcall` becomes a plain C call, each `jp hl` table a C function-
pointer table. The 12 `home/` files here are the canonical resolutions the later
phases apply at their callsites; nothing in the ported surface retains the deleted
hardware couplings.
