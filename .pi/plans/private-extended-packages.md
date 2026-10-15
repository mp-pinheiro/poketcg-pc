# Goal
Enable real private Extended package creation on Linux and Windows, retain honest unverified redistribution metadata, and exercise the generated packages without uploading them.

# Files in scope
- `justfile`: local profile package recipes invoke explicit private mode and build their real prerequisites.
- `tools/package_profiles.py`: private artifact names, orchestration and stage validation; artifact creation does not require permission metadata.
- `tools/appimage/build.sh`: reuse the pinned linuxdeploy builder for the staged multi-profile product.
- `tools/appimage/AppRun-profiles`: launch the bundled profile chooser and forward runtime arguments.
- `tools/appimage/poketcg-profiles.desktop`: identify the multi-profile application and launcher.
- `tools/windows/build.sh`: cross-compile and stage all three PE executables and Windows dependencies.
- `tools/windows/mingw-w64.cmake`: existing pinned MinGW and SDL2 toolchain.
- `tools/windows/Play-profiles.bat`: launch the Windows profile chooser.
- `tools/windows/README.txt`: document the private profiles bundle alongside the existing vanilla bundle.
- `README.md`: private package commands and separate redistribution status.
- `tests/test_package_profiles.py`: meaningful package-policy or platform-boundary regressions where required.

# Contracts
- User explicitly permits private packages; no private artifact is uploaded or represented as licensed for redistribution.
- Keep `profiles/extended/provenance.toml` permission evidence truthful and unchanged.
- Parent owns `tools/package_profiles.py`, `justfile`, root README and integration; implementation slices own disjoint platform files.
- AppImage builder contract: `tools/appimage/build.sh --profiles APPDIR OUTPUT_DIR PACKAGE_NAME`, with the complete product already staged under APPDIR/usr/bin; create OUTPUT_DIR/PACKAGE_NAME.AppImage.
- Windows builder contract: `tools/windows/build.sh --profiles VANILLA_PACK EXTENDED_PACK STAGE_DIR`; cross-compile and populate STAGE_DIR without creating a ZIP, leaving archive creation and exclusion checks to the parent.
- Preserve existing single-profile packaging commands and paths; default Ninja work is serialized under `POKETCG_NINJA_JOBS=-j1`.
- Every artifact contains the real game binaries, chooser, both correct sparse packs, required runtime libraries and notices; a Windows ZIP must contain PE executables, never renamed ELF files.

# Pattern to copy
Reuse `tools/appimage/build.sh` pinned linuxdeploy download/checksum and `tools/windows/build.sh` pinned SDL2/MinGW acquisition, compilation and license staging.

# Non-goals
Do not publish bundles, invent license grants, change ROM/game behavior, weaken package artifact exclusions, or redesign unrelated build/evidence systems.

# Acceptance
- Private Linux package creation succeeds :: POKETCG_NINJA_JOBS=-j1 just appimage-profiles
- Private Windows package creation succeeds :: POKETCG_NINJA_JOBS=-j1 just windows-profiles
- Package policy regression passes :: python3 -m unittest tests.test_package_profiles
- Repository build remains green :: POKETCG_NINJA_JOBS=-j1 just build
