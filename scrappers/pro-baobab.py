import os
import requests
from bs4 import BeautifulSoup
import json
import re
# utf-8
urls = ["http://pro-baobab.jp/men-all.html", "http://pro-baobab.jp/women-all.html"]
actors = []
for url in urls:
    response = requests.get(url)# html lang="ja",
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    fonts =[i.text for i in soup.find_all("font", size="2") if i.text != "\u3000"]
    print(fonts)
    actor_homepages = ["http://pro-baobab.jp/" + i["href"] for i in soup.find_all("a", href=re.compile("(ladies|men)/(.*)/index.html"))]
    for (font, homepage) in zip(fonts, actor_homepages):
        actors.append({"name": font, "homepage": homepage, "sex":"Male" if not "women" in url else "Female"})
actors
# name, homepage, sex
import re
import json
def get_voices(homepage:str):
    response = requests.get(homepage)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    voices = []
    for a in soup.find_all("a", href=re.compile("(.*).mp3")):
        url = "/".join(homepage.split("/")[:-1]) + "/" + a["href"]
        name = a["href"]
        desc = a.find("img")["alt"].strip()
        voices.append({"url":url, "name":name, "description":desc})
# url, name, description
    return voices

#get_voices("http://pro-baobab.jp/ladies/ichijo_m/index.html")
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
with open("../jsons/pro-baobab.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)