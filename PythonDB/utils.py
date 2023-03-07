import pandas as pd
import numpy as np
import datetime

#df = pd.read_csv('PythonDB/PumpData.csv')
#df['Open_Time'] = pd.to_datetime(df['Open_Time']) #Converting to datetime
#df['Close_Time'] = pd.to_datetime(df['Close_Time']) #Converting to datetime
#df['Close_Time'] = (df['Close_Time'].view(np.int64) / int(1e6)).map(int)#Switching to epoch timestamp (switch back later...) 
#df['Open_Time'] = (df['Open_Time'].view(np.int64) / int(1e6)).map(int)#Switching to epoch timestamp (switch back later...) 
#df = df.drop(columns=['Unnamed: 0'])
#df.to_json('PumpData.json', orient='records')
#print(df)

print(datetime.datetime.now() + datetime.timedelta(minutes=15))
from datetime import datetime, timedelta

def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta

print(ceil_dt(datetime.now(), timedelta(minutes=15)))

def split_list(alist, wanted_parts=1):  #Splitting the data up so it can be downloading without placing intense workloads on RAM
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] for i in range(wanted_parts) ]

def getMins(time):
    return(int(time[:-3]))

def getSecs(time):
    return(int(time[3:]))
