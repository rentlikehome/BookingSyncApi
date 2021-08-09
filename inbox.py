import json
import traceback
from BookingSyncApi.api import API
import pandas as pd

BOOKINGSYNC_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

def export_messages(filename, updated_since):
    base_messages_url = '/inbox/messages?include=sender,hosts'
    if updated_since:
        base_messages_url += f'&updated_since={updated_since.strftime(BOOKINGSYNC_DATE_FORMAT)}'

    columns = ['id', 'origin', 'sent_at', 'sender_type', 'host [firstname lastname (email)]', 'content']

    try:
        df = pd.read_excel(filename, index_col='id', usecols=columns)
    except:
        df = pd.DataFrame(columns=columns)

    api = API()

    hostPages = int(api.get('/hosts').json()['meta']['X-Total-Pages'])
    hosts = {}
    for page in range(1, hostPages+1):
        hostData = api.get(f'/hosts?page={page}').json()
        hosts.update({ host['id'] : host for host in hostData['hosts']})

    rows = []

    response = api.get(base_messages_url)

    try:
        pages = int(response.json()['meta']['X-Total-Pages'])
        print(f'Exporting messages. Number of pages: {pages}')
    except:
        print(f'Error at getting the number of pages.\n{response.status_code}\n{response}')
        return

    for page in range(1, pages + 1):
        print(page)
        try:
            messages = api.get(base_messages_url + f'&page={page}').json()['messages']
        except:
            print('Error at getting the page.')
            continue

        for message in messages:
            if message['id'] in df.index:
                print(f'Message update {message["id"]}')
            try:
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
            except:
                print('Error at row.')
                traceback.print_exc()
                print()

    

    new_df = pd.DataFrame(rows, columns=columns).set_index('id')

    df = df.combine_first(new_df)
    df.update(new_df)

    if not filename:
        filename = 'inbox_messages.xlsx'

    writer = pd.ExcelWriter(filename, engine='xlsxwriter', options={'strings_to_urls' : False})
    df.to_excel(writer)
    writer.close()

    return df

def export_conversations():
    api = API()

    rows = []

    pages = int(api.get('/inbox/conversations').json()['meta']['X-Total-Pages'])
    for page in range(1, pages + 1):
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

    return df

if __name__ == '__main__':
    export_messages(None, None)
# exportMessages('inbox_messages.xlsx', '2021-08-05T00:00:00Z')
# exportConversations()
