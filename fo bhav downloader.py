import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import os
import requests

#------------Develop the filenames list

directory = "C:\\Users\\Desktop\\Data\\....."
base = "https://archives.nseindia.com/content/historical/DERIVATIVES/"


start_date = '5/12/2000'        #start date to download from
end_date = '8/28/2021'          #end date for download

period = pd.bdate_range(start_date, end_date)               #generate weekdays for the date range given
period = pd.Series(period.format(date_format='%d-%b-%Y'))   #convert the datetime index generated to string format for extraction


data = pd.DataFrame(columns = ['dates', 'day', 'month','year','link'],index = range(0,len(period))) #create a dataframe to add all data together to generate links
data.dates = period       #add period data series to dataframe in the dates column

for i in range(0,len(data.dates)):          #add other columns from dates column using extract string methods
    print(i)
    data.day[i] = data.dates[i][0:2]
    data.month[i] = data.dates[i][3:6]
    data.year[i] = data.dates[i][7:11]
    data.link[i] = base+data.year[i]+"/"+data.month[i]+"/"+"fo"+data.day[i]+data.month[i]+data.year[i]+"bhav.csv.zip"



#-------Download the files
def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

for i in range(0,len(data.link)):
    download(data.link[i], dest_folder = directory)

download(data.link[0], dest_folder = directory)
