#!/usr/bin/env bash
# PreToolUse (Bash): .factory/blocked.toml is an input to the derived work
# records in site/data, so a commit that carries the blocker without the rebuilt
# snapshot publishes a report that disagrees with its own blocker file. CI then
# fails `report.py check` on that push and on every later one until somebody
# republishes -- runs #197, #198 and #201 were all this. Fails open wherever the
# working copy cannot be read (no colocated jj, no jq, no jj binary as in CI).
set -uo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HOOK_DIR/../.." && pwd)"
[ -d "$REPO_ROOT/.jj" ] || exit 0
command -v jq >/dev/null 2>&1 || exit 0
command -v jj >/dev/null 2>&1 || exit 0

cmd=$(jq -r '(.tool_input.command // .command // empty)' 2>/dev/null)
[ -n "$cmd" ] || exit 0
printf '%s' "$cmd" | grep -Eq 'jj[[:space:]]+(commit|squash)([[:space:]]|$)' || exit 0

# A plain `jj commit` sweeps the whole working copy, so the blocker rides along
# whatever the path arguments say; treating any dirty blocker as in-scope keeps
# the guard one grep long and errs toward the rebuild, which is idempotent.
dirty=$(cd "$REPO_ROOT" && jj diff --name-only 2>/dev/null) || exit 0
printf '%s\n' "$dirty" | grep -qx '\.factory/blocked\.toml' || exit 0
printf '%s\n' "$dirty" | grep -qx 'site/data/progress\.json' && exit 0

echo "BLOCKED: .factory/blocked.toml is dirty but site/data/progress.json is not." >&2
echo "An operational blocker is an input to the derived work records, so committing" >&2
echo "the blocker alone publishes a snapshot that contradicts it and fails" >&2
echo "'report.py check' on this push and every later one. Rebuild, then commit both:" >&2
echo "  python3 tools/progress/report.py build" >&2
exit 2
