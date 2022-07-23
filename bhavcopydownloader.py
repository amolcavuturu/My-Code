import requests
import io
import zipfile
import pandas as pd
import datetime
import sys
from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save, bhavcopy_index_save
import urllib.request 
from os import path

def download_extract_zip(url):
    """
    Download a ZIP file and extract its contents in memory
    yields (filename, file-like object) pairs
    """
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
        for zipinfo in thezip.infolist():
            with thezip.open(zipinfo) as thefile:
                if zipinfo.filename.split('.')[-1] == "csv":
                    return pd.read_csv(thefile)
                

def getDateString(dateObj):
    return dateObj.strftime('%d%m%Y')

if __name__ == '__main__':

    start_date = datetime.date(2021, 4, 22)

#### Download data
    filename = "FOVOLT_" + getDateString(start_date) + ".csv"
    nseURL = "https://www1.nseindia.com/archives/nsccl/volt/FOVOLT_" + getDateString(start_date) + ".csv"
    print (filename)
    try:
        r = requests.get(nseURL)  
        with open('C:\\Work\\OI\\Daily\\'+filename, 'wb') as f:
            f.write(r.content)
    except Exception as ex:
        print(ex)

    try:
        #for fo data
        bhavcopy_fo_save(start_date, "C:\\Work\\OI\\Daily\\")
        #for index
        bhavcopy_index_save(start_date, "C:\\Work\\OI\\Daily\\")
        #for stocks
        bhavcopy_save(start_date, "C:\\Work\\OI\\Daily\\")
    except Exception as ex:
        print(ex)

    filename = "MTO_" + getDateString(start_date) + ".DAT"
    nseURL = "https://www1.nseindia.com/archives/equities/mto/MTO_" + getDateString(start_date) + ".DAT"
    print (filename)
    try:
        r = requests.get(nseURL)  
        with open('C:\\Work\\OI\\Daily\\'+filename, 'wb') as f:
            f.write(r.content)
    except Exception as ex:
        print(ex)

### process all data

### process index data

    filename = "ind_close_all_" + getDateString(start_date) + ".csv"
    print (filename)
    
    try:
        if path.exists('C:\\Work\\OI\\Daily\\'+filename):
            mydateparser = lambda x: pd.datetime.strptime(x, "%d-%m-%Y")
            bhavdf = pd.read_csv('C:\\Work\\OI\\Daily\\'+filename, parse_dates=['Index Date'],date_parser=mydateparser)
            bhavdf['Index Date'] = bhavdf['Index Date'].apply(lambda x: x.strftime('%Y%m%d'))
            #print(bhavdf.head())
            #for col in bhavdf.columns:
            #    print(col)
            csv_data = bhavdf.to_csv('C:\\Work\\OI\\Daily\\Clean\\'+filename, header=['Symbol', 'Date', 'Open', 'High', 'Low', 'Close','Volume','Aux1'],columns=['Index Name', 'Index Date','Open Index Value','High Index Value','Low Index Value','Closing Index Value','Volume','P/E'],index=False)
    except Exception as ex:
        print(ex)

### process stock data

    filename = "cm" + start_date.strftime('%d') + start_date.strftime('%B').upper()[:3] + start_date.strftime('%Y') + "bhav.csv"
    print (filename)
    
    try:
        if path.exists('C:\\Work\\OI\\Daily\\'+filename):
            #mydateparser = lambda x: pd.datetime.strptime(x, "%d-%M-%Y")
            #bhavdf = pd.read_csv('C:\\Work\\OI\\StockData\\'+filename, parse_dates=['TIMESTAMP'],date_parser=mydateparser)
            bhavdf = pd.read_csv('C:\\Work\\OI\\Daily\\'+filename, parse_dates=['TIMESTAMP'])
            bhavdf['TIMESTAMP'] = bhavdf['TIMESTAMP'].apply(lambda x: x.strftime('%Y%m%d'))
            options = ['EQ']
            rslt_df = bhavdf.loc[bhavdf['SERIES'].isin(options)]                     
            #print(bhavdf.head())
            #for col in bhavdf.columns:
            #    print(col)
            csv_data = rslt_df.to_csv('C:\\Work\\OI\\Daily\\Clean\\'+filename, header=['Symbol', 'Date', 'Open', 'High', 'Low', 'Close','Volume'],columns=['SYMBOL', 'TIMESTAMP','OPEN','HIGH','LOW','CLOSE','TOTTRDQTY'],index=False)
    except Exception as ex:
        print(ex)

