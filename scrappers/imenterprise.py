import os
import requests
from bs4 import BeautifulSoup
import json
import re
# https://www.wonder-space.net/
# utf-8
urls = ["https://www.imenterprise.jp/profile_list.php"]
actors = []
for url in urls:
    response = requests.get(url)# html lang="ja",
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    rows = soup.findAll("div", class_="row")
    for row in rows:
        females = row.findAll("div", class_="card xs-3 text-center border-danger2-profile")
        males = row.findAll("div", class_="card xs-3 text-center border-primary2-profile")
        for va in males:
            a = va.find("a")
            actor = {}
            actor["name"] = a.text.replace("\u3000"," ").strip()
            actor["name"] = re.sub(r"\s+", " ", actor["name"])
            actor["homepage"] = a["href"].replace("./", "https://www.imenterprise.jp/")
            actor["sex"] = "Male"
            actors.append(actor)
        for va in females:
            a = va.find("a")
            actor = {}
            actor["name"] = a.text.replace("\u3000"," ").strip()
            actor["name"] = re.sub(r"\s+", " ", actor["name"])
            actor["homepage"] = a["href"].replace("./", "https://www.imenterprise.jp/")
            actor["sex"] = "Female"
            actors.append(actor)
        # for a in table.find_all("a"):
        #     actor = {}       
        #     actor["name"] = a.text.replace("\u3000"," ").strip()
        #     actor["homepage"] = a["href"]
        #     actor["sex"] = "Male" if url == urls[1] else "Female"
        #     actors.append(actor)
actors


import re
def get_voices(homepage:str):
    response = requests.get(homepage)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    #print(soup)
    voices = []
    ol = soup.find("ol", class_="voiceList")
    for i, li in enumerate(ol.find_all("li")): #<p class="valign_m">
        a = li.find("a")
        voice = {}
        voice["url"] = a.get("data-src").replace("./", "https://www.imenterprise.jp/")
        #print(a.text)
        voice["name"] = voice["url"].split("/")[-1]
        voice["description"] = a.text
        voices.append(voice)
    return voices

#get_voices("https://www.imenterprise.jp/profile.php?id=94")

import tqdm
for actor in tqdm.tqdm(actors):
    actor["voices"] = get_voices(actor["homepage"])
actors


import json
with open("../jsons/imenterprise.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)

