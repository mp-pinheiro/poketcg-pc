"""The frame allowance a case grants the native probe, shared by both lanes.

`tools/oracle/gbref/compare_one.py` and `tests/test_leaves.py` must stop the
probe at the same frame as their reference, which is what `src/probe.c` states
as its invariant. The mutation lane sent no allowance at all until 2026-09-09,
so a frame-driven routine ran until the probe's own `RLIMIT_CPU` killed it
(`ExecuteGameEvent` died on SIGXCPU at 240 s while the PyBoy lane passed the
same case in 7 s), and every such canary was unprovable.

This module imports nothing beyond the standard library on purpose:
`tests/cases/random.py` shadows stdlib `random` for any importer that has
`tests/cases` on `sys.path`, which is why the mutation lane cannot import
`test_leaves` directly.
"""

from __future__ import annotations

DEFAULT_FRAMES = 240
CYCLES_PER_FRAME = 70224


def lane_frames(case: dict) -> int | None:
    """Frames the probe may render for `case`, or None to use the lane default.

    gbref bounds a run by `cycle_budget` and PyBoy by ticks, so a case that
    declares a large cycle budget is asking for that much time on both.
    """
    budget = case.get("cycle_budget")
    if not budget:
        return None
    try:
        from pyboy_oracle import MAX_FRAMES
    except ImportError:
        MAX_FRAMES = DEFAULT_FRAMES
    return max(MAX_FRAMES, int(budget) // CYCLES_PER_FRAME + 1)
