import os
import random

import img2pdf
import requests


def PhotoGetMax(att, numberofpic):
    print('PGM')
    max_pics = []
    for i in range(numberofpic):
        att2 = att[i]['photo']
        id1 = att2['sizes']
        d = sorted(list(set([i['height'] for i in id1])))
        max_pics.append([j['url'] for j in id1 if j['height'] == d[-1]][0])

    return max_pics


class LongPoll:
    def __init__(self):
        self.groupId = 'your_group_id'
        self.params = {'v': 5.124,
                       'access_token': 'your_access_token'}
        self.server, self.key, self.ts = self.get_LongPoll()

    def get_LongPoll(self):
        params = self.params
        params['group_id'] = self.groupId
        r = requests.post(
            f"https://api.vk.com/method/groups.getLongPollServer", data=params).json()
        r = r['response']
        print('upd')
        return r['server'], r['key'], r['ts']

    def longPoll(self):
        long_pool = f'{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25'
        r = requests.get(long_pool).json()
        print('ts')
        if ('failed' in r.keys()) and (int(r['failed']) == 2):
            print('failed')
            a, self.key, self.ts = self.get_LongPoll()
            long_pool = f'{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25'
            r = requests.get(long_pool).json()
        if self.ts != str(r['ts']):
            self.ts = str(r['ts'])
        return r['updates']


class MessageSend:

    def __init__(self):

        self.groupId = 'your_group_id'
        self.params = {'v': 5.124,
                       'access_token': 'your_access_token'}
        self.random_id = random.randint(-2147483648, +2147483648)

    def forMessage(self, attach, need_type, peer_id, file_name='dz'):
        s = PhotoGetMax(attach, len(attach))
        attachment = ''
        if need_type == 'image':
            attachment = self.GetImageForServer(s)
            attachment = f"{','.join(attachment)}"
        if need_type == 'doc':
            attachment = self.saveHomeWork(s, peer_id, file_name)
        return attachment

    def api(self, method, names, params_api):
        params = self.params
        for i in range(len(names)):
            params[names[i]] = params_api[i]
        g = requests.post(f"https://api.vk.com/method/{method}", data=params).json()
        return g['response']

    def saveHomeWork(self, s, from_who, filename):
        images_list = []
        id_dz = random.randint(0, 1000)
        for photo in s:
            photoget = requests.get(photo)
            with open(f"dz{s.index(photo)}.jpg", "wb") as f:
                f.write(photoget.content)
                f.close()
                images_list.append(f"dz{s.index(photo)}.jpg")
        with open(f"dz{id_dz}.pdf", "wb") as f:
            f.write(img2pdf.convert(images_list))
            f.close()
        for b in images_list:
            os.remove(b)
        data = self.params
        data['peer_id'] = from_who
        r = requests.post('https://api.vk.com/method/docs.getMessagesUploadServer', data=data).json()['response']
        save = requests.post(r['upload_url'],
                             files={'file': open(f"dz{id_dz}.pdf", 'rb')}).json()['file']
        ids = (self.api('docs.save', ['file', 'title'], [save, str(filename)]))['doc']
        doc_id = f'doc{ids["owner_id"]}_{ids["id"]}'
        os.remove(f"dz{id_dz}.pdf")
        return doc_id

    def GetImageForServer(self, s):
        print('GIFS')
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
