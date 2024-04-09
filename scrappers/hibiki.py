import os
import requests
from bs4 import BeautifulSoup
import json
import re
# utf-8
urls = ["https://hibiki-cast.jp/hibiki_f/", "https://hibiki-cast.jp/hibiki_m/"]
actors = []
for url in urls:
    response = requests.get(url)# html lang="ja",
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    for a in soup.find_all("a", href=re.compile("^https://hibiki-cast.jp/hibiki_(.*)/(.*)")):
        homepage = a["href"]
        name = a.find("p").text.strip()
        actors.append({"name": name, "homepage": homepage, "sex":"Male" if not "m" in url else "Female"})
actors
# name, homepage, sex

import re
import json
def get_voices(homepage:str):
    response = requests.get(homepage)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    voices = []
    #print(soup.find_all("source"))
    for src in soup.find_all("source"):
        url = src["src"]
        name = url.split("/")[-1]
        description = ""
        voices.append({"url": url, "name": name, "description": description})
# url, name, description
    return voices

#get_voices("https://hibiki-cast.jp/hibiki_f/mimori_suzuko/")
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
with open("../jsons/hibiki.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)