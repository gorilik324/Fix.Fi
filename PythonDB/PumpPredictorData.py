# Procedure: 1) Get windows around pump data, and random windows, calculate intrinsic features, add external data like market-cap and export.
# 1) Retreive 38 months of data
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re #Using RegEx to filter through the symbols. 

# Binance library and client (no API key required).
from binance import Client
client = Client()
import datetime

# For coinmarketcap parsing
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor


#Splitlist from utils
from utils import split_list

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

# ---------- Used to get somne random windows from all tokens - to help with balancing data with no just pumped tokens. 
def getGeneralBinanceData(lagBefore, observations, start, finish, symbolListQuantity = 1):
    # ---------- Finding all market pairs from Binance, REGEXing them, and placing them into a list:
    symbolsLists = split_list(getBinanceSymbols(), wanted_parts=symbolListQuantity) #Splitting symbols into three lists. [[aBSD, SDAS, SAD], [], ...]
    _15minInMs = 900000

    # ---------- GETTING THE DATASET:
    countParts = 0
    dfmain = pd.DataFrame()
    for symbolList in symbolsLists:
        count = 0
        for symbol in symbolList:
            #Generating a random time within the period
            date = start + round((finish - start) * random.random())
            df = getSymbolsData(symbol, (date - (_15minInMs * (lagBefore + observations))), date)
            df = addIntrinsicFeatures(lagBefore, df)
            df['willPump'] = 0
            dfmain = pd.concat([dfmain, df]) #Concatinate to parent dataframe
            count = count + 1
            print("%s/%s %s" % (count, len(symbolList), symbol))
        countParts = countParts + 1
    # ---------- Consolidating all fractional datasets:
    print(dfmain)
    return dfmain

