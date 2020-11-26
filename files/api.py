import os
import random

import requests


def PhotoGetMax(att, numberofpic):
    max_pics = []
    for i in range(numberofpic):
        att2 = att[i]['photo']
        id1 = att2['sizes']
        d = sorted(list(set([i['height'] for i in id1])))
        max_pics.append([j['url'] for j in id1 if j['height'] == d[-1]][0])

    return max_pics


class LongPoll:
    def __init__(self):
        self.groupId = int
        self.params = {'v': 5.124,
                       'access_token': ''}
        self.server, self.key, self.ts = self.get_LongPoll()

    def get_LongPoll(self):
        params = self.params
        params['group_id'] = self.groupId
        r = requests.post(
            f"https://api.vk.com/method/groups.getLongPollServer", data=params).json()
        r = r['response']
        return r['server'], r['key'], r['ts']

    def longPoll(self):
        long_pool = f'{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25'
        r = requests.get(long_pool).json()
        if ('failed' in r.keys()) and (int(r['failed']) == 2):
            a, self.key, self.ts = self.get_LongPoll() # 'a' not need, idk how get only server\ts
            long_pool = f'{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25'
            r = requests.get(long_pool).json()
        if self.ts != str(r['ts']):
            self.ts = str(r['ts'])
        return r['updates']


class MessageSend:

    def __init__(self):
        self.groupId = 'айди группы'
        self.params = {'v': 5.124,
                       'access_token': 'мой токен'}
        self.random_id = random.randint(-2147483648, +2147483648)

    def forMessage(self, attach):
        s = PhotoGetMax(attach, len(attach))
        attachment = self.GetImageForServer(s)
        attachment = f"{','.join(attachment)}"
        return attachment

    def api(self, method, names, params_api):
        params = self.params
        for i in range(len(names)):
            params[names[i]] = params_api[i]

        g = requests.post(f"https://api.vk.com/method/{method}", data=params).json()

        return g['response']

    def GetImageForServer(self, s):
        photo_ids = []
        path = f"img{random.randint(1, 100)}.jpg"
        for i in s:
            p = requests.get(i)
            out = open(path, "wb")
            out.write(p.content)
            out.close()
            r = requests.post(
                "https://api.vk.com/method/photos.getMessagesUploadServer", data=self.params).json()['response']
            r = requests.post(r['upload_url'],
                              files={'photo': open(path, 'rb')}).json()
            params = [r["server"], r["photo"], r["hash"]]
            names = ["server", "photo", "hash"]
            saveToMessage1 = self.api('photos.saveMessagesPhoto', names, params)[0]

            photo_id = f"photo{saveToMessage1['owner_id']}_{saveToMessage1['id']}"
            photo_ids.append(photo_id)
            os.remove(path)
        return photo_ids
