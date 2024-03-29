import os
import requests
from bs4 import BeautifulSoup
import json
import re
# utf-8
urls = ["https://mausu.net/talent/male/","https://mausu.net/talent/female/"]


actors = []
for i, url in enumerate(urls):
    # Trust the site, no need to check the status code
    response = requests.get(url, verify=False)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    ul = soup.find("ul", class_="actors-list")
    for a in ul.findAll("a"):
        actor = {}
        actor["name"] = a.find("span", class_ = "person-name").text.replace("\u3000"," ").strip()
        actor["homepage"] = a["href"]
        actor["sex"] = "Female" if "female" in url else "Male"
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
    response = requests.get(homepage, verify=False)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    print(soup)
    voices = []
    voice = {}
    for div in soup.find_all("a", class_="sample-voice"):
        voice = {}
        voice["url"] ="https://mausu.net" + div["href"]
        voice["name"] = voice["url"].split("/")[-1]
        voice["description"] = "サンプルボイス"
        voices.append(voice)
    return voices

#get_voices("https://mausu.net/talent/anzai-kazuhiro.html")

import tqdm
pbar = tqdm.tqdm(actors)
for actor in pbar:
    actor["voices"] = get_voices(actor["homepage"])
    pbar.set_description(str(len(actor["voices"])))
actors

import json
with open("../jsons/mausu.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)

import re
def get_voices(homepage:str):
    response = requests.get(homepage, verify=False)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    #print(soup)
    voices = []
    voice_samples = soup.findAll("li", class_="voiceTab")
    for voice_sample in voice_samples:
        for li in voice_sample.findAll("li"):
            voice = {}
            voice["url"] = "https://www.kenproduction.co.jp"+li.find("source")["src"]
            voice["name"] = voice["url"].split("/")[-1]
            voice["description"] = li.find("p").text
            voices.append(voice)
    return voices

#get_voices("https://www.kenproduction.co.jp/talent/151")

import tqdm
pbar = tqdm.tqdm(actors)
for actor in pbar:
    actor["voices"] = get_voices(actor["homepage"])
    pbar.set_description(str(len(actor["voices"])))
actors