# ---------- Used to get a snapshot of the symbols data in 1 min time interval
def getSymbolsData(symbol, start, finish, interval='15m'):
    start = str(start)
    finish = str(finish)

    klines = client.get_historical_klines(""+symbol+"", interval, start_str=start, end_str=finish) # First ever pump on binance was on 06/09/2018 
    df = pd.DataFrame(klines, columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df = df.drop(columns=['Ignore']) # Dropping unneeded columns
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
    return df

# ---------- Takes windows around pump time for the respective token, 
def getPumpDataWindows(lagBefore, lagAfter, interval = '1m'):
    dfPump = pd.read_csv('PythonDB/PumpData.csv', index_col=0)
    dfPump['Open_Time'] = pd.to_datetime(dfPump['Open_Time']) - datetime.timedelta(minutes=15)  #We remove 15 mins to recieve the market state BEFORE the pump...
    dfPump['Open_Time'] = (dfPump['Open_Time'].view(np.int64) / int(1e6)).map(int)#Switching to epoch timestamp (switch back later...) 
    ms_to_min15Min = 900000
    timeSubtractor = 1
    dfMain = pd.DataFrame()
    #Iterating over each pump event...
    count = 0 
    for index, row in dfPump.iterrows():
      print(str(count) + '/' + str(len(dfPump.index)) + ' of all pump windows')
      count += 1
      df = addIntrinsicFeatures(lagBefore, getSymbolsData(row['Symbol'], row['Open_Time'] - (1 + (ms_to_min15Min * (lagBefore + timeSubtractor))), row['Open_Time'] + (ms_to_min15Min * (lagAfter - timeSubtractor)))) # Adjusted to be 2 lags before - allowing 1 lag for prediction.  
      df['willPump'] = 1
      print(df)
      dfMain = pd.concat([dfMain, df], axis=0)
    
    #returning the opentime back to dateTime format.. 
    return(dfMain)    

def addIntrinsicFeatures(lagBefore, df):
    for lag in range(1, int((lagBefore / 2) + 1)): #ensuring there is enough data for 99m to be returned
        inhours = lag * 0.25

        df['logReturns%sH' % (inhours)] = np.log(df['Close_Price']/df['Close_Price'].shift(lag)) #Adding log returns, used log returns as it's additative, and can be used in combination with volatility measures below...
        df['volLogReturns%sH' % (inhours)] = df['logReturns%sH' % (inhours)].rolling(lag+1).std() #Creating volatility, note that it's s+1 as log returns is already formed from a rolling (thus 1 s.d is lost) (Volatility is calculated in standard errors)

        df['volumeBTCfrom%sH' % (inhours)] = df['BTC_Volume'].rolling(lag).sum() #Adding rolling window sum of volume
        df['volVolumeBTCfrom%sH' % (inhours)] = df['volumeBTCfrom%sH' % (inhours)].rolling(lag+1).std() #Creating volatility, note that it's s+1 as log returns is already formed from a rolling (thus 1 s.d is lost)

        df['volumeASSETfrom%sH' % (inhours)] = df['Asset_Volume'].rolling(lag).sum()
        df['volVolumeASSETfrom%sH' % (inhours)] = df['volumeASSETfrom%sH' % (inhours)].rolling(lag+1).std() #Creating volatility, note that it's s+1 as log returns is already formed from a rolling (thus 1 s.d is lost)

        df['Open_Time_day'] = df['Open_Time'].dt.day #Time related features - note we then observe these times are cyclical features and apply cosine, sine etc.
        df['Open_Time_hour'] = df['Open_Time'].dt.hour
        df['Open_Time_minute'] = df['Open_Time'].dt.minute
        df['Open_Time_dayofweek'] = df['Open_Time'].dt.dayofweek
    df = df.dropna(how='any')    
    return df

# ---------- PULLING PRESENT MARKET DATA/SOCIO-ECONOMIC DATA FROM COINMARKETCAP
def getDataCMC():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'3',
    'limit':'5000',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '7c011288-0358-43d3-b95b-0e139e738a67',
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        dfMarketCap = pd.json_normalize(data['data'])
        dfMarketCap = dfMarketCap[['symbol', 'quote.USD.fully_diluted_market_cap', 'num_market_pairs', 'cmc_rank']]
        dfMarketCap['symbol'] =  dfMarketCap['symbol'].astype(str) + 'BTC'
        dfMarketCap = dfMarketCap.rename(columns={'symbol': 'Symbol', "quote.USD.fully_diluted_market_cap": "MktCapUSD"})
        dfMarketCap = dfMarketCap.sort_values("Symbol") # Sort columns...
        dfMarketCap = dfMarketCap.sort_values("MktCapUSD") # Sort columns by market cap.. keeping second(largest market cap of duplicate)
        dfMarketCap = dfMarketCap.drop_duplicates(subset = "Symbol", keep = "last")
        return(dfMarketCap)
    except(ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    
# ---------- Aggregating both as our dataset, We use multithreading here to speed up the process..
def getAggregateData(lagBefore = 192, lagAfter = 0):
    print('-------------Downloading General Data -------')
    #5 random recent times to sample all market data

    #Randomly sampled over the last 7 years (these are the timestamps) - done for each token 30 times to get a fair representation of it's market behaviour over the time.
    quantRandomSamples = 30
    generalDF = pd.DataFrame()
    futures = []
    for i in range(quantRandomSamples):
        future = ThreadPoolExecutor(quantRandomSamples).submit(getGeneralBinanceData, lagBefore, 1, 1501160900000, 1678139051000)
        futures.append(future)
    for future in futures:
        generalDF = pd.concat([generalDF, future.result()])
        print(generalDF)

    print('-------------Downloading Window Data -------')
    windowedDF = getPumpDataWindows(lagBefore, lagAfter, '15m')
    condensedDF = pd.concat([generalDF, windowedDF])
    condensedDF = condensedDF.dropna()

    #Adding Market Cap Data
    dfMarketCap = getDataCMC()
    condensedDF = pd.merge(dfMarketCap, condensedDF, on='Symbol', validate="1:m") #NEEDS RE-EVALUATING, AND MERGING ON DATES TOO! - SAME CLOSE TIMES BUT WITH DIFFERENT MARKET CAPS! LOOK INTO IT.
    print(condensedDF)
    condensedDF.to_csv('EntireData.csv')

if __name__ == "__main__":
    getAggregateData()


