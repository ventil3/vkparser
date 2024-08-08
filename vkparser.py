import vk_api
import datetime
import csv
import pandas as pd


name = 'имя_файла.csv'
group_id = 11111111
login = 'ВК_логин'
password = 'ВК_пароль'
date = datetime.datetime(year=2023, month=4, day=6).timestamp()


vk_session = vk_api.VkApi(login, password)
vk_session.auth()
access_token = vk_session.token['access_token']


date = datetime.datetime(year=2023, month=5, day=13, hour=0, minute=0).timestamp()

response = vk_session.method('groups.getMembers', {'group_id': group_id, 'fields': 'last_seen', 'count': 1000})
vk_session = vk_api.VkApi(token=access_token)


members = []
offset = 0
while len(members) < response['count']:
    response = vk_session.method('groups.getMembers', {'group_id': group_id, 'fields': 'last_seen', 'count': 1000, 'offset': len(members)})
    members += response['items']


online_friends = [friend['id'] for friend in members if 'last_seen' in friend and friend['last_seen']['time'] > date]
members_final = []
chunk_size = 1000
chunks = [online_friends[i:i+chunk_size] for i in range(0, len(online_friends), chunk_size)]
for chunk in chunks:
    code = 'return ['
    for member_id in chunk:
        code += f'{member_id},'
    code = code[:-1] + '];'
    response = vk_session.method('execute', {'code': code})
    members_final += response


with open(name, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id'])
    for member in members_final:
        writer.writerow((member,))

df = pd.read_csv(name, header=None)
df = df.drop_duplicates()
df.to_csv(name, index=False, header=None)