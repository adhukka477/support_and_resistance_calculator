# import necessary libraries

import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime as dt
import datetime



class Ticker():
  
    def __init__(self, ticker, interval = 'd', period = 'max'):

        self.ticker = ticker
        self.interval = interval
        self.period = period

        if str(self.interval).lower() == 'd':
            self.df = self.getDailyPrice()
        elif str(self.interval).lower() == 'm':
            self.df = self.getMonthlyData()
        elif str(self.interval).lower() == 'w':
            self.df = self.getWeeklyData()
        else:
            self.df = self.getDailyPrice()

    # get stock prices using yfinance library
    def getDailyPrice(self):

        sym = yf.Ticker(self.ticker)
        df = sym.history(interval = '1d', period = self.period)
        df['Date'] = pd.to_datetime(df.index).tz_localize(None)
        df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close', "Volume"]]
        df.reset_index(drop = True, inplace = True)
        
        return(df)
    
    def getWeeklyData(self):
        # Load the daily stock data into a DataFrame
        df = self.getDailyPrice()
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
        df = self.getDailyPrice()
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
