import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from pandas import ExcelWriter #directly write it into an excel spreadsheet

yf.pdr_override()
start = dt.datetime(2017,12,1)
now = dt.datetime.now()

root = Tk() #create a Tk object
ftypes = [(".xlsm", "*.xlsx", ".xls")] #specifies what type of files the dialog box can accept
ttl = "Title" #part of path
dir1 = 'C:\\' #part of path
filePath = askopenfilename(filetypes = ftypes, initialdir = dir1, title = ttl) #create the filepath using the interface
#filePath=r"C:\Users\megha\Documents\KIW\Twitter\1-24-2020\MeghanStocks.xlsx"

stocklist = pd.read_excel(filePath)
#stocklist = stocklist.head()
#creating a pandas dataframe with these column names
exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA", "150 Day MA", "200 Day MA", "52 Week Low", "52 Week High"])
#will output stocks that meet the criteria to an excel spreadsheet
for i in stocklist.index:
    stock = str(stocklist["Symbol"][i])
    RS_Rating=stocklist["RS Rating"][i]

    try:
        #create another pandas dataframe that accesses the open, high, low, adj close, etc
        #calculate the 50 day, 150 day, and 200 day MA
        df = pdr.get_data_yahoo(stock, start, now)

        smaUsed = [50,150,200]
        for x in smaUsed:
            sma=x
            df["SMA_"+str(sma)]=round(df.iloc[:4].rolling(window=sma).mean(),2) #calculating the 3 diff simple moving averages very quickly

        currentClose = df["Adj Close"][-1] #most recent adj close in the yf database
        moving_average_50=df["SMA_50"][-1]
        moving_average_150=df["SMA_150"][-1]
        moving_average_200=df["SMA_200"][-1]
        low_of_52week=min(df["Adj Close"][-260:]) #taking the last 260 adj close & finding min value
        high_of_52week=max(df["Adj Close"][-260:])

        try:
            #need 200 sma to be trending up for at least 1 month
            moving_average_200_20past=df["SMA_200"][-20] #twenty days past
        except Exception:
            moving_average_200_20past=0 #if throws an error, set avg to 0

        print("Checking "+stock+".....")

        #Condition 1: Current Price > 150 SMA and > 200 SMA
        if(currentClose>moving_average_50 and currentClose>moving_average_200):
            cond_1=True
        else:
            cond_1=False
        #Condition 2: 150 SMA and > 200 SMA
        if(moving_average_150>moving_average_200):
            cond_2=True
        else:
            cond_2=False
        #Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
        if(moving_average_200>moving_average_200_20past):
            cond_3=True
        else:
            cond_3=False
        #Condition 4: 50 SMA > 150 SMA and 50 SMA > 200 SMA
        if(moving_average_50>moving_average_150 and moving_average_50 > moving_average_200):
            cond_4=True
        else:
            cond_4=False
        #Condition 5: Current Price > 50 SMA
        if(currentClose>moving_average_50):
            cond_5=True
        else:
            cond_5=False
        #Condition 6: Current Price is at least 30% above 52 week low (Many of the best are up 100-30)
        if(currentClose>(1.3*low_of_52week)):
            cond_6=True
        else:
            cond_6=False
        #Condition 7: Current Price is within 25% of 52 week high
        if(currentClose>=(.75*high_of_52week)):
            cond_7=True
        else:
            cond_7=False
        #Condition 8: IBD RS rating > 70 and the higher the better
        if(RS_Rating>70):
            cond_8=True
        else:
            cond_8=False

        if(cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6 and cond_7 and cond_8):
            exportList = exportList.append({'Stock': stock, "RS_Rating": RS_Rating, "50 Day MA": moving_average_50, "150 Day MA": moving_average_150, "200 Day MA": moving_average_200, "52 Week Low": low_of_52week, "52 Week High": high_of_52week})
    except Exception:
        print("No data on "+stock)

print(exportList)

newFile = os.path.dirname(filePath)+"/ScreenOutput.xlsx"

writer=ExcelWriter(newFile)
#exportList is the pandas dataframe that we want to convert
exportList.to_excel(writer, "Sheet1")
writer.save()