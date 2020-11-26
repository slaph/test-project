import json
import time

import requests


def getToken(token):
    print(2)
    with open('tokenShikimori.json', 'r') as f:
        a = json.loads(f.readline())
        access_token, refresh_token = a['access_token'], a['refresh_token']
        f.close()

    if token == 'access_token':
        return access_token
    if token == 'refresh_token':
        return refresh_token


def access():
    access_token = getToken("access_token")
    headers = {'User-Agent': "shap", "Content-Type": "application/json",
               "Authorization": f'Bearer {access_token}'}
    return headers


client_id = "айди приложения"
client_secret = "секрет приложения"


def UpdateToken():
    print(1)
    url = "https://shikimori.one/oauth/token"
    post_request = requests.post(url, headers={"User-Agent": "YOU APP"}, params={"grant_type": "refresh_token",
                                                                                  "client_id": client_id,
                                                                                  "client_secret": client_secret,
                                                                                  "refresh_token": getToken(
                                                                                      'refresh_token')
                                                                                  }).json()

    with open(r'tokenShikimori.json', 'w') as f:
        tokens = {'access_token': post_request['access_token'], 'refresh_token': post_request['refresh_token']}
        f.write(json.dumps(tokens, indent=2))
        f.close()


class Access:
    def __init__(self):
        self.headers = access()
        self.session = requests.session()
        self.session.headers.update(self.headers)
        if (self.session.get('https://shikimori.one/api/mangas')).status_code == 401:
            time.sleep(1)
            UpdateToken()
            self.headers = access()
            self.session.headers.update(self.headers)


class ItemTitles(Access):

    def __init__(self, listtodo):
        super().__init__()
        self.listodo = listtodo
        self.my_id = 708889
        self.characteristics = {'манга': {'type': 'manga', 'typePart': 'chapters'},
                                'аниме': {'type': 'anime', 'typePart': 'episodes'}}

    def getTitle(self):
        titleType = (self.characteristics[self.listodo[0]])['type']
        part = (self.characteristics[self.listodo[0]])['typePart']

        r = self.session.get(f'https://shikimori.one/api/{titleType}s?search={self.listodo[1]}').json()

        titleId = r[0]['id']

        time.sleep(1)

        r = self.session.get(f'https://shikimori.one/api/{titleType}s/{titleId}').json()

        time.sleep(1)

        info = {'name': [r['name'], r['russian']], 'image': r['image']['original'], 'description': r['description']}

        r = self.session.get(f'https://shikimori.one/api/users/{self.my_id}/{titleType}_rates?limit=1000').json()

        titleInMy = {}

        cell_id = 0

        for i in r:

            itemIdTitle = i[titleType]['id']

            if itemIdTitle == titleId:
                titleInMy = {'status': i['status'], 'parts': str(i[part])}
                cell_id = i['id']

        if len(titleInMy) == 0:
            titleInMy = {'in list': 'нет в списке'}
        return [info, titleInMy, cell_id, titleId]
