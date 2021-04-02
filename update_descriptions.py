import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

en = """Due to public safety restrictions, stays with check-in from 20/03/2020 to 09/04/2021 may only be available to guests traveling for certain reasons:
- business trips in accordance with the list specified in the regulation, - - participation in sports-related competitions or groupings,
- being a health care worker, patient or his guardian,
- beeing a foreigner unable to continue traveling to a permanent place of residence.

Stay with us in the above-mentioned The period will require a CERTIFICATE issued by the relevant institutions, depending on the reason for travel.

---"""

pl = """Ze względu na ograniczenia bezpieczeństwa publicznego pobyty z zameldowaniem od 20.03.2020 do 09.04.2021 mogą być dostępne tylko dla gości podróżujących z określonych powodów:
- podróże służbowe zgodne z listą określoną w rozporządzeniu,
- udział w zawodach lub zgrupowaniach związanych ze sportem,
- bycie pracownikiem służby zdrowia, pacjentem lub jego opiekunem,
- bycie cudzoziemcem niemogącym kontynuować podróży do stałego miejsca zamieszkania.

Pobyt u nas w ww. Okresie będzie wymagał ZAŚWIADCZENIA wydanego przez odpowiednie instytucje, w zależności od powodu podróży.

---"""

pages = int(api.get('/rentals').json()['meta']['X-Total-Pages'])

rows = []
for page in range(1, pages + 1):
    data = api.get(f'/rentals?page={page}').json()
    for rental in data['rentals']:
        # Only the rest
        if rental['name'][:3] in ['WRO', 'POZ', 'MIE', 'ZAK', 'KOŁ']:
        # Only for KOŁ and GDA
        # if rental['name'][:3] in ['WAW', 'GDA']:
        # ALL
        # if True:
            print(rental['name'][:3], rental['id'])
            try:
                description_en = rental['description']['en'] 
            except:
                description_en = ''

            try:
                description_pl = rental['description']['pl'] 
            except:
                description_pl = ''

            if description_pl and '---' in description_pl:
                split = description_pl.split('---') 
                split[0] = pl
                new_pl = ''.join(split)
            elif description_pl:
                new_pl = pl + '\n\n' + description_pl
            else:
                new_pl = ''

            if description_en and '---' in description_en:
                split = description_en.split('---') 
                split[0] = en 
                new_en = ''.join(split)
            elif description_pl:
                new_en = en + '\n\n' + description_en
            else:
                new_en =''


            payload = {
                "rentals" : [
                    {
                        "description_en" : new_en,
                        "description_pl" : new_pl,

                    }
                ]
            }

            print(api.put(f'/rentals/{rental["id"]}', payload).status_code)
            new_row = [rental['id'], description_pl, description_en]
            rows.append(new_row)

columns = ['id', 'pl', 'en']
df = pd.DataFrame(rows, columns=columns)
df.to_excel('desc_backup.xlsx')
