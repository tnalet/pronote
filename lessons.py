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

fr = datetime.today()
to = datetime.today() + timedelta(days=10)

for lesson in client.lessons(fr,to):
    print(f'{lesson.subject}')
