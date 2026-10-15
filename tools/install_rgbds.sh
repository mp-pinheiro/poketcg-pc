#!/usr/bin/env bash
set -euo pipefail
version=1.0.0
release="https://github.com/gbdev/rgbds/releases/download/v${version}"
case "$(uname -m)" in
    x86_64)
        curl --proto '=https' --tlsv1.2 -fsSL "${release}/rgbds-linux-x86_64.tar.xz" \
            | tar -xJ -C /usr/local/bin rgbasm rgblink rgbfix rgbgfx
        ;;
    aarch64)
        apt-get update
        apt-get install -y --no-install-recommends bison libpng-dev pkg-config
        source_dir="$(mktemp -d)"
        curl --proto '=https' --tlsv1.2 -fsSL "${release}/rgbds-source.tar.gz" \
            | tar -xz -C "$source_dir" --strip-components=1
        make -C "$source_dir" -j"$(nproc)" install
        rm -rf "$source_dir"
        ;;
    *)
        echo "unsupported arch: $(uname -m)" >&2
        exit 1
        ;;
esac
rgbasm --version
