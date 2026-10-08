import importlib.util
import itertools
import os
import sys
from pathlib import Path

from tests.cases import _symbols

CASES_DIR = Path(__file__).resolve().parent
TABLES = ("CONTRACT", "CASES", "SCHEMA2_CASES", "MUTATIONS")
_STDLIB = Path(os.__file__).resolve().parent
_COUNTER = itertools.count()
_PROBES = ((0x3E, 0x7EEE), (0x3F, 0x7FEF))


def _stdlib_copy():
    module = sys.modules.get("copy")
    if module is not None and Path(module.__file__).resolve().parent == _STDLIB:
        return module
    spec = importlib.util.spec_from_file_location("_inherit_stdlib_copy", _STDLIB / "copy.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_deepcopy = _stdlib_copy().deepcopy


def _load(stem: str) -> tuple[dict, ...]:
    path = CASES_DIR / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(f"inherit_{stem}_{next(_COUNTER)}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return tuple(_deepcopy(getattr(module, name, {})) for name in TABLES)


def _load_with_absent(stem: str, bank: int, address: int) -> tuple[dict, ...]:
    cached = set(sys.modules)
    try:
        with _symbols.absent_symbols_as(bank, address):
            return _load(stem)
    finally:
        for name in set(sys.modules) - cached:
            if name.startswith("tests.cases."):
                del sys.modules[name]


def _routines(tables: tuple[dict, ...]) -> set[str]:
    return {fn for table in tables for fn in table}


def _without(tables: tuple[dict, ...], drop: set[str]) -> tuple[dict, ...]:
    return tuple({fn: value for fn, value in table.items() if fn not in drop} for table in tables)


def inherit(stem: str, remove: tuple[str, ...] = ()) -> tuple[dict, dict, dict, dict]:
    drop = set(remove)
    try:
        tables = _load(stem)
    except KeyError:
        tables, other = (_load_with_absent(stem, *probe) for probe in _PROBES)
        dependent = sorted(
            fn for fn in _routines(tables) | _routines(other)
            if fn not in drop and any(repr(a.get(fn)) != repr(b.get(fn)) for a, b in zip(tables, other)))
        if dependent:
            raise KeyError(f"{stem}: {', '.join(dependent)} use symbols absent from {_symbols.sym_path()}; remove them") from None
    unknown = sorted(drop - _routines(tables))
    if unknown:
        raise KeyError(f"{stem}: remove names routines it does not define: {', '.join(unknown)}")
    return _without(tables, drop)
