import os
import requests
from bs4 import BeautifulSoup
import json
import re
# utf-8
urls = ["https://kenyu-office.com/shozoku_man/","https://kenyu-office.com/jyun_men/", "https://kenyu-office.com/azukari_men/","https://kenyu-office.com/shozoku_woman/", "https://kenyu-office.com/jyun_women/", "https://kenyu-office.com/azukari_women/" ]


actors = []

for i, url in enumerate(urls):
    # Trust the site, no need to check the status code
    response = requests.get(url, verify=False)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")

    #print(soup)
    ul = soup.find("ul", class_="display-posts-listing")
    a_s = ul.findAll("a", class_="title")
    for a in a_s:
        actor = {}
        actor["name"] = a.text.split("：")[0]
        actor["homepage"] = a["href"]
        actor["sex"] = "Female" if "woman" in url or "women" in url else "Male"
        actors.append(actor)
actors

import re
import json
def get_voices(homepage:str):
    response = requests.get(homepage)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    voices = []
    voice_script = soup.find("script", class_="wp-playlist-script").text
    voice_json = json.loads(voice_script)
    #print(json.dumps(voice_json, indent=2, ensure_ascii=False))
    # ["tracks"] --> "type"="audio/mpeg" 获取: title, src

    for voice_sample in voice_json["tracks"]:
        voice = {}
        voice["url"] = voice_sample["src"]
        voice["name"] = voice_sample["src"].split("/")[-1]
        voice["description"] = voice_sample["title"]
        # voice["url"] = voice_sample.find("a")["href"]
        # voice["name"] = voice_sample["src"].split("/")[-1]
        # voice["description"] = voice_sample.find("span").text.strip()
        voices.append(voice)
    return voices

#get_voices("https://kenyu-office.com/nozomi/")
import tqdm
pbar = tqdm.tqdm(actors)
for actor in pbar:
    try:
        actor["voices"] = get_voices(actor["homepage"])
    except:
        actor["voices"] = []
    pbar.set_description(str(len(actor["voices"])))
actors

import json
with open("../jsons/kenyu-office.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)