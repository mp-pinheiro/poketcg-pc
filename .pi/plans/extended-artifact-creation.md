# Goal
Remove the remaining permission-based distribution policy. Delete the standalone checker and record distribution status as unverified, with license and permission evidence unchanged. Rebuild local Linux and Windows artifacts without publishing anything.

# Files in scope
- `tools/package_profiles.py`: remove distribution approval from artifact creation; keep optional private artifact naming.
- `tools/check_profile_distribution.py`: delete the obsolete distribution-policy checker.
- `profiles/extended/provenance.toml`: change only distribution status from blocked to unverified.
- `tools/windows/README.txt`: remove private-only wording from the shared package instructions.
- `.pi/plans/3449-asm-delta-ports.md`: replace the stale packaging-block claim with exercised artifact results.
- `README.md`: explain package creation and its separation from distribution approval.
- `.pi/plans/extended-profile-port.md`: replace the obsolete artifact-creation failure contract with the current boundary.
- `.pi/plans/private-extended-packages.md`: clarify that private naming does not authorize distribution.
- `tests/test_package_profiles.py`: retain ROM/disassembly exclusion coverage unchanged.

# Contracts
- Keep repository pins, attribution, license and permission evidence unchanged; record distribution status as unverified.
- Remove the standalone permission checker and its obsolete invocations and policy documentation.
- Preserve real ELF/PE binaries, both sparse packs, chooser behavior, notices and forbidden-artifact checks.
- Preserve `--private` as an artifact naming option; both flagged and unflagged local builds work.
- Do not publish, push or upload code or artifacts.

# Pattern to copy
Reuse the existing `appimage()` and `windows()` builders and stage validation in `tools/package_profiles.py`; retain the provenance notice without any permission-based build gate.

# Non-goals
No game behavior, save formats, ROMs, permission evidence, public uploads or unrelated build changes.

# Acceptance
- [x] Unflagged Linux artifact creation succeeds :: POKETCG_BUILD=build-cmake-generic2 POKETCG_NINJA_JOBS=-j1 python3 tools/package_profiles.py --format appimage
- [x] Unflagged Windows artifact creation succeeds :: POKETCG_BUILD=build-cmake-generic2 POKETCG_NINJA_JOBS=-j1 python3 tools/package_profiles.py --format windows
- [x] Provenance records unverified status with unchanged license and evidence :: python3 -c 'import pathlib, tomllib; p = tomllib.loads(pathlib.Path("profiles/extended/provenance.toml").read_text()); assert (p["distribution"], p["license"], p["permission_evidence"]) == ("unverified", "none-declared", [])'
- [x] Package exclusions pass :: python3 -m unittest tests.test_package_profiles
- [x] Repository build remains green :: POKETCG_BUILD=build-cmake-generic2 POKETCG_NINJA_JOBS=-j1 just build
