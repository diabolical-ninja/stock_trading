# Load Required Packages
import pandas as pd
import tqdm

# Tickers
ticker_file = '/Users/yassineltahir/Downloads/companies-2016-2-1470471968768.csv'
codes = pd.read_csv(ticker_file, delimiter=',')

# Incompatible ticker Labels
# incomp_ticker = ['AHG','AHY']
incomp_ticker = []


# Dataframe to store all EOD Data
eod = pd.DataFrame()

for ticker in tqdm.tqdm(codes.Code):    

    # Build URL for ticker
    url = 'http://real-chart.finance.yahoo.com/table.csv?s=' + ticker + '&a=01&b=01&c=2010&d=01&e=01&f=2100&g=d&ignore=.csv'
    
    try:
        # Read Ticker History    
        data = pd.io.parsers.read_csv(url)
        
    except:
        url = 'http://real-chart.finance.yahoo.com/table.csv?s=' + ticker + '.ax&a=01&b=01&c=1900&d=01&e=01&f=2020&g=d&ignore=.csv'
        data = pd.io.parsers.read_csv(url)
    #except:
     #   incomp_ticker.append(ticker)

    # Add ticker symbol
    data['ticker'] = ticker
    
    # Append to EOD
    eod = eod.append(data)


# Output to CSV
eod.to_csv('/users/yassineltahir/Repos/stock_trading/Data/eod_initial.csv',sep='|',index=False)