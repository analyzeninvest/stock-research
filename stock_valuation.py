#!/usr/bin/env python

EXCEL_PATH = '/home/aritra/analyzeninvest-projects/stock-research/save_valuation.xlsx'

def stock_research(stock_ticker, us_or_india, excel_path = EXCEL_PATH):
    moneycontrol = __import__(scrape-moneycontrol-data)
    yahoo = __import__(scrape-yahoo-finance)
    import pandas as pd
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
    yahoo.Valuation_of_stock(stock_name)
    moneycontrol.Historical_Performance_of_stock(stock_ticker)

stock_research('SBI', True)    
stock_research('CDNS', False)    


def stock_research_GUI():
    import tkinter as tk
    root = tk.Tk()
    root.title('Stock Research')
#stock_research_GUI()


