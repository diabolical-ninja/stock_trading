#******************************************************
# Title: Simple Holding
#
# Desc: Calculates Profit/Loss for long term holding of a stock
#       Can be used as a reference/baseline to compare other strategy earnings
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



# 3. Holding Function

def stock_hold(data, dol_buy, brokerage, date_name, start_date = None):    
    
    """
    Simple Long Term Stock Hold
     
     - Buy stock at start date price and hold until today
     - Profit/Loss calculated by selling on day X
    
    Inputs:
        - data: Dataframe containing ticker data
        - dol_buy: Initial Investment Amount
        - brokerage: Cost of brokerage per transaction
        - date_name: Name of date/timestamp column
        - start_date (NULL): Date to make initial purchase
        
    TODO: Include dividend payout & use to purchase more stocks
    """
    
    
    # 1. Sort By Date Ascending
    data = data.sort_values(by=date_name)
    
    
    # 2. If present, filter by start date
    if start_date != None:
        data = data[ data[date_name] > start_date]
        
    
    # 3. Make initial Purchase
    shares_bought = math.floor(dol_buy/data[data[date_name] == min(data[date_name])]['Open'])
    initial_cost = shares_bought * data[data[date_name] == min(data[date_name])]['Open'] + brokerage
    initial_cost = initial_cost.values[0]
    

    # 4. Calculate earnings for each date of ownership
    data['profit_loss'] = shares_bought * data['Open'] - brokerage - initial_cost
    
    return(data)
    

    

## Test Data
# Select Ticker
ticker = np.unique(eod.ticker)[134]
#ticker = 'IRE'
test = eod[eod.ticker==ticker]


try1 = stock_hold(data = test,
                  dol_buy = 1000,
                  brokerage = 20,
                  date_name = 'Date')



# Plot Success (!!!)

try1_sub = try1[['Date','Open','profit_loss']]

try1_melt = pd.melt(try1_sub, id_vars=['Date'])



# Plot Data
data = [go.Scatter(x = try1_melt[try1_melt.variable == var].Date,
                   y=try1_melt[try1_melt.variable == var].value,
                   name=var
               ) for var in np.unique(try1_melt.variable)]

# Plot Nicities
layout = go.Layout(
    title= ('%s: Daily Profit/Loss for basic Long Strategy'%(ticker)),
    yaxis=dict(title='$'),
    xaxis=dict(title='Date')
    )
    
# Combine Plot & Formatting
fig = go.Figure(data=data, layout=layout)

# Generate Plot
plot(fig, filename='test')
    
    
    
    
    
    
    
    
    
    