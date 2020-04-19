#!/usr/bin/env python

EXCEL_PATH = '/home/aritra/analyzeninvest-projects/stock-research/save_valuation.xlsx'

def pull_ratio_from_moneycontrol(stock_ticker, ratio):
    """
    This function will pull the historical ratios for a stock_ticker
    from the moneycontrol website.
    pulled data:
    1. eps
    2. current ratio
    3. debt to equity ratio
    Example :
    https://www.moneycontrol.com/financials/itc/ratiosVI/ITC#ITC
    https://www.moneycontrol.com/financials/itc/ratiosVI/ITC/2#ITC
    https://www.moneycontrol.com/financials/itc/ratiosVI/ITC/3#ITC
    https://www.moneycontrol.com/financials/itc/ratiosVI/ITC/4#ITC
    https://www.moneycontrol.com/financials/itc/consolidated-ratiosVI/ITC#ITC
    https://www.moneycontrol.com/financials/itc/consolidated-ratiosVI/ITC/2#ITC
    https://www.moneycontrol.com/financials/itc/consolidated-ratiosVI/ITC/3#ITC
    https://www.moneycontrol.com/financials/itc/consolidated-ratiosVI/ITC/4#ITC
    """
    import requests, re
    from bs4 import BeautifulSoup
    ratio_consolidated_url1 = 'https://www.moneycontrol.com/financials/itc/consolidated-ratiosVI/'+stock_ticker+'#'+stock_ticker
    ratio_consolidated_url2 = 'https://www.moneycontrol.com/financials/itc/consolidated-ratiosVI/'+stock_ticker+'/2#'+stock_ticker
    ratio_consolidated_url3 = 'https://www.moneycontrol.com/financials/itc/consolidated-ratiosVI/'+stock_ticker+'/3#'+stock_ticker
    ratio_consolidated_url4 = 'https://www.moneycontrol.com/financials/itc/consolidated-ratiosVI/'+stock_ticker+'/4#'+stock_ticker
    ratio_url1 = 'https://www.moneycontrol.com/financials/itc/ratiosVI/'+stock_ticker+'#'+stock_ticker
    ratio_url2 = 'https://www.moneycontrol.com/financials/itc/ratiosVI/'+stock_ticker+'/2#'+stock_ticker
    ratio_url3 = 'https://www.moneycontrol.com/financials/itc/ratiosVI/'+stock_ticker+'/3#'+stock_ticker
    ratio_url4 = 'https://www.moneycontrol.com/financials/itc/ratiosVI/'+stock_ticker+'/4#'+stock_ticker
    standalone_ratio = []
    consolidated_ratio = []
    ratio_values = {}
    print("Consolidated " + ratio)
    for url in [ratio_consolidated_url1, ratio_consolidated_url2, ratio_consolidated_url3, ratio_consolidated_url4]:
        page          = requests.get(url)
        soup          = BeautifulSoup(page.text, 'html.parser')
        td_all  = soup.find_all('td')
        for td in td_all:
            if td.find(text=re.compile(ratio)):
                ratio_name = td.text.strip()
                year1_ratio = td.find_next('td').text.strip()
                if not re.match("[-]?[0-9]+[.]?[0-9]+", year1_ratio):
                    break
                else:
                    consolidated_ratio.append(year1_ratio)
                year2_ratio = td.find_next('td').find_next('td').text.strip()
                if not re.match("[-]?[0-9]+[.]?[0-9]+", year2_ratio):
                    break
                else:
                    consolidated_ratio.append(year2_ratio)
                year3_ratio = td.find_next('td').find_next('td').find_next('td').text.strip()
                if not re.match("[-]?[0-9]+[.]?[0-9]+", year3_ratio):
                    break
                else:
                    consolidated_ratio.append(year3_ratio)
                year4_ratio = td.find_next('td').find_next('td').find_next('td').find_next('td').text.strip()
                if not re.match("[-]?[0-9]+[.]?[0-9]+", year4_ratio):
                    break
                else:
                    consolidated_ratio.append(year4_ratio)
                year5_ratio = td.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text.strip()
                if not re.match("[-]?[0-9]+[.]?[0-9]+", year5_ratio):
                    break
                else:
                    consolidated_ratio.append(year5_ratio)
    consolidated_ratio_name = "consolidated " + ratio_name 
    ratio_values.update({consolidated_ratio_name:consolidated_ratio})
    print(consolidated_ratio)
    print("Standalone " + ratio)
    for url in [ratio_url1, ratio_url2, ratio_url3, ratio_url4]:
        page          = requests.get(url)
        soup          = BeautifulSoup(page.text, 'html.parser')
        td_all  = soup.find_all('td')
        for td in td_all:
            if td.find(text=re.compile(ratio)):
                ratio_name = td.text.strip()
                year1_ratio = td.find_next('td').text.strip()
                if not re.match("[-]?[0-9]+[.]?[0-9]+", year1_ratio):
                    break
                else:
                    standalone_ratio.append(year1_ratio)
                year2_ratio = td.find_next('td').find_next('td').text.strip()
                if not re.match("[-]?[0-9]+[.]?[0-9]+", year2_ratio):
                    break
                else:
                    standalone_ratio.append(year2_ratio)
                year3_ratio = td.find_next('td').find_next('td').find_next('td').text.strip()
                if not re.match("[-]?[0-9]+[.]?[0-9]+", year3_ratio):
                    break
                else:
                    standalone_ratio.append(year3_ratio)
                year4_ratio = td.find_next('td').find_next('td').find_next('td').find_next('td').text.strip()
                if not re.match("[-]?[0-9]+[.]?[0-9]+", year4_ratio):
                    break
                else:
                    standalone_ratio.append(year4_ratio)
                year5_ratio = td.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text.strip()
                if not re.match("[-]?[0-9]+[.]?[0-9]+", year5_ratio):
                    break
                else:
                    standalone_ratio.append(year5_ratio)
    print(consolidated_ratio)
    standalone_ratio_name = "standalone " + ratio_name 
    ratio_values.update({"Standalone "+ratio_name:standalone_ratio})
    return(ratio_values)
                    

    
