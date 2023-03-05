import pandas as pd
import numpy as np

df = pd.read_csv('PythonDB/PumpData.csv')
df['Open_Time'] = pd.to_datetime(df['Open_Time']) #Converting to datetime
df['Close_Time'] = pd.to_datetime(df['Close_Time']) #Converting to datetime
df['Close_Time'] = (df['Close_Time'].view(np.int64) / int(1e6)).map(int)#Switching to epoch timestamp (switch back later...) 
df['Open_Time'] = (df['Open_Time'].view(np.int64) / int(1e6)).map(int)#Switching to epoch timestamp (switch back later...) 
df = df.drop(columns=['Unnamed: 0'])
df.to_json('PumpData.json', orient='records')
print(df)
