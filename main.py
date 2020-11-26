import random
import time
from files import shikilist
from files.api import MessageSend
from files.api import LongPoll
from datetime import datetime
import threading

lp = LongPoll()
rps = 0
cell_id_list = []


def object_find_and_send(for_id,from_who, rpS, current_id, taken_message, attc):
    Api = MessageSend()
    if taken_message.startswith(('добавить', 'в список', 'аниме', 'манга')) and from_who == 532831815:
        input_message1 = taken_message.split()
        if input_message1[0] == 'аниме' or input_message1[0] == 'манга':
            cell_id_list.clear()
            listtodo = [input_message1[0], '%20'.join(input_message1[1:])]

            test = shikilist.ItemTitles(listtodo)

            info, titleInMy, cell_id, titleId = test.getTitle()
            current_id['object'] = titleId
            inf_about_title = [*info['name'], str(info['description']), *list(titleInMy.values())]
            cell_id_list.append(cell_id)
            names = ['peer_id', 'message', 'random_id']  # для ответа в лс должно быть peer_id

            params = [for_id, '\n--------------------\n'.join(inf_about_title),
                          random.randint(-2147483648, +2147483648)]

            Api.api('messages.send', names, params)

            rpS += 5
            # if input_message1[0] == 'в список':
    if taken_message.startswith('дз'):
        names = ['peer_id', 'attachment', 'random_id']
        params = [for_id, Api.forMessage(attc,'doc',from_who, taken_message[2:].strip() if len(taken_message) != 2 else 'dz'), random.randint(-2147483648, +2147483648)]
        Api.api('messages.send', names, params)
    if len(taken_message) == 0:
        names = ['peer_id', 'attachment', 'random_id']
        params = [for_id, Api.forMessage(attc,'image',for_id), random.randint(-2147483648, +2147483648)]
        Api.api('messages.send', names, params)


def message(event):
    print(threading.currentThread().getName())
    start = time.time()
    if event['type'] == 'message_new':
        forid = event["object"]['peer_id']
        from_id = event["object"]['from_id']
        #current[event["object"]['from_id']] = 0
        input_message = event["object"]['text'].lower()
        att = (event["object"])['attachments']
        if (len(att) == 0) and (len(event["object"]['fwd_messages']) != 0):
            att = []
            for j in event["object"]['fwd_messages']:
                for h in j['attachments']:
                    att.append(h)
            object_find_and_send(forid,0, rps, current, input_message, att)
        else:
            object_find_and_send(forid,from_id, rps, current, input_message, att)
        print(datetime.now())
        print(time.time() - start)


current = {}
while True:
    try:
        a = lp.longPoll()
        while len(a) == 0:
            a = lp.longPoll()
        event_raw = a[0]
        for i in range(1):
            my_thread = threading.Thread(target=message, daemon=True, args=(event_raw,))
            my_thread.start()

    except Exception as e:
        print(str(e))