### FO VOlt process

    filename = "FOVOLT_" + getDateString(start_date) + ".csv"
    print (filename)
    
    try:
        if path.exists('C:\\Work\\OI\\Daily\\'+filename):
            bhavdf = pd.read_csv('C:\\Work\\OI\\Daily\\'+filename, parse_dates=['Date'])
            bhavdf['Date'] = bhavdf['Date'].apply(lambda x: x.strftime('%Y%m%d'))
            #print(bhavdf.head())
            #for col in bhavdf.columns:
            #    print(col)
            csv_data = bhavdf.to_csv('C:\\Work\\OI\\Daily\\Clean\\'+filename, header=['Symbol', 'Date', 'Aux2'],columns=[' Symbol', 'Date',' Applicable Daily Volatility (M) = Max (E or K)'],index=False)
    except Exception as ex:
        print(ex)

### COI Process data

    filename = filename= "/fo" + start_date.strftime('%d') + start_date.strftime('%B').upper()[:3] + start_date.strftime('%Y') + "bhav.csv"
    print (filename)
    
    try:
        if path.exists('C:\\Work\\OI\\Daily\\'+filename):
            bhavdf = pd.read_csv('C:\\Work\\OI\\Daily\\'+filename, parse_dates=['TIMESTAMP'])
            #bhavdf['Date'] = bhavdf['Date'].apply(lambda x: x.strftime('%Y%m%d'))
            #print(bhavdf.head())
            #for col in bhavdf.columns:
            #    print(col)
            #csv_data = bhavdf.to_csv('C:\\Work\\OI\\FutData\\Clean\\'+filename, header=['Symbol', 'Date', 'OI'],columns=[' Symbol', 'TIMESTAMP',''],index=False)
            options = ['FUTIDX', 'FUTSTK']
            #rslt_df = bhavdf.loc[bhavdf['INSTRUMENT'].isin(options)] 

            #rslt_df =(bhavdf.loc[(((bhavdf['INSTRUMENT'] == 'FUTIDX') & (bhavdf['SYMBOL'] == 'BANKNIFTY' | bhavdf['SYMBOL'] == 'NIFTY')) | (bhavdf['INSTRUMENT'] == 'FUTSTK'))])                    
            rslt_df =bhavdf.loc[(((bhavdf['INSTRUMENT'] == 'FUTIDX') & ((bhavdf['SYMBOL'] == 'BANKNIFTY') | (bhavdf['SYMBOL'] == 'NIFTY') ) ) | (bhavdf['INSTRUMENT'] == 'FUTSTK')) ]                    
                
                #rslt_df =bhavdf[(bhavdf['Salary_in_1000']>=100) & (bhavdf['Age']<60) & bhavdf['FT_Team'].str.startswith('S')]

            #csv_data = rslt_df.to_csv('C:\\Work\\OI\\FutData\\Clean\\'+filename, header=['Symbol', 'Date', 'OI'],columns=[' Symbol', 'TIMESTAMP',''],index=False)
            csv_data = rslt_df.to_csv('C:\\Work\\OI\\Daily\\Temp\\'+filename, index=False)

    except Exception as ex:
        print(ex)

