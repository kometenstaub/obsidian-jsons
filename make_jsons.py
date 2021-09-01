#!/bin/python3
import os
import json
import urllib.parse

description_regex = r"^.*(?:\n.*){10}"
description_regex_small = r"^.*(?:\n.*){5}"

color : int = 3092790

for dirpath, dirnames, files in os.walk("./obsidian-docs/en/"):
    #print(f"Found directory: {dirnames}, located here:{dirpath}")
    for file_name in files:
        if file_name.endswith(".md"):
            normalised_path = os.path.normpath(dirpath + "/" + file_name)

            file_dict : dict = {}
            url : str = "https://help.obsidian.md/"
            title : str = ""
            description : str = ""

            # URL
            split_path : list = normalised_path.split("/")[2:]
            unencoded_url_part : str = "/".join(split_path)
            url += urllib.parse.quote(unencoded_url_part)
            url = url.replace("%20", "+")
            if url == "https://help.obsidian.md/Obsidian/Index.md":
                url = url.replace("Obsidian/", "")
            url = url.replace(".md", "")
            #print(url)
            file_dict["url"] = url
            
            # title
            title = file_name.replace(".md", "")
            file_dict["title"] = title
            
            # color
            file_dict["color"] = color

            #print(f"Found file: {file_name}")
            #print(normalised_path)

            # description
            with open(normalised_path, "r", encoding="utf-8") as f:
                content : dict = f.readlines()
                result : str = ""
                if len(content) >= 10:
                    result = "".join(content[:10])
                    if len(result) >= 2000:
                        result = result[:2000]
                else:
                    result = "".join(content)
                file_dict["description"] = result

            #print(file_dict)

            