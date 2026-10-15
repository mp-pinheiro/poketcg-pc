# poketcg-pc

A native C11/SDL2 port of Pokémon Trading Card Game for Game Boy Color, with Vanilla and [Extended](https://github.com/ElectroDeoxys/Pokemon-TCG-Extended) profiles. The game preserves the original 160x144 pixel canvas.

## Build and play

Install the [build dependencies](docs/building.md#dependencies), then run from the repository root:

```sh
just bootstrap
just bootstrap-profile extended
POKETCG_NINJA_JOBS=-j1 just build-profiles
just play
```

The launcher offers both games and remembers the last selection.

## Packages

[GitHub releases](https://github.com/mp-pinheiro/poketcg-pc/releases) currently contain source snapshots, not attached game binaries. The [packaging guide](docs/building.md#create-packages) builds Linux AppImages and 64-bit Windows ZIPs locally.

## Guides

| Task | Read |
|---|---|
| Controls, profiles, saves, and diary import | [Playing](docs/playing.md) |
| Dependencies, source builds, and packages | [Build and package](docs/building.md) |
| Architecture, verification, maintenance, and profile authoring | [Documentation index](docs/README.md) |

## Project links

- [Canonical repository](https://forgejo.yfrit.com/fairfruit/poketcg-pc)
- [GitHub mirror](https://github.com/mp-pinheiro/poketcg-pc)
- [Verification dashboard](https://poketcg-pc.pages.dev/)
- [Generated changelog](CHANGELOG.md)

