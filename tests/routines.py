"""Routine registry, derived from tests/cases/*.py CONTRACT declarations.

Registration is a side effect of a case module existing: every module
``tests/cases/<basename>.py`` contributes ``ROUTINES[<basename>] =
tuple(CONTRACT.keys())``.  There is nothing to hand-edit here, so two
concurrent ports can never lose each other's registrations (the duplicate-key
silent-loss failure recorded in site/data/history.jsonl, 623 -> 562 functions
between commits 220c7b27 and 93198a95).

Consequences:
- A routine is registered exactly when its CONTRACT entry exists; a
  "registered but caseless" gate failure is impossible by construction.
- ``tools/progress/report.py backfill`` cannot text-parse revisions after
  this change; backfill replays only literal-dict revisions and skips newer
  ones.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _load() -> dict[str, tuple[str, ...]]:
    routines: dict[str, tuple[str, ...]] = {}
    for path in sorted((_ROOT / "tests" / "cases").glob("*.py")):
        if path.name.startswith("_") or path.name == "__init__.py":
            continue
        spec = importlib.util.spec_from_file_location(f"registry_{path.stem}", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"routines: cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        contract = getattr(module, "CONTRACT", {})
        if contract:
            routines[path.stem] = tuple(contract.keys())
    return routines


ROUTINES: dict[str, tuple[str, ...]] = _load()

EXCLUSIONS: dict[str, dict[str, dict[str, str]]] = {}


ALL = tuple(fn for group in ROUTINES.values() for fn in group)
