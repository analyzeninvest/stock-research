#!/usr/bin/env python

def get_balancesheet_parameter_from_moneycontrol(stock, parameter):
    """This is a generic function for getting the historical parameters
    like EPS, EV etc from moneycontrol website.
    http://www.moneycontrol.com/india/financials/infosys/balance-sheet/IT?classic=true
    Idea is to generate a table for org mode later on for plottiing.
    """
    import requests, re, csv
    from bs4 import BeautifulSoup
    from datetime import date
    url        = 'http://www.moneycontrol.com/india/financials/'+stock+'/balance-sheet/IT?classic=true'
    flag       = False
    count      = 5
    page       = requests.get(url)
    soup       = BeautifulSoup(page.content, 'html.parser')
    all_tables = soup.find_all('table')
    for table in all_tables:
        tr = table.find('tr')
        td = tr.find_all('td')
        #print td
        for line in td:
            match = re.search('^.*Mar .([0-9]+).*$', str(line))
            if match:
                string = "\nYear: 20" + match.group(1)
                print(string)
        tr = table.find_all('tr')
        for each_td in tr:
            td = each_td.find_all('td')
            #print td
            for line in td:
                if flag and count != 0:
                    book_value_match = re.search('([0-9]+.[0-9]+)', str(line))
                    string           = "\nBook Value:" + book_value_match.group(1)
                    print(string)
                    count -= 1
                match = re.search('^.*Book Value.*$', str(line))
                if match:
                    flag = True


def get_balancesheet_parameter_from_screener(stock, parameter):
    """This is a generic function for getting the historical parameters
    like EPS, EV etc from moneycontrol website.
    https://www.screener.in/company/AMBUJACEM/consolidated/#ratios
    Idea is to generate a table for org mode later on for plottiing.
    """
    import requests, re, csv
    from bs4 import BeautifulSoup
    from datetime import date
    url        = 'https://www.screener.in/company/'+stock+'/consolidated/'
    flag       = False
    count      = 5
    page       = requests.get(url)
    soup       = BeautifulSoup(page.content, 'html.parser')
    all_tables = soup.find_all('table')
    print(all_tables)
    for table in all_tables:
        tr = table.find('tr')
        td = tr.find_all('td')
        #print td
        for line in td:
            match = re.search('^.*Mar .([0-9]+).*$', str(line))
            if match:
                string = '\nYear: 20' + match.group(1)
                print(string)
        tr = table.find_all('tr')
        for each_td in tr:
            td = each_td.find_all('td')
            #print td
            for line in td:
                if flag and count != 0:
                    book_value_match = re.search('([0-9]+.[0-9]+)', str(line))
                    string = "\nBook Value:" + book_value_match.group(1)
                    print(string)
                    count -= 1
                match = re.search('^.*Book Value.*$', str(line))
                if match:
                    flag = True
                    
#get_balancesheet_parameter_from_moneycontrol('infosys', 'book value')
#get_balancesheet_parameter_from_screener('INFY', 'book value')


def pull_10y_data_from_screener(stock):
    """
    This funtion will pull 10 years of data from the scrneer.in
    The data will be next plotted. The fetched data are:
    Income statement / profit loss statement:
    EPS
    Rations:
    debt/equity
    current ratio
    """
    import requests, re, csv
    from bs4 import BeautifulSoup
    from datetime import date
    url        = 'https://www.screener.in/company/'+stock+'/consolidated/'
    flag       = False
    count      = 15
    page       = requests.get(url)
    soup       = BeautifulSoup(page.content, 'html.parser')
    all_tables = soup.find_all('table')
    for table in all_tables:
        td = table.find_all('th')
        for each_td in td:
            # this has issues , need to find a way to search only after certain tag
            match = re.search('([Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec]+ [0-9]+)',str(each_td))
            if match and count != 0:
                if count <= 12:
                    print(match.group(1))
                flag = True
                count -= 1
            if count == 0:
                flag = False



print('INFOSYS')    
pull_10y_data_from_screener('INFY')
print('AMBUJA CEMENT')    
pull_10y_data_from_screener('AMBUJACEM')
