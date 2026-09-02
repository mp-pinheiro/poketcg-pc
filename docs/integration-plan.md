# Vision Integration — full working port program

## Context

poketcg-pc has all 2,960 ROM routines ported to C (~133k asm lines) and per-function
byte-verified, but the composed native game does not behave like the ROM. This plan is
the integration program that closes `docs/vision.md` phases 2–8 and the release gate:
a playable, byte-equivalent-at-scene-level native port, then widescreen strictly on top.
It runs the mutation-receipt closure loop in parallel as one of its lanes.

Assessment this plan is built on (all verified this session, file:line in each step):

- **Forgejo tracker (fj, `fairfruit/poketcg-pc`)**: 34 open issues = projection of the 26
  `completion:v2` requirements. Failing set (`lifecycle/failing`): #3178 reference-state
  export, #3182 PPU scanline host effects, #3183 deterministic PCM, #3189 interactive
  card lists, #3190 duel callee-owned state, #3192 IR peer fixtures, #3196 indirect
  dispatch debt, #3209 enhanced corpus. `.factory/blocked.toml` is empty — no blockers.
- **Gate**: 5/26 requirements PASS; 8 failing, 13 missing (8 have no producer tool, 4 have
  scenario branches hardcoded to FAIL, `raster-effects` is runnable today but never run).
- **Root causes of scene divergence** (ranked):
  1. The ROM's `VBlankHandler` work (OAM DMA, hSCX/hSCY/hWX/hWY + wLCDC flush,
     `wVBlankFunctionTrampoline`, `FlushPalettesIfRequested`) has no native counterpart —
     deliberately omitted for the per-function probe world (`tools/factory/prompt.py:264-268`).
     Result: palettes pinned white (deferred flushes never drain), `g_oam` never populated
     (only the probe calls `DMA()`), scroll/window registers sampled once at boot.
  2. Timer cadence: native calls `TimerHandler()` once per frame; hardware fires it every
     1088 CPU cycles (TAC=$07, TMA=$BC) ≈ 64.5×/frame → serial timeout, play-time, and APU
     divergence (native 1,479 vs reference 6,554 APU writes in 600 frames, first mismatch
     at write 8).
  3. Boot-loop structure truncated: asm has two infinite loop levels
     (`GameLoop` → `_GameLoop` `.main_menu_loop` + `MainMenuFunctionTable` dispatch);
     the C runs `_GameLoop()` once then spins bare `DoFrame()` forever — the game cannot
     structurally progress. `MainMenu_ContinueFromDiary`/`_ContinueDuel` are stubs,
     `MainMenu_CardPop` never loops back.
  4. Intro/menu divergences: extra early `PlaySong(MUSIC_TITLESCREEN)` (`src/home/intro.c:57`),
     missing `.ShowPressStart` epilogue, missing `CopyDMAFunction` in `Start`, missing
     A+B+Start+Select soft reset, missing PAD_SELECT debug pause.
  5. Parked indirect dispatch: `wCardListUpdateFunction`, `TryExecuteEffectCommandFunction`
     `jp hl` into bank $0b, `wVBlankFunctionTrampoline`, >4 `wDoFrameFunction` targets —
     all silently no-op today.
- **Harness gaps**: no per-frame state bisect tooling; `state_dump.c` emits exactly one
  hardcoded edge so `completion-cfg` (15,828 required asm edges) can never pass; scenario
  branches missing for `boot-title-negative`, `save-interchange`, `audio-pcm`,
  `faithful-4x3:package`; 13 missing evidence artifacts.
- **Mutation campaign**: 2,410/2,477 receipts RED; 67 unresolved (52 missing + 15
  invalid). Seeded deferral list from the prior session:
  `CreateEnergyCardListFromDiscardPile_AllEnergy`, `GetAttacksEnergyCostBits`. A prior
  session already repaired the `ApplyBackgroundScroll` primary-evidence defect and the
  `ApplyCardCGBAttributes` hardcoded-palette production bug through this loop.

