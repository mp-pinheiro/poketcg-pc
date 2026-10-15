Pokemon TCG (native PC port) for 64-bit Windows

Run it: double-click Play.bat.
Windows may warn that the game is from an unknown publisher because it is not code-signed: click "More info", then "Run anyway".

Controls: arrow keys = D-pad, Z = A, X = B, Enter = Start, Backspace = Select.

For the single-profile package, the save is written to %APPDATA%\poketcg\poketcg.sav when you close the window and loads automatically next time.

Vanilla and Extended profile package:

Run Play.bat to open the profile chooser. The chooser selects Vanilla or Extended; arguments passed to Play.bat are forwarded to the chooser.

The profiles have separate saves under %APPDATA%\poketcg: Vanilla uses poketcg.sav and Extended uses poketcg-extended.sav. Play.bat selects the shared options.conf configuration in that directory.

Creating this package does not grant permission to redistribute the included game data or third-party components. Source attribution and recorded distribution status are included in NOTICE-EXTENDED.txt.
