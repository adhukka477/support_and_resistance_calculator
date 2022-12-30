import numpy as np
from resources.tickers import Ticker

class FractalScanner():

    def __init__(self):
        self.levels = []

    #method 1: fractal candlestick pattern
    # determine bullish fractal 
    def isSupport(self, df, i, window):  
        cond = []
        for i in np.linspace(i, i+window-1, window): 
            cond.append(df['Low'][int(i)] < df['Low'][int(i)-1])
        return sum(cond) == len(cond)
    # determine bearish fractal
    def isResistance(self, df, i, window): 
        cond = []
        for i in np.linspace(i, i+window-1, window): 
            cond.append(df['High'][int(i)] > df['High'][int(i)-1]) 
        return sum(cond) == len(cond)
    # to make sure the new level area does not exist already
    def isFarFromLevel(self, value, levels, df):    
        ave =  np.mean(df['High'] - df['Low'])    
        return np.sum([abs(value-level) < ave for _,level in levels])==0


    def calculatePriceLevels(self, df, window):
        self.levels = []
        for i in range(window, df.shape[0] - window):  
            if self.isSupport(df, i, window):    
                low = df['Low'][i]    
                if self.isFarFromLevel(low, self.levels, df):      
                    self.levels.append((i,low))
            elif self.isResistance(df, i, window):    
                high = df['High'][i]    
                if self.isFarFromLevel(high, self.levels, df):      
                    self.levels.append((i,high))

class WindowScanner(FractalScanner):

    def __init__(self, ticker, df=None, window = 10, shift = 15):
        super(WindowScanner, self).__init__()

        self.ticker = ticker
        self.window = window
        self.shift = shift
        
        self.interval = '1wk'
        self.period = 'max'

        if df is None:
            self.df = Ticker(ticker = self.ticker).get_stock_price_history(period = self.period, interval = self.interval).data
        else:
            self.df = df

    def calculatePriceLevels(self):
        self.levels = []
        max_list = []
        min_list = []


        for i in range(self.window, len(self.df)-self.window):
            # taking a window of candles
            high_range = self.df['High'][i-self.window:i+self.window]
            current_max = high_range.max()
            # if we find a new maximum value, empty the max_list 
            if current_max not in max_list:
                max_list = []
            max_list.append(current_max)
            # if the maximum value remains the same after shifting 5 times
            if len(max_list)==self.shift and self.isFarFromLevel(current_max,self.levels, self.df):
                self.levels.append((high_range.idxmax(), current_max))

            low_range = self.df['Low'][i-self.window:i+self.window]
            current_min = low_range.min()
            if current_min not in min_list:
                min_list = []
            min_list.append(current_min)
            if len(min_list)==self.shift and self.isFarFromLevel(current_min,self.levels, self.df):
                self.levels.append((low_range.idxmin(), current_min))