Decisions already made with the user:
- **CFG gate semantics**: function-level edges. Amend `tools/completion/cfg.py` so
  `required_edges` = cross-function edges (call/jp between distinct registered routine
  labels + `<indirect>` edges matched by resolved-target edges), keep the full
  label-level set as report-only data. Emit real function-level edges from a
  trace-instrumented native build. Lowest rework risk; label-fallthrough coverage is
  unobservable-by-construction in a C port.
- **Parallel topology**: jj workspaces + serialized landing (see Parallelization).
- **Mutation-receipt loop**: kept, not replaced — it runs as Wave-1 Lane 5 under the
  loop's own contract (embedded in step 20), with pushes routed through the integrator's
  light landing path.

Intended end state: `just oracle-release-gate` exits 0 with all 26 requirements PASS,
mutation campaign `complete: true`, and cfg required-edges covered;
`./build/poketcg --data-pack build/completion/data-pack.bin` plays intro → title →
menus → duel with working save; widescreen corpus green on top.

## Approach

Execution is wave-ordered. Within a wave, lanes run fully parallel in separate jj
workspaces; one integrator serializes landings (Parallelization section). Step numbering
is global; "after W1" means after Wave 1 has landed and passed its landing checks.

### Wave 0 — seams pre-landing (integrator, single commit, before fan-out)

1. Add the two hook points every wave-1 lane needs, so no later lane edits `src/runtime.c`
   concurrently:
   - `runtime.h`: `typedef void (*RuntimeStateDumpCb)(uint32_t frame, const RuntimeResult *r);`
     and `void runtime_set_state_dump_frames(RuntimeStateDumpCb cb, const uint32_t *frames, size_t count);`
     — implemented in `src/runtime.c` host loop: after each frame's work, if the frame
     index is in `frames`, invoke `cb`. No-op default.
   - `src/runtime.c` host loop: add `uint32_t timer_cycles;` to `RuntimeState`
     (Lane 1 fills in the call loop).
   - Landing scaffold: `just land-lock *CMD` recipe wrapping the command in
     `flock .locks/land.lock`; create `.locks/` (gitkeep).
2. Rebuild + `just oracle-diff DoFrame` (unchanged, must stay PASS) + `just package-smoke`.
   Commit `chore(runtime): add integration seams`.

### Wave 1 — substrate + structure + tooling + receipts (5 parallel lanes)

**Lane 1 — host frame substrate** (owns `src/runtime.c`, `src/ppu.c`, new `src/home/vblank.{c,h}`)

3. Create `src/home/vblank.c` with `void RuntimeVBlankHandler(void)` porting
   `poketcg/src/home/vblank.asm:3-37` in exact order:
   (a) if `wVBlankOAMCopyToggle` requests it → `DMA()` (`src/home/dma.c:11-21`) and mirror
   the asm's toggle handling exactly (read vblank.asm:11-16 for the reset semantics);
   (b) flush `hSCX`/`hSCY` → `$FF42`/`$FF43` and `hWX`/`hWY` → `$FF4A`/`$FF4B`
   (vblank.asm:17-24); (c) flush `wLCDC` → `$FF40` (vblank.asm:26-27);
   (d) dispatch `wVBlankFunction`/trampoline fail-loud (see step 13);
   (e) `FlushPalettesIfRequested()` (`src/home/palettes.c:56-73`).
   Leave `wVBlankCounter++` inside `DoFrame` (already at the faithful position).
4. `src/runtime.c` host loop, per frame after `shell_pump`, before granting resume, in
   this order: timer batch (step 5) → `RuntimeVBlankHandler()` → existing
   `ppu_render_frame`/audio. This is the halt-return semantics: handler work is visible
   to game code after `DoFrame` returns.
5. Timer cadence in the same host block:
   `state.timer_cycles += 70224; while (state.timer_cycles >= 1088) { TimerHandler(); state.timer_cycles -= 1088; }`
   (70224 cycles/frame; 1088 = 16-cycle tick × 68-tick period from TAC=$07/TMA=$BC;
   the double-speed path is deleted in this port so 1088 is unconditional). If the APU
   write sequence still mismatches after this, mirror gb-recompiled's ISR batching model
   instead (contingency, see Assumptions).
