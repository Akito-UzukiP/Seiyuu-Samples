import os
import requests
from bs4 import BeautifulSoup
import json
import re
# utf-8
urls = ["https://www.vims.co.jp/talent_profile.php"]


actors = []
for i, url in enumerate(urls):
    # Trust the site, no need to check the status code
    response = requests.get(url, verify=False)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    #print(soup)
    talent_boxes = soup.find_all("div", class_="talentBox")
    for i, talent_box in enumerate(talent_boxes):
        for a in talent_box.find_all("a"):
            actor = {}
            actor["name"] = a.text.replace("\u3000"," ").strip()
            if actor["name"] == "":
                continue
            actor["homepage"] = a["href"].replace("./", "https://www.vims.co.jp/")
            actor["sex"] = "Male" if i == 0 else "Female"
            actors.append(actor)
actors

import re
def get_voices(homepage:str):
    response = requests.get(homepage, verify=False)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    #print(soup)
    voices = []
    voice_samples = soup.findAll("ol", class_="voiceList")
    for voice_sample in voice_samples:
        for li in voice_sample.findAll("li"):
            a = li.find("a")
            if a is None:
                continue
            voice = {}
            voice["url"] = a["data-src"].replace("./", "https://www.vims.co.jp/")
            voice["name"] = voice["url"].split("/")[-1]
            voice["description"] = a.text
            voices.append(voice)
    return voices

# get_voices("https://www.vims.co.jp/talent_profile_detail.php?id=139")

import tqdm
pbar = tqdm.tqdm(actors)
for actor in pbar:
    actor["voices"] = get_voices(actor["homepage"])
    pbar.set_description(str(len(actor["voices"])))
actors

import json
with open("../jsons/vims.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)