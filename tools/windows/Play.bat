@echo off
set "here=%~dp0"
set "data=%APPDATA%\poketcg"
if not exist "%data%" mkdir "%data%"
set "POKETCG_CONFIG=%data%\options.conf"
set load=
if exist "%data%\poketcg.sav" set load=--load-save "%data%\poketcg.sav"
start "" "%here%poketcg.exe" --data-pack "%here%data-pack.bin" --frames 0 --save "%data%\poketcg.sav" %load% %*