6. `src/ppu.c`: stop consuming the boot-time `ppu_init_offsets` snapshot; read
   SCX/SCY/WX/WY from `g_io` at each render call (move the offset read into
   `ppu_render_frame`). Keep the LCD-off 0x7FFF fill as-is (`ppu.c:87-92`).
7. Verify (Lane 1): `just oracle-diff-group frames`, `oracle-diff-group lcd`,
   `oracle-diff-group palettes` stay PASS (probe world untouched — no boundary installed
   there); `python3 tools/completion/scenario.py audio-catalog` shows native_writes
   ≈ 6,500±130 and first_mismatch pushed past 100; a 900-frame no-input native run's
   framebuffer is no longer uniformly 0x7FFF (distinct pixel values > 1).

**Lane 2 — boot-loop structure + intro parity** (owns `src/home/game_loop.c`, `src/home/main_menu.c`, `src/home/start.c`, `src/home/intro.c`, `src/home/input.c`)

8. Restore the two-level loop: `GameLoop()` becomes `for (;;) { _GameLoop(); }`
   (`game_loop.asm:22-23`); `_GameLoop()` becomes the `.main_menu_loop` port: set
   `wLastSelectedStartMenuItem = 0xFF`, loop `Func_c1f8(); HandleTitleScreen();`
   then dispatch `MainMenuFunctionTable[wStartMenuChoice]` via a function-pointer table,
   mirroring `main_menu.asm:11-20` carry semantics (`jr c, .main_menu_loop` vs restart).
9. Unfold the menu dispatch out of `HandleTitleScreen` (`start.c:360-374`) into
   `_GameLoop`. Port the truncated bodies: `MainMenu_ContinueFromDiary` and
   `MainMenu_ContinueDuel` from `main_menu.asm:42-68` (save validation, load,
   `ExecuteGameEvent`); `MainMenu_CardPop` loop-back per `main_menu.asm:36-40`.
   New/changed routines get factory-contract quartet entries (cases: all-zero, POISON,
   boundaries; mutation with receipt) matching the existing marker style.
10. Intro parity in `src/home/intro.c` + `start.c`: delete the early
    `PlaySong(MUSIC_TITLESCREEN)` at `intro.c:57` (music comes from the
    `intro_seq_play_title_screen_music` command, `data/sequences/intro.asm:44`);
    port `.ShowPressStart` (`intro.asm:52-73`: SPRITE_PRESS_START at (48,112), anim
    190/191 by console, `Func_12ac9` with bc=60); re-call `LoadTitleScreenSprites`
    after the intro (`start.asm:20`); add `CopyDMAFunction` to `Start` — port
    `home/dma.asm`'s HRAM copy so `g_hram` state matches the bytes the asm copies.
