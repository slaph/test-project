import random
import time
from test_git import shikilist
from test_git.api import MessageSend
from datetime import datetime
import threading
Api = MessageSend()
rps = 0


def object_find_and_send(for_id, rpS, message, attc):
    if int(for_id) > 2000000000:  # только для беседы

        if message.startswith(('добавить', 'в список', 'тайтл')) and rpS != 90:
            input_message1 = message.split()
            if input_message1[0] == 'тайтл':
                # listtodo = [input_message1[0], input_message1[1], '%20'.join(input_message1[2:])]

                # test = shikilist.ItemTitles(listtodo)

                # info, titleInMy, cell_id = test.getTitle()

                # inf_about_title = [*info['name'], str(info['description']), *list(titleInMy.values())]

                # names = ['chat_id', 'message', 'random_id'] # для ответа в лс должно быть peer_id

                # params = [str(for_id)[-1], '\n--------------------\n'.join(inf_about_title), random.randint(-2147483648, +2147483648)]

                # Api.api('messages.send', names, params)

                rpS += 5

        if len(message) == 0:
            names = ['chat_id', 'attachment', 'random_id']
            params = [str(for_id)[-1], Api.forMessage(attc), random.randint(-2147483648, +2147483648)]
            Api.api('messages.send', names, params)


def message(event):
    print(threading.currentThread().getName())
    start = time.time()
    if event['type'] == 'message_new':
        forid = event["object"]['peer_id']
        input_message = event["object"]['text'].lower()
        att = (event["object"])['attachments']
        if (len(att) == 0) and (len(event["object"]['fwd_messages']) != 0):
            object_find_and_send(forid, rps, input_message, event["object"]['fwd_messages'][0]['attachments'])
        else:
            object_find_and_send(forid, rps, input_message, att)
        print(datetime.now())
        print(time.time() - start)


while True:
    try:
        a = Api.longPoll()
        while len(a[1]) == 0:
            print('noevents')
            a = Api.longPoll()
        print(len(a[1]))
        event = (a[1])[0]
        for i in range(1):
            my_thread = threading.Thread(target=message, args=(event,))
            my_thread.start()



    except Exception:
        print(Exception)
