
from supabase import create_client, Client as SupaBaseClient
import os
from keras.utils import normalize
from concurrent.futures import ThreadPoolExecutor
import random
import time
import json
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests import Session
import pickle
import numpy as np
import pandas as pd
import re  # Using RegEx to filter through the symbols.
import schedule
from datetime import datetime, timedelta

# Binance library and client (no API key required).
from binance import Client
client = Client()

url: str = "https://tlzdgevojpvplmjxfufr.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRsemRnZXZvanB2cGxtanhmdWZyIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzgxNTU3MTMsImV4cCI6MTk5MzczMTcxM30.qEO7kWnMn93hjVSm3opkSZ5a2BDS48ef34cc4RgkCz8"
supabase: SupaBaseClient = create_client(url, key)

_15minInMs = 900000

def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta

def getBinanceSymbols(symbol='BTC'):
    # ---------- Finding all market pairs from Binance, REGEXing them, and placing them into a list:
    symbols = []
    exchange_info = client.get_exchange_info()
    for s in exchange_info['symbols']:
        # REGEX FOR ENDING WITH BTC (AS VAST MAJORITY OF PUMPS ARE IN BTC)
        pattern = ".*%s$" % (symbol)
        if (re.search(pattern, s['symbol'])):
            symbols.append(s['symbol'])
    symbols = sorted(symbols)  # Done for convenience...
    return (symbols)

# ---------- Used to get somne random windows from all tokens - to help with balancing data with no just pumped tokens.

def getGeneralBinanceData(lagBefore, observations, start, finish):
    # ---------- Finding all market pairs from Binance, REGEXing them, and placing them into a list:
    # Splitting symbols into three lists. [[aBSD, SDAS, SAD], [], ...]
    symbolsList = getBinanceSymbols()
    dfReturned = pd.DataFrame()

    # Multithreading to get the job done faster.
    futures = []
    for symbol in symbolsList:
        future = ThreadPoolExecutor(len(symbolsList)).submit(
            getSymbolsData, symbol, (start - (_15minInMs * (lagBefore + observations))), finish)
        futures.append(future)
    for future in futures:
        df = addIntrinsicFeatures(lagBefore, future.result())
        # Concatinate to parent dataframe
        dfReturned = pd.concat([dfReturned, df])
    return dfReturned

# ---------- Used to get a snapshot of the symbols data in 1 min time interval


def getSymbolsData(symbol, start, finish, interval='15m'):
    time.sleep(random.random() * 45)
    start = str(start)
    finish = str(finish)

    # First ever pump on binance was on 06/09/2018
    klines = client.get_historical_klines(
        ""+symbol+"", interval, start_str=start, end_str=finish)
    df = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                      'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df = df.drop(columns=['Ignore'])  # Dropping unneeded columns
    # Renaming columns...
    df = df.rename(columns={'Open time': 'Open_Time', "Close": "Close_Price", "Close Time": "Close_Time",
                   "Quote asset volume": "BTC_Volume", "Number of trades": "Trades", 'Volume': 'Asset_Volume'})
    # Adding symbol name to columns...
    df.insert(0, column='Symbol', value=symbol)

    # Time related features - note we are data engineering
    df['Open_Time'] = pd.to_datetime(
        df['Open_Time'], origin='unix', unit='ms')  # Converting to datetime
    df['Close_Time'] = pd.to_datetime(
        df['Close_Time'], origin='unix', unit='ms')  # Converting to datetime
    # Converting numerical columns to numerical datatypes...
    df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['High'] = pd.to_numeric(
        df['High'], errors='coerce')  # converting to numeric
    # converting to numeric...
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
    # Converting numerical columns to numerical datatypes...
    df['Close_Price'] = pd.to_numeric(df['Close_Price'], errors='coerce')
    df['Asset_Volume'] = pd.to_numeric(
        df['Asset_Volume'], errors='coerce')  # converting to numeric
    # converting to numeric...
    df['BTC_Volume'] = pd.to_numeric(df['BTC_Volume'], errors='coerce')
    # Converting numerical columns to numerical datatypes...
    df['Trades'] = pd.to_numeric(df['Trades'], errors='coerce')
    df['Taker buy base asset volume'] = pd.to_numeric(
        df['Taker buy base asset volume'], errors='coerce')  # converting to numeric
    df['Taker buy quote asset volume'] = pd.to_numeric(
        df['Taker buy quote asset volume'], errors='coerce')  # converting to numeric...

    df = df.dropna()  # Dropping all rows with NAN's... As 4 days is the max amount of consecutive NAN's, we will lose 4 days at the start of every datapull. SNAPSHOT NEEDS TO BE A MINIMUM OF 96 HOURS(4 DAYS)
    return df


