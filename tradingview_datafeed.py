import pandas as pd
import numpy as np
import datetime
import logging
import time
import os
from tvDatafeed import TvDatafeed,Interval

#logging.basicConfig(level=logging.DEBUG)
#####--------------------------Login into chrome tradingview
#username = 
#password = 
#tv = TvDatafeed(username, password, chromedriver_path=None)

tv = TvDatafeed(auto_login=False)


#####---------------------------Download the data from TV

#create save data folder and tickerlist path
savepath = ""
directory = "...\tickerlist.csv"

#read the tickerlist file
data = pd.read_csv(directory)

#create an empty list for storing tickerlist, futures tickers and other tickers
tickerlist = []
tickerlist = data.symbol.dropna()

futurelist = []
futurelist = data.futures.dropna()

otherlist = []
otherlist = data.others.dropna()

start_time = time.time() #calculate download start time

#loop code for downloading each ticker
# NSE stocks
print("Starting download...")
for ticker in tickerlist:
    try:
        data = tv.get_hist(symbol=ticker,exchange='NSE',interval=Interval.in_1_minute,n_bars=5000)
        #time.sleep(2) #wait till download complete
        data.symbol = data["symbol"][0].split(':')[1]
        print(data.symbol[0])
        data["date"] = data.index.date
        data["time"] = data.index.time
        data = data.to_csv(savepath+'Stock\\'+ticker+'.csv')
    except AttributeError:
        continue
stock_time = round((time.time()-start_time)/60) #calculate stocks download time in mins

# futures continuous contract
for ticker in futurelist:
   try:
       data = tv.get_hist(symbol=ticker,exchange='NSE',interval=Interval.in_1_minute,n_bars=5000,fut_contract=1)
       #time.sleep(2) #wait till download complete
       data.symbol = data["symbol"][0].split(':')[1]
       print(data.symbol[0])
       data["date"] = data.index.date
       data["time"] = data.index.time
       data = data.to_csv(savepath+'Future\\'+ticker+'.csv')
   except AttributeError:
       continue
future_time = round(((time.time()-start_time)-stock_time)/60) #calculate future download time in mins

# MCX futures data
for ticker in otherlist:
    try:
        data = tv.get_hist(symbol=ticker,exchange='MCX',interval=Interval.in_1_minute,n_bars=5000,fut_contract=1)
        #time.sleep(2) #wait till download complete
        data.symbol = data["symbol"][0].split(':')[1]
        print(data.symbol[0])
        data["date"] = data.index.date
        data["time"] = data.index.time
        data = data.to_csv(savepath+'MCX\\'+ticker+'.csv')
    except AttributeError:
        continue
other_time = round(((time.time()-start_time)-future_time)/60) #calculate other download time in mins
total_time = round((time.time()-start_time)/60)  #calculate total download time in mins

print("Stocks downloaded in",stock_time,"mins")
print("Future downloaded in",future_time,"mins")
print("Others downloaded in",other_time,"mins")
print("Total download time is",total_time,"mins")
print("//////////Download Complete///////////")

#####-------------------clear cache for issues
#tv.clear_cache()