import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

en = "According to the new law, all stays starting in between 7.11.2020 and 29.11.2020 can only take place in one of the circumstances below:\r\n\r\n- Business trip\r\n- Players during groupings and competitions\r\n- Healthcare professionals, patients and their caretakers providing treatment\r\n\r\nA stay in between aforementioned dates requires signing of a statement by a person making a reservation.\r\n\r\n---\r\n\r\n"

pl = "Zgodnie z nowymi przepisami, pobyty rozpoczynaj\u0105ce si\u0119 pomi\u0119dzy 7.11.2020 a 29.11.2020 mog\u0105 by\u0107 zrealizowane w jednym z poni\u017cszych przypadk\u00f3w:\r\n\r\n- Podr\u00f3\u017c s\u0142u\u017cbowa\r\n- Zawodnicy w czasie zgrupowa\u0144 i wsp\u00f3\u0142zawodnictwa\r\n- Pracownicy medyczni, pacjenci oraz ich opiekunowie w trakcie \u015bwiadczenia opieki zdrowotnej.\r\n\r\nPobyt w wy\u017cej wymienionym terminie wymaga podpisania o\u015bwiadczenia ze strony os\u00f3b rezerwuj\u0105cych nocleg.\r\n\r\n\r\n---\r\n\r\n"

pages = int(api.get('/rentals').json()['meta']['X-Total-Pages'])

rows = []
for page in range(1, pages + 1):
    data = api.get(f'/rentals?page={page}').json()
    for rental in data['rentals']:
        try:
            description_en = rental['description']['en'] 
        except:
            description_en = ''

        try:
            description_pl = rental['description']['pl'] 
        except:
            description_pl = ''


        payload = {
            "rentals" : [
                {
                    "description_en" : en + description_en,
                    "description_pl" : pl + description_pl,

                }
            ]
        }

        print(api.put(f'/rentals/{rental["id"]}', payload).status_code)
        new_row = [rental['id'], description_pl, description_en]
        rows.append(new_row)

columns = ['id', 'pl', 'en']
df = pd.DataFrame(rows, columns=columns)
df.to_excel('desc_backup.xlsx')
