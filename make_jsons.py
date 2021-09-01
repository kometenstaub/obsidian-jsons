#!/bin/python3
import os
import json
import re
import urllib.parse

for dirpath, dirnames, files in os.walk("./obsidian-docs/en/"):
    #print(f"Found directory: {dirnames}, located here:{dirpath}")
    for file_name in files:
        if file_name.endswith(".md"):
            normalised_path = os.path.normpath(dirpath + "/" + file_name)

            file_dict : dict = {}
            url : str = "https://help.obsidian.md/"
            title : str = ""
            description : str = ""
            color : str = ""

            split_path : list = normalised_path.split("/")[2:]
            unencoded_url_part : str = "/".join(split_path)
            url += urllib.parse.quote(unencoded_url_part)
            url = url.replace("%20", "+")
            if url == "https://help.obsidian.md/Obsidian/Index.md":
                url = url.replace("Obsidian/", "")
            url = url.replace(".md", "")
            print(url)

            #print(f"Found file: {file_name}")
            #print(normalised_path)

