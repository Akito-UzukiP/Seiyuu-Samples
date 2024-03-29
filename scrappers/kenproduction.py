import os
import requests
from bs4 import BeautifulSoup
import json
import re
# utf-8
urls = ["https://www.kenproduction.co.jp/talent?search_voice=0&search_talent_type_id%5B%5D=2&search_talent_type_id%5B%5D=4&search_keyword=&search_prefecture_id=","https://www.kenproduction.co.jp/talent?search_voice=0&search_talent_type_id%5B%5D=1&search_talent_type_id%5B%5D=3&search_keyword=&search_prefecture_id="]


actors = []
for i, url in enumerate(urls):
    # Trust the site, no need to check the status code
    response = requests.get(url, verify=False)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    #print(soup)
    ul = soup.find("div", class_="search--talent--result--inner inner")
    print(len(ul.findAll("a")))
    for a in ul.findAll("a"):
        actor = {}
        actor["name"] = a.find("span").text.replace("\u3000"," ").strip()
        actor["homepage"] = a["href"]
        actor["sex"] = "Female" if i == 1 else "Male"
        actors.append(actor)
        # for a in table.find_all("a"):
        #     actor = {}       
        #     actor["name"] = a.text.replace("\u3000"," ").strip()
        #     actor["homepage"] = a["href"]
        #     actor["sex"] = "Male" if url == urls[1] else "Female"
        #     actors.append(actor)


import json
with open("../jsons/kenproduction.json", "w",encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=2)

all_voices = []
for actor in actors:
    for voice in actor["voices"]:
        all_voices.append(voice)
len(all_voices)