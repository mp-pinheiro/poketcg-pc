# Changelog

All notable changes to this project are documented here.
This changelog is generated automatically from [Conventional Commits](https://www.conventionalcommits.org) by [git-cliff](https://github.com/orhun/git-cliff).
## v0.2.0 - 2026-08-10

### Bug Fixes

- Regenerate full changelog on release
- Write TxRam high bytes to the adjacent slot
- Model ClassifyTextCharacterPair carry as a flag output
- Isolate scene replay persistence and split oracle recipes
- Propagate reloaded d/e out of text tile lookup
- Send generated font tiles to their VRAM address
- Return real exit registers from text header writes
- Model header read clobber and terminator flag
- Model HandleTxRam2Or3 exit registers, diff remaining text cases
- ReadJoypad input line was forced high
- *(harness)* Canonicalize bus readback
- *(animation)* Model reset output
- *(animation)* Preserve reset registers
- *(oracle)* Fail probe crashes and timeouts
- *(oracle)* Remove unusable barrier
- *(oracle)* Require comparator artifacts
- *(oracle)* Generalize timed comparator
- *(oracle)* Reject unsupported case state
- *(oracle)* Validate schema case shape
- *(oracle)* Enforce state and preservation checks
- *(oracle)* Label incomplete barrier
- *(oracle)* Serialize SM83 flags
- *(oracle)* Validate exclusion anchors
- *(duel)* Preserve reset animation callees
- *(oracle)* Load schema case helpers
- *(oracle)* Stabilize GBRT copy proofs
- *(oracle)* Harden backend verification
- *(progress)* Add tests/cases path for gate imports
- *(ci)* Add User-Agent to git-cliff download
- *(ci)* Use gh release download for git-cliff

### Documentation

- Rewrite vision from research findings
- Correct C standard to C11
- Add porting guide and contract
- Record blocked animation orchestrators
- Add agent contract and track vcs guards
- Mark step 0 landed in plan status
- Record wave 1 barrier and gate at 354
- Update gate count to 375
- Update gate to 400 routines
- Update gate to 423 routines
- *(plan)* Record gfx commit
- *(plan)* Checkpoint sprite phase 2
- Document project dependencies
- Harden replay oracle setup
- *(plan)* Record sprite animations

### Features

- Add layout-locked C memory substrate
- Add PyBoy per-function oracle harness
- Port 19 home leaf routines to C
- Model the MBC5 SRAM-enable latch
- Port ClearSRAMBGMaps
- Port save/SRAM subsystem to C
- Add virtual PPU arrays and scanline rasteriser
- Add SDL shell, snapshot and replay harness
- Add ROM data extraction pipeline
- Port tilemap and BG-map layer
- Port tile fill and 1bpp copy routines
- Port text box geometry and font tile routines
- Port joypad input and menu framework core
- Port text header and text id lookup routines
- Port frame boundary and LCD control routines
- Port textbox draw chain with banked VRAM diffing
- Add gb-recompiled scene oracle harness
- Port upper text processing cluster
- Port text drivers, name copy, and text data
- Add case prelude and fix text tile cache
- Gate against probe adapters that reimplement
- Port save remainder and SaveGame
- Port PrintText and text item placement
- Dissolve GB hardware plumbing into flat memory
- Port gameplay palette and scroll leaves
- Extract built assets and LZ blobs
- Port text box cursor parameters
- Port sprite animation buffer helpers
- Port animation status and frame hooks
- Port overworld permission map helpers
- Port loaded NPC pointer helpers
- Trace ordered APU register writes
- Port timer setup configuration
- Port serial timer handler
- Port duelist variable layer
- Port deck index lookup family
- Port trainer-to-pokemon conversion
- Port deck index card loaders
- Port subtract HP routine
- Port sand attack check substatus
- Port map script pointer lookup
- Port card list builders
- Port duel temp list helpers
- Port hand and energy list builders
- Port deck shuffle
- Port card id list sort
- Port hand sort by card id
- Port color to weakness ratio
- Port card count and attack flag routines
- Port card damage and max HP lookup
- Port pkmn power counters
- Port tile loaders and font copiers
- Port duel deck hand and play area routines
- Port substatus condition handlers
- Port save trampolines and card collection
- Port serial link and printer packet routines
- Port overworld map and sprite animation
- Port menu cursor and text box drawing
- Port small leaf routines across eight files
- Port VRAM setup and CGB palette flush
- Model held joypad keys in oracle cases
- Port input waiters and scrollable text
- Port damage modifiers and card colours
- Port wave 3 inline routines
- Port audio engine and SFX (partial)
- Port audio home wrappers and register sound routines
- Expand music1 cases to 37 routines
- Port duel core portable routines
- *(duel_core)* Port WaitAttackAnimation
- *(duel_core)* Port ApplyStatusConditionQueue
- *(duel_core)* Port GetCardOneStageBelow
- *(gfx)* Port default palettes
- *(gfx)* Port loaders and fades
- *(gfx)* Port sprite animations
- *(port)* Complete engine slices
- *(oracle)* Pin reference environment
- *(oracle)* Add GBRT runner
- *(oracle)* Add case audit gate
- *(oracle)* Seed GBRT registers
- *(oracle)* Parse GBRT register seeds
- *(oracle)* Restore function barrier
- *(oracle)* Compare GBRT function case
- *(oracle)* Migrate first schema case
- *(oracle)* Apply mapper case state
- *(oracle)* Add GBRT function command
- *(oracle)* Add contract-aware cases
- *(oracle)* Add HtimesL case matrix
- *(oracle)* Expand primary case matrices
- *(oracle)* Emit GBRT state projection
- *(oracle)* Compare memory projections
- *(oracle)* Derive state spans from cases
- *(oracle)* Add migrated case barrier
- *(oracle)* Support pre-ret completion
- *(oracle)* Route completion modes
- *(oracle)* Support event completion
- *(oracle)* Add event predicate protocol
- *(oracle)* Normalize event predicates
- *(oracle)* Execute schema two cases
- *(oracle)* Apply WRAM seed spans
- *(oracle)* Add fixed inventory gate
- *(oracle)* Add GBRT verification lanes
- *(oracle)* Validate routine exclusions
- *(oracle)* Fingerprint PyBoy distribution files
- *(oracle)* Migrate copy routine proof
- *(oracle)* Complete copy primary cases
- *(progress)* Port progress dashboard
- *(progress)* Add --report to GBRT gate (oracle-fn-all)
- *(progress)* Deploy to Cloudflare Pages

### Miscellaneous

- Register wave 1 routines in the gate
- Register wave 2 routines and update plan
- *(feat)* Duel core wip
- *(oracle)* Record animation exclusions

### Refactor

- *(oracle)* Require explicit contracts

### Tests

- Ground NPC pointer cases in table data
- Diff IO registers against the real ROM
- *(oracle)* Migrate division cases
- *(oracle)* Migrate write-number case
- *(oracle)* Migrate damage cases
- *(oracle)* Migrate RNG cases

