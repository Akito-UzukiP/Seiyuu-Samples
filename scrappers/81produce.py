import os
import requests
from bs4 import BeautifulSoup
import json
import re
# utf-8
urls = ["http://www.81produce.co.jp/actor/woman.html","https://www.81produce.co.jp/actor/men.html"]
actors = []
for url in urls:
    response = requests.get(url)# html lang="ja",
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table", class_="table01")
    for a in table.find_all("a"):
        actor = {}       
        actor["name"] = a.text.replace("\u3000"," ").strip()
        actor["homepage"] = a["href"]
        actor["sex"] = "Male" if url == urls[1] else "Female"
        actors.append(actor)


import re
def get_voices(homepage:str):
    response = requests.get(homepage)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    #print(soup)

    #print(soup)
    # 用re找到所有 www开头,.mp3结尾的链接
    voices_url = re.findall(r"www.*?\.mp3", content)
    voices = []
    for i, a in enumerate(soup.find_all("p", class_="valign_m")): #<p class="valign_m">
        voice = {}
        voice["url"] = voices_url[i]
        #print(a.text)
        voice["name"] = voice["url"].split("/")[-1]
        voice["description"] = a.parent.parent.find("p", class_="valign_m").text.strip()
        voices.append(voice)
    return voices

#get_voices("https://www.81produce.co.jp/dcms_plusdb/index.php/item?cell003=%E3%82%8F%E8%A1%8C&cell029=%E7%94%B7%E6%80%A7&keyword=&cell028=&cell004=&name=%E8%8B%A5%E6%9E%97%E3%80%80%E4%BD%91&id=133&label=1")

import tqdm
for actor in tqdm.tqdm(actors):
    actor["voices"] = get_voices(actor["homepage"])

import json
with open("../jsons/81produce.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)
