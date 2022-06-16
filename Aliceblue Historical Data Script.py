import pandas as pd
import datetime as dt
import numpy as np
import requests
import dateutil
import pytz

HEADERS = {
    'X-Authorization-Token': open('......', 'r').read().strip()
}

'''
fetch("https://ant.aliceblueonline.com/api/v1/screeners/gainerslosers?index=nifty_50", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-authorization-token": open('auth_token.txt', 'r').read().strip(),
    "x-device-type": "web"
  },
  "referrer": "https://ant.aliceblueonline.com/app/home",
  "referrerPolicy": "no-referrer-when-downgrade",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
});


'''

def gainerslosers(index="nifty_50"):
    index = index.lower()
    try:
        r = requests.get("https://ant.aliceblueonline.com/api/v1/screeners/gainerslosers?index={}".format(index), headers=HEADERS)
        data = r.json()
        return format_intraday(data)
    except Exception as e:
        print(
            "{} Error occurred.".format(e))

def historical_data(exchange, token, starttime, endtime, interval=1):
    PARAMS = {
        'candletype': 1,
        'data_duration': interval,
        'starttime': starttime,
        'endtime': endtime,
        'exchange': exchange,
        'type': 'historical',
        'token': token
    }
    try:
        r = requests.get(
            "https://ant.aliceblueonline.com/api/v1/charts", params=PARAMS, headers=HEADERS)
        data = r.json()
        return format_intraday(data)
    except Exception as e:
        print(
            "{} Error occurred in getting intraday data for ticker :: {}".format(e,token))

def intraday_data(exchange, token, starttime, endtime, interval=1):
    PARAMS = {
        'candletype': 1,
        'data_duration': interval,
        'starttime': starttime,
        'endtime': endtime,
        'exchange': exchange,
        'type': 'live',
        'token': token
    }
    try:
        r = requests.get(
            "https://ant.aliceblueonline.com/api/v1/charts", params=PARAMS, headers=HEADERS)
        data = r.json()
        return format_intraday(data)
    except Exception as e:
        print(
            "{} Error occurred in getting intraday data for ticker :: {}".format(e, token))


def format_intraday(data):
    records = data['data']
    df = pd.DataFrame(records, columns=[
                      'datetime', 'open', 'high', 'low', 'close', 'volume'])  # , index=0)
    df['datetime'] = df['datetime'].apply(
        pd.Timestamp, unit='s', tzinfo=pytz.timezone("Asia/Kolkata"))
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float).div(100)
    df.set_index('datetime', inplace=True)
    if(df.empty):
        print("Pandas DataFrame is empty.")
    return df


tday = dt.date.today()
startTime = int(dt.datetime(tday.year, tday.month, tday.day,
                            hour=9, minute=0, second=0).timestamp())
endTime = int(dt.datetime(tday.year, tday.month, tday.day,
                          hour=23, minute=59, second=0).timestamp())

# RELIANCE 2885, ADANIPORTS 11287, CIPLA 694, GOLDM SEP FUT 220754, CRUDEOIL SEP FUT 219405, SBIN 3045
print(dt.datetime.now())
for token in [3045, 2885, 11287, 694]:
    print(intraday_data('NSE', token=token, starttime=startTime, endtime=endTime, interval=5))

for token in [220754, 219405]:
    print(intraday_data('MCX', token=token, starttime=startTime, endtime=endTime, interval=10))

print(dt.datetime.now())
# Get data from 1st January 2020 till yesterday. There might be no data for MCX FUTURES for a given token
startTime = int(dt.datetime(tday.year, 1, 1,
                            hour=9, minute=0, second=0).timestamp())
endTime = int(dt.datetime(tday.year, tday.month, tday.day-1,
                          hour=23, minute=59, second=0).timestamp())

for token in [2885, 11287, 694, 3045]:
    stock = historical_data('NSE', token=token, starttime=startTime, endtime=endTime, interval=15)
    stock.to_csv('{}_15m.csv'.format(token))

for token in [220754, 219405]:
    print(historical_data('MCX', token=token, starttime=startTime, endtime=endTime, interval=5))

print(dt.datetime.now())