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
  
    def __init__(self, ticker, start = "1970-01-02", end = dt.strftime(dt.now(), "%Y-%m-%d"), interval = 'd'):

        self.ticker = ticker
        self.interval = interval
        self.start = int(dt.timestamp(dt.strptime(start, "%Y-%m-%d")))
        self.end = int(dt.timestamp(dt.strptime(end, "%Y-%m-%d")))


        if str(self.interval).lower() == 'd':
            self.getDailyData()
        elif str(self.interval).lower() == 'm':
            self.getMonthlyData()
        elif str(self.interval).lower() == 'w':
            self.getWeeklyData()

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
        self.df = pd.read_csv(io.StringIO(soup.text), sep=",")

        self.df = self.df.loc[:,['Date', 'Open', 'High', 'Low', 'Close', "Volume"]]
        self.df.sort_values("Date", inplace=True)
    
    def getWeeklyData(self):

        url = "https://query1.finance.yahoo.com/v7/finance/download/" + self.ticker +\
              "?period1=" + str(self.start)+\
              "&period2=" + str(self.end)+\
              "&interval=1wk"+\
              "&events=history&includeAdjustedClose=true"

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req)
        soup = BeautifulSoup(html, "html.parser")
        self.df = pd.read_csv(io.StringIO(soup.text), sep=",")

        self.df = self.df.loc[:,['Date', 'Open', 'High', 'Low', 'Close', "Volume"]]
        self.df.sort_values("Date", inplace=True)
    
    def getMonthlyData(self):

        url = "https://query1.finance.yahoo.com/v7/finance/download/" + self.ticker +\
              "?period1=" + str(self.start)+\
              "&period2=" + str(self.end)+\
              "&interval=1mo"+\
              "&events=history&includeAdjustedClose=true"

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req)
        soup = BeautifulSoup(html, "html.parser")
        self.df = pd.read_csv(io.StringIO(soup.text), sep=",")

        self.df = self.df.loc[:,['Date', 'Open', 'High', 'Low', 'Close', "Volume"]]
        self.df.sort_values("Date", inplace=True)


