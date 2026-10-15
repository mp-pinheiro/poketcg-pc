# poketcg-pc architecture and acceptance

## Product architecture

poketcg-pc is a native C11/SDL2 port of the Pokémon Trading Card Game for Game Boy Color. Game logic runs without an emulator or ROM at runtime. The simulation and verified framebuffer are fixed at 160×144 pixels; host-side integer scaling and letterboxing/pillarboxing do not change game state or canvas dimensions.

The port retains the cartridge memory model and generated symbol layout. Game routines access emulated addresses through the memory bus, while host services provide presentation, audio output, and serial transport. ROM-derived data is supplied through the generated data pack. Profile-specific data and evidence remain isolated; the profile build configuration selects the `CardId` width.

The game RNG is deterministic software state: `UpdateRNGSources` advances `wRNG1`, `wRNG2`, and `wRNGCounter`; the codebase has zero reads of `rDIV`. This supports reproducible seeded verification, not exhaustive session coverage.

IR remains bus-level behavior. Ported transmit/receive routines access RP through the memory bus, whose runtime model supplies a synthetic response stream. The host socket transport implements serial SB/SC exchanges; it does not replace IR. Recorded linked-reference sessions establish serial link-duel behavior and printer output, but do not cover complete Card Pop or Gift Center IR routes. The bounded hardware transform is recorded in [phase1-transform.md](phase1-transform.md).

## Component boundaries

| Component | Implementation | Boundary |
|---|---|---|
| Native game routines | `src/home/`, `src/profiles/<profile>/` | Shared logic plus composed profile-specific blocks. |
| Cartridge state and bus | `src/mem.c`, generated layout headers | Game addresses, bank state, and mutable memory retain cartridge semantics. |
| Rendering and sound | `src/ppu.c`, `src/apu.c` | Software rendering and audio state produce the game's fixed-canvas output. |
| Host interface | `src/runtime.c`, `src/shell.c`, `src/presentation.c` | Input, frame execution, devices, and host scaling surround the simulation. |
| Persistence and selection | `src/persistence.c`, `src/profile.c`, `src/launcher.c` | Tagged saves and the launcher keep game identities separate. |
| Build and proof tools | `tools/`, `tests/`, `profiles/profiles.json` | Generate data and compare independent reference execution; they are not a runtime emulator requirement. |

## Acceptance claims

The claims below are machine-bound by `tools/completion/requirements.toml`. A successful reference-backed result requires native/reference agreement for every required representation field at the comparison anchors throughout the complete declared recording, with no early truncation. Each claim remains bounded to its configured scenario or corpus; measured evidence is not exhaustive coverage.

### Reset and substrate

- `completion:v2:reset:baseline`: pin the source ROM identity, map, symbols, and canonical routine inventory in a baseline artifact with `BASELINE_PINNED`.
- `completion:v2:reset:rom-coverage`: account for every ROM byte as code, data, header, or padding; close the partition with `ROM_COVERAGE_CLOSED`.
- `completion:v2:reset:routine-bijection`: establish the canonical routine-to-registration mapping, native disposition, and source span; close with `ROUTINE_MAPPING_CLOSED`.
- `completion:v2:p0:substrate`: demonstrate routine and replay comparison over required memory and the 160×144 framebuffer; emit `SUBSTRATE_READY`.
- `completion:v2:p1:hardware-removal`: evidence the named hardware-transform state, timer/frame, mapper, and input-latch semantics; emit `HARDWARE_TRANSFORM_CLOSED`.

### Save, boot, and leaves

- `completion:v2:p2:leaves`: close the leaf routine corpus with memory and function-boundary register observations; emit `LEAF_CORPUS_CLOSED`.
- `completion:v2:p2:save-interchange`: prove save interchange through the declared round-trip event and all four SRAM banks; emit `SAVE_ROUND_TRIP`.
- `completion:v2:p2:boot-title`: from pinned CGB boot, enter a new game after at least 600 rendered frames and compare required game state and pixels; emit `NEW_GAME_ENTERED`.
- `completion:v2:p2:boot-title-negative`: perturb one expected state byte and report the first mismatch region and offset; emit `FIRST_MISMATCH`.

