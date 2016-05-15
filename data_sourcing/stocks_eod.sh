#!/bin/bash

#***************************************************************************
# Source all EOD (End of Day) data from Yahoo Finance for Stocks (eg companies)
# 
#***************************************************************************
echo ""
echo 'Downloading EOD Stock Data...'

# File containing all Stock Tickers
tickers=/Users/yassineltahir/Repos/stock_trading/ref/tickers_stock.csv

# Output Location for sourced data
loc='/Users/yassineltahir/Repos/stock_trading/data/stock'

while read line; do
	
	# Get stock ticker
	stock=$(echo $line | awk -F\| '{print $1}')

	# Move to save location
	cd $loc

	# Ignore Header
	if [ "$stock" != "Ticker" ]
	then
		
		# Build save file name
		out='eod_'$stock'.csv'
		
		# Source stock data
		curl -s 'http://real-chart.finance.yahoo.com/table.csv?s='$stock'&a=01&b=01&c=1900&d=01&e=01&f=2020&g=d&ignore=.csv' -o $out
	fi
done < $tickers

echo 'Downloading EOD Stock Data...Done'


#***************************************************************************
echo 'Remove Empty Data Files...'
cd $loc

for f in *.csv; do

	# Extract first line of file
	first_line=$(head -1 "$f")

	# Should contain the phrase "HTML" if a failed file
	value=$( grep -ic "HTML" <<<$first_line)
	if [ $value -eq 1 ]
	then
	
	  # Delete Junk File
  	  rm $f
  	  
  	  # Capture name of empty file
	  echo $f >> /Users/yassineltahir/Repos/stock_trading/ref/file_removed.txt


	fi
done

echo 'Remove Empty Data Files...Done'

#***************************************************************************

# Count number of files sourced
cd $loc
count="$(ls -1 | wc -l)"
echo "Downloaded $count files"


# Get Sum of all file sizes
cd $loc
file_size="$(du -ch $file_list | tail -1 | cut -f 1)"
echo "Downloaded $file_size"
echo ""