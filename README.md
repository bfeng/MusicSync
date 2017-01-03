# MusicSync: Sync Songs between NeteaseMusic and iTunes with ID3 Tags Correction

This software contains a set of console commands to copy songs between folders enabling ID3 tags correction. It features copying MP3 files, fixing ID3 tags from NeteaseMusic MP3 files and importing into iTunes music library. A GUI is under development and will be launched in future.

## Install

1. Clone or download source code

2. For first time Mac users who do not have `pip` installed, please install `pip` with `easy_install`
    ```bash
    sudo easy_install pip
    ```

3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Usage
All commands should be run in the following pattern with a Python interpreter. Example:
```bash
python main.py <action> [parameters]
```

## Description

There are several actions available. Each action comes with different parameters.

- `print`

```bash
python main.py print ~/Music/网易云音乐/song.mp3
python main.py print ~/Music/网易云音乐/*
```

- `fix`

```bash
python main.py fix -dryrun "~/Music/网易云音乐/song.mp3"
python main.py fix "~/Music/网易云音乐/song.mp3"
python main.py print ~/Music/网易云音乐/*
```

- `cp_itunes`

```bash
python main.py cp_itunes "~/Music/网易云音乐" "/Users/bfeng/Music/iTunes"
```

- `rsync`

**Under development**


- `help`
