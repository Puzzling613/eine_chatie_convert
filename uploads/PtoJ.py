# prompt.txt와 ChatInfo.json 필요
import json
import uuid

"""
class UUIDEncoder(json.JSONEncoder): 
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)
"""


class Character:
    def __init__(self, id, name, display_name, profile_image, status_message):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.profile_image = profile_image
        self.status_message = status_message

    def general(self):
        return {"id": self.id, "name": self.name, "display_name": self.display_name,
                "status_message": self.status_message, "profile_image": self.profile_image}

    def char(self):
        return {"id": self.id, "name": self.name, "display_name": self.display_name,
                "status_message": self.status_message, "profile_image": self.profile_image, "is_pov": False}

    def user(self):
        return {"id": self.id, "name": self.name, "display_name": self.display_name,
                "status_message": self.status_message, "profile_image": self.profile_image, "is_pov": True}


class Scene:
    def __init__(self, id, name, sender_ids, items):
        self.id = id
        self.name = name
        self.sender_ids = sender_ids
        self.items = items

    def scene(self):
        return {"id": self.id, "name": self.name, "sender_ids": self.sender_ids, "items": self.items}


class ChatItem:
    def __init__(self, id, char_id, iobject):
        self.id = id
        self.char_id = char_id
        self.iobject = iobject

    def effect(self):
        rdict = {"id": self.id, "character_id": self.char_id, "object_type": "effect", "object": self.iobject}
        return {key: value for key, value in rdict.items() if value is not None}

    def text(self):
        rdict = {"id": self.id, "character_id": self.char_id, "object_type": "text", "object": self.iobject}
        return {key: value for key, value in rdict.items() if value is not None}


class Image:
    def __init__(self, key, attachment_type, attachment):
        self.key = key
        self.attachment_type = attachment_type
        self.attachment = attachment

    def imagine(self):
        return {"key": self.key, "attachment_type": self.attachment_type, "attachment_format": "image",
                "attachment": self.attachment}


class Attachment:
    def __init__(self, content_type, url, original_filename, width, height, checksum):
        self.content_type = content_type
        self.url = url
        self.original_filename = original_filename
        self.width = width
        self.height = height
        self.checksum = checksum

    def attach(self):
        rdict = {"content_type": self.content_type, "url": self.url, "original_filename": self.original_filename,
                 "width": self.width, "hegiht": self.height, "checksum": self.checksum}
        return {key: value for key, value in rdict.items() if value is not None}


class Object:
    def __init__(self, name):
        self.name = name

    def init(self):
        return {"name": self.name}

    def text(self, text):
        return {"text": text}

    def option(self, options):
        return {"name": self.name, "options": options}


class Options:
    def __init__(self, color, display_name_color, bubble_color, text_color):
        self.color = color
        self.display_name_color = display_name_color
        self.bubble_color = bubble_color
        self.text_color = text_color

    def image(self, image):
        rdict = {"color": self.color, "display_name_color": self.display_name_color, "image": image,
                "bubble_color": self.bubble_color, "text_color": self.text_color}
        return {key: value for key, value in rdict.items() if value is not None}

    # prompt to chatie


def ctoj(prompt, chatinfo):  # prompt = "prompt.txt", chatinfo = "ChatInfo.json"
    with open(chatinfo, "r", encoding='utf-8-sig') as info:
        info_dict = json.load(info)
    name = info_dict.get("title")  # 제목
    characters = []  # 캐릭터
    for character in info_dict.get("characters"):
        if character.get("name") == "전지적":
            characters.append(
                Character(str(0), character.get("name"), character.get("display_name"), character.get("profile_image"),
                          "").general())
        else:
            characters.append(Character(str(uuid.uuid1()), character.get("name"), character.get("display_name"),
                                        character.get("profile_image"), "").char())

    scenes = []
    view_type = "CHAT"
    extra = {}
    items = []
    clearchat = ChatItem(str(uuid.uuid1()), None, Object("CLEAR_CHATS").init()).effect()  # clearchat 아이템
    items.append(clearchat)
    p = open(prompt, "r")
    line = None
    teller = None
    line = p.readline()
    while line != "":
        if line[0] == "=":  # line != "" and
            sender_ids = []
            sender_name = info_dict.get("scenes")["sender"]
            # print("출력:",sender_name) #여기부터 다시
            for character in characters:
                if character["name"] in sender_name: sender_ids.append(character["id"])
            scene = Scene(str(uuid.uuid1()), "1", sender_ids, items).scene()
            scenes.append(scene)
            items = [clearchat]
            line = p.readline()
            continue

        if line[:1] == "*":
            teller = "전지적"
        else:
            for chara in characters:  # characters 안에 character 객체
                if line[:len(chara["name"]) + 1] == chara["name"] + ":":  # 캐릭터 이름이 세글자가 아니라면
                    teller = chara["name"]
                    teller_id = chara["id"]

        if teller == "전지적":
            if line[0] == "*" and line[-2] != "*":
                items.append(ChatItem(str(uuid.uuid1()), "0", Object(None).text(line[1:len(line) - 1])).text())
            elif line[0] != "*" and line[-2] == "*":
                items.append(ChatItem(str(uuid.uuid1()), "0", Object(None).text(line[0:len(line) - 2])).text())
            elif line[0] == "*" and line[-2] == "*":
                items.append(ChatItem(str(uuid.uuid1()), "0", Object(None).text(line[1:len(line) - 2])).text())
            else:
                items.append(ChatItem(str(uuid.uuid1()), "0", Object(None).text(line[0:len(line) - 1])).text())
        else:
            if line[0:len(teller)] == teller:
                items.append(ChatItem(str(uuid.uuid1()), teller_id,
                                      Object(None).text(line[len(teller) + 1:len(line) - 1])).text())
            else:
                items.append(ChatItem(str(uuid.uuid1()), teller_id, Object(None).text(line[0:len(line) - 1])).text())

        line = p.readline()

    chatie_dict = {"id": str(uuid.uuid1()), "name": name, "characters": characters, "view_type": view_type,
                   "scenes": scenes, "extra": extra}
    p.close()

    # dict to json
    with open("./uploads/chatie.json", "w", encoding='UTF-8-sig') as f:
        f.write(json.dumps(chatie_dict, ensure_ascii=False, indent=True))  # cls=UUIDEncoder ->uuid json serialize 안 될 때

# ctoj("./uploads/prompt.txt","./uploads/ChatInfo.json")
