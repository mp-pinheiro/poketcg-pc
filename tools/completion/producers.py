from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from tools.completion import completion, scenario, widescreen, witness

ROOT = Path(__file__).resolve().parents[2]


class ProducerUnavailable(RuntimeError):
    pass


def _descriptor(
    producer: str,
    handler: str | None,
    *,
    producer_files: list[str],
    comparator_files: list[str],
    native: bool = True,
    reference: bool = True,
    corpus: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    producer_closure = sorted(set(producer_files + ["tools/completion"]))
    comparator_closure = set(comparator_files + ["tools/completion"])
    if any(path.startswith("tools/oracle") for path in comparator_closure):
        comparator_closure.add("tools/oracle")
    if any(path.startswith("tests") for path in comparator_closure):
        comparator_closure.add("tests")
    return {
        "producer": producer,
        "handler": handler,
        "producer_files": producer_closure,
        "comparator_files": sorted(comparator_closure),
        "native": {"files": ["build/poketcg", "build/completion/data-pack.bin"]}
        if native
        else {"files": []},
        "reference": {"files": ["tools/completion/gambatte_pins.toml"]}
        if reference
        else {"files": []},
        "corpus": list(corpus or []),
    }


_COMMON = ["tools/completion/producers.py", "tools/completion/completion.py"]
_SCENARIO = _COMMON + ["tools/completion/scenario.py", "tools/completion/refstream.py"]
_WITNESS = _SCENARIO + [
    "tools/completion/witness.py",
    "tools/completion/session.py",
    "tools/completion/gambatte_runner.py",
]
_WITNESS_COMPARATORS = [
    "tools/completion/witness.py",
    "tools/completion/session.py",
    "tools/completion/refstream.py",
    "tools/completion/gambatte_runner.py",
]


_REGISTRY: dict[str, dict[str, Any]] = {
    "completion:v2:reset:baseline": _descriptor(
        "baseline",
        "baseline",
        producer_files=_COMMON,
        comparator_files=["tools/progress/inventory.py"],
        native=False,
        reference=False,
    ),
    "completion:v2:reset:rom-coverage": _descriptor(
        "rom-coverage",
        "rom-coverage",
        producer_files=_COMMON + ["tools/completion/rom_inventory.py"],
        comparator_files=[
            "tools/progress/inventory.py",
            "tools/completion/rom_inventory.py",
        ],
        native=False,
        reference=False,
    ),
    "completion:v2:reset:routine-bijection": _descriptor(
        "routine-mapping",
        "routine-mapping",
        producer_files=_COMMON,
        comparator_files=["tests/routines.py", "tests/cases"],
        native=False,
        reference=False,
    ),
    "completion:v2:p0:substrate": _descriptor(
        "substrate",
        "substrate",
        producer_files=_COMMON,
        comparator_files=["tools/oracle", "tests/test_leaves.py"],
    ),
    "completion:v2:p1:hardware-removal": _descriptor(
        "hardware-removal",
        "hardware-removal",
        producer_files=_COMMON,
        comparator_files=[
            "tools/oracle",
            "tools/lint_adapters.py",
            "tools/lint_constants.py",
        ],
    ),
    "completion:v2:p2:leaves": _descriptor(
        "leaves",
        "leaves",
        producer_files=_COMMON + ["tools/completion/mutation_campaign.py"],
        comparator_files=["tests/cases", "tools/oracle/mutation_receipts"],
    ),
    "completion:v2:p2:save-interchange": _descriptor(
        "save-interchange",
        "scenario:save-interchange",
        producer_files=_SCENARIO,
        comparator_files=["tools/oracle/gbrecomp_oracle.py", "tests/scene_diff.py"],
    ),
    "completion:v2:p2:boot-title": _descriptor(
        "boot-title",
        "scenario:boot-title",
        producer_files=_WITNESS,
        comparator_files=_WITNESS_COMPARATORS,
        corpus=witness.corpus("boot-title"),
    ),
    "completion:v2:p2:boot-title-negative": _descriptor(
        "boot-title-negative",
        "scenario:boot-title-negative",
        producer_files=_WITNESS,
        comparator_files=_WITNESS_COMPARATORS,
        corpus=witness.corpus_for(("boot-menu",)),
    ),
    "completion:v2:p3:audio-trace": _descriptor(
        "audio-trace",
        "scenario:audio-catalog",
        producer_files=_WITNESS,
        comparator_files=_WITNESS_COMPARATORS,
        corpus=witness.corpus("audio-catalog"),
    ),
    "completion:v2:p3:audio-pcm": _descriptor(
        "audio-pcm",
        "scenario:audio-pcm",
        producer_files=_WITNESS,
        comparator_files=_WITNESS_COMPARATORS,
        corpus=witness.corpus("audio-pcm"),
    ),
    "completion:v2:p4:ui-corpus": _descriptor(
        "ui-corpus",
        "scenario:ui-corpus",
        producer_files=_WITNESS,
        comparator_files=_WITNESS_COMPARATORS,
        corpus=witness.corpus("ui-corpus"),
    ),
    "completion:v2:p4:raster-effects": _descriptor(
        "raster-effects",
        "scenario:raster-effects",
        producer_files=_WITNESS,
        comparator_files=_WITNESS_COMPARATORS,
        corpus=witness.corpus("raster-effects"),
    ),
    "completion:v2:p5:duel-state": _descriptor(
        "duel-state",
        "scenario:duel-state",
        producer_files=_WITNESS,
        comparator_files=_WITNESS_COMPARATORS,
        corpus=witness.corpus("duel-state"),
    ),
    "completion:v2:p5:seeded-duel": _descriptor(
        "seeded-duel",
        "scenario:seeded-duel",
        producer_files=_WITNESS,
        comparator_files=_WITNESS_COMPARATORS,
        corpus=witness.corpus("seeded-duel"),
    ),
    "completion:v2:p6:script-vm": _descriptor(
        "script-vm",
        "scenario:script-vm",
        producer_files=_WITNESS,
        comparator_files=_WITNESS_COMPARATORS + ["tools/oracle/mutation_receipts"],
        corpus=witness.corpus("script-vm")
        + [{"path": "site/data/coverage.json"}, {"path": "tools/completion/session_ratchet.json"}],
    ),
    "completion:v2:p6:maps-and-campaign": _descriptor(
        "maps-and-campaign",
        "scenario:all-maps-scripts",
        producer_files=_WITNESS,
        comparator_files=_WITNESS_COMPARATORS,
        corpus=witness.corpus("all-maps-scripts"),
    ),
    "completion:v2:p7:link-ir": _descriptor(
        "link-ir",
        "scenario:link-ir-printer",
        producer_files=_WITNESS,
        comparator_files=_WITNESS_COMPARATORS,
        corpus=witness.corpus("link-ir-printer"),
    ),
    "completion:v2:p7:printer": _descriptor(
        "printer",
        "scenario:printer",
        producer_files=_WITNESS,
        comparator_files=_WITNESS_COMPARATORS,
        corpus=witness.corpus("printer"),
    ),
    "completion:v2:faithful-4x3:release": _descriptor(
        "faithful-release",
        "scenario:new-game-to-credits",
        producer_files=_WITNESS,
        comparator_files=_WITNESS_COMPARATORS,
        corpus=witness.corpus("new-game-to-credits"),
    ),
    "completion:v2:faithful-4x3:package": _descriptor(
        "package",
        "package",
        producer_files=_COMMON + ["tools/completion/package_smoke.py"],
        comparator_files=["tools/completion/package_smoke.py", "tools/gen_data.py"],
    ),
    "completion:v2:p8:ppu:span-widening": _descriptor(
        "span-widening",
        "scenario:span-widening",
        producer_files=_WITNESS + ["tools/completion/widescreen.py"],
        comparator_files=_WITNESS_COMPARATORS + ["tools/completion/widescreen.py"],
        corpus=widescreen.corpus("span-widening"),
    ),
    "completion:v2:p8:runtime:viewport-rect": _descriptor(
        "viewport-rect",
        "scenario:viewport-rect",
        producer_files=_WITNESS + ["tools/completion/widescreen.py"],
        comparator_files=_WITNESS_COMPARATORS + ["tools/completion/widescreen.py"],
        corpus=widescreen.corpus("viewport-rect"),
    ),
    "completion:v2:p8:ui:wide-layouts": _descriptor(
        "wide-layouts",
        "scenario:wide-layouts",
        producer_files=_WITNESS + ["tools/completion/widescreen.py"],
        comparator_files=_WITNESS_COMPARATORS + ["tools/completion/widescreen.py"],
        corpus=widescreen.corpus("wide-layouts"),
    ),
    "completion:v2:p8:features:render-only": _descriptor(
        "render-only",
        "scenario:render-only",
        producer_files=_WITNESS + ["tools/completion/widescreen.py"],
        comparator_files=_WITNESS_COMPARATORS + ["tools/completion/widescreen.py"],
        corpus=widescreen.corpus("render-only"),
    ),
    "completion:v2:p8:release:enhanced-corpus": _descriptor(
        "enhanced-corpus",
        "scenario:widescreen-corpus",
        producer_files=_WITNESS + ["tools/completion/widescreen.py"],
        comparator_files=_WITNESS_COMPARATORS + ["tools/completion/widescreen.py"],
        corpus=widescreen.corpus("widescreen-corpus"),
    ),
}


def describe(requirement_id: str) -> dict[str, Any]:
    try:
        value = _REGISTRY[requirement_id]
    except KeyError as exc:
        raise ProducerUnavailable(
            f"no producer descriptor for {requirement_id}"
        ) from exc
    return json.loads(json.dumps(value, sort_keys=True))


def executable(requirement_id: str) -> bool:
    return isinstance(describe(requirement_id).get("handler"), str)


def ids() -> tuple[str, ...]:
    return tuple(sorted(_REGISTRY))


def handler_for(name: str) -> Callable[[], int]:
    commands: dict[str, Callable[[], int]] = {
        "baseline": completion.command_baseline,
        "rom-coverage": completion.command_rom_coverage,
        "routine-mapping": completion.command_routine_mapping,
        "substrate": completion.command_substrate,
        "hardware-removal": completion.command_hardware_removal,
        "leaves": completion.command_leaves,
        "package": completion.command_package,
    }
    if name in commands:
        return commands[name]
    if name.startswith("scenario:"):
        scenario_name = name.split(":", 1)[1]
        return lambda: scenario.main([scenario_name])
    raise ProducerUnavailable(f"unknown producer handler: {name}")
