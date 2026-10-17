# Playing

Use a profile bundle built with [the build guide](building.md), or run `just play` after `just build-profiles`. The launcher offers Vanilla and Extended on first use and remembers the game played last.

## Start a game

| Installation | Start |
|---|---|
| Source build | `just play` |
| Linux profile AppImage | Run the AppImage file |
| Windows profile ZIP | Extract the ZIP and run `Play.bat` |

To select a profile explicitly from a source build:

```sh
just play --profile vanilla
just play --profile extended
```

AppImage arguments and arguments passed to `Play.bat` are forwarded to the launcher. Direct game binaries bypass the chooser.

## Controls

| Keyboard | Game button |
|---|---|
| Arrow keys | D-pad |
| Z | A |
| X | B |
| Enter | Start |
| Backspace | Select |

The game renders on the original 160x144 pixel grid. Host scaling preserves nearest-neighbour pixels; unused window space is outside the game canvas.

## Switch profiles

When started through the launcher, PC OPTIONS offers PLAY EXTENDED or PLAY ORIGINAL in its GAMEPLAY section. Switching writes the current cartridge save the same way a normal application close does, then starts the other game. Save through the game's diary when you want that progress available to Continue from Diary.

Each profile has its own save. Their tagged formats are different; renaming one profile's save is not a conversion.

## Gameplay options

The GAMEPLAY section of PC OPTIONS holds PLAYER (Mark or Mint), NEW GAME SELECT, MESSAGE SPEED (1 to 5), and DUEL ANIM (SHOW ALL, SKIP SOME, NONE) in both profiles. With a save present, MESSAGE SPEED and DUEL ANIM show and change the values stored in that save, the same bytes the in-game Config menu edits. Without a save, the choices are kept in `options.conf` and applied when New Game starts, so the intro and the practice duel already use them.

## Saves and settings

These locations apply to the launcher and packaged entry points:

| Platform | Save directory | Settings |
|---|---|---|
| Linux | `${XDG_DATA_HOME:-~/.local/share}/poketcg/` | `${XDG_CONFIG_HOME:-~/.config}/poketcg/options.conf` |
| Windows via `Play.bat` | `%APPDATA%\poketcg\` | `%APPDATA%\poketcg\options.conf` |

Vanilla uses `poketcg.sav`; Extended uses `poketcg-extended.sav`. `last-game` in the save directory records the launcher selection. Both profiles share the options file.

Native source builds and Linux AppImages accept `POKETCG_CONFIG` as an options-file override. Windows `Play.bat` sets that variable to the options path shown above.

`display` in `options.conf` selects the monitor the window opens on, counted from 0 in the order the system reports displays. The window is centered on that monitor and stays centered on it when RESOLUTION or SGB changes its size.

An explicit `--save`, `--load-save`, or `--data-pack` selects custom launcher paths and disables automatic Vanilla-to-Extended import and launcher-backed profile switching.

## Direct launches

`just play-vanilla` and `just play-extended` launch game binaries directly. They do not automatically select, load, or write a save file. Supply `--save` to persist cartridge SRAM, and add `--load-save` when resuming an existing file:

```sh
just play-vanilla --save /path/to/vanilla.sav
just play-vanilla --load-save /path/to/vanilla.sav --save /path/to/vanilla.sav
```

Use `play-extended` with an Extended save and the matching profile/build selection for an isolated Extended build.

## Continue a Vanilla diary in Extended

On the first Extended launch without an Extended save, the launcher imports an existing Vanilla save from the default save directory. It uses the state restored by Vanilla's Continue from Diary and leaves the Vanilla file untouched.

The import carries the player, collection, decks, medals, world progress, and play time. It drops an unfinished duel. The converter fills Extended's 50 saved-deck slots and reports any excess decks it could not fit.

The launcher does not replace a pre-existing Extended save. A manual conversion overwrites its output path, so back up that file first. From a both-profile source build:

```sh
build/poketcg-extended --data-pack build/completion/data-pack-extended.bin \
  --convert-vanilla-save /path/to/poketcg.sav /path/to/poketcg-extended.sav
```

The converter requires this port's tagged Vanilla `PKSR` format; a raw emulator SRAM image is not accepted. Developer-generated seeded SRAM scenarios use the separate [reach harness](reach-harness.md) path.

## Transport support

The native `--link-fd` transport is Linux-only. The [reach harness](reach-harness.md) describes peer and printer diagnostics and their reference proof; a transport diagnostic is not an ordinary player matchmaking interface.

