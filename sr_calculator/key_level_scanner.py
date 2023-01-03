import numpy as np
from yahoo_finance.tickers import Ticker

class FractalScanner():

    def __init__(self):
        self.levels = []

    # determine bullish fractal 
    def isSupport(self, df,i):  
        cond1 = df['Low'][i] < df['Low'][i-1]   
        cond2 = df['Low'][i] < df['Low'][i+1]   
        cond3 = df['Low'][i+1] < df['Low'][i+2]   
        cond4 = df['Low'][i-1] < df['Low'][i-2]  
        return (cond1 and cond2 and cond3 and cond4) 
    # determine bearish fractal
    def isResistance(self, df,i):  
        cond1 = df['High'][i] > df['High'][i-1]   
        cond2 = df['High'][i] > df['High'][i+1]   
        cond3 = df['High'][i+1] > df['High'][i+2]   
        cond4 = df['High'][i-1] > df['High'][i-2]  
        return (cond1 and cond2 and cond3 and cond4)
    # to make sure the new level area does not exist already
    def isFarFromLevel(self, value, levels, df):    
        ave =  np.mean(df['High'] - df['Low'])    
        return np.sum([abs(value-level)<ave for level in levels])==0

    def consolidateValues(self, values, alpha = 0.05):
        consolidated = []

        for i, value in enumerate(values):
            within_range = False
            for j, other_value in enumerate(values):
                if i == j:
                    continue
                diff = abs((value - other_value) / other_value)
                if diff <= alpha:
                    within_range = True
                    break

            if within_range:
                avg = (value + other_value) / 2
                consolidated.append(avg)
                values.remove(value)
                values.remove(other_value)
            else:
                consolidated.append(value)

        return consolidated
    
class WindowScanner(FractalScanner):

    def __init__(self, ticker, df=None, window = 10, shift = 15, interval = 'w', alpha = 0.05):
        super(WindowScanner, self).__init__()

        self.ticker = ticker
        self.window = window
        self.shift = shift
        self.alpha = alpha
        
        self.interval = interval

        if df is None:
            ticker_manager = Ticker(ticker = self.ticker, interval=self.interval)
            self.df = ticker_manager.df
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