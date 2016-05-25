#!/bin/bash
#***************************************************************************
# Extract Currency Ticker 
#***************************************************************************

# Initiate runtime capture
SECONDS=0

echo ""
echo 'Extracting Currency Ticker...'

# All USD to XXX currency conversions
#http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json
currencies="/Users/yassineltahir/Repos/stock_trading/ref/tickers_currencies_raw.json"

out="/Users/yassineltahir/Repos/stock_trading/ref/tickers_currency.txt"

while read line; do
	
	# Look for ticker symbol in file
	value=$( grep -ic "symbol" <<<$line)
	if [ $value -eq 1 ]
	then
		string=$(echo $line | awk -F: '{print $2}')
		string=$(echo "${string//,}")
		string=$(echo "${string//\"}")
		
		echo $string >> $out
			
	fi

	#echo $value

done<"$currencies"


echo 'Extracting Currency Ticker...Done'

# Capture Runtime
duration=$SECONDS
echo "Runtime: $(($duration / 60)) minutes and $(($duration % 60)) seconds"