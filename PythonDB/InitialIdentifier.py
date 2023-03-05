# Procedure: 1) Get 38 Month Binance DATA, Merge All Pumps Data with it, Merge CoinMarketCap data with it, 
# 1) Retreive 38 months of data
from calendar import month
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re #Using RegEx to filter through the symbols. 
from multiprocessing import Process, Queue

# Binance library and client (no API key required).
from binance import Client
client = Client()

# ----------- This app gets a few months worth of minute data for each coin, and identifies if there was any pumps on them...  
def getBinanceSymbols(symbol = 'BTC'):
    
    # ---------- Finding all market pairs from Binance, REGEXing them, and placing them into a list:
    symbols = []
    exchange_info = client.get_exchange_info()
    for s in exchange_info['symbols']:
     pattern = ".*%s$" % (symbol) #REGEX FOR ENDING WITH BTC (AS VAST MAJORITY OF PUMPS ARE IN BTC)
     if (re.search(pattern, s['symbol'])): 
         symbols.append(s['symbol'])
    symbols = sorted(symbols) #Done for convenience...
    return(symbols)

# ---------- Used to get a snapshot of the symbols data in 1 min time interval
def getSymbolsData(symbol):

    #
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_15MINUTE, "6 year ago UTC") # First ever pump on binance was on 06/09/2018 
    df = pd.DataFrame(klines, columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df = df.rename(columns={'Open time': 'Open_Time', "Close": "Close_Price", "Close Time": "Close_Time", "Quote asset volume": "BTC_Volume", "Number of trades": "Trades", 'Volume': 'Asset_Volume'}) # Renaming columns...
    df.insert(0, column='Symbol', value=symbol)   # Adding symbol name to columns...
    
    #Time related features - note we are data engineering 
    df['Open_Time'] = pd.to_datetime(df['Open_Time'], origin='unix', unit='ms') #Converting to datetime
    df['Close_Time'] = pd.to_datetime(df['Close_Time'], origin='unix', unit='ms') #Converting to datetime
    df['Open'] = pd.to_numeric(df['Open'], errors='coerce') # Converting numerical columns to numerical datatypes... 
    df['High'] = pd.to_numeric(df['High'], errors='coerce') # converting to numeric
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce') # converting to numeric...
    df['Close_Price'] = pd.to_numeric(df['Close_Price'], errors='coerce') # Converting numerical columns to numerical datatypes... 
    df['Asset_Volume'] = pd.to_numeric(df['Asset_Volume'], errors='coerce') # converting to numeric
    df['BTC_Volume'] = pd.to_numeric(df['BTC_Volume'], errors='coerce') # converting to numeric...
    df['Trades'] = pd.to_numeric(df['Trades'], errors='coerce') # Converting numerical columns to numerical datatypes... 
    df['Taker buy base asset volume'] = pd.to_numeric(df['Taker buy base asset volume'], errors='coerce') # converting to numeric
    df['Taker buy quote asset volume'] = pd.to_numeric(df['Taker buy quote asset volume'], errors='coerce') # converting to numeric...
            
    df = df.dropna() #Dropping all rows with NAN's... As 4 days is the max amount of consecutive NAN's, we will lose 4 days at the start of every datapull. SNAPSHOT NEEDS TO BE A MINIMUM OF 96 HOURS(4 DAYS)    
    return df #commit

# ------------ Getting 2 months of minute data for all symbols. 
def addMovingAvCheckThresh(df, window):
    
    #Adding the MA column with our needed window 
    df['volumeMA_' + str(window)] = df['BTC_Volume'].rolling(window).mean()

    #Adding our threshold, adding our check that the time is less than 5 mins after the hour.  
    thresholdVolume = 150
    thresholdPercAboveOpen = 10
    thresholdTime = 10 #Require minimum 5 mins after hour.
    thresholdPecCloseBelowHigh = 20 # require 50% lower than high
    timeAfterHour = df['Open_Time'].dt.minute
    percAboveOpen = 100 * (df['High'] - df['Open']) / df['Open']
    percentCloseBelowHigh = - 100 * (df['Close_Price'] - df['High']) / df['High']
    percAboveVol = 100 * (df['BTC_Volume'] - df['volumeMA_' + str(window)]) / df['volumeMA_' + str(window)]
    df['hasPumped'] = np.where(
       (percAboveOpen >= thresholdPercAboveOpen) & 
       (percAboveVol >= thresholdVolume) & 
       (timeAfterHour <= thresholdTime) &
       (percentCloseBelowHigh >= thresholdPecCloseBelowHigh)
       , 1, 0)
    df = df.drop(columns=['volumeMA_' + str(window)])
    return df

# ----------- Getting 2 months of minute data for all symbols. 
import random
def checkMAThresh(i):
   time.sleep(random.random() * 10 * 60)
   df = addMovingAvCheckThresh(getSymbolsData(i), 12)
   df = df.loc[df['hasPumped'] == 1]
   df = df.drop(columns=['hasPumped'])
   print('----------------- ' + i + '  ----------------------------------')
   print(df)
   return df

from concurrent.futures import ThreadPoolExecutor
import time
if __name__ == "__main__":
  dfMain = pd.DataFrame()
  symbols = getBinanceSymbols()
  print(len(symbols))
  executor = ThreadPoolExecutor(12)
  futures = []
  for symbol in symbols:
     future = executor.submit(checkMAThresh, (symbol))
     futures.append(future)
  for future in futures:
     dfMain = pd.concat([dfMain, future.result()])
  print(dfMain)
  dfMain.to_csv('PumpData.csv')
