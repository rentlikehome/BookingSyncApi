from api import API

api = API('5a07f0e26aedab2a2c9d4bc26419e388cfcc061f0ed3e519e192be83a867df62')

with open('bookings_fees.csv', 'w') as csvfile:
    fieldnames = ['id', 'booking_id', 'name', 'price', 'required', 'included_in_price', 'times_booked', 'created_at', 'updated_at', 'locked', 'canceled_at']
    writer = csv.DictWriter(csvfile, fieldnames, extrasaction='ignore')
    writer.writeheader()
    for page in range(1, 60):
        json = api.get(f'/bookings_fees?page={page}').json()
        for fee in json['bookings_fees']:
            fee['name'] = fee['name']['en']
            fee['booking_id'] = fee['links']['booking']
            writer.writerow(fee)
