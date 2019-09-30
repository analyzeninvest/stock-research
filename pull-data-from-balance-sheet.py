#!/usr/bin/env python

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
    ###########################################################################
    #                           Initilize variables                           #
    ###########################################################################
    url     = 'https://www.screener.in/company/'+stock+'/consolidated/'
    page    = requests.get(url)
    soup    = BeautifulSoup(page.content, 'html.parser')
    headers = soup.find_all('h2')
    eps     = []
    year    = []
    debt    = []
    ###########################################################################
    #                     Profit & Loss / Income Statement                    #
    ###########################################################################
    for header in headers:
        if header.find(text=re.compile("Profit & Loss")):
            thelink = header
            break
    years_tr_tag = thelink.findNext('tr')
    ths = years_tr_tag.find_all('th')
    for th in ths:
        match = re.search('([Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec]+ [0-9]+)',str(th))
        if match:
            print("Reported Month / Year in Profit & Loss: " + match.group(1))
            year.append(match.group(1))
    next_table = header.findNext('table')
    trs = next_table.find_all('tr')
    for tr in trs:
        match = re.search('EPS',str(tr))
        if match:
            td = tr.findNext('td').findNext('td')
            for i in range(len(year)+1):
                match = re.search('([0-9]+[.][0-9]+)',str(td))
                eps.append(match.group(1))
                print("EPS: "+eps[i])
                td = td.findNext('td')                
    ###################################################################
    #                          Balance Sheet                          #
    ###################################################################
    for header in headers:
        if header.find(text=re.compile("Balance Sheet")):
            thelink = header
            break
    years_tr_tag = thelink.findNext('tr')
    ths = years_tr_tag.find_all('th')
    for th in ths:
        match = re.search('([Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec]+ [0-9]+)',str(th))
        if match:
            print("Reported Month / Year in Balance Sheet: " + match.group(1))
    ###################################################################
    #                            Cash Flow                            #
    ###################################################################
    for header in headers:
        if header.find(text=re.compile("Cash Flow")):
            thelink = header
            break
    # print(thelink)
    years_tr_tag = thelink.findNext('tr')
    ths = years_tr_tag.find_all('th')
    for th in ths:
        # print(th)
        match = re.search('([Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec]+ [0-9]+)',str(th))
        if match:
            print("Reported Month / Year in Cash Flow: " + match.group(1))




print('INFOSYS')    
pull_10y_data_from_screener('INFY')
print('AMBUJA CEMENT')    
pull_10y_data_from_screener('AMBUJACEM')
