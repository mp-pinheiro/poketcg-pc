# Build and package

These commands use the repository's Linux build scripts. Linux AppImages and 64-bit Windows ZIPs are built locally; GitHub releases currently contain source snapshots rather than attached game binaries.

## Get the source

Clone the canonical repository:

```sh
git clone https://forgejo.yfrit.com/fairfruit/poketcg-pc.git
cd poketcg-pc
```

The GitHub mirror is for reading; repository writes target Forgejo as described in [jj workflow](jj-workflow.md).

## Dependencies

Use a C11 compiler, CMake 3.20 or newer, Ninja, Python 3.11 or newer, Git, SDL2 development headers, and `just`. The Python build generators use the standard library. Oracle tools are separate and are only needed for development and verification.

On Debian or Ubuntu:

```sh
sudo apt install build-essential cmake ninja-build python3 git libsdl2-dev pkg-config curl xz-utils zip
```

Install `just` through your package manager or the [upstream installer](https://just.systems/). The CI configuration records the version used by repository checks.

The disassemblies require RGBDS 1.0.0. The repository installer writes its tools to `/usr/local/bin`:

```sh
sudo bash tools/install_rgbds.sh
```

The installer uses the upstream Linux x86_64 archive; on AArch64 it builds from source. Check available memory before a source build.

## Build both games

From the repository root:

```sh
just bootstrap
just bootstrap-profile extended
POKETCG_NINJA_JOBS=-j1 just build-profiles
just play
```

`bootstrap` prepares the pinned Vanilla disassembly and shared graphics source. `bootstrap-profile extended` prepares and verifies the pinned Extended source. `build-profiles` generates separate data packs and builds both games, probes, and the SDL profile chooser.

The default output directory is `build`. [Playing](playing.md) covers controls, saves, profile switching, and diary import.

## Build one profile

For a Vanilla game/probe build:

```sh
just bootstrap
POKETCG_NINJA_JOBS=-j1 just build-profile vanilla
```

For an isolated Extended game/probe build:

```sh
just bootstrap
just bootstrap-profile extended
POKETCG_PROFILE=extended POKETCG_NINJA_JOBS=-j1 just build-profile extended
```

These builds do not include the chooser. Direct launch recipes require explicit save/load paths; see [direct launches](playing.md#direct-launches). The both-profile launcher manages persistence automatically.

`POKETCG_PROFILE` selects catalog paths. `POKETCG_BUILD` overrides the build directory when a private tree is needed. Keep the same selection for dependent build, pack, and run commands. Profile authoring belongs in [porting a profile](porting-a-profile.md).

## Create packages

The profile bundles include Vanilla, Extended, the chooser, both data packs, runtime libraries, and notices:

| Package | Command | Default output |
|---|---|---|
| Linux, both profiles | `POKETCG_NINJA_JOBS=-j1 just appimage-profiles` | `build/appimage-profiles/poketcg-profiles-VERSION-private-x86_64.AppImage` |
| Windows, both profiles | `POKETCG_NINJA_JOBS=-j1 just windows-profiles` | `build/windows-profiles/poketcg-profiles-VERSION-private-windows.zip` |
| Linux, Vanilla only | `POKETCG_NINJA_JOBS=-j1 just appimage` | `build/appimage/poketcg-VERSION-x86_64.AppImage` |
| Windows, Vanilla only | `POKETCG_NINJA_JOBS=-j1 just windows` | `build/windows/poketcg-VERSION-windows.zip` |

Run the bootstrap steps before packaging. The Windows builder cross-compiles on Linux using packages downloaded from the host's Ubuntu apt repositories and the pinned SDL2 MinGW archive; it needs `apt-get` and `dpkg`. It does not require Wine. The AppImage bundles SDL2 and other selected libraries, but its glibc compatibility floor comes from the build host.

Profile package outputs follow the selected build directory. The older Vanilla-only recipes use the default `build` package paths shown above.

The profile recipes pass `--private`, which only adds a filename marker. After building both profiles, these commands create bundles without that marker:

```sh
python3 tools/package_profiles.py --format appimage
python3 tools/package_profiles.py --format windows
```

Packaging does not upload files or grant redistribution rights. Extended attribution and the unverified distribution record are included as `NOTICE-EXTENDED.txt`; there is no permission-based build gate.

## Verification tools

This section is for maintainers. Playing the native game does not require these tools.

Install `uv` using its [upstream instructions](https://docs.astral.sh/uv/getting-started/installation/).

Gambatte verification also requires a separately supplied CGB boot image matching `tools/completion/gambatte_pins.toml`. Obtain an image you are entitled to use; it is not downloaded, committed, or included in game packages. Put it at the pinned path and verify its SHA-1 before bootstrap:

```sh
mkdir -p build/completion/gambatte
cp /path/to/cgb_boot.bin build/completion/gambatte/cgb_boot.bin
printf '%s  %s\n' 1293d68bf9643bc4f36954c1e80e38f39864528d build/completion/gambatte/cgb_boot.bin | sha1sum -c -
```

Prepare and check the pinned PyBoy and Gambatte environments:

```sh
just oracle-venv
just completion-gambatte-bootstrap
just oracle-health-pyboy
just completion-gambatte-health
```

The routine and replay lanes also use GB Recompiled. Its Linux x86_64 archive and hashes are pinned in `tools/oracle/artifacts.json`. Install the matching release in the paths expected by the recipes:

```sh
mkdir -p "$HOME/.local/gbrecomp"
curl -L --fail --silent --show-error \
  -o /tmp/gb-recompiled-linux-x64.tar.gz \
  https://github.com/arcanite24/gb-recompiled/releases/download/v0.1.0/gb-recompiled-linux-x64.tar.gz
printf '%s  %s\n' \
  b77fbf8913a9dd770097df81e8e0f84cf2e0d9e3a44dc1a1ee4d1846c5035535 \
  /tmp/gb-recompiled-linux-x64.tar.gz | sha256sum -c -
tar -xzf /tmp/gb-recompiled-linux-x64.tar.gz -C "$HOME/.local/gbrecomp"
"$HOME/.local/gbrecomp/gb-recompiled-linux/gbrecomp" --version
POKETCG_GBRECOMP_JOBS=1 just oracleb-regenerate
just oracleb-replay
```

`POKETCG_GBRECOMP` can select another verified compiler path; `POKETCG_ORACLEB_DIR` selects the generated replay directory. `GBRT_RUNTIME_DIR` selects the routine runner's runtime source. Defaults are the extracted compiler's `runtime` directory and `$HOME/.local/share/gbrecompiled/poketcg` for replay output.

The compiler archive is a verification dependency, not part of the game bundle. Keep reference work serial or bounded to measured cgroup headroom. Use the [maintenance workflow](grind.md) for evidence refresh, routine/session checks, and publication.
