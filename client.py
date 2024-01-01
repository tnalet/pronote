import pronotepy
import json
from datetime import datetime


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

for period in client.periods:
    # Iterate over all the periods the user has. This includes semesters and trimesters.

    for grade in period.grades:         # the grades property returns a list of pronotepy.Grade
        dic=grade.to_dict()
        #print(f'{grade.id} {grade.period.name} {grade.date} {grade.subject.name} {grade.grade}') # This prints the actual grade. Could be a number or for example "Absent" (always a string)

try:
    with open(f'{client.current_period.name}_notes.json', 'r', encoding='utf-8') as f:
        loaded_grades=json.load(f)
except Exception as e:
    loaded_grades=[]

# for g in loaded_grades:
#     print(f'{g["subject"]["name"]}')
#     print(f'{float(g["grade"])}')

all_grades=[]
new_note=[]
# print only the grades from the current period
for grade in client.current_period.grades:
    all_grades.append(grade.to_dict())
    exist=next((item for item in loaded_grades if item["grade"] == str(grade.grade) and item["date"] == str(grade.date) and item["subject"]["name"]==grade.subject.name), None)
    if exist is None:
        new_note.append(f'{grade.period.name} {grade.date} {grade.subject.name} {grade.grade} / {grade.out_of}')

with open(f'{client.current_period.name}_notes.json', 'w', encoding='utf-8') as f:
    json.dump(all_grades, f, ensure_ascii=False, indent=4, default=str)

with open(f"{client.current_period.name}_notes_{datetime.today().strftime('%Y-%m-%d')}.json", 'w', encoding='utf-8') as f:
    json.dump(all_grades, f, ensure_ascii=False, indent=4, default=str)

for note in new_note:
    print(f'{note}')
