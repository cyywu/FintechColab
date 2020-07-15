import urllib.request
import json
import ssl
context = ssl._create_unverified_context()

# Monetary Base Data released by hkma monthly
url = 'https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/monetary-operation/monetary-base-endperiod'

records = []

# retrieve data from hkma api, 100 entries per call, untill every data are retrieveed
offset = 0
while True:
    with urllib.request.urlopen(url+"?offset="+str(offset), context=context) as req:
        data = json.loads(req.read().decode())
        records += data['result']['records']
    if data['result']['datasize'] <= 0:
        break
    else:
        offset += 100

# records are now loaded with all data

print('end')
