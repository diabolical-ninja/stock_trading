#********************************************************************************
# Title: Daily Chanage Analysis
#
# Desc: Analysis of daily change for a variety of metrics:
#           - % & $ Diff
#           - % & $ Dollar Volume
#
# Inputs: eod_initial.csv
#
#********************************************************************************


# 1. Load Packages & Set Global Variables

import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import plot




# 2. Source Data & Transform

#eod = pd.read_csv('/users/yassineltahir/Repos/stock_trading/Data/eod_initial.csv',sep='|')
eod = pd.read_csv('C:/Users/yassin.eltahir/Documents/Repositories/stock_trading/Data/eod_initial.csv',sep='|')
eod['Date'] = pd.to_datetime(eod.Date)


# Calculate Daily $ Change
eod['dol_change'] = eod.Close - eod.Open

# Calculate Daily % Change
eod['pct_change'] = eod.dol_change/eod.Open


# Calculate Rolling Average over window
#eod = eod.sort_values
eod['rolling_pct_change'] = eod.groupby('ticker')['pct_change'].apply(pd.rolling_mean, 5, min_periods=3)
eod['rolling_pct_change'] = eod['rolling_pct_change'] * float(100)


# Calculate Average pct change per ticker & find highest values
ave_pct_change = eod[eod.Date > '2016-08-01'].groupby('ticker')['pct_change'].apply(np.mean).reset_index('ticker')
top_5 = ave_pct_change.sort_index(by='pct_change', ascending=False).head(5)
bottom_5 = ave_pct_change.sort_index(by='pct_change', ascending=True).head(5)



# 3. Plot Top 5 Stocks

# Plot 5 based on average % change over the last 1.5 months
tickers_of_interest = np.array(top_5.ticker)
#tickers_of_interest = np.array(bottom_5.ticker)


# Plot Data
data = [go.Scatter(x = eod[(eod.Date > '2016-07-01') & (eod.ticker==ticker)].Date,
                   y=eod[(eod.Date > '2016-07-01') & (eod.ticker==ticker)]['rolling_pct_change'],
                   name=ticker
               ) for ticker in tickers_of_interest]

# Plot Nicities
layout = go.Layout(
    title= '5 day Rolling Average of % Change (Close - Open)',
    yaxis=dict(title='% Change'),
    xaxis=dict(title='Date')
    )
    
# Combine Plot & Formatting
fig = go.Figure(data=data, layout=layout)

# Generate Plot
plot(fig, filename='test')



# 4. Plot Stoct Avg Change with Actual Change


