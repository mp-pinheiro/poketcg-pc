@echo off
set "here=%~dp0"
set "data=%APPDATA%\poketcg"
if not exist "%data%" mkdir "%data%"
set "POKETCG_CONFIG=%data%\options.conf"
start "" "%here%poketcg-launcher.exe" %*
