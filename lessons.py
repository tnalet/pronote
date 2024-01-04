import pronotepy
import json
from datetime import datetime, timedelta


# creating the client from qrcode_login
# qrcodelogin = pronotepy.Client.qrcode_login({"jeton":"QRCODE","login":"QRLOGIN","url":"URL"},
#                                   "VERIF","RandomGeneratedUuid")

#with open('credentials.json', 'w', encoding='utf-8') as f:
#    json.dump(credentials, f, ensure_ascii=False, indent=4)

with open('credentials.json', 'r', encoding='utf-8') as f:
    loaded_credentials=json.load(f)

client = pronotepy.Client.token_login(
    loaded_credentials["url"],
    loaded_credentials["username"],
    loaded_credentials["password"],
    loaded_credentials["uuid"])

credentials = {
    "url": client.pronote_url,
    "username": client.username,
    "password": client.password,
    "uuid": client.uuid,
}

with open('credentials.json', 'w', encoding='utf-8') as f:
    json.dump(credentials, f, ensure_ascii=False, indent=4)

try:
    with open('lessons.json', 'r', encoding='utf-8') as f:
        loaded_lessons=json.load(f)
except Exception as e:
    loaded_lessons=[]

fr = datetime.today()
to = datetime.today() + timedelta(days=10)

lesson_changed=[]

for lesson in client.lessons(fr,to):
    exist=next((item for item in loaded_lessons if item["subject"]["name"] == lesson.subject.name and item["start"] == str(lesson.start) and item["end"]==str(lesson.end)), None)
    if exist is None:         
    	loaded_lessons.append(lesson.to_dict())
    else:
    	if(exist["canceled"]!=lesson.canceled):
    		lesson_changed.append(f'Cours modifié {lesson.subject.name} {lesson.start}')
        	exist["canceled"]=lesson.canceled
    		
for lesson_change in lesson_changed:
    print(lesson_change)


with open('lessons.json', 'w', encoding='utf-8') as f:
    json.dump(loaded_lessons, f, ensure_ascii=False, indent=4, default=str)
