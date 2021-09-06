# Obsidian docs to json for Carl-bot

This repo contains a python script that will transform the Obsidian docs into json files (limited to the first 10 lines of each file or all the headings, if any) for use with Carl-bot.

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
python3 make_jsons.py <api_dev_key> <api_user_key>
```


All files will be uploaded, the old files will be deleted on Pastebin.

The `tagscript` file is updated every time, so is the `paste_ids.py` file.

The paste `api_paste_private` key is set to 1, so pastes are unlisted. Keep in mind the limit of 10 unlisted pastes for free accounts. Set it to 0 to upload public pastes.


## Testing

For testing, I have left in the counter variable. You need to uncomment it in three places if you want to limit uploads:

```python
#counter : int = 0

for dirpath, dirnames, files in os.walk("./obsidian-docs/en/"):
    for file_name in files:
        if file_name.endswith(".md"):
            normalised_path = os.path.normpath(dirpath + "/" + file_name)
            if file_name in included_files:# and counter < 3:
                #counter += 1
```