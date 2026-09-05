# Changelog

All notable changes to Spongia are documented here.

## [0.1.1] - 2026-09-05

### Fixed

- Avoided collisions with `translations.py` modules from sibling projects by using the unique `spongia_translations.py` module name.
- Fixed the installed `spongia` entry point on environments containing multiple Python projects.

## [0.1.0] - 2026-09-05

### Added

- Disk usage analysis for heavy files and top-level directories.
- Safe deletion to the system trash with optional permanent deletion.
- Confirmation prompts and protected system/profile directories.
- Spanish, English, and Brazilian Portuguese messages.
- Repeated `--exclude` patterns for file and directory searches.
- Installable `spongia` command through `pyproject.toml`.
- Automated tests on Ubuntu and Windows with Python 3.10–3.13.

### Security

- Recursive deletion requires `--recursive`.
- Protected directories include the user profile and Windows system directory.
- Symlink targets are not recursively followed during deletion.
