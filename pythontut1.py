#Looking at if Close is higher/lower than moving avg (50 day)
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

stock=input("Enter a stock ticker symbol: ")
print(stock)

startyear=2019
startmonth=1
startday=1

start=dt.datetime(startyear,startmonth,startday)

now=dt.datetime.now()

df=pdr.get_data_yahoo(stock,start,now) #dataframe

ma=50 #moving average (50 days)

smaString="Sma_"+str(ma) 

df[smaString]=df.iloc[:,4].rolling(window=ma).mean()
#creating column with name smaString, column is our rolling moving avg
#with a window size of our moving avg (50 days)
#made from our 4th column in the df (our adj close)

df=df.iloc[ma:]
#get rid of first 50 days when don't have moving avg
#start at 3/15 instead of 1/1

numH=0
numC=0

#i is the date
for i in df.index:
    #print(df.iloc[:,4][i])
    #print(df["Adj Close"][i])
    #print the adj close (4th column) for each date(i)
    #print(df[smaString][i])
    if(df["Adj Close"][i]>df[smaString][i]):
        print("The Close is higher")
        numH+=1
    else:
        print("The Close is lower")
        numC+=1
print("Close is higher: "+ str(numH)+ " times")
print("Close is lower: " + str(numC)+ " times")
