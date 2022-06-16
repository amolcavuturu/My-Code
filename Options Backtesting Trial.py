#First you will import the relevant modules in Jupyter notebook –
import nsepy
from nsepy import get_history
import datetime
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# past data saved in table 'Optionpivot' imported
Table = pd.read_csv('Optionpivot.csv')
Table['month'] = pd.to_datetime(Table['Date']).dt.strftime('%m')
#Table is created to get ATM strike at beginning of the month
Table1 = Table.groupby('month').first()
Table1['M'] = pd.to_datetime(Table1['Date']).dt.strftime('%m')
Table1['ATM_Strike'] = round(Table1['Nifty']/100)*100
# Monthly date wise prices of option strikes fetched in table 2 thru for loop and appended in table3.
Table3 = pd.DataFrame({"Date":['0'], "Close":['0'], "Expiry":['0'], "Type":['0'], "month":['0'], "ATM":
['0'], "OTM":['0'], "Ratio":['0'], "P&L":['0']})
Table4 = pd.DataFrame({"Date":['0'], "Close":['0'], "Expiry":['0'], "Type":['0'], "month":['0'], "ATM":
['0'], "OTM":['0'], "Ratio":['0'], "P&L":[0]})
for x in range (0,9):
    e = Table1.M[x]
#Value of month taken in variable ‘e’ from row x
    d = Table1.Expiry[x]
#Value of Expiry taken in variable ‘d’ from row x
    a= int((Table1.ATM_Strike[x]))
#Value of ATM strike taken in variable ‘a’ from Table1
    a = a + 200
    b = a + 200
    f1 = str(a)
#value of a converted from integer to string type
    f2 = str(b)
Table2 = pd.DataFrame({"Date": Table["Date"], "Close":
Table["Nifty"], "Expiry": Table["Expiry"], "Type": Table["Type"], "month": Table["month"], "ATM": Table[f1], "OTM": Table[f2] })
Table2= Table2.where((Table2.month == e) & (Table2.Expiry == d) & (Table2.Type == "CE"))
Table2 = Table2.dropna()
Table2['Ratio']= Table2['ATM'] -(Table2['OTM']*2)
Table2['P&L']=Table2['Ratio'].diff().cumsum()
Table3 = Table3.append(Table2)
Table4= Table4.append(Table2.where((Table2.Date == d)))
Table4 = Table4.dropna()
Table4.drop(["Date", "Close", "Expiry", "Type", "ATM", "OTM", "Ratio"], axis = 1, inplace = True)
Table4['Total_P&L']=Table4['P&L'].cumsum()
print (Table4)