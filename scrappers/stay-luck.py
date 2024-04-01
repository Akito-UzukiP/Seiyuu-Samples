import os
import requests
from bs4 import BeautifulSoup
import json
import re
# utf-8
urls = ["https://stay-luck.com/talent/?gender%5B%5D=dansei&birthplace=&s=", "https://stay-luck.com/talent/?gender%5B%5D=jyosei&birthplace=&s="]


actors = []


for i, url in enumerate(urls):
    # Trust the site, no need to check the status code
    response = requests.get(url, verify=False)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")

    #print(soup)
    imgs = soup.find_all("img",id = "featured_img")
    for i, img in enumerate(imgs):
        a = img.find_parent("a")
        actor = {}
        actor["name"] = img["alt"]
        actor["homepage"] = a["href"]
        actor["sex"] = "Female" if i == 1 else "Male"
        actors.append(actor)
actors

import json
with open("../jsons/stay-luck.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)