<!-- cSpell:words kaize backupper -->

<!-- omit in toc -->
# (Unofficial) Kaize.io List Backupper

Backup your anime & manga lists on [Kaize] in JSON format by scraping HTML, powered by Python under [MIT License][LICENSE].

This script mainly used for [nattadasu/animeManga-autoBackup](https://github.com/nattadasu/animeManga-autoBackup) project for backup anime & manga lists automation in PowerShell from several sites.

<!-- omit in toc -->
## Table of Contents

* [Requirements](#requirements)
* [Usage](#usage)
* [Arguments](#arguments)
  * [`-u`, `--username`](#-u---username)
  * [`-t`, `--type`](#-t---type)
  * [`-o`, `--out-file`, `--output`](#-o---out-file---output)
  * [`-h`, `--help`](#-h---help)

## Requirements

This script may requires Python 3.6 or greater. You may need to install required dependencies by running following command in terminal/command prompt:

```bash
python -m pip install -r requirements.txt
```

Or

```bash
pip install -r requirements.txt
```

**Note**: Depends on the OS and distro, use `python3` to `python` to avoid any issue.

## Usage

```bash
python ./main.py
```

## Arguments

### `-u`, `--username`

**Type**: String

Set Kaize profile name (username) for backup.

If argument did not called, script will prompt in initialization.

### `-t`, `--type`

**Type**: String\
**Options**: `anime`, `manga`

Select which media type to export.

If argument did not called, script will prompt in initialization.

### `-o`, `--out-file`, `--output`

**Type**: String (Path)\
**Default**: `./kaize_animeList.json`, `./kaize_mangaList.json`

Set where file will be saved as JSON.

Script will automatically append `.json` to file name if not set.

### `-h`, `--help`

Show a help menu.

<!-- Refs -->
[Kaize]: https://kaize.io
[LICENSE]: ./LICENSE
