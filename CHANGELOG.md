# Changelog

All notable changes to this project are documented here.
This changelog is generated automatically from [Conventional Commits](https://www.conventionalcommits.org) by [git-cliff](https://github.com/orhun/git-cliff).
## v0.220.0 - 2026-09-03

### Bug Fixes

- *(runtime)* Grant single vblank per disable lcd
- *(tools)* Exclude free-running div from io compare
- *(tools)* Exclude timer and if latches from io compare
- *(tools)* Exclude hardware timing fabric from io compare
- *(tools)* Correct vblank counter exclusion offset
- *(port)* Consume menu print vblank at init
- *(tools)* Exclude stat and audio fabric from io compare
- *(tools)* Widen input presses for frame axis fidelity
- *(port)* Use overworld map names table
- *(runtime)* Restore asm doframe boundary order
- *(tools)* Exclude timer counter from wram compare
- *(runtime)* Declare service pass accessor
- *(port)* Use full font index for glyph offset
- *(runtime)* Sample input one scanout late

### Documentation

- *(plan)* Add integration program plan

### Features

- *(runtime)* Classify service and frame boundary passes

