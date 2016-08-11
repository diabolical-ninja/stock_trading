# Import Required Packages
import feedparser
import pandas as pd
import tqdm
import time


# Tickers
ticker_file = 'C:/Users/yassin.eltahir/Downloads/companies-2016-2-1470371480687.csv'
codes = pd.read_csv(ticker_file, delimiter=',')

# Variable to populate with articles
headline = []

# Loop through each ticker
for ticker in tqdm.tqdm(codes.Code):
    
    # Build Headlines URL string
    url = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=' + ticker + '.AX&region=US&lang=en-US'
    
    # Source headlines
    info = feedparser.parse(url)
    
    # Extract title, link & date
    for entry in info.entries:
        
        if entry.title != 'Yahoo! Finance: RSS feed not found':
            headline.append([ticker,entry.title, entry.link, entry.published])

articles = pd.DataFrame(headline)


# Export to CSV
date = time.strftime("%Y%m%d")
file_name = date + '_headlines'
loc = 'C:/Users/yassin.eltahir/Downloads/asx_200_headlines/'+ file_name + '.csv'

articles.to_csv(loc, header=True, index=False, encoding='utf-8', sep='|')
