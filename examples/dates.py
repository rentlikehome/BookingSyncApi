import csv
from datetime import datetime, timedelta

def prepareFile():
    with open('import_status_WAW-1.csv', encoding='utf-8-sig') as inputfile, open('new_import.csv', 'w') as outputfile:
        reader = csv.DictReader(inputfile, delimiter=';')
        writer = csv.DictWriter(outputfile, fieldnames=reader.fieldnames, delimiter=';')
        writer.writeheader()

        for row in reader:
            if not row['bookingID']:
                parsedStartDate = datetime.strptime(row['startDate'], '%d.%m.%Y %H:%M')
                parsedStartDate = parsedStartDate.replace(hour=16)
                parsedEndDate = datetime.strptime(row['endDate'], '%d.%m.%Y %H:%M') + timedelta(days=1)
                parsedEndDate = parsedEndDate.replace(hour=11)
                current = parsedStartDate
                while current < parsedEndDate:
                    new = row
                    new['startDate'] = current.strftime('%d.%m.%Y %H:%M')
                    nextDay = current + timedelta(days=1)
                    nextDay = nextDay.replace(hour=11)
                    new['endDate'] = nextDay.strftime('%d.%m.%Y %H:%M')

                    current += timedelta(days=1)
                    writer.writerow(new)
                    

prepareFile()


