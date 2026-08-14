# Copilot coding-agent sandbox

This file governs **only** the GitHub Copilot coding-agent sandbox. It differs
from an interactive session in exactly one respect: there is no `.jj/` directory
and the `.claude/hooks/` guards do not run, so version control is plain `git`.

```sh
git add -A
git commit -m "feat(port): <subject>"
git push
```

Conventional Commits, subject ≤50 chars, no body, no emoji — CI enforces this via
git-cliff.

Everything else is `AGENTS.md` and the docs it routes to: the port contract, the
four-file quartet, verification, and the definition of done. Do not restate the
port loop here. It was maintained as a second copy once and drifted twice — it
told agents to hand-edit `tests/routines.py` and to hand-write `SCHEMA2_CASES`,
both of which are derived and rejected by the tooling.
