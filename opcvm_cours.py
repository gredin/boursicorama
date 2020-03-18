import datetime
import json
import os
import random
import time

import requests

epoch = datetime.date.fromtimestamp(0)

url_identifiers = []
with open('boursorama/boursorama_opcvm.jl') as f:
    for line in f:
        row = json.loads(line)

        url_identifiers.append(row["url_identifier"])

for i, url_identifier in enumerate(url_identifiers):
    print(i + 1, url_identifier)

    cours_filepath = 'opcvm_cours/%s.csv' % url_identifier

    if os.path.isfile(cours_filepath):
        continue

    time.sleep(0.4 * (1 + 0.5 * random.random()))

    resp = requests.get("https://www.boursorama.com/bourse/action/graph/ws/GetTicksEOD?symbol=%s&length=7300&period=0&guid=" % url_identifier, headers={
        "Referer": "https://www.boursorama.com/bourse/opcvm/cours/%s/" % url_identifier,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
    })

    if resp.status_code != 200:
        print("Status code", resp.status_code, url_identifier)
        continue

    try:
        json_data = resp.json()

        quotes = []
        for quote in json_data['d']['QuoteTab']:
            days_since_epoch = quote['d']
            value = quote['c']

            date = epoch + datetime.timedelta(days=days_since_epoch)

            quotes.append((days_since_epoch, date.isoformat(), value))
    except Exception as e:
        print("Exception", url_identifier)
        print(e)

        continue

    with open(cours_filepath, 'w') as file:
        for days_since_epoch, date_isoformat, value in quotes:
            file.writelines(str(days_since_epoch) + ";" + str(date_isoformat) + ";" + str(value) + "\n")
