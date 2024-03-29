import os
import requests
from bs4 import BeautifulSoup
import json
import re
# https://www.wonder-space.net/
# utf-8
urls = ["https://www.artsvision.co.jp/talent_female/","https://www.artsvision.co.jp/talent_male/"]
actors = []
for url in urls:
    # Trust the site, no need to check the status code
    response = requests.get(url, verify=False)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    for div in soup.findAll("div", class_="list_box"):
        actor = {}
        actor["name"] = div.find("p").text
        actor["homepage"] = div.find("a")["href"]
        actor["sex"] = "Female" if url == urls[0] else "Male"
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
    #print(soup)
    voices = []
    # 东西在一个<script>里面 结构如下：
					# 				{
					# 	title:"セリフ2",
					# 	mp3:"https://www.artsvision.co.jp/wp-content/uploads/2015/12/03asakura_azumi_05.mp3"
					# }
    script = soup.find("div", id="voice_data").find("script").text
    #print(script)
    found_voices = re.findall(r'title:"(.*?)",\s*mp3:"(.*?)"', script)

    for description, url in found_voices: #<p class="valign_m">
        voice = {}
        voice["url"] = url.strip()
        voice["name"] = voice["url"].split("/")[-1]
        voice["description"] = description.strip()
        voices.append(voice)
    return voices

#get_voices("https://www.artsvision.co.jp/talent/14219/")

import tqdm
for actor in tqdm.tqdm(actors):
    actor["voices"] = get_voices(actor["homepage"])
actors

import json
with open("../jsons/artsvision.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)