import os
import requests
from bs4 import BeautifulSoup
import json
import re
# utf-8
urls = ["https://amuleto.jp/talents"]
actors = []
for url in urls:
    response = requests.get(url)# html lang="ja",
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    uls = soup.find("section", id="talents").find_all("ul")[:2]
    for i, ul in enumerate(uls):
        a_s = ul.find_all("a", href=re.compile(r"^https://amuleto.jp/talents/"))
        for a in a_s:
            homepage = a["href"]
            name = a.find("div",{ "class":"info"}).find("p").text.replace("\u3000", " ")
            actors.append({"name": name, "homepage": homepage, "sex":"Male" if i == 1 else "Female"})
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
    #descriptions = 
    script = [i for i in soup.find_all("script") if ".mp3" in str(i) or ".wav" in str(i)][0]
    # wav or mp3
    files = re.findall(r"https:.*\.(?:wav|mp3)", str(script))
    players = soup.find_all("div", {"class":"jp-jplayer"})
    for i, player in enumerate(players):
        description = player.parent.previous_sibling.previous_sibling.text.strip()
        url = files[i]
        name = url.split("/")[-1]
        voices.append({"url": url, "name": name, "description": description})
    
# url, name, description
    return voices
#get_voices("https://amuleto.jp/talents/akesakasatomi.html")
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
with open("../jsons/amuleto.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)