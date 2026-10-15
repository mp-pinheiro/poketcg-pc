#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
mode=vanilla
if [ "${1:-}" = --profiles ]; then
	mode=profiles
	shift
fi
if [ "$mode" = profiles ]; then
	[ "$#" -eq 3 ] || { echo "usage: build.sh --profiles VANILLA_PACK EXTENDED_PACK STAGE_DIR" >&2; exit 2; }
	vanilla_pack="$(realpath "$1")"
	extended_pack="$(realpath "$2")"
	stage="$(mkdir -p "$3" && cd "$3" && pwd)"
else
	[ "$#" -eq 1 ] || { echo "usage: build.sh PACK" >&2; exit 2; }
	pack="$(realpath "$1")"
fi
out="$root/build/windows"
tools="$out/tools"
version="$(tr -d '[:space:]' < "$root/VERSION")"
sdl=SDL2-2.32.10
sdl_url=https://github.com/libsdl-org/SDL/releases/download/release-2.32.10/SDL2-devel-2.32.10-mingw.tar.gz
sdl_sha256=83a5d74012311edc3c0d40ea6faecbe57ad692aa033fa5dc273cc937e3938ff2
mkdir -p "$tools"
if [ ! -d "$tools/$sdl" ]; then
	curl -fsSL -o "$tools/$sdl-mingw.tar.gz" "$sdl_url"
	echo "$sdl_sha256  $tools/$sdl-mingw.tar.gz" | sha256sum -c --quiet
	tar -xzf "$tools/$sdl-mingw.tar.gz" -C "$tools"
fi
if [ ! -x "$tools/mingw/usr/bin/x86_64-w64-mingw32-gcc-posix" ]; then
	rm -rf "$tools/debs" "$tools/mingw"
	mkdir -p "$tools/debs"
	(cd "$tools/debs" && apt-get download gcc-mingw-w64-x86-64-posix gcc-mingw-w64-x86-64-posix-runtime \
		gcc-mingw-w64-base binutils-mingw-w64-x86-64 mingw-w64-x86-64-dev mingw-w64-common)
	for deb in "$tools"/debs/*.deb; do
		dpkg -x "$deb" "$tools/mingw"
	done
fi
if [ "$mode" = profiles ]; then
	tree="$out/cmake-profiles"
	cmake -G Ninja -S "$root" -B "$tree" -DCMAKE_BUILD_TYPE=RelWithDebInfo \
		-DCMAKE_TOOLCHAIN_FILE="$root/tools/windows/mingw-w64.cmake" \
		-DPOKETCG_ENABLE_EXTENDED=ON -DPOKETCG_ENABLE_LAUNCHER=ON \
		-DPOKETCG_DATA_PACK="$vanilla_pack" \
		-DPOKETCG_PROFILE_EXTENDED_DATA_PACK="$extended_pack" -DPORT_FILES=""
	ninja ${POKETCG_NINJA_JOBS:--j1} -C "$tree" poketcg poketcg-extended poketcg-launcher
	rm -rf "$stage"
	mkdir -p "$stage/licenses"
	"$tools/mingw/usr/bin/x86_64-w64-mingw32-strip" -o "$stage/poketcg.exe" "$tree/poketcg.exe"
	"$tools/mingw/usr/bin/x86_64-w64-mingw32-strip" -o "$stage/poketcg-extended.exe" "$tree/poketcg-extended.exe"
	"$tools/mingw/usr/bin/x86_64-w64-mingw32-strip" -o "$stage/poketcg-launcher.exe" "$tree/poketcg-launcher.exe"
	cp "$tools/$sdl/x86_64-w64-mingw32/bin/SDL2.dll" "$stage/"
	cp "$vanilla_pack" "$stage/data-pack.bin"
	cp "$extended_pack" "$stage/data-pack-extended.bin"
	sed 's/$/\r/' "$root/tools/windows/Play-profiles.bat" > "$stage/Play.bat"
	sed 's/$/\r/' "$root/tools/windows/README.txt" > "$stage/README.txt"
	cp "$root"/third_party/fonts/*LICENSE*.txt "$stage/licenses/"
	cp "$tools/$sdl/LICENSE.txt" "$stage/licenses/SDL2-LICENSE.txt"
	cp "$tools/mingw/usr/share/doc/mingw-w64-x86-64-dev/copyright" "$stage/licenses/mingw-w64-runtime-copyright.txt"
else
	cmake -G Ninja -S "$root" -B "$out/cmake" -DCMAKE_BUILD_TYPE=RelWithDebInfo \
		-DCMAKE_TOOLCHAIN_FILE="$root/tools/windows/mingw-w64.cmake" -DPORT_FILES=""
	ninja ${POKETCG_NINJA_JOBS:--j1} -C "$out/cmake" poketcg
	name="poketcg-$version-windows"
	stage="$out/$name"
	rm -rf "$stage" "$out/$name.zip"
	mkdir -p "$stage/licenses"
	"$tools/mingw/usr/bin/x86_64-w64-mingw32-strip" -o "$stage/poketcg.exe" "$out/cmake/poketcg.exe"
	cp "$tools/$sdl/x86_64-w64-mingw32/bin/SDL2.dll" "$stage/"
	cp "$pack" "$stage/data-pack.bin"
	sed 's/$/\r/' "$root/tools/windows/Play.bat" > "$stage/Play.bat"
	sed 's/$/\r/' "$root/tools/windows/README.txt" > "$stage/README.txt"
	cp "$root"/third_party/fonts/*LICENSE*.txt "$stage/licenses/"
	cp "$tools/$sdl/LICENSE.txt" "$stage/licenses/SDL2-LICENSE.txt"
	cp "$tools/mingw/usr/share/doc/mingw-w64-x86-64-dev/copyright" "$stage/licenses/mingw-w64-runtime-copyright.txt"
	(cd "$out" && zip -qr -9 "$name.zip" "$name")
	echo "$out/$name.zip"
fi