def addIntrinsicFeatures(lagBefore, df):
    # ensuring there is enough data for 99m to be returned
    for lag in range(1, int((lagBefore / 2) + 1)):
        inhours = lag * 0.25

        # Adding log returns, used log returns as it's additative, and can be used in combination with volatility measures below...
        df['logReturns%sH' % (inhours)] = np.log(
            df['Close_Price']/df['Close_Price'].shift(lag))
        # Creating volatility, note that it's s+1 as log returns is already formed from a rolling (thus 1 s.d is lost) (Volatility is calculated in standard errors)
        df['volLogReturns%sH' % (inhours)] = df['logReturns%sH' %
                                                (inhours)].rolling(lag+1).std()

        df['volumeBTCfrom%sH' % (inhours)] = df['BTC_Volume'].rolling(
            lag).sum()  # Adding rolling window sum of volume
        # Creating volatility, note that it's s+1 as log returns is already formed from a rolling (thus 1 s.d is lost)
        df['volVolumeBTCfrom%sH' %
            (inhours)] = df['volumeBTCfrom%sH' % (inhours)].rolling(lag+1).std()

        df['volumeASSETfrom%sH' %
            (inhours)] = df['Asset_Volume'].rolling(lag).sum()
        # Creating volatility, note that it's s+1 as log returns is already formed from a rolling (thus 1 s.d is lost)
        df['volVolumeASSETfrom%sH' %
            (inhours)] = df['volumeASSETfrom%sH' % (inhours)].rolling(lag+1).std()

        # Time related features - note we then observe these times are cyclical features and apply cosine, sine etc.
        df['Open_Time_day'] = df['Open_Time'].dt.day
        df['Open_Time_hour'] = df['Open_Time'].dt.hour
        df['Open_Time_minute'] = df['Open_Time'].dt.minute
        df['Open_Time_dayofweek'] = df['Open_Time'].dt.dayofweek
    df = df.dropna(how='any')
    print(df)
    return df

# ---------- PULLING PRESENT MARKET DATA/SOCIO-ECONOMIC DATA FROM COINMARKETCAP
def getDataCMC():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '3',
        'limit': '5000',
        'convert': 'USD'
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
        dfMarketCap = dfMarketCap[[
            'symbol', 'quote.USD.fully_diluted_market_cap', 'num_market_pairs', 'cmc_rank']]
        dfMarketCap['symbol'] = dfMarketCap['symbol'].astype(str) + 'BTC'
        dfMarketCap = dfMarketCap.rename(
            columns={'symbol': 'Symbol', "quote.USD.fully_diluted_market_cap": "MktCapUSD"})
        dfMarketCap = dfMarketCap.sort_values("Symbol")  # Sort columns...
        # Sort columns by market cap.. keeping second(largest market cap of duplicate)
        dfMarketCap = dfMarketCap.sort_values("MktCapUSD")
        dfMarketCap = dfMarketCap.drop_duplicates(subset="Symbol", keep="last")
        return (dfMarketCap)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


# ---------- Aggregating both as our dataset, We use multithreading here to speed up the process..
def getAggregateData(lagBefore=192, lagAfter=0):
    print('-------------Downloading General Data -------')
    # 5 random recent times to sample all market data

    # Randomly sampled over the last 7 years (these are the timestamps) - done for each token 30 times to get a fair representation of it's market behaviour over the time.
    timeGiven = int(time.time_ns() / 1000000) - _15minInMs + 1 #Pulled back 15 mins to ensure we get ALL data
    generalDF = getGeneralBinanceData(lagBefore, 1, timeGiven, timeGiven)
    print(generalDF)

    # Adding Market Cap Data
    dfMarketCap = getDataCMC()
    # NEEDS RE-EVALUATING, AND MERGING ON DATES TOO! - SAME CLOSE TIMES BUT WITH DIFFERENT MARKET CAPS! LOOK INTO IT.
    condensedDF = pd.merge(dfMarketCap, generalDF, on='Symbol', validate="1:m")
    return condensedDF


def repeatedProcess():
    try:
        Time = str(ceil_dt(datetime.now(), timedelta(minutes=15)))
        df = getAggregateData() #Retrieving current data
        #df=pd.read_csv('NewData.csv', index_col=0)
        dfSymbol = df['Symbol']  # Keeping the symbol column for after
        df = normalize(df.drop(columns=['Close_Time', 'Symbol', 'Open_Time']), axis=1)

        # Importing Model That We Use
        XGBoost = pickle.load(open("PythonDB/Models/XGBoost.sav", "rb"))
        y_predict_proba = XGBoost.predict_proba(df)
        probability = pd.DataFrame({"Symbol": list(dfSymbol), "Probability": list(y_predict_proba)})
        probability['Probability'] = probability['Probability'].str[1] * 100
        probability = probability.sort_values('Probability', ascending=False).head(4)

        print('--------- NEW PUMP PREDICTION ---------')
        print(Time)
        print(probability)

        # Iterating over 4 most likely probabilities and sending them off to the database.
        supabase.table('Probabilities').insert({
            'Time': Time,
            'Coin_1': probability.iloc[0, 0], 'Coin_1_Prob': str(probability.iloc[0, 1]),
            'Coin_2': probability.iloc[1, 0], 'Coin_2_Prob': str(probability.iloc[1, 1]),
            'Coin_3': probability.iloc[2, 0], 'Coin_3_Prob': str(probability.iloc[2, 1]),
            'Coin_4': probability.iloc[3, 0], 'Coin_4_Prob': str(probability.iloc[3, 1]),
        }).execute()
    except:
        print('An error occured')

if __name__ == "__main__":

    #Creating repeating functions as to keep updating the predictions to the database. 
    repeatedProcess()
    schedule.every(1).hours.at(":00").do(repeatedProcess)
    schedule.every(1).hours.at(":15").do(repeatedProcess)
    schedule.every(1).hours.at(":30").do(repeatedProcess)
    schedule.every(1).hours.at(":45").do(repeatedProcess)
    #repeatedProcess()
    while True:
        schedule.run_pending()
        time.sleep(1)
