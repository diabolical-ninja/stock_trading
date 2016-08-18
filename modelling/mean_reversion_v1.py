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



# 2. Source Data & Transform

eod = pd.read_csv('/users/yassineltahir/Repos/stock_trading/Data/eod_initial.csv',sep='|')
eod['Date'] = pd.to_datetime(eod.Date)


# Look at only last 6months of data
min_date = datetime.datetime.today() - datetime.timedelta(days=180)
eod = eod[eod.Date > min_date]





ticker = np.unique(eod.ticker)[20]
test = eod[eod.ticker==ticker]

trade_amount=1000
shares_owned = 0
brokerage = 20
expenses = 0
revenue = 0


# 1. Sort By Date
date_name = 'Date'
test = test.sort_values(by=date_name)

# Calculate rolling average of size "mean_window"
mean_window = 10 #10-day rolling average
roll = pd.DataFrame({'Date':test['Date'],
                     'rolling_open':test['Open'].rolling(window = mean_window, min_periods = mean_window).mean()
                     })

# Align the rolling mean with tomorrows date
# Want to check current price against yesterdays average (don't know todays)
roll['Date'] = roll['Date'] + datetime.timedelta(days=1)

# Join to Ticker data
test['rolling_open'] = roll.rolling_open




# For interests sake, track the buy/sell action
bs_action = []

# Capture Revenue State
cash_flow = []

# For each day, compare min(high, close) to rolling mean
for day in test[mean_window:test.shape[0]].iterrows():
    
    # Check if open is above/below mean
    if day[1]['Open'] > day[1]['rolling_open']:
        action = 'sell'
    elif day[1]['Open'] < day[1]['rolling_open']:
        action = 'buy'
    else:
        action = 'Nothing'
    
    # Track Action
    bs_action.append(action)    
    
    if action == 'sell':
                    
        # Identify min(High, Close)
        # Chosen so to pick "Worst" return of the 2
        # In reality the difference between buy & sell will probably be small still
        price = min(day[1]['High'],day[1]['Close'])
        
        # Sell Shares
        if shares_owned != 0:
            cash = price * shares_owned - brokerage
        else:
            cash = 0
        
        revenue = revenue + cash
        
        # Rest number of shares owned
        shares_owned = 0
        
        
    if action == 'buy':
        
        # Calculate number of stocks to buy given max trade_amount
        shares_bought = math.floor(trade_amount/day[1]['Open'])
        
        # Cumulate number of numebrs
        shares_owned = shares_owned + shares_bought
        
        # Cumulate transaction cost
        expenses = expenses + shares_bought*day[1]['Open'] + brokerage
        
        
    if action == 'sell':
        tmp1 = cash
        tmp2 = 0
    elif action == 'buy':
        tmp1 = 0
        tmp2 = shares_bought*day[1]['Open'] + brokerage
    else:
        tmp1 = 0
        tmp2 = 0
    
    out = [day[1]['Date'],action, revenue-expenses, tmp1, tmp2, tmp1 - tmp2, day[1]['Open'],day[1]['Close'],day[1]['High'],day[1]['rolling_open'],shares_owned]
    cash_flow.append(out)
        

profit = revenue - expenses

cashFlow= pd.DataFrame(cash_flow)
cashFlow.columns = ['Date','action','cumulative_profit', 'Sell','Buy','sell_buy','Open','Close','High','Rolling_Open','shares_owned']

cashFlow_melt = pd.melt(cashFlow, id_vars=['Date'])

import plotly.graph_objs as go
from plotly import tools
from plotly.offline import plot


# Plot Data
data = [go.Scatter(x = cashFlow_melt[cashFlow_melt.variable == var].Date,
                   y=cashFlow_melt[cashFlow_melt.variable == var].value,
                   name=var
               ) for var in np.unique(cashFlow_melt.variable)]

# Plot Nicities
layout = go.Layout(
    title= ticker + ': Daily Profit/Loss on simple Mean Reversion Strategy',
    yaxis=dict(title='$'),
    xaxis=dict(title='Date')
    )
    
# Combine Plot & Formatting
fig = go.Figure(data=data, layout=layout)

# Generate Plot
plot(fig, filename='test')







# 3. Mean By/Sell Function


def mean_reversion(data,trade_amount,mean_window,brokerage):
    
    """
    Simple Mean Reversion Stratergy
    
    - If price goes above N-day rolling average then sell
    - If price goes below N-day rolling average then buy
    - Trades happen once per day





# FN COMMENTS
# Might be worth having an input be a list of column name mappings
#       eg, date_name = "Date", open_name="Open" etc