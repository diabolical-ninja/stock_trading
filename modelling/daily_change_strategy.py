#********************************************************************************
# Title: Daily Chanage Strategy
#
# Desc: Buy & Sell Largest Movers over previous N days
#           - Purchase Orders submitted between close & open
#           - Assume $1000 per purchase order
#
# Inputs: eod_initial.csv
#
#********************************************************************************


# 1. Load Packages & Set Global Variables

import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import plot
import math
from tqdm import tqdm




# 2. Source Data & Transform

eod = pd.read_csv('/users/yassineltahir/Repos/stock_trading/Data/eod_initial.csv',sep='|')
#eod = pd.read_csv('C:/Users/yassin.eltahir/Documents/Repositories/stock_trading/Data/eod_initial.csv',sep='|')
eod['Date'] = pd.to_datetime(eod.Date)




## ALgorithm
# - Everyday identify top N stocks based on % or $ change over the last M days
# - Buy $XXXX of those stocks
# - Sell once worth more than (shares @ open + 2x brokerage fee)
# (- If stock age is greater than 7, sell)




def change(data, brokerage, num_stocks, num_days, buy_amount, ts_name, change_type, margin=0):

    """
    <Function Description>
    
    data:
    brokerage:
    num_stocks: Top N largest changed
    num_days: Window (in days) to look back at price change
    buy_amount: $ value of shares to buy
    ts_name: Column name of timestamp
    change_type: pct - percent change
                 dol - dollar amount change
    margin: %gain to sell stock
    
    """

    # Initialise Variables
    owned_tickers = []
    expenses = 0
    revenue = 0
    actions = []


    # 1. Sort By Date Ascending
    data = data.sort_values(by=ts_name)


    # 2. Calculate Daily Change
    if change_type == 'dol':
        data['change'] = data.Close - data.Open
    elif change_type == 'pct':
        data['change'] = (data.Close - data.Open)/data.Open


    # For each day
    ## SOMETHING IS WRONG WITH THE DAY FORMAT!!! TO FIX!
    date_range = data[num_days:data.shape[0]].Date.unique
    for day in tqdm(date_range()):

        # Calculate change over last num_days days
        # NOTE: This currently doesn't take into account weekends!!! TO ADD!
        amount_changed = data[(data[ts_name] >= (day-timedelta(days=num_days))) & (data[ts_name] < day)].groupby(by='ticker')['change'].sum()

        # Identify Stocks with largest change
        tick_to_buy = list(amount_changed.nlargest(num_stocks).index)

        # Buying function
        # THIS HAS A LOST OF UNCESSERCARY CODE! Once Fn complete, clean up this section
        def buy(x):
            # If not already owned
            if x not in [tickers[0] for tickers in owned_tickers]:
                open_price = float(data[(data.ticker==x) & (data.Date==day)].Open.values)
                shares_bought = math.floor(buy_amount/open_price)
                owned_tickers.append([x,open_price,shares_bought])
                action = 'buy'

                # Track Expense
                cost = shares_bought * open_price + brokerage
            else:
                open_price = float(data[(data.ticker==x) & (data.Date==day)].Open.values)
                shares_bought = 0
                cost = 0
                action = 'hold'

            # Compile Output
            out = [x, shares_bought, cost, open_price, action]
            return(out)

        # Purchse $buy_amount of each stock if not already owned
        actions.append(map(buy, tick_to_buy))

        # Log expenses
        expenses = expenses + sum([x[2] for x in actions[-1]])


        # Sell Owned Shares Past threshold
        def sell(x):
            
            tick_sell = []
            
            # If in highest changes then don't sell
            if x not in tick_to_buy:
                
                # Check if value is greater than cost + 2xbrokerage
                cost = [ticker[1]*ticker[2] for ticker in owned_tickers if ticker[0]==x][0]
                todays_worth = [ticker[2] for ticker in owned_tickers if ticker[0]==x][0] * float(data[(data.ticker==x) & (data.Date==day)].Open.values)
                
                if (cost + cost*margin - 2*brokerage) > todays_worth:
                    action = 'sell'
                    income = todays_worth - brokerage
                    
                    # Remove from owned_tickers list
                    tick_sell.append(x)
                    
            else:
                action = 'hold'
                income = 0
                    
            # Compile Output
            out = [x,day,income,action]
            return(out)
                
                
                
        # Sell shares where appropriate
        actions.append(map(sell, tick_to_buy))
        
        # Log Revenue
        revenue = revenue + sum([x[2] for x in actions[-1]])
        
                
        # Identify Tickers Sold
        tick_sold = [sold[0] for sold in actions[-1] if sold[3]=='sell']
        owned_tickers = [owned for owned in owned_tickers if owned[0] not in tick_sold]
        
    # Return Expenses, Revenue and Shares Held
    out = [expenses, revenue, owned_tickers]



# Apply "change" function
test = change(data = eod[eod.Date > '2016-01-01'],
       brokerage = 2,
       num_stocks = 3, # purchase top 3
       num_days = 3, # Change based on last 3 days
       buy_amount = 1000, # If buy, then $1000
       ts_name = 'Date',
       change_type = 'pct',
       margin=0)