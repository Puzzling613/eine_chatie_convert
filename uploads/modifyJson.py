import json


def modifyjson(title, characters, mainchara):  # title은 str, characters는 이름이 담긴 리스트
    r = open("./uploads/ChatInfoDefault.json", "r", encoding='utf-8-sig')
    json_dict = json.load(r)
    w = open("./uploads/ChatInfo.json", "w", encoding='utf-8-sig')
    json_dict["title"] = title
    for charaName in characters:
        json_dict["characters"].append({"name": charaName, "display_name": charaName, "profile_image": None})
    json_dict["scenes"] = {"name": "1", "sender": [mainchara]}
    w.write(json.dumps(json_dict, ensure_ascii=False, indent=True))
    # print(type(json_dict))
    w.close()
    r.close()

# modifyjson("제목",["chara"],"한소라")
