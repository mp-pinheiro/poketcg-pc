#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import sys
import tomllib
from dataclasses import dataclass, replace
from pathlib import Path
from collections.abc import Mapping

ROOT = Path(__file__).resolve().parent.parent
import re

CATALOG = ROOT / "profiles" / "profiles.json"
VARIANT_ENV = "POKETCG_PROFILE_VARIANT"


class ProfileError(ValueError):
    pass


@dataclass(frozen=True)
class Profile:
    name: str
    title: str
    source: Mapping[str, Any]
    build: Mapping[str, Any]
    artifacts: Mapping[str, Any]
    evidence: Mapping[str, Any]
    save: Mapping[str, Any]
    features: Mapping[str, bool]
    variant: str | None = None

    @property
    def checkout(self) -> str:
        return str(self.source["checkout"])

    @property
    def source_repository(self) -> str:
        return str(self.source["repository"])

    @property
    def source_commit(self) -> str:
        return str(self.source["commit"])

    @property
    def rom_name(self) -> str:
        return str(self.source["rom"])

    @property
    def map_name(self) -> str:
        return str(self.source["map"])

    @property
    def sym_name(self) -> str:
        return str(self.source["sym"])

    @property
    def binary(self) -> str:
        return str(self.build["binary"])

    @property
    def probe(self) -> str:
        return str(self.build["probe"])

    @property
    def generated_headers(self) -> str:
        return str(self.build["generated_headers"])
    @property
    def default_build_dir(self) -> str:
        return str(self.build["default_build_dir"])


    @property
    def oracle_namespace(self) -> str:
        return str(self.evidence["oracle_namespace"])

    @property
    def session_namespace(self) -> str:
        return str(self.evidence["session_namespace"])

    @property
    def case_namespace(self) -> str:
        return str(self.evidence["case_namespace"])

    @property
    def save_tag(self) -> str:
        return str(self.save["tag"])

    @property
    def save_schema(self) -> int:
        return int(self.save["schema"])

    @property
    def default_save_filename(self) -> str:
        return str(self.save["default_filename"])

    def source_path(self, root: Path = ROOT) -> Path:
        return root / self.checkout

    def rom_path(self, root: Path = ROOT) -> Path:
        return self.source_path(root) / self.rom_name

    def map_path(self, root: Path = ROOT) -> Path:
        return self.source_path(root) / self.map_name

    def sym_path(self, root: Path = ROOT) -> Path:
        return self.source_path(root) / self.sym_name

    def build_path(self, root: Path = ROOT) -> Path:
        return root / os.environ.get("POKETCG_BUILD", self.default_build_dir)

    def binary_path(self, root: Path = ROOT) -> Path:
        return self.build_path(root) / self.binary

    def probe_path(self, root: Path = ROOT) -> Path:
        return self.build_path(root) / self.probe

    def data_pack_path(self, root: Path = ROOT) -> Path:
        return self.build_path(root) / "completion" / "data-pack.bin"

    def session_path(self, root: Path = ROOT) -> Path:
        return root / self.session_namespace

    def case_path(self, root: Path = ROOT) -> Path:
        override = os.environ.get("POKETCG_CASE_PATH")
        if override:
            return root / override
        return root / self.case_namespace

    def receipt_path(self, root: Path = ROOT) -> Path:
        return root / str(self.evidence["receipt_namespace"])

    def hatch_registry_path(self, root: Path = ROOT) -> Path:
        return root / str(self.evidence["hatch_registry"])

    def hatch_ratchet_path(self, root: Path = ROOT) -> Path:
        return root / str(self.evidence["hatch_ratchet"])

    def artifact_path(self, name: str, root: Path = ROOT) -> Path:
        value = self.artifacts.get(name)
        if not isinstance(value, str) or not value:
            raise ProfileError(f"profile {self.name} has no path for artifact {name}")
        return root / value

    @property
    def overlay_root(self) -> str | None:
        value = self.build.get("overlay_root")
        return str(value) if value else None

    @property
    def removed_basenames(self) -> frozenset[str]:
        return frozenset(str(name) for name in self.build.get("removed_basenames", ()))

    def overlay_path(self, root: Path = ROOT) -> Path | None:
        return root / self.overlay_root if self.overlay_root else None

    def _merged(self, shared: Path, overlay: Path | None, suffix: str) -> list[Path]:
        merged = {
            path.stem: path
            for path in sorted(shared.glob(f"*{suffix}"))
            if path.stem not in self.removed_basenames and not path.name.startswith("_")
        }
        if overlay is not None and overlay.is_dir():
            merged.update({path.stem: path for path in sorted(overlay.glob(f"*{suffix}"))})
        return [merged[stem] for stem in sorted(merged)]

    def _composed(self, tree: str, suffix: str, root: Path) -> list[Path]:
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        from tools.compose_profile import merged_paths
        return merged_paths(self, tree, suffix, root)

    def home_sources(self, root: Path = ROOT) -> list[Path]:
        return self._composed("home", ".c", root)

    def home_headers(self, root: Path = ROOT) -> list[Path]:
        return self._composed("home", ".h", root)

    def probe_sources(self, root: Path = ROOT) -> list[Path]:
        return self._composed("probe", ".c", root)

    def case_modules(self, root: Path = ROOT) -> list[Path]:
        shared = root / "tests" / "cases"
        if os.environ.get("POKETCG_CASE_PATH"):
            return sorted(path for path in self.case_path(root).glob("*.py") if not path.name.startswith("_"))
        overlay = self.case_path(root)
        return self._merged(shared, overlay if overlay != shared else None, ".py")

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "title": self.title,
            "source": dict(self.source),
            "build": dict(self.build),
            "artifacts": dict(self.artifacts),
            "evidence": dict(self.evidence),
            "save": dict(self.save),
            "features": dict(self.features),
        }


