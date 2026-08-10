# Copilot instructions for poketcg-pc

## Read first
1. AGENTS.md — the full porting contract (read entirely)
2. docs/port-contract.md — C rules, adapter rules, case-key reference, definition of done
3. The issue body — specifies exactly which routines to port and from which asm file

## Sandbox specifics
- No jj installed. Use plain git: `git add`, `git commit`, `git push`
- No .jj/ directory. The .claude/hooks/ do not run in this sandbox
- CI enforces Conventional Commits via git-cliff. Commit with: `git commit -m "feat(port): <subject>"`
- Subject line ≤50 chars, no body, no emoji

## Port loop
For each routine in the issue:
1. Read the pret asm source at poketcg/src/<path> (the issue gives the exact file and line)
2. Create the four-file quartet following docs/port-contract.md:
   - src/home/<basename>.h — prototypes (stdint.h, guard, function decls)
   - src/home/<basename>.c — the C port (gb_read8/gb_write8, never host pointers)
   - src/probe/<basename>.c — adapters + probe_entries_<basename>[]
   - tests/cases/<basename>.py — CONTRACT, CASES, SCHEMA2_CASES
3. Add the routine to tests/routines.py under the correct ROUTINES key. The key is the pret basename (filename without .asm). If the key doesn't exist, add it. Never edit another key's entry.
4. Run: just oracle-diff <RoutineName>
   - Must print PASS. If not, fix and retry.
5. Mutation test: corrupt one line (flip a comparison), run `just oracle-diff <RoutineName>`, confirm it goes RED, restore, confirm PASS.

## After all routines pass
1. Run `just progress` — regenerates site/data/progress.json + site/data/history.jsonl
2. `git add -A && git commit -m "feat(port): <subject>" && git push`
3. The PR is auto-created by the coding agent

## File quartet pattern
Copy the structure from existing ported routines (e.g. src/home/copy.c). Key rules:
- Every memory access goes through gb_read8/gb_write8 with uint16_t addresses
- Zero means maximum: bc==0 → 65536, c==0 → 256
- Advanced pointers write back through uint16_t* parameters
- Probe adapter: exactly one routine call, no hardcoded addresses >= 0x8000
- Cases: all-zero, poisoned-register (a=0xAA, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234), every boundary (n=0, n=1, n=256/257)
