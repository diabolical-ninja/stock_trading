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
from datetime import datetime



# 2. Source Data & Transform

eod = pd.read_csv('/users/yassineltahir/Repos/stock_trading/Data/eod_initial.csv',sep='|')
eod['Date'] = pd.to_datetime(eod.Date)


# Look at only last 6months of data
min_date = date.today() - timedelta(days=180)
eod = eod[eod.Date > min_date]



# 3. Feature Creation

# Dollar Volume = Price x Volume
eod['dollar_volume'] = eod.Volume * eod.Open


