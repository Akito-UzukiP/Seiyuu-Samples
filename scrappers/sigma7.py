import os
import requests
from bs4 import BeautifulSoup
import json
import re
# utf-8
urls = ["https://sigma7.co.jp/"]


actors = []


for i, url in enumerate(urls):
    # Trust the site, no need to check the status code
    response = requests.get(url, verify=False)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")

    #print(soup)
    divs = soup.findAll("div",class_="actorIndex__ImageWrapper-sc-13itab7-0 iYOgKY")

    for i, div in enumerate(divs):
        actor_hps = div.find_all("a")
        for actor_hp in actor_hps:
            actor = {}
            actor["name"] = actor_hp.text
            actor["homepage"] = "https://sigma7.co.jp" + actor_hp["href"]
            actor["sex"] = "Female" if i % 2 == 1 else "Male"
            actors.append(actor)
actors

import re
import json
def get_voices(homepage:str):
    # https://sigma7.co.jp/page-data/actors/takagi_tatsuya/page-data.json <-- https://sigma7.co.jp/actors/takagi_tatsuya
    js_url = homepage.replace("https://sigma7.co.jp", "https://sigma7.co.jp/page-data") + "/page-data.json"
    response = requests.get(js_url, verify=False)
    content = response.content
    # 看起来得试图下载js

    page_data = json.loads(content)
    voices = []

    # result->data->actor->voices->[cnt]->[filename, label]
    for voice_sample in page_data["result"]["data"]["actor"]["voices"]:
        voice = {}
        filename = voice_sample["filename"]
        filename = filename.replace("/", "%2F")
        url = "https://firebasestorage.googleapis.com/v0/b/sigma7-hp-v2.appspot.com/o/" + filename + "?alt=media"
        voice["url"] = url
        voice["name"] = url.split("/")[-1]
        voice["description"] = voice_sample["label"]
        voices.append(voice)
    return voices

# get_voices("https://sigma7.co.jp/actors/takagi_tatsuya")
#看起来得试图下载js
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
with open("../jsons/sigma7.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)