def _require(mapping: Mapping[str, Any], key: str, name: str) -> Any:
    if key not in mapping:
        raise ProfileError(f"{name} is missing {key}")
    return mapping[key]


def _validate_profile(name: str, raw: Any) -> Profile:
    if not isinstance(raw, dict):
        raise ProfileError(f"profile {name} is not an object")
    title = _require(raw, "title", f"profile {name}")
    if not isinstance(title, str) or not title:
        raise ProfileError(f"profile {name} has an invalid title")
    fields: dict[str, Mapping[str, Any]] = {}
    for key in ("source", "build", "artifacts", "evidence", "save", "features"):
        value = _require(raw, key, f"profile {name}")
        if not isinstance(value, dict):
            raise ProfileError(f"profile {name} has an invalid {key}")
        fields[key] = value
    for key in ("repository", "checkout", "commit", "rom", "map", "sym"):
        value = _require(fields["source"], key, f"profile {name}.source")
        if not isinstance(value, str) or not value:
            raise ProfileError(f"profile {name}.source.{key} is invalid")
    if len(fields["source"]["commit"]) != 40:
        raise ProfileError(f"profile {name}.source.commit is not a full revision")
    for key in ("binary", "probe", "generated_headers", "default_build_dir"):
        value = _require(fields["build"], key, f"profile {name}.build")
        if not isinstance(value, str) or not value:
            raise ProfileError(f"profile {name}.build.{key} is invalid")
    for key in ("inventory", "data_pack", "pack_manifest"):
        value = _require(fields["artifacts"], key, f"profile {name}.artifacts")
        if not isinstance(value, str) or not value:
            raise ProfileError(f"profile {name}.artifacts.{key} is invalid")
    for key in ("oracle_namespace", "session_namespace", "case_namespace", "receipt_namespace",
                "hatch_registry", "hatch_ratchet"):
        value = _require(fields["evidence"], key, f"profile {name}.evidence")
        if not isinstance(value, str) or not value:
            raise ProfileError(f"profile {name}.evidence.{key} is invalid")
    for key in ("tag", "default_filename"):
        value = _require(fields["save"], key, f"profile {name}.save")
        if not isinstance(value, str) or not value:
            raise ProfileError(f"profile {name}.save.{key} is invalid")
    if len(fields["save"]["tag"]) != 4:
        raise ProfileError(f"profile {name}.save.tag must contain four bytes")
    schema = _require(fields["save"], "schema", f"profile {name}.save")
    if not isinstance(schema, int) or isinstance(schema, bool) or schema < 0:
        raise ProfileError(f"profile {name}.save.schema is invalid")
    if any(not isinstance(value, bool) for value in fields["features"].values()):
        raise ProfileError(f"profile {name}.features must contain booleans")
    return Profile(name=name, title=title, **fields)


