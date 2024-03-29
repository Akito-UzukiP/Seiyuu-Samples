import os
import requests
from bs4 import BeautifulSoup
import json
import re
# utf-8
urls_ = ["https://www.aoni.co.jp/actor/","https://www.aoni.co.jp/actress/"]
subfix = ["index.html","ka.html","sa.html","ta.html","na.html","ha.html","ma.html","ya.html","ra.html","wa.html"]
urls = []
for url in urls_:
    for sub in subfix:
        urls.append(url+sub)

actors = []
for i, url in enumerate(urls):
    # Trust the site, no need to check the status code
    response = requests.get(url, verify=False)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    div = soup.find("div", class_="catelistwrap")
    for a in div.findAll("a"):
        actor = {}
        actor["name"] = a.text.replace("\u3000"," ").strip()
        actor["homepage"] = a["href"]
        actor["sex"] = "Female" if "actress" in url else "Male"
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
    try:
        script = soup.find("div", class_="voicewrap clearfix").find("script").text
    except:
        print(homepage)
        return voices
    #print(script)
    found_voices = re.findall(r'title:"(.*?)",\s*mp3:"(.*?)"', script)

    for description, url in found_voices: #<p class="valign_m">
        voice = {}
        voice["url"] = url.strip()
        if voice["url"] == "":
            continue
        voice["name"] = voice["url"].split("/")[-1]
        voice["description"] = description.strip().replace("&nbsp;","")
        voices.append(voice)
    return voices

#get_voices("https://www.aoni.co.jp/search/yomiya-hina.html")

import tqdm
for actor in tqdm.tqdm(actors):
    actor["voices"] = get_voices(actor["homepage"])
actors


import json
with open("../jsons/aoni.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)