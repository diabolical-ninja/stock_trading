#!/bin/bash
#***************************************************************************
# Source EOD Currency Data
#***************************************************************************

# Initiate runtime capture
SECONDS=0

echo ""
echo 'Sourcing Currency Data...'

# All ticker codes
tickers="/Users/yassineltahir/Repos/stock_trading/ref/tickers_currency.txt"

# Location to save data to
loc="/Users/yassineltahir/Repos/stock_trading/data/currency/"

while read line; do
	
	# Extract only base currency from ticker
	currency=$(echo "${line//=X}")


	for year in $(seq 1980 1 2017); do

		# Create output file name
		out=$loc'eod_'$currency'_'$year'.json'
		
		# Download Years data
		curl -s 'https://query.yahooapis.com/v1/public/yql?q=SELECT%20*%20FROM%20yahoo.finance.historicaldata%20WHERE%20symbol%3D%22'$currency'%3DX%22%20and%20startDate%3D%22'$year'-01-01%22%20and%20endDate%3D%22'$(($year+1))'-01-01%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=' -o $out
	
		# Crude check to see if year had data
		# files of 2KB have no data. Delete all files of 2KB
		file_size=$(echo $(wc -c <"$out"))
		if(($file_size < 2200))
		then
			rm $out
		fi
		
	done

done<"$tickers"


echo 'Sourcing Currency Data...Done'

# Capture Runtime
duration=$SECONDS
echo "Runtime: $(($duration / 60)) minutes and $(($duration % 60)) seconds"