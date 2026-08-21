#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--lane', type=Path, required=True)
    parser.add_argument('--basename', required=True)
    parser.add_argument('--fn', action='append', default=[])
    args = parser.parse_args()
    from verify import case_lint, load_cases_module, witness_index
    primary_indices = {fn: [] for fn in args.fn}
    witness_indices = {fn: [] for fn in args.fn}
    try:
        module = load_cases_module(args.lane, args.basename)
    except Exception as exc:
        violations = {
            fn: [f"case module fails to import: {exc}"]
            for fn in args.fn
        }
        witnesses = {fn: None for fn in args.fn}
        counts = {fn: 0 for fn in args.fn}
    else:
        violations = case_lint(args.lane, args.basename, args.fn, module)
        mutations = getattr(module, "MUTATIONS", {})
        schema_cases = getattr(module, "SCHEMA2_CASES", {})
        witnesses = {
            fn: witness_index(mutations[fn]) if fn in mutations else None
            for fn in args.fn
        }
        counts = {fn: len(schema_cases.get(fn) or ()) for fn in args.fn}
        primary_indices = {
            fn: [
                index for index, record in enumerate(schema_cases.get(fn) or ())
                if isinstance(record, dict) and record.get("evidence") == "primary"
            ]
            for fn in args.fn
        }
        witness_indices = {
            fn: [
                int(match.group(1))
                for case_id in (mutations.get(fn, {}).get("case_ids") or [])
                if (match := re.fullmatch(rf"{re.escape(fn)}-(\d+)", str(case_id)))
            ]
            for fn in args.fn
        }
    print(json.dumps({
        "violations": violations,
        "witnesses": witnesses,
        "witness_indices": witness_indices,
        "primary_indices": primary_indices,
        "case_counts": counts,
    }, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
