import numpy as np
import pandas as pd
import os
import re

list_of_indices = [i for i in os.listdir("files/indices_stock_data") if not i.startswith(".")]

position_dict = {"buy": 1, "sell": 0}

def get_stock_trend():
    stocks = dict()

    for index in list_of_indices:
        temp = list()

        for stock_file in os.listdir("files/indices_stock_data/"+index):
            stock = pd.read_csv(f"files/indices_stock_data/{index}/{stock_file}")
            
            try:
                stock_symbol = stock_file.split(".")[0]
                stock_symb, potential = filter_stock(stock, stock_symbol=stock_symbol)

                if stock_symb:
                    temp.append((stock_symb, potential))
            except:
                pass
        if len(temp) != 0:
            stocks[index] = temp
    

    return stocks.items()

# for identifying long term bearish MACD and long term bullish MACD

def filter_stock(stock, stock_symbol=None, prcnt_diff_threshold=0.05, short_period=12, long_period=26, signal_period=9, compare_days=20, mode=None):
    # stock : dataframe
    
    num_records = long_period + compare_days - 1
    
    val = stock.Close.iloc[-num_records:]
    
    potential_type = ["Bearish", "Bullish"]
    
    # calculate 40d MA and 20d MA for the stock
    # slow_ma, fast_ma = get_sma(val, slow=slow, fast=fast)
    macd, signal = calculate_macd(val)
    
    # for long term trend, all values of both ma should either be greater or smaller, no cross
    checker = ((macd.values[-compare_days:] < signal.values[-compare_days:]).sum()/compare_days)
    
    # checker : 1 -> bullish, checker: 0 -> bearish
    if checker == 0 or checker == 1:
    
        # check if difference between last term of 40d MA and 20d MA respectively is smaller than 5% of ltp
        # if False -> break , else continue
        # last_term_diff = slow_ma[-1] - fast_ma[-1]
        last_term_diff = macd.values[-1] - signal.values[-1]
#         prcnt_diff = last_term_diff/val.values[-1]

#         if np.abs(prcnt_diff) < prcnt_diff_threshold:
#             return stock_symbol, potential_type[checker]
        return stock_symbol, potential_type[int(checker)]
    if mode == "test":
        return macd, signal
    


def calculate_macd(close_values, short_period=12, long_period=26, signal_period=9):
    # Calculate the short-term (12-day) exponential moving average (EMA)
    short_ema = close_values.ewm(span=short_period, adjust=False).mean()
    
    # Calculate the long-term (26-day) exponential moving average (EMA)
    long_ema = close_values.ewm(span=long_period, adjust=False).mean()
    
    # Calculate the MACD line
    macd_line = short_ema - long_ema
    
    # Calculate the signal line (9-day EMA of the MACD line)
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    
    # Calculate the MACD histogram (the difference between the MACD line and the signal line)
#     macd_histogram = macd_line - signal_line
    
    return macd_line, signal_line

def trade(stock_close, position_dict, last_pos="buy"):
    macd, signal = calculate_macd(stock_close)
    checker = macd.values[-1] - signal.values[-1]
    
    # if entry position was buy and on checking macd comes below signal, then sell
    if (position_dict[last_pos] == 1 and checker < 0) or (position_dict[last_pos] == 0 and checker < 0):
        return "sell"
    elif (position_dict[last_pos] == 1 and checker > 0) or (position_dict[last_pos] == 0 and checker > 0):
        return "buy"
    

def stock_price_data(stock_symbol, stock_index):
    stock = pd.read_csv(f"files/indices_stock_data/{stock_index}/{stock_symbol}.NS.csv")
    stock["Date"] = pd.to_datetime(stock["Date"]).dt.strftime("%Y-%m-%d")
    stock = stock.set_index("Date")
    res = [{"date":i, "close":round(j,3)} for i,j in zip(stock.Close.index.values, stock.Close.values)]
    return res