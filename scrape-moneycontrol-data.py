#!/usr/bin/env python

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
    from datetime import date
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
                    

    
pull_ratio_from_moneycontrol('ITC', 'Basic EPS')
# pull_ratio_from_moneycontrol('ITC', 'EPS')
pull_ratio_from_moneycontrol('ITC', 'EV/EBITDA')

