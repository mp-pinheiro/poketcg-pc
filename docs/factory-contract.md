# Factory translation contract

This document owns the prompt/output protocol used to generate one source quartet. Shared ABI, memory, register, observation, case-strength and exclusion rules are defined by [port-contract.md](port-contract.md); follow them without creating a second convention.

## Quartet and markers

A source `<file>` produces exactly these owned files: `src/home/<file>.h`, `src/home/<file>.c`, `src/probe/<file>.c`, and `tests/cases/<file>.py`. The probe table is named `probe_entries_<file>[]`. The surrounding skeleton supplies includes, guards, probe table, `POISON`, and schema tail. Do not hand-edit derived `tests/routines.py` or `SCHEMA2_CASES`.

The output uses the exact marker names supplied by the factory prompt. Preserve their spelling and order; do not add surrounding prose, markers, or unrelated files. The documented markers include `===STATICS` for local constants/includes, `===PROBE` for adapters and entries, `===CASES` for case declarations, and `===MUTATION` for mutation declarations. Put prototypes and function bodies only in their corresponding requested sections; preserve the supplied skeleton, including its header guards, probe table, `POISON`, and schema tail.

Preserve the supplied machine/protocol markers. Use tab indentation in C and unsigned `u` suffixes; do not add explanatory code comments, placeholders, TODOs, or dead code.

## Probe output

An adapter is named `adapt_<RoutineName>` (replace `.` with `_`) and accepts `ProbeState *s`. It only marshals inputs, makes exactly one routine call, and marshals real outputs back. Never recompute an answer, hardcode an output, write a preserved register, or use an integer literal at or above `0x8000` in the adapter. Pair assembly/splitting is marshalling, not another routine call.

The adapter table contains `{ "PretName", adapt_PretName }` entries and ends with `{ NULL, NULL }`. Local pret labels retain their exact dotted symbol name in the registration string.

## Cases and mutation declarations

Each routine gets `CONTRACT["Name"]` and `CASES["Name"]` declarations. Use symbolic addresses from `tests/cases/_symbols.py`, not raw address literals. Cases must exercise required semantics and observe the behavior under test as specified by port-contract. Oracle-inaccessible cases require `oracle: False`, a nonempty `why`, and at least one assembly-derived expectation family.

An entry cutpoint is emitted into the schema by a `# >>> factory-completion <Routine>` block that sets `completion` on the derived `SCHEMA2_CASES` records. `_completion` on loaded case dictionaries is readback state, not the authoring hook. Schema inventories are derived; never hand-edit `SCHEMA2_CASES`.

Each mutation declares `MUTATIONS["Name"]` with `source_symbol`, `before`, `after`, and `case_ids`. `after` is a shape-preserving behavioral corruption; the port contract owns anchor resolution and execution requirements.

Execution and receipt requirements belong to [mutation evidence](port-contract.md#mutation-evidence). A declaration or static anchor audit alone does not satisfy them.

## Constants and includes

Use local `#define NAME value` entries in `===STATICS` for constants supplied by the source prompt. Do not invent values. Permitted quoted includes are callee `home/<basename>.h` headers named by the prompt and `generated/wram.h`, `generated/hram.h`, `generated/sram.h`, or `mem.h`. Do not add another constants header or invent include paths.

The marker-delimited factory owns generated output shape; port-contract owns the technical semantics. Keep each rule in its owner and link to it rather than paraphrasing a second version.
