import os
import requests
from bs4 import BeautifulSoup
import json
import re
# utf-8
urls = ["http://www.pro-fit.co.jp/talent.html"]


actors = []


for i, url in enumerate(urls):
    # Trust the site, no need to check the status code
    response = requests.get(url, verify=False)
    content = response.content.decode("shift_jis", "ignore").encode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    #print(soup)
    imgs = soup.find_all("img", width="145")
    #寻找所有的div, transfer_f和transfer_m应当和img的enmuerate一一对应
    divs = [i for i in soup.findAll("div") if i.get("class") == ["transfer_f"] or i.get("class") == ["transfer_m"]]

    for i, img in enumerate(imgs):
        actor = {}
        actor["name"] = img["alt"]
        actor["homepage"] = "http://www.pro-fit.co.jp/" + img.parent["href"]
        actor["sex"] = "Female" if divs[i].get("class") == ["transfer_f"] else "Male"
        actors.append(actor)
actors

import re
def get_voices(homepage:str):
    js_url = "http://www.pro-fit.co.jp/js/jquery.iwish_" + homepage.split("/")[-1].split(".")[0].split("_")[-1] + ".js"
    response = requests.get(js_url, verify=False)
    content = response.content.decode("euc-jp", "ignore").encode("utf-8")
    # 看起来得试图下载js

    soup = BeautifulSoup(content, "html.parser")
    voices = []

    # $("audio").iWish({audioSource: "voice/v25_ishiya", autoPlay: false}); --> http://www.pro-fit.co.jp/voice/v25_ishiya.mp3
    voice_sample = re.search(r"audioSource: \"(.*?)\"", str(soup)).group(1)
    voice = {}
    voice["url"] = "http://www.pro-fit.co.jp/" + voice_sample + ".mp3"
    voice["name"] = voice["url"].split("/")[-1]
    voice["description"] = "ボイスサンプル"
    voices.append(voice)
    return voices

#get_voices("http://www.pro-fit.co.jp/talent_manaka.html")
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
with open("../jsons/pro-fit.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)