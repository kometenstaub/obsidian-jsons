# Obsidian docs to json for Carl-bot

This repo contains a python script that will transform the Obsidian docs into json files (limited to the first 10 lines of each file) for use with Carl-bot.

## Installation

1. Clone this repo.

```bash
git clone https://github.com/kometenstaub/obsidian-jsons
```

2. `cd` into the cloned folder and run

```bash
git clone git@github.com:obsidianmd/obsidian-docs.git
```

if you want to use SSH or

```bash
git clone https://github.com/obsidianmd/obsidian-docs.git
```

if you want to use HTTPS.

## Usage

If you want to create the json files:

```bash
python3 make_jsons.py json
```

If you don't want to create the json files (mainly for testing):

```bash
python3 make_jsons.py
```

The json files will be overwritten each time you run this script with the `json` argument, so no need to delete the folder manually.

Every time, the `tagscript` file will be created. It is also overwritten each time you run the script again, the `json` argument doesn't influence this behaviour.