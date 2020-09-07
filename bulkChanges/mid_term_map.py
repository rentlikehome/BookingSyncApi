from api import API
import json
import pandas as pd

from datetime import datetime

api = API()

def modify_map(rental_id, value, end):
    # print(json.dumps(api.get('/rentals/128555').json(), indent=4))

    rental = api.get(f'/rentals/{rental_id}').json()['rentals'][0]
    midmap_id = rental['links']['mid_term_rate_map']

    response = api.get(f'/mid_term_rate_maps/{midmap_id}').json()
    # print(json.dumps(response, indent=4))

    mapJson = response['mid_term_rate_maps'][0]
    midmap = mapJson['map'].split(',')
    start = datetime.strptime(mapJson['start_date'], "%Y-%m-%d")

    for i in range((end - start).days):
        midmap[i] = value

    midmap = ','.join(midmap)

    newJson = {
            "mid_term_rate_maps": [
                {
                    "map" : midmap,
                }
            ]
    }

    
    response = api.put(f'/mid_term_rate_maps/{midmap_id}', newJson).json()
    print(json.dumps(response, indent=4))


def modify_maps(filename):
    df = pd.read_excel(filename)

    for index, row in df.iterrows():
        converted_value = str(row['value']) + '.0'
        modify_map(row['id'], converted_value, datetime(2020, 9, 30))

modify_maps('mid_term_sheet.xlsx')
    
