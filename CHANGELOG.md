# Changelog

All notable changes to this project are documented here.
This changelog is generated automatically from [Conventional Commits](https://www.conventionalcommits.org) by [git-cliff](https://github.com/orhun/git-cliff).
## v1.2.0 - 2026-09-28

### Bug Fixes

- *(effects)* Restore Poke Ball search texts
- *(mem)* Wrap non-extension ROM bank writes
- *(main-menu)* Stop probe _GameLoop at menu loop
- *(animations)* Treat a null screen update as ret
- *(deck)* Honor the deck build screen carry
- *(core)* Stop comparing de after buffered anims

### CI/CD

- Run tooling tests in quality job
- Ignore nightly tags in release versioning

### Documentation

- *(grind)* Add two session symptom rows

### Features

- *(gate)* Add function gate to release gate
- *(gift-center)* Send cards and decks over IR

### Miscellaneous

- Purge dead code and orphan files
- *(completion)* Remove widescreen scenarios
- Remove unused duel animation defines
- Build warning-free and drop dead code

### Refactor

- *(completion)* Resolve wram offsets lazily
- *(completion)* Break scenario import cycle

### Tests

- *(cases)* Remove gbref harness artefacts

