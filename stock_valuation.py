#!/usr/bin/env python

EXCEL_PATH = '/home/aritra/analyzeninvest-projects/stock-research/save_valuation.xlsx'

def stock_research(stock_ticker, us_or_india, excel_path = EXCEL_PATH):
    import pandas as pd
    import scrape_moneycontrol_data as moneycontrol
    import scrape_yahoo_finance as yahoo
    """ 
    This function calculates the valuation of a stock based on the
    yahoo finance. Then it also prints the max past 20 years of the
    stock performance.  
    """
    if us_or_india:
        stock_end = ".NS"
    else:
        stock_end = ""
    stock_name = stock_ticker + stock_end
    print("Staring the Valuation for " + stock_name)
    yahoo.Valuation_of_stock(stock_name)
    moneycontrol.Historical_Performance_of_stock(stock_ticker)

stock_research('SBIN', True)    
#stock_research('CDNS', False)    


