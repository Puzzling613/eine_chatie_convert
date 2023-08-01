import json
import uuid
import io
import re

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
    def __init__(self, id, name, items, sender_ids):
        self.id = id
        self.name = name
        self.items = items
        self.sender_ids = sender_ids

    def scene(self):
        return {"id": self.id, "name": self.name, "items": self.items, "sender_ids": self.sender_ids}


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

def text2json(p):  # p는 str
    line = None
    teller = None
    characters = []  # 캐릭터
    character_names = []
    scenes = []
    view_type = "CHAT"
    extra = {}
    items = []
    clearchat = ChatItem(str(uuid.uuid1()), None, Object("CLEAR_CHATS").init()).effect()  # clearchat 아이템
    items.append(clearchat)

    linelist = p.split("\n") # 1차적으로 띄어쓰기 기준
    for line in linelist:
        # 장면 전환
        if line[0] == "=":
            scene = Scene(str(uuid.uuid1()), "1", items, ["0"]).scene()
            scenes.append(scene)
            items = [clearchat]
            continue
        # 파싱
        split_line = line.split(": ")
        if len(split_line) > 1 and split_line[0] not in character_names: #캐릭터 추가
            character_names.append(split_line[0])
            characters.append(Character(str(uuid.uuid1()), split_line[0], split_line[0], None, "").char())

        if line[:1] == "*":
            teller = "전지적"
        else:
            for chara in characters:  # characters 안에 character 객체
                if line[:len(chara["name"]) + 1] == chara["name"] + ":":
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
                if line[-1] == "." and line[-2] != ".": # 마침표
                    items.append(ChatItem(str(uuid.uuid1()), teller_id, Object(None).text(line[len(teller) + 1:len(line) - 1 ])).text())
                #elif line[-1] == "\"":
                    #items.append(ChatItem(str(uuid.uuid1()), teller_id, Object(None).text(line[len(teller) + 1:len(line) - 1 ])).text())
                else:
                    items.append(ChatItem(str(uuid.uuid1()), teller_id, Object(None).text(line[len(teller) + 1:len(line)])).text())
            else:
                if line[-1] == "." and line[-2] != ".": # 마침표
                    items.append(ChatItem(str(uuid.uuid1()), teller_id, Object(None).text(line[0:len(line) - 1])).text())
                #elif line[-1] == "\"":
                    #items.append(ChatItem(str(uuid.uuid1()), teller_id, Object(None).text(line[0:len(line) - 1])).text())
                else:
                    items.append(ChatItem(str(uuid.uuid1()), teller_id, Object(None).text(line[0:len(line)])).text())

    chatie_dict = {"id": str(uuid.uuid1()), "name": "InsetTitle", "characters": characters, "view_type": view_type,
                   "scenes": scenes, "extra": extra}

    # dict to json
    in_memory_file = io.StringIO()
    in_memory_file.write(json.dumps(chatie_dict, ensure_ascii=False, indent=True))
    in_memory_file.seek(0)
    return in_memory_file # .read()


# message.json to text

def json2text(messages): # message는 dictionary 가진 list
    conversation_finder = re.compile('^".*?"')
    action_finder = re.compile('^\*.*?\*')
    before_conv_finder = re.compile('^(.*?)\s*(?=")')
    before_action_finder = re.compile('^(.*?)\s*(?=\*)')
    text = ""
    ai_teller = messages[0]["name"]
    user_teller = messages[1]["name"]


    for message in messages: # message는 dictionary
        enter_sentence = message["message"].split("\n")
        teller = message["name"]
        # if teller not in characters:
            # characters.append(teller)
        for sentence in enter_sentence:
            sentence = sentence.replace('\"*','\"').replace('*\"','\"')
            conv_or_action = 0 # 0이면 conv, 1이면 action
            while sentence != "":
                if sentence != "" and sentence[0] == " ": sentence = sentence[1:] # 첫 공백 제거

                if action_finder.match(sentence) is not None: # 지문
                    text += action_finder.match(sentence).group()
                    text += "\n"
                    sentence = re.sub(action_finder,"",sentence)
                    conv_or_action = 0
                    continue
                elif conversation_finder.match(sentence) is not None: # 대사
                    text += teller + ": " + conversation_finder.match(sentence).group()[1:-1]
                    text += "\n"
                    sentence = re.sub(conversation_finder,"",sentence)
                    conv_or_action = 1
                    continue
                else: # 안 감싸진 것
                    if teller == user_teller:
                        if before_action_finder.match(sentence) is not None: # 뒤에 지문 있을 때
                            text += user_teller+ ": " + before_action_finder.match(sentence).group() + "\n"
                            sentence = re.sub(before_action_finder,"",sentence)
                            conv_or_action = 1
                            if before_action_finder.match(sentence).group() == "": #지문 처리(앞에만 *있을 경우)
                                text += sentence + "\n"
                                conv_or_action = 0
                                break
                            else: continue
                        else:
                            text += user_teller + ": " + sentence + "\n"
                            conv_or_action = 1
                            break
                    elif teller == ai_teller: # ai
                        if before_conv_finder.match(sentence) is not None: #뒤에 대사 있을 때 지문 처리
                            text += "*"+before_conv_finder.match(sentence).group()+"*" + "\n"
                            sentence = re.sub(before_conv_finder,"",sentence)
                            conv_or_action = 0
                            continue
                        elif before_action_finder.match(sentence) is not None: #뒤에 지문 있을 때 대사 처리
                            text += ai_teller + ": " + before_action_finder.match(sentence).group() + "\n"
                            sentence = re.sub(before_action_finder,"",sentence)
                            conv_or_action = 1
                            if before_action_finder.match(sentence).group() == "": #지문 처리(앞에만 *있을 경우)
                                text += sentence + "\n"
                                conv_or_action = 0
                                break # 이거 flow 확인 안 함 ===========================
                            else: continue
                        else: # 마지막 안 감싸짐
                            if conv_or_action == 0:
                                text += teller + ": " + sentence + "\n"
                            else: text += "*"+ sentence + "*"+ "\n" #기본적으로 지문 처리인데 앞에 뭐 나왔는지에 따라서 달라짐 ===========================
                            break
                    
    text += "="
    in_memory_file = io.StringIO()
    in_memory_file.write(text)
    in_memory_file.seek(0)
    return in_memory_file
