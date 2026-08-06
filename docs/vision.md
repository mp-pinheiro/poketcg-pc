
 Native PC port of poketcg — the plan

 Ten parallel investigations: four on prior art (source-level, not marketing), six mapping this  codebase. Below is the decision, the mechanism, and the sequence.

 ────────────────────────────────────────────────────────────────────────────────

 1. The decision

 Hand-port every function to C99 + SDL2, keeping a software PPU whose screen and tilemap  dimensions are runtime variables. Preserve the original memory layout byte-for-byte so a  whole-state memcmp against the ROM is a valid correctness oracle. Add widescreen strictly as a  layer on top of already-verified 4:3 code.

 This is zelda3's architecture with suiCune's conversion discipline and Gen1Recomp's variable  logical canvas. Each of those three choices is load-bearing and each has a working precedent.

 The decisive constraint, which I verified directly:

 ```
WRAM   $c000-$dee4   7,909 bytes, FLAT — all 8 rgbds sections are WRAM0, zero WRAMX
HRAM   44 symbols          SRAM   4 banks × 8 KiB, 272 symbols
VRAM   16 KiB (2 banks)    OAM    160 B        palettes 128 B
 ```

 The entire mutable state of this game is ~56 KiB. zelda3 memcmps 128 KiB of SNES WRAM + 64 KiB  VRAM every frame and still runs at turbo speed. Full-state diffing here is free. That single  fact is what converts this from "a multi-year rewrite you hope is correct" into "a multi-month  rewrite that is provably correct at every step".

 ────────────────────────────────────────────────────────────────────────────────

 2. Architecture

              ┌────────────────────────────────────────────────────────────────────────────────               │                                  host layer — new codee layer — layout-locked
              │
              │
 ┌────────┐   │ ┌───────────────────────────────────────────┐     ┌────────────────────────────
 │        │   │ │                                           │     │
 │        │   │ │                                           │     │
 │ oracle │   │ │      SDL2: window, input, audio sink      │  ┌─►│                game
 │        │   │ │                                           │  │  │
 │        │   │ │                                           │  │  │
 └────────┘   │ └───────────────────────────────────────────┘  │  └────────────────────────────
              │                       ▲                        │
              │                       │                        │
              │                       │                        │
              │                       │                        │
              │                       ├────────────────────────┼───────────────────────────────
              │                       │                        │
              │                       │                        │
              │                       │                        │
              │                       │                        │
              │ ┌─────────────────────┴─────────────────────┐  │  ┌────────────────────────────
              │ │                                           │  │  │
              │ │                                           │  │  │            virtual PPU               │ │               TCP transport               │  ├─►┤        scanline rasteriser               │ │          link duel + IR sessions          │  │  │ SCREEN_W / TILEMAP_W are VA
              │ │                                           │  │  │
              │ └───────────────────────────────────────────┘  │  └────────────────────────────
              │                                                │
              │                                                │
              │                       ┌────────────────────────┤
              │                       │                        │
              │                       ▼                        │
              │ ┌─────────────────────┴─────────────────────┐  │  ┌────────────────────────────
              │ │                                           │  │  │
              │ │                                           │  │  │
              │ │    g_wram 8K · g_hram 128 · g_sram 32K    │  └──┤            software APU               │ │     g_vram 16K · g_oam 160 · g_pal 128    │     │     NRxx registers to sampl
              │ │                                           │     │
              │ └───────────────────────────────────────────┘     └────────────────────────────               │                                                                      ▲               └──────────────────────────────────────────────────────────────────────┼─────────                                                                                      │               ┌───────────────────────────────────────────────┐                      │               │ game layer — ported by hand, 59,179 asm lines │                      │               │ ┌───────────────────────────────────────────┐ │                      │               │ │                                           │ │                      │               │ │    home/ utilities, text, tiles, menus    │ │                      │               │ │                                           │ │                      │               │ └───────────────────────────────────────────┘ │                      │               │                                               │                      │               │                                               │                      │               │                                               │                      │               │                                               │                      │               │                                               │                      │               │ ┌───────────────────────────────────────────┐ │                      │               │ │                                           │ │                      │               │ │     duel engine + card effect VM + AI     │ │                      │               │ │                                           │ │                      │               │ └───────────────────────────────────────────┘ │                      │               │                                               │                      │               │                                               │                      │               │                                               │                      │               │                                               │                      │               │                                               │                      │               │ ┌───────────────────────────────────────────┐ │                      │               │ │                                           │ │                      │               │ │      overworld + 104-opcode script VM     │ │                      │               │ │                                           │ │                      │               │ └───────────────────────────────────────────┘ │                      │               │                                               │                      │               │                                               │                      │               │                                               │                      │               │                                               │                      │               │                                               │                      │               │ ┌───────────────────────────────────────────┐ │                      │               │ │                                           │ │                      │               │ │ audio sequencer — original driver, ported ├─┼──────────────────────┘
              │ │                                           │ │
              │ └───────────────────────────────────────────┘ │
              │                                               │
              └───────────────────────────────────────────────┘

              ┌───────────────────────────────────────────────┐
              │   oracle — dev only, excluded from release    │
              │ ┌───────────────────────────────────────────┐ │
              │ │                                           │ │
              │ │            PyBoy: per-function            │ │
              │ │                                           │ │
              │ └───────────────────────────────────────────┘ │
              │                                               │
              │                                               │
              │                                               │
              │                                               │
              │                                               │
              │ ┌───────────────────────────────────────────┐ │
              │ │                                           │ │
              │ │          gb-recompiled: per-scene         │ │
              │ │                                           │ │
              │ └───────────────────────────────────────────┘ │
              │                                               │
              │                                               │
              │                                               │
              │                                               │
              │                                               │
              │ ┌───────────────────────────────────────────┐ │
              │ │                                           │ │
              │ │       memcmp harness + replay corpus      │ │
              │ │                                           │ │
              │ └───────────────────────────────────────────┘ │
              │                                               │
              └───────────────────────────────────────────────┘

 Three rules make it work:

 (a) Game code never sees a host type. It writes g_vram, g_oam, g_wram exactly where the asm  wrote $9800, $ca00, $c200. The wram.h header is generated mechanically from poketcg.sym (make  DEBUG=1 emits all 20,280 symbols; 1,518 are WRAM, at known flat offsets):

 ```c
#define wRNG1                  (*(uint8_t *)(g_wram + 0x0aca))
#define wPlayerDuelVariables   ((uint8_t *)(g_wram + 0x2200))
#define wOAM                   ((OamEnt   *)(g_wram + 0x0a00))
 ```

 suiCune proves the layout with static_assert(offsetof(struct wram_s, f) == f - WRAM_0_ADDR);  do the same for every struct you promote from raw bytes.

 (b) The PPU is the only thing that knows about pixels, and it is a normal, editable C module —  not an emulator you vendored. That is what makes both widescreen and the oracle possible  simultaneously. zelda3 gets 4× Mode-7 upsampling, 240-line mode, and widescreen from this one  property.

 (c) Dimensions are variables from commit one. BCCoordToBGMap0Address
 (src/home/empty_screen.asm:26-38) computes the tilemap stride as five chained add hl,hl — the  ×32 is an instruction pattern, not a constant. Only 15 sites use the symbolic TILEMAP_WIDTH.  Every one of those hand-translates to &bgmap[y * TILEMAP_W + x]. Widescreen is nearly free if  you do this on the way in, and a second full pass if you don't. Non-negotiable.

 ────────────────────────────────────────────────────────────────────────────────

 3. Why not the alternatives

 ┌───────────────┬────────────────────────────────────────────────────────────────────────────┐  │ Rejected      │ Reason                                                                     │  ├───────────────┼────────────────────────────────────────────────────────────────────────────┤  │ Vendor        │ It compiles Peanut-GB into the binary and keeps gb.cpu_reg.pc live         │  │ suiCune's     │ forever. constants/gfx_constants.h hardcodes SCREEN_WIDTH 20, BG_MAP_WIDTH │  │ substrate     │ 32; output is locked to a 160×144 RGB555 texture with                      │  │               │ SDL_RenderSetLogicalSize. Every ported function then does tilemap math     │  │               │ against a 32-tile stride permanently. Excellent method, wrong substrate.   │  ├───────────────┼────────────────────────────────────────────────────────────────────────────┤  │ Native        │ Forecloses the memcmp oracle — and the oracle is the entire reason this is │  │ renderer,     │ finishable. Also breaks the printer, which composes 160-px bands through   │  │ drop tilemaps │ the tile pipeline (src/engine/link/printer.asm:419).                       │  ├───────────────┼────────────────────────────────────────────────────────────────────────────┤  │ Any asm→C     │ CharlesAverill/poketcg is the worked counterexample: one commit,           │  │ transpiler    │ lift_skeleton.py maps jr/jp to comments, 75% of its 212k lines are         │  │               │ commented-out asm, src/home/hblank.c has an empty body, and it does not    │  │               │ compile (registers.h:15: 'CPURegs' has no member named 'regs'). Do not     │  │               │ join, do not salvage. More fundamentally: farcall/bank1call are            │  │               │ implemented by rewriting return addresses on the stack                     │  │               │ (src/home/farcall.asm:3-79) and 149 event macros read their operand from   │  │               │ the return address. No line-by-line lifter survives that. A human deletes  │  │               │ it in a second.                                                            │  ├───────────────┼────────────────────────────────────────────────────────────────────────────┤  │ Bundle the    │ Links Awakening DX HD shipped assets and was DMCA'd within a day of        │  │ ROM or the    │ publicity — the widescreen and 120fps did not save it. Its source fork is  │  │ extracted     │ still up.                                                                  │  │ assets        │                                                                            │  └───────────────┴────────────────────────────────────────────────────────────────────────────┘

 ────────────────────────────────────────────────────────────────────────────────

 4. Widescreen, concretely

 Four mechanisms, all with working source precedents:

 Span widening (from zelda3). Size every scanline buffer 160 + 2*kExtraLeftRight at build time,  bias all writes by that constant so x=0 lands at the offset and negative x is legal, then move  the draw span:

 ```c
/* zelda3 snes/ppu.c:204-208, adapted */
win->edges[0] = -(layer != HUD_LAYER ? ppu->extraLeftCur : 0);
win->edges[1] = SCREEN_W + (layer != HUD_LAYER ? ppu->extraRightCur : 0);
 ```

 The existing, unmodified per-layer rasterisers then emit wider lines. Zero duplicated  renderers. layer != HUD_LAYER is the entire HUD fix at PPU level.

 Variable logical canvas (from Gen1Recomp). Its setUISize lets a game state request a wider  surface — the widescreen battle asks for 304×144 and re-lays-out the menu as 2×2 while "the  battle simulation, timing, animations and rules stay BattleState's". poketcg is menus plus one  duel screen. This is exactly the shape of the problem. Widen the canvas, re-author the  duel/menu screen builders, leave the 826-byte duel state untouched.

 Single viewport rect (from LADX-HD). For the overworld only, derive the render rect from the  live window and feed the same rect to culling, NPC updates, and animation —  GameManager.cs:602-605 → ObjectManager.cs:192-198 (// only update the objects that are in a  tile that is visible). One definition of "active region" means rendering and simulation cannot
 desync. Keep room semantics as a logical grid decoupled from the viewport
 (FieldWidth/FieldHeight + per-field update counters), which is how LADX-HD preserved GB  room-reset behaviour under a 5-room-wide camera.

 The honest problem, and its answer. The GB tilemap is 32×32 and wraps; poketcg is  screen-composed, so there is usually no valid off-screen tile data to reveal. zelda3 handles  the analogous case by clamping the extension to the current room bounds every frame  (ConfigurePpuSideSpace, src/zelda_rtl.c:140-173) so the view narrows back to 4:3 rather than  showing junk, and it disables widescreen for the one effect it cannot widen (dungeon lantern  cone). For poketcg the extra columns must mostly be authored — a background fill or explicitly  uploaded tiles — in the screen builders. Budget widescreen as work in engine/menus/ and the  duel screen, not in the PPU.

 Sprite limits are orthogonal. GB's 10-per-scanline / 40-OAM limits live only in sprite  evaluation, which reads OAM and writes the object buffer — never back into OAM or WRAM. So a  NoSpriteLimits render flag changes pixels only and stays out of the memcmp entirely (zelda3  snes/ppu.c:1247). The game's own allocator is a 40-entry bump list with a carry-on-overflow  contract (src/home/objects.asm:14-19) plus 16 animated slots (SPRITE_ANIM_BUFFER_CAPACITY EQU  16); widening is an array size.

 Raster effects: per-scanline offset arrays, not STAT interrupts. CppRed has the right  abstraction — Point bg_offsets[144]; Point window_offsets[144]; with a range setter. poketcg's  LYC handler (src/home.asm:34-36 calls wLCDCFunctionTrampoline) and src/home/scroll.asm write  ranges into those arrays; the renderer consumes them per line. suiCune's wLYOverrides[LY] +  hLCDCPointer (home/lcd.c:20-24) is the same idea limited to one register — take the array  version.

 ────────────────────────────────────────────────────────────────────────────────

 5. The verification harness

 This is the part that decides whether the project ships, and it is what suiCune did not have  (it used manual playtesting; 4.4 years, 70% done).

 Snapshot vector — everything, since it is only 56 KiB: WRAM + HRAM + SRAM + VRAM(2 banks) +  OAM + palette RAM + the CPU register file. smw's wider vector (adds OAM and CGRAM over  zelda3's) is the right model.

 Two oracles, two granularities:

 Per-function — PyBoy. hook_register(None, "Label", ...) resolves breakpoints against  poketcg.sym directly, with full read/write on registers, all WRAM, both VRAM banks, OAM, and  cart RAM. So: synthesise an input state, run one ROM routine to its RET, capture the output  state. This is zelda3's RunEmulatedFunc(pc, a, x, y, ...) tier, and it is the daily loop —  port a function, diff it, move on.

 Per-scene — gb-recompiled. Deterministic headless replay (--input, --limit-frames), savestates  carrying full memory, and --trace-entries emitting bank:addr in the exact same BB:AAAA  convention as rgblink's .sym — so joining a trace against the symbol table tells you which  routines a scene actually exercises, letting you order the work by real coverage instead of  guessing.

 Its cheap JSON --dump-state covers wram_bank_0_c000_cfff + wram_bank_1_d000_dfff — which,  because poketcg's WRAM is flat and unbanked, is 100% of the game's WRAM. Lucky fit.  VRAM/OAM/SRAM come from --save-state-file, whose header is self-describing ('GBSV' magic,  explicit per-region sizes) and parseable without patching anything.

 Three traps I hit while measuring, documented so you don't:

 1. A stale .sav in --save-dir silently changes the route — the game takes Continue instead of     New Game. My first hang bisection was invalid for exactly this reason. Wipe the save dir
    before every run.
 2. Frame numbering is not comparable across oracles. gb-recompiled starts from a configured     post-boot state (no CGB boot ROM; GBC.md discloses the boot_div-cgb* failures); PyBoy runs     its own bundled bootrom_cgb.bin and overlays a splash. Anchor on game events, never frame
    indices.
 3. Screen comparison is exactly solvable. Both derive from the same CGB 5-bit values and
    differ only in expansion — gb-recompiled does c*255/31 truncated
    (runtime/src/ppu.c:138-143), PyBoy does c<<3. Invert both to the 5-bit domain and     comparison is bit-exact. Also: --dump-frames silently truncates to 100 indices per run
    (MAX_DUMP_FRAMES), and --input caps at 2048 entries — use the periodic
    p<start>-<last>/<period> form for long routes.

 Structure it as smw does, not zelda3. A per-game vtable — run_frame, run_frame_emulated,  fix_snapshot_for_compare, patch_bugs — plus a tri-state RM_BOTH / RM_MINE / RM_THEIRS. And  steal smw's best idea: on mismatch, write saves/bug-<timestamp>.sav and show an on-screen  countdown. Ship the oracle to testers as a crowd-sourced bug reporter.

 Budget an exclusion list. zelda3's is ~25 lines, each with a one-line justification, in three  categories: emulator-authoritative (scratch, uninitialised temporaries, the SM83 stack region  — your C has no GB stack), C-authoritative, and port-only state. For poketcg, day-one  exclusions are rSTAT/rLY, DIV/TIMA, and anything the audio path touches.

 Regression corpus. Base snapshot + RLE'd input log + interleaved patch-byte commands. zelda3  got full-game regression from 13 chapter saves and no test framework. Here the analogue is  seeded duel replays — and they will be bit-exact, because:

 │ UpdateRNGSources (src/home/random.asm) is a pure software LFSR over wRNG1/wRNG2/wRNGCounter.  │ Zero hardware entropy — 0 reads of rDIV anywhere in the codebase. Duel outcomes are fully  │ determined by inputs.

 That is the single most favourable fact about this game for porting.

 Gate the oracle off when features are on. zelda3 src/zelda_rtl.c:742: if (enhanced_features0  != 0) ZeldaRunFrameInternal(...) — "can't compare against real impl when running with extra  features". Verify at 160×144 with zero features; widescreen strictly on top of verified code.

 ────────────────────────────────────────────────────────────────────────────────

 6. Phases

 Ordered by dependency and by how cheaply each slice can be oracle-diffed. Line counts are  measured.

 ### Phase 0 — Substrate (2–3 weeks)

 Memory arrays; wram.h/hram.h/sram.h generated from poketcg.sym with layout assertions; virtual  PPU with variable dimensions + per-scanline offset arrays; SDL2 shell; the PyBoy function  harness and the gb-recompiled route harness; snapshot/compare/replay plumbing.

 Gate: ported ClearSRAMBGMaps (or any trivial leaf) diffs clean against PyBoy, and a recorded  input replay round-trips.

 ### Phase 1 — Delete the hardware (1 week, mechanical)

 This is the highest-leverage transform and it must come first:

 ┌─────────────────────────┬─────────────────────┬────────────────────────────────────────────┐  │ Construct               │ Sites               │ Resolution                                 │  ├─────────────────────────┼─────────────────────┼────────────────────────────────────────────┤  │ farcall / bank1call +   │ 994                 │ plain C call. Delete Bank1Call, FarCall,   │  │ rst $18/$28 trampolines │                     │ SwitchToBankAtSP, BankpushROM, BankpopROM, │  │                         │                     │ hBankROM                                   │  ├─────────────────────────┼─────────────────────┼────────────────────────────────────────────┤  │ SafeCopyDataHLtoDE      │ all tilemap writes  │ unconditional memcpy. Proven safe: it      │  │ HBlank gate             │                     │ writes identical bytes on both branches —  │  │                         │                     │ the LCD-on path only changes when          │  │                         │                     │ (src/home/bg_map.asm:100-115)              │  ├─────────────────────────┼─────────────────────┼────────────────────────────────────────────┤  │ HblankCopyDataHLtoDE    │ src/home/hblank.asm │ delete. A software PPU has no VRAM access  │  │ busy-wait               │                     │ window                                     │  ├─────────────────────────┼─────────────────────┼────────────────────────────────────────────┤  │ halt / WaitForVBlank    │ 3 halt              │ DoFrame() becomes the frame boundary       │  ├─────────────────────────┼─────────────────────┼────────────────────────────────────────────┤  │ stop + KEY1             │ 1                   │ delete; SetupTimer already                 │  │ double-speed            │                     │ rate-compensates                           │  ├─────────────────────────┼─────────────────────┼────────────────────────────────────────────┤  │ inline-operand event    │ 149                 │ SetEventValue(EVENT_FOO, c)                │  │ macros                  │                     │                                            │  ├─────────────────────────┼─────────────────────┼────────────────────────────────────────────┤  │ jp hl / jump tables     │ 17 / 33             │ C function-pointer tables. Remarkably      │  │                         │                     │ small and fully enumerable                 │  ├─────────────────────────┼─────────────────────┼────────────────────────────────────────────┤  │ OAM DMA (hDMAFunction   │ 1                   │ memcpy(g_oam, wOAM, 160)                   │  │ copied into HRAM)       │                     │                                            │  ├─────────────────────────┼─────────────────────┼────────────────────────────────────────────┤  │ SGB path                │ 24 branch sites     │ drop, or keep behind a flag                │  ├─────────────────────────┼─────────────────────┼────────────────────────────────────────────┤  │ HDMA/GDMA               │ 0                   │ nothing to do                              │  └─────────────────────────┴─────────────────────┴────────────────────────────────────────────┘

 ### Phase 2 — Leaves and save (2–3 weeks)

 home/copy·math·division·list·memory·random·decompress·write_number (673 lines, pure  functions). Then SRAM + save + validation (1,157 lines): zero dependencies and immediately  diffable — run SaveAndBackupData in both worlds from identical WRAM and memcmp the 32 KiB  image. Bank 0 uses 7,998/8,192 bytes, mirrored into bank 2 as backup.

 Gate: a save written by the C port loads in an emulator and vice versa.

 ### Phase 3 — Timer, APU, audio (4–6 weeks · 4,812 code + 26,252 data lines)

 Tick the original driver against a software APU. The verdict is evidence-backed: the sequencer  writes raw NRxx across 10 register groups plus wave RAM, channel 4 genuinely uses the hardware  length counter, and NR43 is streamed per tick for percussion timbre — re-synthesis would have  to reimplement all of that anyway. Wave-RAM reloads are always DAC-off-bracketed, so no  corruption modelling is needed; sweep is written but disabled and can be stubbed.

 The cadence is exact and load-bearing: TIMA at 16384 Hz, TMA = −68, gated & 3 → 60.235 Hz, not  60.000. That 0.4% matters twice — audio tempo, and sPlayTimeCounter, which is written to SRAM  and so must diverge from wall-clock exactly as the cartridge does.

 Diffable as a (tick, register, value) write trace. (Alternative worth knowing: LADX-HD embeds  a whole SM83 interpreter solely to run the ROM's GBS driver — lower effort, but it  reintroduces a CPU and a ROM dependency. Rejected here for that reason.)

 ### Phase 4 — Text, tiles, menus (8–10 weeks · 1,740 + 1,160 + 14,813 lines)

 The text engine (13 ROM banks of text, text_offsets.asm 213 KB pointer table, charmaps.asm),  the tilemap/BG-map layer, then the menu framework. This is where widescreen work concentrates  later, so keep every dimension symbolic as you go.

 ### Phase 5 — Duel engine (12–16 weeks · 44,614 lines)

 The bulk, and the most separable — a second developer can own it. It is far more tractable  than the line count suggests:

 The entire duel state is 826 bytes, and the game itself enumerates it — DuelDataToSave
 (src/engine/duel/core.asm:6117-6126, in-tree comment ; 826 bytes, matching
 SAVE_DUEL_DATA_SIZE). Seven regions: two 256-byte page-aligned per-duelist blocks, 272 bytes  of decks + name, 22 bytes of duel state, hWhoseTurn, 3 bytes of RNG, 16 bytes of AI vars.  Anything it omits is derived or presentation. That is your C struct, exactly.

 Two structural notes: the per-duelist blocks are $100-aligned by assertion because  PLAYER_TURN/OPPONENT_TURN are the page bytes — all access is ld l,offset / ld h,hWhoseTurn, so  the duelist selector is the high byte. And the card-effect layer is a command VM whose opcode  tables come from src/macros/; port it as a VM, not as unrolled logic.

 Gate: replay a full seeded duel and memcmp the 826-byte state after every turn.

 ### Phase 6 — Overworld and scripts (6–8 weeks · 12,129 lines)

 104-opcode script VM, dispatch table in src/data/script_table.asm. One trap that will surprise  you: scripts are hybrid. start_script is rst $20; the handler pops its own return address as  the bytecode pointer, interprets until wBreakScriptLoop, then retbc (push bc; ret) resumes  native asm at the byte after the last command. So native code and bytecode interleave inside a  single function — see src/scripts/mason_laboratory.asm:57-77. You cannot split "VM" from "game  code" along file boundaries. Each script file becomes a C function mixing statements with  RunScript(&blob) calls.

 Also: bank co-residency is load-bearing. Func_c943 and HandleMoveModeAPress hardcode  BANK(MapScripts) while dereferencing into npc_map_data.asm/map_objects.asm, which only works  because both sections land in ROMX $04. Deleting banking (Phase 1) resolves it — just don't  preserve it by accident.

 ### Phase 7 — Link, IR, printer (4–5 weeks · 3,468 lines)

 One TCP transport with a session-type byte serves both link duels and IR. IR's physical layer  is cycle-counted bit-banging — a bit is pulse-present-vs-absent in a fixed slot, with the two  code paths deliberately length-matched, di held for the whole session. It has no portable  meaning: delete ir_core.asm:6-240 wholesale. Keep only what is above it: the 8-byte  register-frame ABI, the IRCMD_* dispatcher, param/magic matching, the Card Pop name-list  exchange and its name-hash rarity roll, the Gift Center payloads. The rSTAT VBlank rendezvous  in CloseIRCommunications becomes a no-op.

 Two security fixes while you are there: drop IRCMD_CALL_FUNCTION (ir_core.asm:350-357) — it is  jp hl to a peer-supplied address, i.e. remote code execution by design, and no local caller  ever sends it. And bounds-check the de/c pair in IRCMD_RECEIVE_DATA, an otherwise unchecked  remote memory write.

 Printer: cut at SendPrinterPacket. Keep the composition (layout, 1bpp→2bpp expansion, 40-tile  band slicing — ordinary rendering); replace the 12-step IRQ state machine, RLE compressor and  checksum with a band accumulator that writes a PNG. Strictly less code than emulating a  printer, and "printer not connected" becomes "saved to ~/poketcg/prints/".

 ### Phase 8 — Widescreen and features (6–8 weeks)

 Only after the 4:3 port passes the full replay corpus. Feature bits live in a currently-unused  byte of WRAM, zelda3-style, so they are captured in snapshots and replays stay reproducible.  Version behaviour changes (kRam_BugsFixed) so semantic fixes don't invalidate the corpus.

 Total: 12–18 months solo; 6–9 months with 2–3 developers (Phase 5 splits cleanly). For  calibration: suiCune reached 70% of pokecrystal in 4.4 years solo without an oracle, on a  codebase twice this size (8.56 MB vs 4.26 MB of asm). zelda3 is ~70–80 kLOC of C with an  oracle.

 ────────────────────────────────────────────────────────────────────────────────

 7. Data pipeline

 Extract from the built ROM using poketcg.map section extents + poketcg.sym. Not from the .asm  sources, and not by keeping rgbds in the loop. The rejected options fail concretely:

 - Keep assembling and INCBIN the ROM's data sections — leaves every dw Label as a 16-bit
   bank-relative GB address, requiring a permanent bank-resolution shim.
 - Parse the .asm macros directly — textpointer, gfx, and frame_table cannot be evaluated    without final link addresses, and rgbds' stateful 4-charmap text engine has no standalone
   equivalent.
 - Use the existing Python tools — all eleven are dead. wram.py and gfx.py are Python 2 and    don't parse under 3; script_extractor*.py and extract_anim_data.py are one-shot    bootstrappers reading baserom.gbc at hardcoded offsets; constants.py is a stale    hand-maintained duplicate. Also worth knowing: tools/gfx.c and tools/bgmap.c never run —    they're guarded by $(if $(tools/gfx),...) and nothing in the repo ever sets those variables.

 Drive extraction from a hand-written schema (~20 entries) harvested from src/macros/wram.asm's  struct macros and the existing table_width / assert_table_length annotations. Follow CppRed's  two-stage codegen shape (tables in, C arrays out).

 Assets: convert from the built .2bpp/.1bpp/.pal artifacts, not the PNGs — going back to PNG  erases the whole rgbgfx flag matrix, including all 26 -x N trim-end overrides and the cards'  --columns --colors embedded --auto-palette. Keep 2bpp tile data (175 KB for cards, vs 2.8 MB  as RGBA) and decode to paletted indices at load. Decompress the ~207 .lz blobs at build time  but keep the ~40-line decompressor — two call sites use it as a streaming row-at-a-time API  into strided destinations. Note that byte-exactness of 128 of those blobs depends on  checked-in .lz.match files the greedy compressor cannot reproduce.

 Legal posture: commit the engine and the extractor; commit nothing generated. Gen1Recomp ships  a metadata-only manifest (label → [bank, addr], no dialogue, no images, no ROM bytes) and is  still up; LADX-HD bundled assets and was taken down. The in-tree PNGs make bundling tempting —  that is precisely the failure mode.

 ────────────────────────────────────────────────────────────────────────────────

 8. Top risks

 ┌───┬─────────────────────────┬──────────────────────────────────────────────────────────────┐  │ # │ Risk                    │ Mitigation                                                   │  ├───┼─────────────────────────┼──────────────────────────────────────────────────────────────┤  │ 1 │ Scope collapse from     │ Phase 0 harness before any game code. This is what cost      │  │   │ unbounded per-function  │ suiCune years.                                               │  │   │ verification            │                                                              │  ├───┼─────────────────────────┼──────────────────────────────────────────────────────────────┤  │ 2 │ Dimensions baked in     │ SCREEN_W/TILEMAP_W symbolic from the first commit; assert no │  │   │ during Phases 2–6,      │ literal 32/20/18 in tilemap math in review                   │  │   │ forcing a second pass   │                                                              │  ├───┼─────────────────────────┼──────────────────────────────────────────────────────────────┤  │ 3 │ Hybrid asm+bytecode     │ Design the RunScript re-entry contract in Phase 0, before    │  │   │ scripts resist clean C  │ touching src/scripts/                                        │  │   │ structure               │                                                              │  ├───┼─────────────────────────┼──────────────────────────────────────────────────────────────┤  │ 4 │ Widescreen has no valid │ Author the margins in the screen builders; clamp-to-bounds   │  │   │ off-screen tile data    │ as fallback, zelda3-style                                    │  ├───┼─────────────────────────┼──────────────────────────────────────────────────────────────┤  │ 5 │ Audio timing at 60.235  │ Derive the tick from 16384/68/4 exactly; sPlayTimeCounter    │  │   │ Hz not 60 Hz            │ must stay cartridge-compatible                               │  ├───┼─────────────────────────┼──────────────────────────────────────────────────────────────┤  │ 6 │ Bug-compatibility vs.   │ Preserve original bugs by default behind a faithful/fixed    │  │   │ correctness             │ ruleset gate. Known ones to keep: the Card Pop name-check    │  │   │                         │ loop that discards its result (card_pop.asm:195-208),        │  │   │                         │ VENUSAUR_LV64 unobtainable because both hash halves share    │  │   │                         │ parity (:328-337), SFX preemption not silencing the previous │  │   │                         │ SFX (sfx.asm:485-499).                                       │  └───┴─────────────────────────┴──────────────────────────────────────────────────────────────┘

 ────────────────────────────────────────────────────────────────────────────────

 9. Start here

 1. make DEBUG=1 — you now have poketcg.sym with all 20,280 symbols including the 1,518 WRAM
    ones. This is the input to everything.
 2. Write the .sym → wram.h/hram.h/sram.h generator. Half a day, and it makes the oracle
    possible.
 3. Write the PyBoy function-oracle harness: load state → set registers → break at symbol → run     to RET → dump full state. /tmp/pbenv already has PyBoy 2.7.0 and it auto-loads poketcg.sym.  4. Port UpdateRNGSources (src/home/random.asm) first — 20 lines, pure, zero dependencies, and
    it proves the whole loop end to end.
 5. Keep /tmp/tcgrecomp/out/build/poketcg as the scene oracle. Regenerate it with     --native-patch when you want function-level A/B on that side too; the project I built has     no patch dispatch because I generated it without that flag.

 The one thing I would not compromise on: nothing enters the game layer before the oracle  works. Every precedent that shipped had one; the precedent that stalled at 70% did not.
