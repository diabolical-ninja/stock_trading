#********************************************************************************
# Title: Daily Chanage Analysis
#
# Desc: Analysis of daily change for a variety of metrics:
#           - % & $ Diff
#           - % & $ Dollar Volume
#
#       https://www.quantopian.com/algorithms/57a7346c4b93e1d1a3000755#algorithm
#
# Inputs: eod_initial.csv
#
#********************************************************************************


# 1. Load Packages & Set Global Variables

import pandas as pd
import numpy as np
#import plotly.plotly as py
#import plotly.graph_objs as go
from datetime import datetime


from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
from plotly.graph_objs import *


# 2. Source Data & Transform

eod = pd.read_csv('/users/yassineltahir/Repos/stock_trading/Data/eod_initial.csv',sep='|')
eod['Date'] = pd.to_datetime(eod.Date)


# Calculate Daily $ Change
eod['dol_change'] = eod.Close - eod.Open

# Calculate Daily $ Change
eod['pct_change'] = eod.dol_change/eod.Open



# Calculate Dollar Volume using average day price (open/close)
eod['open_close_avg'] = (eod.Open + eod.Close)/float(2)
eod['dollar_volume'] = eod.Volume * eod.open_close_avg


## Calculate Dollar Volume $ Change
#eod['dv_dol_change'] = 



# Calculate Rolling Average over 2wk window
#eod = eod.sort_values
eod['rolling_pct_change'] = eod.groupby('ticker')['pct_change'].apply(pd.rolling_mean, 10, min_periods=5)


# Calculate Average pct change per ticker & find highest values
ave_pct_change = eod[eod.Date > '2016-07-01'].groupby('ticker')['pct_change'].apply(np.mean).reset_index('ticker')
top_5 = ave_pct_change.sort_index(by='pct_change', ascending=False).head(5)


from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import Bar, Scatter, Figure, Layout
import plotly.plotly as py
init_notebook_mode(connected=True)

# Plot top 5 stocks
data = go.Scatter(
          x=eod[(eod.Date > '2016-07-01') & (eod.ticker=='WHC')].Open,
          y=eod[(eod.Date > '2016-07-01') & (eod.ticker=='WHC')]['pct_change']
         )

go.Figure(data=data)
py.iplot(data)


py.image.save_as(data, filename='test_plot')