### COI ReProcess data

    filename = filename= "/fo" + start_date.strftime('%d') + start_date.strftime('%B').upper()[:3] + start_date.strftime('%Y') + "bhav.csv"
    print (filename)
    
    try:
        if path.exists('C:\\Work\\OI\\Daily\\Temp\\'+filename):
            bhavdf = pd.read_csv('C:\\Work\\OI\\Daily\\Temp\\'+filename, parse_dates=['TIMESTAMP'])
            #bhavdf['Date'] = bhavdf['Date'].apply(lambda x: x.strftime('%Y%m%d'))
            #print(bhavdf.head())
            #for col in bhavdf.columns:
            #    print(col)
            #csv_data = bhavdf.to_csv('C:\\Work\\OI\\FutData\\Clean\\'+filename, header=['Symbol', 'Date', 'OI'],columns=[' Symbol', 'TIMESTAMP',''],index=False)
            options = ['FUTIDX', 'FUTSTK']
            #rslt_df = bhavdf.loc[bhavdf['INSTRUMENT'].isin(options)] 

            #rslt_df =(bhavdf.loc[(((bhavdf['INSTRUMENT'] == 'FUTIDX') & (bhavdf['SYMBOL'] == 'BANKNIFTY' | bhavdf['SYMBOL'] == 'NIFTY')) | (bhavdf['INSTRUMENT'] == 'FUTSTK'))])                    
            rslt_df =bhavdf.loc[(((bhavdf['INSTRUMENT'] == 'FUTIDX') & ((bhavdf['SYMBOL'] == 'BANKNIFTY') | (bhavdf['SYMBOL'] == 'NIFTY') ) ) | (bhavdf['INSTRUMENT'] == 'FUTSTK')) ]                    
                
                #rslt_df =bhavdf[(bhavdf['Salary_in_1000']>=100) & (bhavdf['Age']<60) & bhavdf['FT_Team'].str.startswith('S')]

            #csv_data = rslt_df.to_csv('C:\\Work\\OI\\FutData\\Clean\\'+filename, header=['Symbol', 'Date', 'OI'],columns=[' Symbol', 'TIMESTAMP',''],index=False)
            col_names =  ['SYMBOL','DATE','OPEN','HIGH','LOW','CLOSE','VOLUME','OI']
            my_df  = pd.DataFrame(columns = col_names)
            mySymbol='a'
            for ind in rslt_df.index:
                coi = rslt_df.loc[rslt_df['SYMBOL'] == rslt_df['SYMBOL'][ind], 'OPEN_INT'].sum()
                #print(rslt_df['TIMESTAMP'][ind], rslt_df['SYMBOL'][ind], rslt_df['OPEN'][ind], rslt_df['HIGH'][ind], rslt_df['LOW'][ind], rslt_df['CLOSE'][ind],coi)
                if mySymbol != rslt_df['SYMBOL'][ind] :
                    mySymbol = rslt_df['SYMBOL'][ind]
                    my_df.loc[len(my_df)] = [ rslt_df['SYMBOL'][ind], rslt_df['TIMESTAMP'][ind], rslt_df['OPEN'][ind], rslt_df['HIGH'][ind], rslt_df['LOW'][ind], rslt_df['CLOSE'][ind], rslt_df['CONTRACTS'][ind],coi]

            csv_data = my_df.to_csv('C:\\Work\\OI\\Daily\\Clean\\'+filename, index=False)

    except Exception as ex:
        print(ex)

### Delivery Process data

    filename = "MTO_" + getDateString(start_date) + ".DAT"
    print (filename)
    
    try:
        if path.exists('C:\\Work\\OI\\Daily\\'+filename):
            bhavdf = pd.read_csv('C:\\Work\\OI\\Daily\\'+filename,skiprows = 3)
            bhavdf['Date'] = start_date.strftime('%Y%m%d')
            options = ['EQ']
            rslt_df = bhavdf.loc[bhavdf['Name of Security'].isin(options)]                     
            #print(bhavdf.head())
            #for col in bhavdf.columns:
            #    print(col)
            csv_data = rslt_df.to_csv('C:\\Work\\OI\\Daily\\Clean\\'+filename, header=['Symbol', 'Date', 'Aux1'],columns=['Sr No', 'Date','Deliverable Quantity(gross across client level)'],index=False)
    except Exception as ex:
        print(ex)

