##****************************************************************************************
# Title: Prep Tickers
#
# Desc: List of all Yahoo stock tickers extract from spreadsheet to csv's. 
#       Each csv is saved as pipe delimited csv's. This also addresses the weird 
#       line escaping caused by creating csv's from excel (using OSX).
#       Spreadsheet from http://investexcel.net/all-yahoo-finance-stock-tickers/
#        ** The works these guys provide is super helpful!! **
#
# Author:  2016-05-18  Yassin Eltahir
#
# Steps: 
#       0 - Setup Environment
#       1 - Read Files, Clean, Output
#
#
##****************************************************************************************


# 0. Setup Environment  ####

# Load Required Packages
if (!require("pacman")) install.packages("pacman")
pacman::p_load(data.table)



# 1. Read Files, Clean, Output  ####

# Get all files like "ticker_*"
files <- list.files('ref/',pattern = 'tickers')

# Read in, and save as pipe delimited csv
for(i in files){
  
  # Read
  ticker <- fread(sprintf('ref/%s',i))
  
  # Output
  write.table(ticker, sprintf('ref/%s',i), quote = F, sep = '|', row.names = F)
  
}