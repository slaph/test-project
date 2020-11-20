import random
import time
from test_git import shikilist
from test_git.api import MessageSend
from datetime import datetime
import threading

api = MessageSend()
rps = 0
cell_id_list = []


def object_find_and_send(for_id, rpS, current_id, taken_message, attc):
    Api = MessageSend()
    if int(for_id) > 2000000000:  # только для беседы

        if taken_message.startswith(('добавить', 'в список', 'аниме', 'манга')) and rpS != 90:
            input_message1 = taken_message.split()
            if input_message1[0] == 'аниме' or input_message1[0] == 'манга':
                cell_id_list.clear()
                listtodo = [input_message1[0], '%20'.join(input_message1[1:])]

                test = shikilist.ItemTitles(listtodo)

                info, titleInMy, cell_id, titleId = test.getTitle()
                current_id['object'] = titleId
                inf_about_title = [*info['name'], str(info['description']), *list(titleInMy.values())]
                cell_id_list.append(cell_id)
                names = ['chat_id', 'message', 'random_id']  # для ответа в лс должно быть peer_id

                params = [str(for_id)[-1], '\n--------------------\n'.join(inf_about_title),
                          random.randint(-2147483648, +2147483648)]

                Api.api('messages.send', names, params)

                rpS += 5
            # if input_message1[0] == 'в список':

        if len(taken_message) == 0:
            names = ['chat_id', 'attachment', 'random_id']
            params = [str(for_id)[-1], Api.forMessage(attc), random.randint(-2147483648, +2147483648)]
            Api.api('messages.send', names, params)


def message(event):
    print(threading.currentThread().getName())
    start = time.time()
    if event['type'] == 'message_new':
        forid = event["object"]['peer_id']
        current[event["object"]['from_id']] = 0
        input_message = event["object"]['text'].lower()
        att = (event["object"])['attachments']
        if (len(att) == 0) and (len(event["object"]['fwd_messages']) != 0):
            att = []
            for mess in event["object"]['fwd_messages']:
                for one_att in mess['attachments']:
                    att.append(one_att)
            object_find_and_send(forid, rps, current, input_message, att)
        else:
            object_find_and_send(forid, rps, current, input_message, att)
        print(datetime.now())
        print(time.time() - start)


current = {}
while True:
    try:
        a = api.longPoll()
        while len(a) == 0:
            a = api.longPoll()
        event = a[0]
        print(event)
        for i in range(1):
            my_thread = threading.Thread(target=message, daemon=True, args=(event,))
            my_thread.start()

    except Exception as e:
        print(str(e))
