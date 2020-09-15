from BookingSyncApi.api import API
import json
import pandas as pd

from datetime import datetime, date

api = API()

def modify_multiple_terms(row):
    try:
        rental = api.get(f'/rentals/{row["id"]}').json()['rentals'][0]
    except:
        print("Apartment doesn't exist")
        return
    midmap_id = rental['links']['mid_term_rate_map']

    response = api.get(f'/mid_term_rate_maps/{midmap_id}').json()

    mapJson = response['mid_term_rate_maps'][0]
    midmap = mapJson['map'].split(',')
    start = datetime.strptime(mapJson['start_date'], "%Y-%m-%d")
    terms = [
                ('rate1', start.date(), date(2020, 11, 1)),
                ('rate2', date(2020, 11, 1), date(2021, 4, 1)),
                ('rate3', date(2021, 4, 1), date(2021, 9, 10))
            ]

    index = 0
    for term in terms:
        for _ in range((term[2] - term[1]).days):
            midmap[index] = str(row[term[0]]) + '.0'
            index += 1

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

    for index in range(df.shape[0]):
        modify_multiple_terms(df.iloc[index])

    # for index, row in df.iterrows():
    #     converted_value = str(row['value']) + '.0'
    #     modify_map(row['id'], converted_value, datetime(2020, 9, 30))

modify_maps('mid_term_sheet.xlsx')
    
