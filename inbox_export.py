import json
from BookingSyncApi.api import API
import pandas as pd

def exportMessages():
    api = API()
    hostData = api.get('/hosts').json()
    hosts = { host['id'] : host for host in hostData['hosts']}

    rows = []

    pages = int(api.get('/inbox/messages?include=sender,hosts').json()['meta']['X-Total-Pages'])
    print(pages)
    for page in range(1, pages):
        print(page)
        try:
            messages = api.get(f'/inbox/messages?include=sender,hosts&page={page}').json()['messages']
        except:
            print('Error')
            continue
        for message in messages:
            row = []
            row.append(message['id'])
            row.append(message['origin'])
            row.append(message['sent_at'])
            row.append(message['sender']['links']['member']['type'])
            if message['sender']['links']['member']['type'] == 'Host':
                host = hosts[message['sender']['links']['member']['id']]
                row.append(f"{host['firstname']} {host['lastname']} ({host['email']})")
            else:
                row.append('-')
            row.append(message['content'])

            rows.append(row)

    columns = ['id', 'origin', 'sent_at', 'sender_type', 'host [firstname lastname (email)]', 'content']
    df = pd.DataFrame(rows, columns=columns)
    df.to_excel("inbox_messages.xlsx", engine='xlsxwriter')


def exportConversations():
    api = API()

    rows = []

    pages = int(api.get('/inbox/conversations').json()['meta']['X-Total-Pages'])
    for page in range(1, pages):
        conversations = api.get(f'/inbox/conversations?page={page}').json()['conversations']
        for conv in conversations:
            row = []
            row.append(conv['id'])
            row.append(conv['created_at'])
            row.append(conv['closed_at'])
            row.append(conv['last_message_at'])
            row.append(len(conv['links']['messages']))
            row.append(conv['subject'])

            rows.append(row)

    columns = ['id', 'created_at', 'closed_at', 'last_message_at', 'num_of_messages', 'subject']
    df = pd.DataFrame(rows, columns=columns)
    df.to_excel("inbox_conversations.xlsx", engine='xlsxwriter')


exportMessages()
# exportConversations()
