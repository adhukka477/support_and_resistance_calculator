# import necessary libraries

import pandas as pd
import numpy as np
from datetime import datetime as dt
import datetime
from urllib.request import Request, urlopen 
from time import mktime
from bs4 import BeautifulSoup
import io


class Ticker():
  
    def __init__(self, ticker, start, end = dt.timestamp(dt.now()), interval = 'd'):

        self.ticker = ticker
        self.interval = interval
        self.start = int(dt.timestamp(dt.strptime(start, "%Y-%m-%d")))
        self.end = int(dt.timestamp(dt.strptime(end, "%Y-%m-%d")))


        if str(self.interval).lower() == 'd':
            self.df = self.getDailyData()
        elif str(self.interval).lower() == 'm':
            self.df = self.getMonthlyData()
        elif str(self.interval).lower() == 'w':
            self.df = self.getWeeklyData()
        else:
            self.df = self.getDailyPrice()

    # get stock prices using yfinance library
    def getDailyData(self):

        url = "https://query1.finance.yahoo.com/v7/finance/download/" + self.ticker +\
              "?period1=" + str(self.start)+\
              "&period2=" + str(self.end)+\
              "&interval=1d"+\
              "&events=history&includeAdjustedClose=true"

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req)
        soup = BeautifulSoup(html, "html.parser")
        df = pd.read_csv(io.StringIO(soup.text), sep=",")

        df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close', "Volume"]]
        
        return(df)
    
    def getWeeklyData(self):
        # Load the daily stock data into a DataFrame
        df = self.getDailyData()
        # Convert the Date column to a datetime index
        df.index = pd.to_datetime(df['Date'])

        # Resample the data to weekly frequency and calculate the mean, max, min, first, and last
        df_weekly = df.resample('W').agg(['sum', 'max', 'min', 'first', 'last'])

        date = pd.to_datetime(df_weekly.index).tz_localize(None)
        date = date + datetime.timedelta(days = -6)
        open = df_weekly.Open["first"]
        high = df_weekly.High["max"]
        low = df_weekly.Low["min"]
        close = df_weekly.Close["last"]
        volume = df_weekly.Volume["sum"]

        df_weekly = pd.DataFrame(zip(date, open, high, low, close, volume), columns=['Date', 'Open', 'High', 'Low', 'Close', "Volume"])

        return df_weekly
    
    def getMonthlyData(self):

        # Load the daily stock data into a DataFrame
        df = self.getDailyData()
        # Convert the Date column to a datetime index
        df.index = pd.to_datetime(df['Date'])

        # Resample the data to monthly frequency and calculate the mean, max, min, first, and last
        df_monthly = df.resample('M').agg(['sum', 'max', 'min', 'first', 'last'])

        date = pd.to_datetime(df_monthly.index).tz_localize(None)
        date = date + datetime.timedelta(days=-30)
        open = df_monthly.Open["first"]
        high = df_monthly.High["max"]
        low = df_monthly.Low["min"]
        close = df_monthly.Close["last"]
        volume = df_monthly.Volume["sum"]

        df_monthly = pd.DataFrame(zip(date, open, high, low, close, volume), columns=['Date', 'Open', 'High', 'Low', 'Close', "Volume"])

        return df_monthly