### Audio and presentation

- `completion:v2:p3:audio-trace`: close the APU register-write trace with timer/frame state observations; emit `AUDIO_TRACE_CLOSED`.
- `completion:v2:p3:audio-pcm`: close the declared PCM window with trace and framebuffer evidence; emit `PCM_WINDOW_CLOSED`.
- `completion:v2:p4:ui-corpus`: close the UI scene corpus with memory, VRAM, OAM, palette, and fixed-canvas framebuffer observations; emit `UI_CORPUS_CLOSED`.
- `completion:v2:p4:raster-effects`: close raster-effect scenes with framebuffer and both VRAM banks observed; emit `RASTER_EFFECTS_CLOSED`.

### Duel and campaign

- `completion:v2:p5:duel-state`: close the duel-state vector with memory, deterministic RNG, and input observations; emit `DUEL_VECTOR_CLOSED`.
- `completion:v2:p5:seeded-duel`: replay the seeded duel through terminal outcome with native/reference agreement on required state, RNG, framebuffer, and save observations throughout the full declared session; emit `DUEL_TERMINAL_OUTCOME`.
- `completion:v2:p6:script-vm`: close script opcode coverage with memory, mapper, and input-latch observations; emit `SCRIPT_OPCODE_CLOSED`.
- `completion:v2:p6:maps-and-campaign`: reach credits through the complete declared campaign recording with native/reference agreement on required game state, framebuffer, save, and RNG observations; emit `CREDITS_REACHED`.

### Transport, printer, and release

- `completion:v2:p7:link-ir`: compare both native consoles against their linked serial reference cores through the complete recorded link-duel sessions, including required transport, memory, and input observations; this is not an end-to-end IR claim. Emit `LINK_SESSION_CLOSED`.
- `completion:v2:p7:printer`: produce printer pages whose rendered output matches the linked reference pages, with no missing or extra pages; emit `PRINTER_PNG_CLOSED`.
- `completion:v2:faithful-4x3:release`: attest the faithful fixed-canvas release across the declared memory, hardware, runtime, audio, render, persistence, transport, and printer fields, with reference agreement through the complete required recordings; emit `CREDITS_REACHED`.
- `completion:v2:faithful-4x3:package`: pass the 600-frame package smoke and prove a package missing a required data span fails with `MISSING_DATA`; verify the executable and generated data pack contain no ROM; emit `PACKAGE_ROM_FREE`.

The completion manifest defines each claim's dependencies, minimum frames/events, state fields, artifact schema, and command. Audio PCM acceptance uses its declared thresholds, not byte-exact waveform equality. A scenario or corpus proves only its complete recorded inputs and declared scope. Current measured evidence is recorded in generated completion artifacts; it is not exhaustive coverage of all routines, branches, scenes, or hardware behavior.

## Proof identity and provenance

The executable acceptance contract is the parsed completion manifest and its producer/comparator code. Evidence keys retain every contract field except the documentation source path, source SHA, and requirement anchors. Those excluded fields are checked against this page separately; moving or rewriting prose does not change the game inputs.

The release attestation records the measured source revision, full source hash, and an execution hash. The execution hash excludes only `README.md`, `CHANGELOG.md`, and Markdown under `docs/`, plus generated dashboard outputs. Code, cases, configuration, agent instructions, and runtime artifacts retain their checks. A reused attestation keeps its original measurement revision, logs, and durations; the gate reports the current validated revision separately.

The attestation includes the measured routine registry and completion audit. A source-only checkout can validate and regenerate the dashboard without ROMs, native binaries, or local evidence. Publication commands belong to [maintenance and diagnostics](grind.md#source-bound-release).
