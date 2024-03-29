import os
import requests
from bs4 import BeautifulSoup
import json
import re

# Actor Json属性:
# 1. 名字 2. 性别 3. 录音文件 4. homepage
# Bungakuza.com
url_male = "https://www.bungakuza.com/member/index.html"
url_female = "https://www.bungakuza.com/member/engibu2.html"
urls = [url_female,url_male]
actors = []
for url in urls:
    response = requests.get(url)# html lang="ja",
    content = response.content.decode("shift_jis", errors="ignore").encode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    #print(soup)
    #print(soup.find("table", border="0", width="700", cellpadding="0"))
    table = soup.find("table", border="0", width="700", cellpadding="0")
    for a in table.find_all("a"):
        actor = {}
        actor["name"] = a.text
        actor["homepage"] = "https://www.bungakuza.com/member/" + a["href"]
        actor["sex"] = "female" if url == url_female else "male"
        actors.append(actor)


def get_voices(homepage:str):
    response = requests.get(homepage)
    content = response.content.decode("shift_jis", errors="ignore").encode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    #print(soup)
    voices = []
    td = soup.find("td", valign="top", align="right")
    #print(td)

    voice_names = td.text.split("↓")[-1].split("\n")
    has_voice_name = len(voice_names) > 1
    for i, a in enumerate(td.find_all("a")):
        voice = {}
        voice["url"] = a["href"]
        #print(a.text)
        voice["name"] = a["href"].split("/")[-1]
        voice["description"] = voice_names[i] if has_voice_name else ""
        voices.append(voice)
    return voices

#get_voices("https://www.bungakuza.com/member/prof/komai-kensuke.htm")

import tqdm
for actor in tqdm.tqdm(actors):
    actor["voices"] = get_voices(actor["homepage"])


import json
with open("bungakuza.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)
