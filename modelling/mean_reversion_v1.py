#******************************************************
# Title: Mean Reversion v1
#
# Desc: Recreate Quantopian Sample Mean Demp
#       https://www.quantopian.com/algorithms/57a7346c4b93e1d1a3000755#algorithm
#
# Inputs: eod_initial.csv
#
#******************************************************


# 1. Load Packages & Set Global Variables

import pandas as pd
import numpy as np
import datetime
import math
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import plot




# 2. Source Data & Transform

eod = pd.read_csv('/users/yassineltahir/Repos/stock_trading/Data/eod_initial.csv',sep='|')
#eod = pd.read_csv('C:/Users/yassin.eltahir/Documents/Repositories/stock_trading/Data/eod_initial.csv',sep='|')
eod['Date'] = pd.to_datetime(eod.Date)





# 3. Mean By/Sell Function


def mean_reversion(data,dol_buy,mean_window,brokerage, mean_type, date_name, buy_sell_buffer):
    
    """
    Simple Mean Reversion Stratergy
    
    - If price goes above N-day rolling average then sell
    - If price goes below N-day rolling average then buy
    - Trades happen once per day
    
    Inputs:
        - data: Dataframe containing ticker data
        - dol_buy: Amount ($'s) of stock to buy each time
        - mean_window: Window size to calculate rolling averages
        - brokerage: Cost of brokerage per transaction
        - mean_type: Rolling function to use, eg EWMA
        - date_name: Name of timestamp column to use
        - buy_sell_buffer: How far above/below mean to buy/sell as a %
        
    """

    # Initialise Variables
    shares_owned = 0
    expenses = 0
    revenue = 0
    trade_info = []

    
    # 1. Sort By Date Ascending
    data = data.sort_values(by=date_name)
    
    # 2. Calculate rolling average of size "mean_window"
    if mean_type == "MA":  # Moving Average
        roll = pd.DataFrame({'Date':data['Date'],
                         'rolling_open':data['Open'].rolling(window = mean_window, min_periods = mean_window).mean()
                         })
    elif mean_type == "EWMA": #Exponentially Weighted Moving Average
        roll = pd.DataFrame({'Date':data['Date'],
                         'rolling_open':pd.ewma(data['Open'],span = mean_window  ,min_periods = mean_window)
                         })
    
    # Align the rolling mean with tomorrows date
    # Want to check current price against yesterdays average (don't know todays)
    roll['Date'] = roll['Date'] + datetime.timedelta(days=1)
    
    # Join to Ticker data
    data['rolling_open'] = roll.rolling_open


    # 3. Buy/Sell Action

    # For each day, compare min(high, close) to rolling mean
    for day in data[mean_window:data.shape[0]].iterrows():

        # Check if open is above/below mean
        if day[1]['Open'] > day[1]['rolling_open'] * (1+buy_sell_buffer):
            action = 'sell'
        elif day[1]['Open'] < day[1]['rolling_open']*(1-buy_sell_buffer):
            action = 'buy'
        else:
            action = 'Nothing'
               
        
        if action == 'sell':
            # Identify min(High, Close)
            # Chosen so to pick "Worst" return of the 2
            price = min(day[1]['High'],day[1]['Close'])
            
            # Sell Shares
            if shares_owned != 0:
                income = price * shares_owned - brokerage
            else:
                income = 0
            
            revenue = revenue + income
            
            # Reset number of shares owned
            shares_owned = 0
            
            
        if action == 'buy':
            
            # Calculate number of stocks to buy given max dol_buy
            shares_bought = math.floor(dol_buy/day[1]['Open'])
            
            # Cumulate number of numebrs
            shares_owned = shares_owned + shares_bought
            
            # Cumulate transaction cost
            expenses = expenses + shares_bought*day[1]['Open'] + brokerage
            
            # No Income when buying
            income = 0
            
        if action == 'Nothing':
            
            # No income
            income = 0
            
            # No Shares Bought
            shares_bought = 0
        
        
        # 4. Capture Daily Action Details
        
        # Collect Days Trading Information
        out = np.append(np.array(day[1]),  # Initial Data
                       [action,  # What Happened
                       income,  # If a sale, how much money did it bring in
                       shares_bought*day[1]['Open'] + brokerage if action=='buy' else 0, # If a purchase, what was the cost
                       shares_bought if action=='buy' else 0,
                       shares_owned,
                       revenue - expenses])
                       
                       
        # Capture days trading events               
        trade_info.append(out)
         
    # Format for fn output    
    trade_info= pd.DataFrame(trade_info)
    trade_info.columns = np.append(np.array(day[1].index),
                                   ['action', 'revenue','expense','shares_bought','shares_owned','profit_loss'])    
    
    # Output Trading History
    return(trade_info)
    
         

# FN COMMENTS
# Might be worth having an input be a list of column name mappings
#       eg, date_name = "Date", open_name="Open" etc



## Test Data
# Select Ticker
ticker = np.unique(eod.ticker)[134]
#ticker = 'IRE'
test = eod[eod.ticker==ticker]


margin = 0.1
try1 = mean_reversion(data=test, 
                      dol_buy = 1000,
                      mean_window = 20,
                      brokerage = 17,
                      mean_type = 'MA',
                      date_name = 'Date',
                      buy_sell_buffer = margin)




# Plot Success (!!!)

try1_sub = try1[['Date','Open','shares_owned','profit_loss']]

try1_melt = pd.melt(try1_sub, id_vars=['Date'])



# Plot Data
data = [go.Scatter(x = try1_melt[try1_melt.variable == var].Date,
                   y=try1_melt[try1_melt.variable == var].value,
                   name=var
               ) for var in np.unique(try1_melt.variable)]

# Plot Nicities
layout = go.Layout(
    title= ('%s: Daily Profit/Loss on simple Mean Reversion Strategy - Buy/Sell Threshold = %0.0f%%'%(ticker,margin*100)),
    yaxis=dict(title='$'),
    xaxis=dict(title='Date')
    )
    
# Combine Plot & Formatting
fig = go.Figure(data=data, layout=layout)

# Generate Plot
plot(fig, filename='test')


#try1[(try1.Date > '2013-04-01') & (try1.Date < '2014-01-01')].to_csv('test_out')