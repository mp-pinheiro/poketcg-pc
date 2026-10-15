# TAS diagnostics

The completion TAS is a diagnostic input, not the primary progress gate or a session runbook. Use [grind](grind.md) for issue and session work.

## Progress measurement

```sh
just build-trace
just completion-tas-progress
```

The command compares the native trace with the reference replay and reports reached and executed routine counts, frontier misses, and ordinal-derived diagnostics. The ordinal is a ceiling indicator, not a monotone depth measure: an incidental call to a routine first observed late in the reference can raise it while earlier work remains blocked. `blockers[]` filters misses at or beyond that ordinal and can therefore hide genuine earlier misses; inspect unfiltered `misses[]` as well, especially its first entry.

The TAS ratchet and its acceptance semantics are owned by `tools/completion/tas_progress.py` and its configuration. This report is diagnostic and does not supersede recorded-session verification or source-bound release evidence.

## Composition diagnostics

Per-routine oracle cases cannot establish that calls compose correctly across routines. Run:

```sh
just completion-composition-audit
just completion-trace-diff SCENARIO --trace build/completion/native-trace.bin
just completion-frame-census SCENARIO
just completion-writers SCENARIO ADDRESS
just completion-reftrace SCENARIO --routines A,B
```

The composition audit reports remaining structural classes; routine call-count diffs can include legitimate inlining, wrappers, or bank-trampoline differences, so interpret them against assembly and the corresponding reference interval. Frame census identifies the earliest bad byte and preceding writer; it is byte diagnosis, not progression evidence.

The TAS and trace tools do not replace [port-contract](port-contract.md) case-coverage rules, session verification, or the audio and reach proof owners. Do not use checkpoint injection as proof that a game route works.
