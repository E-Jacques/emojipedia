import requests
from json import dumps
from typing import List


def getData(pathLs: List[str]):
    emotes: List[dict] = []
    idx = 0
    for path in pathLs:
        print(path)
        data = requests.get(path).text
        # print(data)
        emoteList = data.split('<ul class="emoji-list">')[1].split("</ul>")[0]
        ls = emoteList.split("<li>")
        for e in ls:
            if e == "":
                continue
            try:
                idx += 1
                o = {
                    "id": idx,
                    "emote": e.split('<span class="emoji">')[1].split("</span>")[0],
                    "keywords": [e.split("</span> ")[1].split("</a>")[0]]
                }
                emotes.append(o)
            except IndexError:
                print(e)

    print(emotes)
    json = dumps(emotes, ensure_ascii=False)

    with open("./data.json", "w") as f:
        f.write(json)


if __name__ == "__main__":
    getData(["https://emojipedia.org/people/", "https://emojipedia.org/nature/", "https://emojipedia.org/food-drink/", "https://emojipedia.org/activity/",
            "https://emojipedia.org/travel-places/", "https://emojipedia.org/objects/", "https://emojipedia.org/symbols/", "https://emojipedia.org/flags/"])
