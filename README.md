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

This script may requires Python 3.6 or greater. You may need to run dependencies by running:

```bash
python -m pip -r requirements.txt
```

Or

```bash
pip -r requirements.txt
```

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

**Type**: Array: `anime`, `manga`

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
