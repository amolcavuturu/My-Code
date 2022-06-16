###This program is to remove null data in the price
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

#rename file by using extension
directory = "......"
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        name = filename.split(".")
        newname = name[0]+'.csv'
        os.rename(directory + filename, directory + newname)



#clean the data by removing 0 values in the data
directory = '.....'
filepath = Path(directory)
filenames = [fname for fname in filepath.iterdir() if fname.is_file() and fname.suffix == '.csv']

for filename in filenames:
    with filename.open() as fp:
        data = pd.read_csv(filename, index_col=['Date'], parse_dates=['Date'])
        data = data[(data.Close != 0) & (data.Volume != 0)]
        data = data.to_csv(filename, date_format="%Y-%m-%d")



#Rename the Ticker column to reflect symbol
directory = "......"
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        name = filename.split(".")
        newname = name[0]
        data = pd.read_csv(directory+filename, index_col=['Date'], parse_dates=['Date'])
        #data.Ticker.convert_dtypes(convert_string = True)
        #data.dtypes
        data.loc[:,'Ticker'] = newname
        data = data.to_csv(directory+filename, date_format="%Y-%m-%d") 






