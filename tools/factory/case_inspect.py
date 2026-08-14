#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--lane', type=Path, required=True)
    parser.add_argument('--basename', required=True)
    parser.add_argument('--fn', action='append', default=[])
    args = parser.parse_args()
    path = args.lane / 'tests' / 'cases' / f'{args.basename}.py'
    spec = importlib.util.spec_from_file_location('factory_case_inspect', path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'cannot load {path}')
    from verify import case_lint, load_cases_module, witness_index
    violations = case_lint(args.lane, args.basename, args.fn)
    module = load_cases_module(args.lane, args.basename)
    mutations = getattr(module, "MUTATIONS", {})
    witnesses = {
        fn: witness_index(mutations[fn]) if fn in mutations else None
        for fn in args.fn
    }
    print(json.dumps({"violations": violations, "witnesses": witnesses}, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
