#!/usr/bin/python3
import os
import json
import urllib.parse
import sys

if_json : bool = False

try:
    if sys.argv[1].lower() == "json":
        if_json = True
except:
    pass

color : int = 3092790
tagscript_file : str = """
{=(b-obsidian):Obsidian/Obsidian}
{c:cembed https://raw.githubusercontent.com/kometenstaub/obsidian-docs-json/main/{{path-to-json}}}\n\n
"""
tagscript_file_list : list = []

github_url : str = "https://raw.githubusercontent.com/kometenstaub/obsidian-docs-json/main/"

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
            file_dict["url"] = url
            
            # title
            title = file_name.replace(".md", "")
            file_dict["title"] = title
            
            # color
            file_dict["color"] = color

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

            # convert dict to json
            json_string = json.dumps(file_dict, indent=4)


            # make file path for json file
            json_path = normalised_path.split("/")[2:]

            # json_folder is where the jsons will we stored
            json_folder : str = "/".join(json_path[:-1])

            json_path = "/".join(json_path)
            json_path = json_path.replace(".md", ".json")

            # write json files only if "json" argument provided
            if if_json:
                # check if directory already exists; if not, create it
                if not os.path.isdir(f"obsidian-jsons/{json_folder}"):
                    os.makedirs(f"obsidian-jsons/{json_folder}")
                # write the json string
                with open(f"obsidian-jsons/{json_path}", "w", encoding="utf-8") as j:
                    j.write(json_string)

            # append files for tagscript file
            tagscript_title : str = title.replace(" ", "-").lower()
            after_github_path : str = urllib.parse.quote(json_path)
            tagscript_file_list.append("{=(" + tagscript_title + "):" + after_github_path + "}")
            

tagscript_file += "\n".join(tagscript_file_list)

# write tagscript
with open("tagscript", "w", encoding="utf-8") as t:
    t.write(tagscript_file)