#Yahoo Finance & Moving Averages
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

# ma=50 

# smaString="Sma_"+str(ma) 

# df[smaString]=df.iloc[:,4].rolling(window=ma).mean()

emasUsed=[3,5,8,10,12,15,30,35,40,45,50,60]
for x in emasUsed:
    ema=x
    df["Ema_"+str(ema)]=round(df.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)

print(df.tail())

pos=0 #enter if 1 (not entered if 0) use to determine if we are entering a position
num=0 #keep track of row we are on
percentchange=[] #empty list, add results of our trade in

for i in df.index:
    cmin=min(df["Ema_3"][i],df["Ema_5"][i],df["Ema_8"][i],df["Ema_10"][i],df["Ema_12"][i],df["Ema_15"][i])
    cmax=min(df["Ema_30"][i],df["Ema_35"][i],df["Ema_40"][i],df["Ema_45"][i],df["Ema_50"][i],df["Ema_60"][i])

    close=df["Adj Close"][i]

    #if we are in a red white blue pattern
    if(cmin>cmax):
        print("Red White Blue")
        if(pos==0):
            bp=close #buy price
            pos=1 #turning on our position
            print("Buying now at "+str(bp))

    elif(cmin<cmax):
        print("Blue White Red")
        if(pos==1):
            pos=0
            sp=close #sell price
            print("Selling now at "+str(sp))
            pc=(sp/bp-1)*100 #calculate percent change
            percentchange.append(pc) #store percent change in list
    if(num==df["Adj Close"].count()-1 and pos==1): #simulate closing out our position
        pos=0
        sp=close 
        print("Selling now at "+str(sp))
        pc=(sp/bp-1)*100 
        percentchange.append(pc) 

    num+=1

print(percentchange)

gains=0
ng=0 #number of gains
losses=0
nl=0 #number of losses
totalR=1 #total return

for i in percentchange:
    if(i>0): #if a winning trade
        gains+=i
        ng+=1
    else:
        losses+=i
        nl+=1
    totalR=totalR*((i/100)+1)

totalR=round((totalR-1)*100,2) #look nicer to user

if(ng>0):
    avgGain=gains/ng
    maxR=str(max(percentchange))#find best trade
else:
    avgGain=0
    maxR="undefined"

if(nl>0):
    avgLoss=losses/nl
    maxL=str(min(percentchange))#find worst trade
    ratio=str(-avgGain/avgLoss)
else:
    avgLoss=0
    maxL="undefined"
    ratio="inf"

if(ng>0 or nl>0):
    battingAvg=ng/(ng+nl)
else:
    battingAvg=0

print()
print("Results for "+ stock +" going back to "+str(df.index[0])+", Sample size: "+str(ng+nl)+" trades")
print("EMAs used: "+str(emasUsed))
print("Batting Avg: "+str(battingAvg))
print("Gain/loss ratio: "+ ratio)
print("Average Gain: "+ str(avgGain))
print("Average Loss: "+ str(avgLoss))
print("Max Return: "+ maxR)
print("Max Loss: "+ maxL)
print("Total return over "+str(ng+nl)+" trades: "+str(totalR)+"%")
print()
