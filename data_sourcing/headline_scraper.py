# Import Required Packages
import feedparser
import pandas as pd
import tqdm

# References:
# https://developer.yahoo.com/python/python-rss.html
# https://developer.yahoo.com/finance/company.html


# Tickers
ticker_file = 'companies-2016-2-1470371480687.csv'
codes = pd.read_csv(ticker_file, delimiter=',')

# Variable to populate with articles
headline = []

# Loop through each ticker
for ticker in tqdm.tqdm(codes.Code):
    
    # Build Headlines URL string
    url = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=' + ticker + '&region=US&lang=en-US'
    
    # Source headlines
    info = feedparser.parse(url)
    
    # Extract title, link & date
    for entry in info.entries:
        
        if entry.title != 'Yahoo! Finance: RSS feed not found':
            headline.append([ticker,entry.title, entry.link, entry.published])

articles = pd.DataFrame(headline)

