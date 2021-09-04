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

print(api_dev_key)
print(api_user_key)

#raise Exception

color : int = 3092790
tagscript_file : str = """
{=(b-obsidian):Obsidian/Obsidian}
{c:cembed https://pastebin.com/{{block}}}\n\n
"""
tagscript_file_list : list = []

#github_url : str = "https://raw.pastebin.com/"

included_files : list = ["Android app.md", "iOS app.md", "Mobile app beta.md", "Obsidian.md", "Obsidian Mobile.md", "How Obsidian stores data.md", "Third-party plugins.md", "Insider builds.md", "YAML front matter.md", "Catalyst license.md", "Commercial license.md", "Obsidian Publish.md", "Obsidian Sync.md", "Obsidian Unlimited.md", "Refund policy.md", "Add aliases to note.md", "Folding.md", "Format your notes.md", "Link to blocks.md", "Templates.md"] 


all_urls : dict = {}

paste_ids : list = []

for dirpath, dirnames, files in os.walk("./obsidian-docs/en/"):
    for file_name in files:
        if file_name.endswith(".md"):
            normalised_path = os.path.normpath(dirpath + "/" + file_name)
            url : str = "https://help.obsidian.md/"
            # URL
            split_path : list = normalised_path.split("/")[2:]
            unencoded_url_part : str = "/".join(split_path)
            url += urllib.parse.quote(unencoded_url_part)
            url = url.replace("%20", "+")
            if url == "https://help.obsidian.md/Obsidian/Index.md":
                url = url.replace("Obsidian/", "")
            url = url[:-3]
            all_urls[file_name[:-3]] = url

def replace_links(content_str : str) -> str:
    content_str = content_str
    link_result = re.compile(r"\[\[(.*?)(?=(?:\]\]|#|\|))(?:.+?)?\]\]", re.MULTILINE)
    for match in link_result.finditer(content_str):
        link_url : str = all_urls[match.group(1)]
        content_str = content_str.replace(match.group(0), f"[{match.group(1)}]({link_url})")
    return content_str


#print(all_urls)
counter : int = 0

for dirpath, dirnames, files in os.walk("./obsidian-docs/en/"):
    #print(f"Found directory: {dirnames}, located here:{dirpath}")
    for file_name in files:
        if file_name.endswith(".md"):
            normalised_path = os.path.normpath(dirpath + "/" + file_name)
            if file_name in included_files and counter < 1:
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
                url = url[:-3]
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
                    result = re.findall(r"^(#{1,4})\s(.+)", content_str, re.MULTILINE)
                    # if there are no headings, use the raw text
                    if len(result) == 0:
                        result = "".join(content[:10])
                        content_str = replace_links(content_str)
                        # convert highlights to bold
                        content_str = re.sub(r"==(.+?)==", r"**\1**", content_str)
                        # limit result to 10 lines
                        result = "\n".join(content_str.split("\n")[:10])
                    # if there are headings, replace them all with links to the headings
                    # on the Obsidian Publish help site
                    else:
                        result_headings : list = []
                        for el in result:
                            heading : str = el[0] + f" [{el[1]}]" + f"({url}/"
                            heading += "#" + urllib.parse.quote(el[1]).replace("%20", "+") + ")"
                            result_headings.append(heading)
                        result = "\n\n".join(result_headings)

                    print(file_name)
                    #print(normalised_path)
                    print(result)
                    file_dict["description"] = result

                # convert dict to json
                json_string = json.dumps(file_dict, indent=4)
                print(json_string)

                # make file path for json file
                #json_path = normalised_path.split("/")[2:]

                # json_folder is where the jsons will we stored
                #json_folder : str = "/".join(json_path[:-1])

                #json_path = "/".join(json_path)
                #json_path = json_path.replace(".md", ".json")

                ## write json files only if "json" argument provided
                #if if_json:
                #    # check if directory already exists; if not, create it
                #    if not os.path.isdir(f"obsidian-jsons/{json_folder}"):
                #        os.makedirs(f"obsidian-jsons/{json_folder}")
                #    # write the json string
                #    with open(f"obsidian-jsons/{json_path}", "w", encoding="utf-8") as j:
                #        j.write(json_string)

                data_to_post : dict = {'api_dev_key':api_dev_key, 'api_user_key':api_user_key, 'api_option':'paste', 'api_paste_code':json_string, 'api_paste_name':title, 'api_paste_format':'json', 'api_paste_private':0, 'api_paste_expire_date':'N'}

                # TODO: make the POST request to pastebin
                pastebin_id = requests.post(url="https://pastebin.com/api/api_post.php", data=data_to_post)
                pastebin_id = pastebin_id.text
                print(pastebin_id)

                paste_ids.append(pastebin_id)



                # append files for tagscript file
                tagscript_title : str = title.replace(" ", "-").lower()

                # TODO: This needs to be replaced with what the POST command returns
                #after_github_path : str = urllib.parse.quote(json_path)
                tagscript_file_list.append("{=(" + tagscript_title + "):" + str(pastebin_id) + "}")
            

tagscript_file += "\n".join(tagscript_file_list)

# write tagscript
with open("tagscript", "w", encoding="utf-8") as t:
    t.write(tagscript_file)

    

with open("paste_ids.py", "w", encoding="utf-8") as p:
    p.write("to_delete = " + str(paste_ids))