11. `src/home/input.c`: port the A+B+Start+Select soft-reset (`input.asm:36-44`):
    `Reset()` longjmps to a `setjmp` in `run_game` that re-runs `Start(0x11); GameLoop();`
    (WRAM preserved, matching hardware). Port the PAD_SELECT debug-pause loop
    (`frames.asm:29-39`) as a `DoFrameDebugPause` helper called from `DoFrame`
    (coordinate the `frames.c` call-site insertion with Lane 3's landing).
12. Verify (Lane 2): `just oracle-diff-group main_menu`, `start`, `intro`, `input`,
    `game_loop` PASS (new cases included); no-input 10,000-frame headless run
    (`timeout 300 ./build/poketcg --headless --frames 10000 --data-pack
    build/completion/data-pack.bin --trace-entries /tmp/t.json`) completes without
    wedge and its trace shows `TITLE_READY`. If it wedges, the candidates in priority
    order are `HandleAnimationFrame`'s frame-parse `for(;;)` (`sprite_animations.c:192-214`),
    `AnimateRandomTitleScreenOrb`'s pick `do{}while` (`intro_sequence_commands.c:47-56`),
    `Music1_PlayNextNote`'s `for(;;)` (`music1.c:318-383`); pin with `gdb -p` on the
    wedged worker (thread backtrace) and fix the underlying parity bug.

**Lane 3 — indirect dispatch completion (#3196)** (owns `src/home/frames.c` dispatch, new `src/home/indirect_dispatch.{c,h}`, `src/home/deck_configuration.c`, `src/home/deck_machine.c`, `src/home/effect_commands.c`)

13. Generalize the `CallDoFrameFunction` pattern into a shared fail-loud helper:
    `void DispatchIndirect(const char *site, uint16_t target)` — unknown nonzero
    target → `fprintf(stderr, "indirect dispatch miss site=%s target=$%04X\n", ...)`
    + `abort()`. Replace the silent default in `frames.c:73-77`.
14. Enumerate and resolve every parked site, registering each asm target to its C body:
    `wCardListUpdateFunction` (targets enumerated from the `CardListParameters` writers
    in bank-2 asm; parked comments at `deck_configuration.c:1209`, `deck_machine.c:674`),
    `TryExecuteEffectCommandFunction`'s bank-$0b `jp hl` (`effect_commands.c:21-23`;
    dispatch to the ported effect functions via the `src/macros/` tables),
    `wVBlankFunction` (Lane 1's step 3d; known target `HandleAllSpriteAnimations`), and
    any `wDoFrameFunction` target beyond the four in `frames.c:15-18` (grep
    `wDoFrameFunction` writers in `poketcg/src/**.asm`). `wListFunctionPointer` is
    already called directly (`core.c:7662-7666`) — verify only.
15. Verify (Lane 3): `just oracle-diff-group deck_configuration`, `deck_machine`,
    `effect_functions` PASS; with Wave 1 landed, a scripted input run reaching a card
    list no longer aborts and navigates.

**Lane 4 — harness tooling** (owns `tools/completion/*`, `src/main.c` flags, `tools/oracle/gbrecomp_oracle.py` if needed)

16. Native per-frame dumps: `--dump-state-frames 100,400,900` flag in `src/main.c`
    wiring `runtime_set_state_dump_frames` (Wave 0 seam) to call `runtime_write_state`
    with a `-f<N>` path suffix. No `runtime.c` edit needed.
17. New `tools/completion/frame_bisect.py`: given a scenario id and field list, run the
    native lane with `--frames N` and the oracle-b lane with `--limit-frames N` for the
    same input timeline, compare final states via `tests/scene_diff.py` normalization,
    binary-search the smallest N with a mismatch, then linear-scan fields/offsets.
    Emits `{"frame", "field", "offset", "native", "reference"}` JSON. Oracle-b per-frame
    via limit sweeps is O(N²) at ≤2000 frames ≈ 11 runs — acceptable; do not patch
    gb-recompiled unless a sweep exceeds 10 min (contingency).
18. Implement the `boot-title-negative` branch (`scenario.py:317-318`): cold-boot both
    lanes on the same input, bisect to first mismatch, write `negative-evidence-v1`
    with `first_mismatch_region`/`first_mismatch_offset`/`replay_artifact` per
    `requirements.toml:284-293`. Implement the `save-interchange` branch (native
    `--save` ↔ emulator save round-trip, `SAVE_ROUND_TRIP`, `requirements.toml:259-267`)
    and the `faithful-4x3:package` producer (`PACKAGE_ROM_FREE`: package_smoke evidence
    → `package-proof-v1`, `requirements.toml:441-449`). Implement the `p2:leaves`
    producer (`function-corpus-v2`: new `completion.py leaves` subcommand summarizing
    per-function corpus + receipt state into the artifact).
19. Verify (Lane 4): `python3 tools/completion/scenario.py raster-effects` (runnable
    today) produces an artifact; `python3 tools/completion/frame_bisect.py boot-title`
    prints a real first mismatch; each new producer writes a schema-valid artifact
    (PASS or honest FAIL).

**Lane 5 — mutation-receipt closure loop** (owns `tools/oracle/mutation_receipts/*.json` and canonical `CASES`/`CONTRACT`/`MUTATIONS` edits in `tests/cases/*.py` for basenames not owned by Lanes 2–3)

20. Run the established receipt-closure loop to completion. Starting state: 2,410 RED /
    15 invalid / 52 missing (2,477 total); seeded deferral list:
    `CreateEnergyCardListFromDiscardPile_AllEnergy`, `GetAttacksEnergyCostBits`.
    Per unresolved witness:
    - Run `just completion-mutation-campaign --missing --limit 1`, or directly
      `python3 tools/run_mutation.py <Fn> tests/cases/<file>.py --index <primary-index> --build build --runner tools/oracle/gbref/build/gbref_runner`.
    - On RED: rerun the report and require `receipt_red` +1 and
      `receipt_missing + receipt_invalid` −1; commit exactly that witness
      (`fix(port): cover <short-name> mutation`, subject ≤50 chars, no body).
    - On FAIL, apply the established taxonomy:
      (A) `SCHEMA comparator slice requires primary evidence` — case-selection defect:
      trace the mutation's first `case_ids` entry to its `SCHEMA2_CASES` index and make
      it select a real primary oracle case, adding the smallest canonical primary case
      that observes the corruption if none exists;
      (B) `MUTATION_GREEN` — strengthen or add a canonical primary case observing the
      corruption; replace the mutation only if genuinely stale/non-observable;
      (C) `MUTATION_BASELINE_FAILED` with PORT mismatch — root-cause the parity failure
      and repair the production routine, adapter, contract, or case at the actual fault
      (re-derived from the assembly), like the `ApplyCardCGBAttributes` palette fix;
      (D) missing/ambiguous/stale anchor — re-derive `before`/`after` as one unique,
      shape-preserving, observably wrong corruption;
      (E) build/execution failure — repair repository-local causes and confirm the
      runner restored the original source.
    - Verification quadruple after any change: `just oracle-diff <Fn>` baseline PASS,
      mutated PORT mismatch, restored PASS, tool-generated RED receipt.
    - Never: hand-create/edit/copy/mark a receipt RED, weaken a mutation into a trivial
      corruption, suppress a comparator failure, hand-edit `SCHEMA2_CASES` or
      `tests/routines.py`, run the central gate / factory commands / tracker updates
      from this lane, or narrow `vread`/`compare` spans to dodge a genuine divergence
      (the `DrawDuelHorizontalSeparator` precedent — if the asm writes bytes the port
      does not, fix the port).
    - Anti-stall: after two materially different, evidence-based repair attempts fail,
      record the witness + attempts in the lane's deferred list, leave the tree clean,
      and move to the next non-deferred name; revisit deferred names after one full pass.
    - Landing: one commit per witness in the workspace; the integrator lands
      receipt-only batches on the light path (step 39) so per-witness throughput is
      preserved without this lane ever pushing `main`.
    Completion: `just completion-mutation-campaign --report` shows `complete: true`
    (receipt_red 2477, missing 0, invalid 0), or every remaining witness is deferred
    with a consolidated blocker table after a zero-progress retry pass.

### Wave 2 — boot-title green (after W1; single lane — the fix loop)

21. Iterate to `just completion-scenario boot-title` PASS: run the scenario, take the
    mismatch list, run `frame_bisect.py boot-title`, fix the first divergent write
    under the normal per-function oracle discipline (`just oracle-diff <Fn>` after each
    fix), repeat. PASS requires: terminal_event `NEW_GAME_ENTERED` (input timeline
    A@1000, DOWN@1100, A@1101, START@1200, A@1201), events ≥ 3, zero mismatches across
    the 22 state fields at frame 2000.
22. Regenerate the five stale producers (`just completion-baseline`,
    `completion-rom-coverage`, `completion-routine-mapping`, `completion-substrate`,
    `completion-hardware-removal`) so their `content_key` is current.
23. Close p2: `boot-title-negative` PASS (real FIRST_MISMATCH evidence under its
    perturbation), `save-interchange` PASS, `leaves` PASS. Playable check: windowed run
    (`./build/poketcg --data-pack build/completion/data-pack.bin`) reaches the start
    menu and starts a New Game with visible, correctly-paletted intro/title.

### Wave 3 — audio + UI/raster (2 parallel lanes, after W2)

24. **Audio lane**: drive `audio-catalog` to PASS (APU (address,value) sequence
    equality; cadence landed in step 5 — remaining deltas are per-function fixes via
    APU-trace diffing). Implement the `audio-pcm` branch (`PCM_WINDOW_CLOSED`,
    `audio-pcm-v1`: windowed PCM via existing `apu_trace_render_pcm`; if oracle-b
    cannot export PCM windows, the contract is APU-register equality plus native PCM
    determinism across two runs — record the rationale in the artifact `detail`).
25. **UI/raster lane**: `ui-corpus` to PASS (framebuffer + wram/vram/oam/palette
    equality on its scenario); `raster-effects` to PASS (per-scanline offset arrays —
    ensure `wLYOverrides`/`hLCDCPointer`/`scroll.asm` range writes reach the PPU's
    per-scanline offsets each frame, extending step 6's per-frame read to per-line
    array semantics per the CppRed model in vision.md).
26. Interactive-card-list debt (#3189) closes here: scripted menu corpora reach card
    lists through Lane 3's dispatch; add corpus scenarios as the requirement's
    state_fields demand.

### Wave 4 — duel (after W3)

27. `p5:duel-state`: define the `duel-vector-v1` producer (new scenario mapping in
    `scenario.py` + a driver setting up duel vectors via `setup` preludes on both
    lanes); PASS = `DUEL_VECTOR_CLOSED` with wram/rng/input_latch equality. Model
    callee-owned state per #3190 with the 826-byte duel state
    (`DuelDataToSave`, `core.asm:6117-6126`) as the compared anchor.
28. `p5:seeded-duel`: scripted seeded-duel replay, memcmp the duel state every turn
    (extend `frame_bisect`/`scene_diff` with turn-boundary snapshots marked via a new
    runtime event recorded at turn transitions). Effects frame-wait bounds (#3188):
    corpus inputs must exercise and bound every `DoFrame`-waiting effect path.

### Wave 5 — overworld + scripts (after W4)

29. `p6:maps-and-campaign` campaign inputs: boot→first duel (#3197), eight medals
    (#3198), dome→credits (#3199) — long RLE input scripts (`p<start>-<last>/<period>`
    form; `--input` caps at 2048 entries). Bisect divergences with per-frame dumps.
30. `p6:script-vm`: `script-coverage-v1` producer counting the 104 opcodes executed by
    the corpus (bitmap counter on `script_dispatch_generated.c` dispatch, trace build
    only); PASS = `SCRIPT_OPCODE_CLOSED` with every opcode exercised or enumerated
    unreachable-in-corpus with asm-derived justification.

### Wave 6 — transport, IR, printer (starts after W2; parallel with W4/W5; vision.md Phase 7)

31. Delete `ir_core.asm`'s bit-banged physical layer wholesale per vision; keep the
    8-byte register-frame ABI, `IRCMD_*` dispatcher, param/magic matching, Card Pop
    name-list exchange + name-hash rarity roll, Gift Center payloads. Apply the two
    security fixes: drop `IRCMD_CALL_FUNCTION` (RCE by design), bounds-check the
    `de`/`c` pair in `IRCMD_RECEIVE_DATA`.
32. TCP session transport (#3201) with the session-type byte serving link duels + IR;
    deterministic IR peer fixtures (#3192) for the corpus (the scripted RP protocol in
    `mem.c:389-447` is the seam — extend it to fixture replay).
33. Printer (#3202): cut at `SendPrinterPacket`; band accumulator writing PNG (layout +
    1bpp→2bpp + 40-tile band slicing kept; 12-step IRQ state machine, RLE, checksum
    replaced). Output: `--print-dir` flag, default `$XDG_DATA_HOME/poketcg/prints`.
    `p7:printer` producer (`PRINTER_PNG_CLOSED`, `printer-corpus-v1`); `p7:link-ir`
    corpus over TCP loopback fixtures.

### Wave 7 — widescreen + release (after W5/W6; vision.md Phase 8)

34. Span widening (#3205) in the PPU (dimensions are runtime variables already);
    single viewport rect (#3206) for overworld culling/NPC/animation; authored wide
    layouts (#3207) in menu builders + duel screen (extra columns authored, not
    revealed; clamp-to-bounds fallback); render-only isolation (#3208) behind a feature
    flag that gates the oracle off (zelda3 pattern, vision.md).
35. `p8:release:enhanced-corpus` (#3209): replay corpus green at 4:3 with zero
    features, widescreen additive on top. `faithful-4x3:release`: implement the
    `new-game-to-credits` comparison branch (real input script to credits, oracle-b vs
    native state+pixel equality). `faithful-4x3:package` from step 18's producer.
36. Edge-trace closure (CFG): trace build with `-finstrument-functions`; bounded
    open-addressing edge table in new `src/edge_trace.c` (caller/callee pointer pairs,
    ~64k slots, duplicates coalesce); dispatch sites (step 13) emit resolved edges into
    it; `runtime_write_trace` dumps raw pairs; a tools script resolves addresses →
    pret names via `nm` + the symbol table. Amend `tools/completion/cfg.py`:
    `required_edges` = edges where source and target are distinct registered routine
    entries (cross-function call/jp) plus `<indirect>` edges matched by resolved-target
    edges; the full 15,828-edge enumeration stays in the report as informational.
    Drive the corpus until `uncovered_required_edges == 0`.
37. Final: `just completion-mutation-campaign --report` exit 0; regenerate all 26
    artifacts; `just oracle-release-gate` exit 0; `just completion-tracker-sync` +
    `completion-tracker-check`; push. Release tag per repo convention.

## Parallelization

Topology: **jj workspaces + serialized landing** (user-approved).

- One shared jj repo at the checkout. Each lane: `jj workspace add ../poke-<lane>`
  (own working copy + commits), private build dir `POKETCG_BUILD=build-<lane>`. Lanes
  never push `main`.
- **File ownership is the concurrency contract.** Wave 1 ownership:
  Lane 1 `src/runtime.c`, `src/ppu.c`, `src/home/vblank.*`;
  Lane 2 `src/home/{game_loop,main_menu,start,intro,input}.c`;
  Lane 3 `src/home/{frames,indirect_dispatch,deck_configuration,deck_machine,effect_commands}.c`;
  Lane 4 `tools/completion/*`, `src/main.c`, `tools/oracle/gbrecomp_oracle.py`;
  Lane 5 `tools/oracle/mutation_receipts/*` + `tests/cases/*.py` edits outside Lanes 2/3
  basenames. Cross-lane needs route through the Wave 0 seams (why steps 1–2 exist).
- **Landing protocol** (integrator session — only writer of `main`, only gate runner):
  38. Acquire `.locks/land.lock` (flock via `just land-lock`); import/rebase the lane's
      commits in change-id order; `just build`.
  39. Light path for receipt-only batches (Lane 5): `python3
      tools/completion/mutation_campaign.py --report` shows the expected red delta and
      no new invalid/missing, then push `main` immediately — no full gate, preserving
      the receipt loop's per-witness throughput. Full path for code-bearing batches:
      `just oracle-release-gate` must pass before push; on failure, bisect the batch by
      splitting it in half and recursing (factory rejection discipline), quarantining
      the failing commit back to its lane with the diagnostic.
  40. After each full-path landing: `just completion-tracker-sync` +
      `completion-tracker-check`, release lock.
- Concurrency budget: ≤16 concurrent agents total. Mechanical fan-out (receipts,
  campaign input authoring, per-function fix loops in Wave 2+) uses `task` batches
  inside a lane; each child gets basename-scoped instructions and skips validators.
- Escalation rule (from project history): lanes own routine-level failures themselves;
  only missing external infrastructure (oracle binaries, ROM bootstrap) blocks the loop.

## Critical files & anchors

- `src/runtime.c:110-160` — host frame loop; the seam where timer batch + VBlank handler
  land (steps 4–5). Everything about whole-game cadence is here.
- `poketcg/src/home/vblank.asm:3-37` — the exact contract `RuntimeVBlankHandler` ports
  (step 3); the single highest-leverage fix in the program.
- `src/home/main_menu.c:77-85` + `poketcg/src/engine/menus/main_menu.asm:4-20` — the
  two-level boot loop being restored (steps 8–9).
- `tools/completion/scenario.py:142-335` — scenario runner with the four unimplemented
  branches at :317-320 and the boot-title comparison at :197-236 (steps 18, 35).
- `tools/completion/cfg.py:52-132` — edge enumeration and required-set filter site
  (step 36).

## Verification

End-to-end proof, in order (each step's PASS is the next step's gate):

1. Substrate (step 7): `python3 tools/completion/scenario.py audio-catalog` — native
   APU writes within 2% of reference count; 900-frame no-input native framebuffer has
   >1 distinct pixel value (was uniform 0x7FFF).
2. Structure (step 12): 10,000-frame no-input headless run completes under
   `timeout 300`, trace JSON shows `TITLE_READY` (was BOOT_STARTED-only + wedge).
3. Receipts (step 20): `just completion-mutation-campaign --report` prints
   `"complete": true` (2,477/2,477) or a consolidated deferred-blocker table after a
   zero-progress retry pass.
4. Wave 2 (step 21): `just completion-scenario boot-title && just completion-check
   completion:v2:p2:boot-title` — artifact PASS, zero state mismatches; then the same
   for boot-title-negative, save-interchange, leaves.
5. Playable (step 23): windowed `./build/poketcg --data-pack
   build/completion/data-pack.bin` — intro animates with visible sprites and correct
   palettes, PRESS START appears, A opens the start menu, New Game reaches name entry;
   `--save`/`--load-save` round-trips a save.
6. Phases (steps 24–35): `just completion-check <each of the 26 requirement ids>` PASS.
7. Terminal (step 37): `just oracle-release-gate` exit 0 (all constituents PASS, cfg
   `uncovered_required_edges == 0`); `jj git push --bookmark main` clean;
   `just completion-tracker-check` exit 0.

Prerequisites for scenario work: `just build`, `just completion-data-pack`,
`just oracleb-regenerate` (oracle-b binary), `uv sync --project tools/oracle --frozen`.
Prerequisite for cfg: a trace from the instrumented build via package-smoke
(`POKETCG_CFG_TRACE` env, `tools/oracle/release_gate.py:139-142`).

## Assumptions & contingencies

- **CFG gate semantics (user-approved)**: function-level required edges. If a later
  audit pass objects, the fallback is the same build emitting edges plus an explicit
  documented exclusion list for intra-routine fallthroughs — never hand-instrument
  2,960 routines for synthetic coverage.
- **Timer batching**: batched 1088-cycle ticks at the frame boundary is the model. If
  the APU write *sequence* still mismatches after cadence (order-sensitive
  interleaving with game APU writes), read gb-recompiled's ISR scheduler and mirror its
  batching boundary exactly instead of inventing a finer interleave.
- **rVBK literal**: `Start` writes `rVBK=0xFE` vs asm's `BankswitchVRAM0` (0). Same
  effective bank; change to 0 only if `io` field mismatches persist after Wave 2.
- **Soft reset mechanism**: setjmp/longjmp in `run_game`. If probe contracts regress
  (`Reset` reachable from probe cases), guard with `frame_boundary_is_installed()`.
- **Oracle-b per-frame dumps**: limit-frame sweeps only; patch gb-recompiled for
  periodic dumps only if a bisect sweep exceeds 10 minutes.
- **Deferred receipts**: the two seeded deferrals may need production-code fixes in
  `src/home/` basenames owned by Lanes 2/3 during Wave 1 — route those fixes through
  the owning lane (message via the integrator) rather than cross-editing.
- **audio-pcm reference**: if oracle-b cannot export PCM windows, register-level
  equality plus native PCM determinism satisfies the requirement; record the rationale
  in the artifact `detail` field rather than weakening the schema.
- **Playtime cadence**: `IncrementPlayTimeCounter` semantics are already ported
  (`time.c:18-19`); timer cadence (step 5) is what makes it observable — no separate
  work unless boot-title shows wPlayTime* drift after Wave 2.
- Stale `local/full-game-findings.json` (v1 scaffold) is superseded by this plan; the
  Forgejo tracker remains the projection of record — `completion-tracker-sync` keeps it
  honest after every full-path landing wave.
