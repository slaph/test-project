import asyncio
import random
import threading
import logging

from datetime import datetime

from files import shikilist
from files import MessageSend
from files import LongPoll

logging.basicConfig(filename="log.log", level=logging.INFO)
log = logging.getLogger("ex")
lp = LongPoll()
RPS = 0


# cell_id_list = []


def workWithMessage(PEER_ID, MESSAGE_OWNER_ID, rpS, current_id, taken_message, attc):
    Api = MessageSend()
    RANDOM_ID = random.randint(-2147483648, +2147483648)

    if taken_message.startswith(('добавить', 'в список', 'аниме', 'манга')):  # или and MESSAGE_OWNER_ID == мой id :
        input_message1 = taken_message.split()
        if input_message1[0] == 'аниме' or input_message1[0] == 'манга':
            title_to_search = [input_message1[0], '%20'.join(input_message1[1:])]
            raw_title = shikilist.ItemTitles(title_to_search)
            INFO_RAW, TITLE_IN_MY_LIST, CELL_ID, TITLE_ID = raw_title.getTitle()
            # current_id['object'] = TITLE_ID

            inf_about_title = [*INFO_RAW['name'], str(INFO_RAW['description']), *list(TITLE_IN_MY_LIST.values())]
            names = ['peer_id', 'message', 'random_id']

            params = [PEER_ID, '\n--------------------\n'.join(inf_about_title), RANDOM_ID]
            Api.api('messages.send', names, params)

            rpS += 5

        # if input_message1[0] == 'в список':

    NAMES = ['peer_id', 'attachment', 'random_id']
    if taken_message.startswith('2pdf'):
        params = [PEER_ID, Api.forMessage(attc, 'doc', MESSAGE_OWNER_ID,
                                          taken_message[2:].strip() if len(taken_message) != 4 else 'pdf'), RANDOM_ID]
        Api.api('messages.send', NAMES, params)

    if len(taken_message) == 0:
        params = [PEER_ID, Api.forMessage(attc), RANDOM_ID]
        Api.api('messages.send', NAMES, params)


async def inputEvent(event):
    if event['type'] == 'message_new':
        peer_id = event["object"]['peer_id']
        FROM_ID = event["object"]['from_id']
        # current[event["object"]['from_id']] = 0
        INPUT_MESSAGE = event["object"]['text'].lower()
        ATTACHMENTS = (event["object"])['attachments']
        if (len(ATTACHMENTS) == 0) and (len(event["object"]['fwd_messages']) != 0):
            ATTACHMENTS = []
            for fwd_message in event["object"]['fwd_messages']:
                for attachment in fwd_message['attachments']:
                    ATTACHMENTS.append(attachment)
            workWithMessage(peer_id, FROM_ID, RPS, current, INPUT_MESSAGE, ATTACHMENTS)
        else:
            workWithMessage(peer_id, FROM_ID, RPS, current, INPUT_MESSAGE, ATTACHMENTS)


current = {}


async def Long(raw):
    task = asyncio.create_task(inputEvent(raw))
    await task


while True:
    try:
        response_raw = lp.longPoll()
        while len(response_raw) == 0:
            response_raw = lp.longPoll()[0]
        asyncio.run(Long(response_raw))

    except Exception:
        log.exception(f"Error! {datetime.now()}")
