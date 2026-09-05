# 🧽 Spongia — Disk Tools

[![Tests](https://github.com/cryptonahue/spongia-disk-tools/actions/workflows/tests.yml/badge.svg)](https://github.com/cryptonahue/spongia-disk-tools/actions/workflows/tests.yml)

Command-line tools to analyze disk usage and safely remove files and folders.

Current release: **0.1.1**. See [CHANGELOG.md](CHANGELOG.md) for the release history.

## Features

- Find the largest files in a directory.
- Find the largest top-level folders.
- Send files and folders to the system trash.
- Permanently delete files only when explicitly requested.
- Protect the user profile and system directories.
- Require `--recursive` before deleting folders.
- Exclude files or folders with repeatable glob patterns.
- English, Spanish, and Brazilian Portuguese messages.

## Usage

### Find large files

```bash
# Files of at least 10 MB, top 20
spongia find

# Analyze a specific directory
spongia find --dir D:\Downloads

# Custom minimum size and result count
spongia find --dir . --min-size 100MB --top 50

# Find the largest top-level folders
spongia find dirs --dir .

# Exclude folders or files; --exclude can be repeated
spongia find --dir . --exclude .git --exclude "*.pyc"
```

### Remove files and folders

By default, Spongia sends the target to the system trash and asks for confirmation.

```bash
# Send a file to the trash
spongia remove locked_file.pdf

# Send a folder to the trash
spongia remove ./folder --recursive

# Permanently delete a file
spongia remove file.txt --permanent

# Skip confirmation (use with care)
spongia remove file.txt --force
```

> ⚠️ **Safety:** confirmation is required unless `--force` is used. The user profile, the Windows directory, and their descendants are protected. Install `send2trash` to enable safe trash operations.

## Installation

### From the repository

```bash
pip install .
```

### Optional trash support

```bash
pip install ".[trash]"
```

### Development tests

```bash
python -m unittest discover -s . -p "test_*.py" -v
```

## Dependencies

| Package | Required for |
| --- | --- |
| `send2trash` | Sending files to the system trash (optional) |

## Command reference

### `find`

| Argument | Default | Description |
| --- | --- | --- |
| `mode` | `files` | `files` for files or `dirs` for folders |
| `--dir, -d` | `.` | Directory to analyze |
| `--min-size` | `10MB` | Minimum file size, such as `50MB` or `1GB` |
| `--top` | `20` | Number of results |
| `--exclude` | — | Exclusion pattern; can be repeated |
| `--lang, -L` | `en` | `en`, `es`, or `pt` |

### `remove`

| Argument | Default | Description |
| --- | --- | --- |
| `ruta` | — | File or folder to remove |
| `--recursive, -r` | off | Allow folder removal |
| `--permanent` | off | Permanently delete instead of using the trash |
| `--force, -f` | off | Skip confirmation |
| `--lang, -L` | `en` | `en`, `es`, or `pt` |

## Project files

```text
spongia.py          # CLI and application logic
spongia_translations.py     # English, Spanish, and Portuguese messages
test_spongia.py     # Unit tests
pyproject.toml      # Package configuration
requirements.txt    # Optional dependency list
CHANGELOG.md        # Release history
LICENSE             # MIT license
```

## License

MIT — see [LICENSE](LICENSE).
