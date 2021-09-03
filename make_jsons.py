#!/usr/bin/python3
import os
import json
import urllib.parse
import sys
import requests
import re

api_dev_key : str = ""
api_user_key : str = ""

api_option : str = "paste"
api_paste_format : str = "json"
api_paste_private : int = 0
api_paste_expiry_date : str = "N"

try:
    if sys.argv[1]:
        api_dev_key = sys.argv[1]
    if sys.argv[2]:
        api_user_key = sys.argv[2]
except:
    pass

color : int = 3092790
tagscript_file : str = """
{=(b-obsidian):Obsidian/Obsidian}
{c:cembed https://raw.githubusercontent.com/kometenstaub/obsidian-docs-json/main/{{path-to-json}}}\n\n
"""
tagscript_file_list : list = []

github_url : str = "https://raw.githubusercontent.com/kometenstaub/obsidian-docs-json/main/"

included_files : list = ["Android app.md", "iOS app.md", "Mobile app beta.md", "Obsidian.md", "Obsidian Mobile.md", "How Obsidian stores data.md", "Third-party plugins.md", "Insider builds.md", "YAML front matter.md", "Catalyst license.md", "Commercial license.md", "Obsidian Publish.md", "Obsidian Sync.md", "Obsidian Unlimited.md", "Refund policy.md", "Add aliases to note.md", "Folding.md", "Format your notes.md", "Link to blocks.md", "Templates.md"] 

counter : int = 0

for dirpath, dirnames, files in os.walk("./obsidian-docs/en/"):
    #print(f"Found directory: {dirnames}, located here:{dirpath}")
    for file_name in files:
        if file_name.endswith(".md"):
            normalised_path = os.path.normpath(dirpath + "/" + file_name)
            if file_name in included_files:
                # TODO: remove counter when API works
                counter += 1

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
                    content = f.readlines()
                    content_str = "".join(content)
                    #if len(content) >= 10:
                    #    result = "".join(content[:10])
                    #    if len(result) >= 2000:
                    #        result = result[:2000]
                    #else:
                    #    result = "".join(content)
                    result = re.findall(r"^#{1,4}\s(.+)", content_str, re.MULTILINE)
                    # if there are no headings, use the raw text
                    if len(result) == 0 len(content) >= 10:
                        result = "".join(content[:10])
                        if len(result) >= 2000:
                            result = result[:2000]
                    elif len(content) < 10:
                        result = "".join(content)
                    else:
                        
                    print(file_name)
                    print(result)
                    file_dict["description"] = result

                # convert dict to json
                json_string = json.dumps(file_dict, indent=4)


                # make file path for json file
                json_path = normalised_path.split("/")[2:]

                # json_folder is where the jsons will we stored
                json_folder : str = "/".join(json_path[:-1])

                json_path = "/".join(json_path)
                json_path = json_path.replace(".md", ".json")

                ## write json files only if "json" argument provided
                #if if_json:
                #    # check if directory already exists; if not, create it
                #    if not os.path.isdir(f"obsidian-jsons/{json_folder}"):
                #        os.makedirs(f"obsidian-jsons/{json_folder}")
                #    # write the json string
                #    with open(f"obsidian-jsons/{json_path}", "w", encoding="utf-8") as j:
                #        j.write(json_string)

                # append files for tagscript file
                tagscript_title : str = title.replace(" ", "-").lower()
                after_github_path : str = urllib.parse.quote(json_path)
                tagscript_file_list.append("{=(" + tagscript_title + "):" + after_github_path + "}")
            

tagscript_file += "\n".join(tagscript_file_list)

# write tagscript
with open("tagscript", "w", encoding="utf-8") as t:
    t.write(tagscript_file)