# pull_ratio_from_moneycontrol('ITC', 'Basic EPS')
# pull_ratio_from_moneycontrol('ITC', 'EV/EBITDA')
# pull_ratio_from_moneycontrol('ITC', 'Total Debt/Equity')
# pull_ratio_from_moneycontrol('ITC', 'Current Ratio')
# pull_ratio_from_moneycontrol('ITC', 'Price/BV')
# print(pull_ratio_from_moneycontrol('ITC', 'Dividend Payout Ratio .NP.'))
# pull_ratio_from_moneycontrol('ITC', 'Net Profit Margin')


def Historical_Performance_of_stock(stock_ticker, excel_path = EXCEL_PATH):
    """
    This function will give the historical performance of a stock with
    max value going to 20 years.
    The Data is collected from the moneycontrol key ratios.
    Covered ratios are :
    1. Basic EPS
    2. Current Ratio
    3. Debt/ Equity Ratio
    4. Dividend Payout Ratio
    5. EV/EBITDA
    Then the details are store in the xls. The XLS is same as the valuation. 
    """
    import pandas as pd
    from openpyxl import load_workbook
    from datetime import date
    today                              = date.today()
    current_year                       = today.year
    writer                             = pd.ExcelWriter(excel_path, engine = 'openpyxl')
    writer.book                        = load_workbook(excel_path)
    writer.sheets                      = dict((ws.title, ws) for ws in writer.book.worksheets)
    historical_data                    = {}
    eps_from_moneycontrol              = pull_ratio_from_moneycontrol(stock_ticker, 'Basic EPS')
    ev_ebitda_from_moneycontrol        = pull_ratio_from_moneycontrol(stock_ticker, 'EV/EBITDA')
    debt_equity_from_moneycontrol      = pull_ratio_from_moneycontrol(stock_ticker, 'Total Debt/Equity')
    price_to_book_from_moneycontrol    = pull_ratio_from_moneycontrol(stock_ticker, 'Price/BV')
    dividend_payout_from_moneycontrol  = pull_ratio_from_moneycontrol(stock_ticker, 'Dividend Payout Ratio .NP.')
    historical_data.update(eps_from_moneycontrol)
    historical_data.update(ev_ebitda_from_moneycontrol)
    historical_data.update(debt_equity_from_moneycontrol)
    historical_data.update(price_to_book_from_moneycontrol)
    historical_data.update(dividend_payout_from_moneycontrol)
    df_historical_stock_performance    = pd.DataFrame(data=historical_data)
    row_nums = df_historical_stock_performance.shape[0]
    years = []
    for i in range(row_nums):
        current_year = current_year-1
        years.append(current_year)
    df_historical_stock_performance.index = years
    print(df_historical_stock_performance)
    sheet_name  = stock_ticker + ".NS"
    df_historical_stock_performance.to_excel(writer , sheet_name=sheet_name,float_format="%.2f",index=True, startrow=200)
    writer.save()
    writer.close()
    
#Historical_Performance_of_stock('ITC')