def load_catalog(path: Path = CATALOG) -> tuple[str, dict[str, Profile]]:
    try:
        document = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise ProfileError(f"cannot read {path}: {error}") from error
    if not isinstance(document, dict) or document.get("schema") != 1:
        raise ProfileError(f"unsupported profile catalog: {path}")
    default = document.get("default")
    raw_profiles = document.get("profiles")
    if not isinstance(default, str) or not isinstance(raw_profiles, dict):
        raise ProfileError(f"invalid profile catalog: {path}")
    profiles = {name: _validate_profile(name, raw) for name, raw in raw_profiles.items()}
    if default not in profiles:
        raise ProfileError(f"catalog default is not a profile: {default}")
    return default, profiles
SYMBOL_RE = re.compile(r"^([0-9A-Fa-f]{2,3}):([0-9A-Fa-f]{4})\s+(\S+)\s*$")


def symbol_table(profile: Profile, root: Path = ROOT) -> dict[str, tuple[int, int]]:
    result: dict[str, tuple[int, int]] = {}
    for line in profile.sym_path(root).read_text(errors="replace").splitlines():
        match = SYMBOL_RE.match(line.strip())
        if match:
            result.setdefault(match.group(3), (int(match.group(1), 16), int(match.group(2), 16)))
    return result


def symbol_address(
    profile: Profile,
    name: str,
    root: Path = ROOT,
    default: tuple[int, int] | None = None,
) -> tuple[int, int]:
    value = symbol_table(profile, root).get(name)
    if value is None:
        if default is None:
            raise ProfileError(f"profile {profile.name} has no symbol {name}")
        return default
    return value



def apply_variant(profile: Profile, variant: str, root: Path = ROOT) -> Profile:
    path = root / "profiles" / profile.name / f"{variant}.toml"
    if not path.is_file():
        raise ProfileError(f"profile {profile.name} has no variant {variant} ({path.relative_to(root)})")
    table = tomllib.loads(path.read_text()).get("variant")
    if not isinstance(table, dict):
        raise ProfileError(f"{path.relative_to(root)} has no [variant] table")
    name = f"profile {profile.name} variant {variant}"
    fields = {key: _require(table, key, name) for key in (
        "checkout", "rom_sha256", "build_dir", "inventory", "session_namespace")}
    for key, value in fields.items():
        if not isinstance(value, str) or not value:
            raise ProfileError(f"{name}.{key} is invalid")
    pack = f"{fields['build_dir']}/completion/data-pack.bin"
    return replace(
        profile,
        variant=variant,
        source={**profile.source, "checkout": fields["checkout"], "rom_sha256": fields["rom_sha256"]},
        build={**profile.build, "default_build_dir": fields["build_dir"]},
        artifacts={**profile.artifacts, "inventory": fields["inventory"], "data_pack": pack,
                   "pack_manifest": pack.removesuffix(".bin") + ".json"},
        evidence={**profile.evidence, "session_namespace": fields["session_namespace"]},
    )


def get_profile(name: str | None = None, root: Path = ROOT) -> Profile:
    default, profiles = load_catalog(root / "profiles" / "profiles.json")
    selected = name or os.environ.get("POKETCG_PROFILE") or default
    try:
        profile = profiles[selected]
    except KeyError as error:
        choices = ", ".join(sorted(profiles))
        raise ProfileError(f"unknown profile {selected}; choose one of {choices}") from error
    variant = os.environ.get(VARIANT_ENV)
    return apply_variant(profile, variant, root) if variant else profile


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        profile = get_profile(args.profile, args.root.resolve())
    except ProfileError as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(profile.as_dict(), indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(f"{profile.name}: {profile.title}")
        print(f"source={profile.source_path(args.root.resolve())}")
        print(f"rom={profile.rom_path(args.root.resolve())}")
        print(f"binary={profile.binary} probe={profile.probe}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
