
import random


import requests



class MessageSend:

    def __init__(self):
        self.groupId = 'айди группы'
        self.params = {'v': 5.124,
                       'access_token': 'мой токен'}
        self.random_id = random.randint(-2147483648, +2147483648)

    def forMessage(self, attach):
        s = self.PhotoGetMax(attach, len(attach))
        attachment = self.GetImageForServer(s)
        attachment = f"{','.join(attachment)}"
        return attachment

    def api(self, method, names, params_api):
        params = self.params
        for i in range(len(names)):
            params[names[i]] = params_api[i]

        g = requests.post(f"https://api.vk.com/method/{method}", data=params).json()

        return g['response']

    def longPoll(self):
        params = self.params
        params['group_id'] = self.groupId
        r = requests.post(
            f"https://api.vk.com/method/groups.getLongPollServer", data=params).json()

        lp = r['response']
        long_pool = f'{lp["server"]}?act=a_check&key={lp["key"]}&ts={lp["ts"]}&wait=29'
        r = requests.get(long_pool).json()

        return [r['ts'], r['updates']]

    def GetImageForServer(self, s):
        print('GIFS')
        photoid = []
        for i in s:
            p = requests.get(i)
            out = open("img.jpg", "wb")
            out.write(p.content)
            out.close()
            r = requests.post(
                "https://api.vk.com/method/photos.getMessagesUploadServer", data=self.params) .json()['response']
            r = requests.post(r['upload_url'],
                              files={'photo': open(f"img.jpg", 'rb')}).json()
            params = [r["server"], r["photo"], r["hash"]]
            names = ["server", "photo", "hash"]
            saveToMessage1 = self.api('photos.saveMessagesPhoto', names, params)[0]

            road = f"photo{saveToMessage1['owner_id']}_{saveToMessage1['id']}"
            photoid.append(road)
        return photoid

    def PhotoGetMax(self, att, numberofpic):
        print('PGM')
        ddd = []
        for i in range(numberofpic):
            att2 = att[i]['photo']
            id1 = att2['sizes']
            d = sorted(list(set([i['height'] for i in id1])))
            ddd.append([j['url'] for j in id1 if j['height'] == d[-1]][0])

        return ddd
