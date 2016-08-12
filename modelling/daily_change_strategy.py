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
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import plot




# 2. Source Data & Transform

#eod = pd.read_csv('/users/yassineltahir/Repos/stock_trading/Data/eod_initial.csv',sep='|')
eod = pd.read_csv('C:/Users/yassin.eltahir/Documents/Repositories/stock_trading/Data/eod_initial.csv',sep='|')
eod['Date'] = pd.to_datetime(eod.Date)



# 3. Calculate Variables

# Calculate Daily $ Change
eod['dol_change'] = eod.Close - eod.Open

# Calculate Daily % Change
eod['pct_change'] = eod.dol_change/eod.Open




## ALgorithm
# - Everyday identify top 5 (subject to change) stocks based on % change over the last 3 days
# - Buy $1000 of those stocks
# - The following day, if those stocks worth more than cost + $40 (2x brokerage fee) then sell, else keep
# - If stock age is greater than 7, sell


# Dates to run over
#day_range = 
date_list = [datetime.today() - datetime.timedelta(days=x) for x in range(0, numdays)]

 pd.date_range(pd.datetime.today(), periods=10).tolist()
pd.date_range(end = pd.datetime.today(), start = '2016-08-01').tolist()