#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
version="$(tr -d '[:space:]' < "$root/VERSION")"
profiles=0
if [[ "${1:-}" == --profiles ]]; then
	profiles=1
	appdir="$(realpath "${2:?usage: build.sh --profiles APPDIR OUTPUT_DIR PACKAGE_NAME}")"
	out_dir="$(realpath -m "${3:?usage: build.sh --profiles APPDIR OUTPUT_DIR PACKAGE_NAME}")"
	package_name="${4:?usage: build.sh --profiles APPDIR OUTPUT_DIR PACKAGE_NAME}"
	output="$out_dir/$package_name.AppImage"
else
	binary="$(realpath "${1:?usage: build.sh BINARY PACK OUTPUT_DIR}")"
	pack="$(realpath "${2:?usage: build.sh BINARY PACK OUTPUT_DIR}")"
	out_dir="$(realpath -m "${3:?usage: build.sh BINARY PACK OUTPUT_DIR}")"
	appdir="$out_dir/AppDir"
	output="$out_dir/poketcg-$version-x86_64.AppImage"
fi
linuxdeploy="$out_dir/tools/linuxdeploy-x86_64.AppImage"
url=https://github.com/linuxdeploy/linuxdeploy/releases/download/1-alpha-20251107-1/linuxdeploy-x86_64.AppImage
sha256=c20cd71e3a4e3b80c3483cef793cda3f4e990aca14014d23c544ca3ce1270b4d
if ! echo "$sha256  $linuxdeploy" | sha256sum -c --status 2>/dev/null; then
	mkdir -p "$out_dir/tools"
	curl -fsSL -o "$linuxdeploy.part" "$url"
	echo "$sha256  $linuxdeploy.part" | sha256sum -c --quiet
	chmod +x "$linuxdeploy.part"
	mv "$linuxdeploy.part" "$linuxdeploy"
fi
if (( profiles )); then
	executables=(
		--executable "$appdir/usr/bin/poketcg"
		--executable "$appdir/usr/bin/poketcg-extended"
		--executable "$appdir/usr/bin/poketcg-launcher"
	)
	desktop="$root/tools/appimage/poketcg-profiles.desktop"
	apprun="$root/tools/appimage/AppRun-profiles"
else
	rm -rf "$appdir" "$output"
	install -Dm644 "$pack" "$appdir/usr/share/poketcg/data-pack.bin"
	for licence in "$root"/third_party/fonts/*LICENSE*.txt; do
		install -Dm644 "$licence" "$appdir/usr/share/licenses/poketcg/$(basename "$licence")"
	done
	executables=(--executable "$binary")
	desktop="$root/tools/appimage/poketcg.desktop"
	apprun="$root/tools/appimage/AppRun"
fi
cd "$out_dir"
APPIMAGE_EXTRACT_AND_RUN=1 LDAI_OUTPUT="$output" LDAI_NO_APPSTREAM=1 "$linuxdeploy" \
	--appdir "$appdir" \
	"${executables[@]}" \
	--desktop-file "$desktop" \
	--icon-file "$root/tools/appimage/poketcg.png" \
	--custom-apprun "$apprun" \
	--output appimage
echo "$output"
