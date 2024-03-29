import os
import requests
from bs4 import BeautifulSoup
import json
import re
# utf-8
urls = ["https://osawa-inc.co.jp/men/","https://osawa-inc.co.jp/women/"]


actors = []
for i, url in enumerate(urls):
    # Trust the site, no need to check the status code
    response = requests.get(url, verify=False)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    div = soup.find("div", class_="index0")
    for a in div.findAll("a"):
        actor = {}
        if not a.has_attr("title"):
            continue
        actor["name"] = a["title"].replace("\u3000"," ").strip()
        actor["homepage"] = a["href"]
        actor["sex"] = "Female" if "women" in url else "Male"
        actors.append(actor)
        # for a in table.find_all("a"):
        #     actor = {}       
        #     actor["name"] = a.text.replace("\u3000"," ").strip()
        #     actor["homepage"] = a["href"]
        #     actor["sex"] = "Male" if url == urls[1] else "Female"
        #     actors.append(actor)
actors

import re
import base64
def get_voices(homepage:str):
    response = requests.get(homepage, verify=False)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    #print(soup)
    voices = []
    #print(soup)
    voice_player_divs = soup.findAll("div", class_="mjp-s-wrapper s-graphic unsel-mjp")
    #print(voice_player_divs)
    if len(voice_player_divs) == 0:
        return voices
    found_voices = []
    for voice_player_div in voice_player_divs:
        script = voice_player_div.next_sibling.next_sibling.text
        
        # MP3jPLAYLISTS.inline_0 = [
        # 	{ name: "サンプル1", formats: ["mp3"], mp3: "aHR0cDovL29zYXdhLWluYy5jby5qcC93b3JkcHJlc3Mvd3AtY29udGVudC90aGVtZXMvb3Nhd2EvdGFsZW50L3dvbWVuL0Fva2lOYW5hL05Z44Kv44Oq44K544Oe44K5Lm1wMw==", counterpart:"", artist: "", image: "", imgurl: "" }
        # ];
        found_voice = re.findall(r'name: "(.*?)", formats: \["mp3"\], mp3: "(.*?)"', script)
        found_voices.extend(found_voice)
    # try:
    #     script = soup.find("div", class_="voicewrap clearfix").find("script").text
    # except:
    #     print(homepage)
    #     return voices
    # #print(script)
    # found_voices = re.findall(r'title:"(.*?)",\s*mp3:"(.*?)"', script)

    for description, url in found_voices: #<p class="valign_m">
        voice = {}
        url = base64.b64decode(url).decode("utf-8")
        voice["url"] = url.strip()
        if voice["url"] == "":
            continue
        voice["name"] = voice["url"].split("/")[-1]
        voice["description"] = description.strip().replace("&nbsp;","")
        voices.append(voice)
    return voices

#get_voices("https://osawa-inc.co.jp/women/aokinana/")

import tqdm
pbar = tqdm.tqdm(actors)
for actor in pbar:
    actor["voices"] = get_voices(actor["homepage"])
    pbar.set_description(str(len(actor["voices"])))
actors

import json
with open("../jsons/osawa-inc.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)