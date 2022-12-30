# import necessary libraries

import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime as dt

class Ticker():
  
    def __init__(self, ticker):
        self.ticker = ticker

    # get stock prices using yfinance library
    def get_stock_price_history(self, interval = '1d', period = 'max'):

        sym = yf.Ticker(self.ticker)
        df = sym.history(interval = interval, period = period, actions = "False")
        df['Date'] = pd.to_datetime(df.index).tz_localize(None)
        df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close', "Volume"]]
        df.reset_index(drop = True, inplace = True)
        
        return(df)
    

