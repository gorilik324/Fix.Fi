# Procedure: 1) Get 38 Month Binance DATA, Merge All Pumps Data with it, Merge CoinMarketCap data with it, 
# 1) Retreive 38 months of data
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re #Using RegEx to filter through the symbols. 
import time
import datetime

# Binance library and client (no API key required).
from binance import Client
client = Client()

# This app gets the previous mins OHLC data, formats it with a a MA, checks if the latest close %(price + vol) > threshold, if so label 1, if not label 0. 
# Then submit to the DB - for reading by the webapp. 

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
def getSymbolsData(symbol, start, finish):

    klines = client.get_historical_klines(symbol=""+symbol+"", interval=Client.KLINE_INTERVAL_1MINUTE) # First ever pump on binance was on 06/09/2018 
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
    print(df)
    return df

# Need to get the previous minute, then cycle through all tokens and get their current price. 
for i in getBinanceSymbols():
    getSymbolsData(i, 1580518860000, 1580518860000)
