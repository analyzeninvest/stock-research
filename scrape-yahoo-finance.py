#!/usr/bin/env python

def pull_attribute_from_yahoo(stock_ticker, attribute):
    """
    This function is for pulling the data from yahoo finance.
    Idea is to pass the argument & find it from the website.
    Following Data are needed for the FCF Calculation:
    |-------------------------+------------------|
    | attribute               | page             |
    |-------------------------+------------------|
    | shares outstanding      | statistics       |
    | beta                    | statistics       |
    | total market capital    | statistics       |
    | total revenue           | Income Statement |
    | net income              | Income Statement |
    | EBITDA                  | Income Statement |
    | D & A                   | Cash Flow        |
    | income before tax       | Income Statement |
    | income tax expenses     | Income Statement |
    | Current Assets          | Balance Sheet    |
    | Current Liabilities     | Balance Sheet    |
    | Capital Expenditure     | Cash Flow        |
    | Interest Expenses       | Income Statement |
    | Long Term Loans         | Balance Sheet    |
    | Estimated total Revenue | Analysis         |
    |-------------------------+------------------|
    """
    import requests, re, csv
    from bs4 import BeautifulSoup
    from datetime import date
    statistics_url = 'https://finance.yahoo.com/quote/'+stock_ticker+'/key-statistics?p='+stock_ticker+''
    income_statement_url = 'https://finance.yahoo.com/quote/'+stock_ticker+'/financials?p='+stock_ticker+''
    balance_sheet_url = 'https://finance.yahoo.com/quote/'+stock_ticker+'/balance-sheet?p='+stock_ticker+''
    cash_flow_url = 'https://finance.yahoo.com/quote/'+stock_ticker+'/cash-flow?p='+stock_ticker+''
    analysis_url = 'https://finance.yahoo.com/quote/'+stock_ticker+'/analysis?p='+stock_ticker+''

    if attribute in ['beta', 'marketCap', 'sharesOutstanding']:
        page = requests.get(statistics_url)
        order = False
        skip = 0
        data = False
    elif attribute in ['revenue', 'netIncome', 'ebit', 'interestExpense']:
        page = requests.get(income_statement_url)
        order = False
        skip = 0
        data = False
        estimate = False
    elif attribute in ['incomeBeforeTax', 'incomeTaxExpense']:
        page = requests.get(income_statement_url)
        order = False
        skip = 4
        data = False        
        estimate = False
    elif attribute in ['totalCurrentAssets', 'totalCurrentLiabilities', 'longTermDebt']:
        page = requests.get(balance_sheet_url)
        order = True
        skip = 0
        data = True
        estimate = False
    elif attribute in ['depreciation', 'capitalExpenditures']:
        page = requests.get(cash_flow_url)
        order = True
        skip = 0
        data = True
        estimate = False
    elif attribute in ['revenueEstimate']:
        page = requests.get(analysis_url)
        order = False
        skip = 0
        data = False
        estimate = True
    
    soup = BeautifulSoup(page.text, 'html.parser')
    match_string = '"'+attribute+'":{"raw":([0-9.]+),"fmt":"[0-9.]*[A-Z]*.*"}'
    
    pattern = re.compile(match_string, re.MULTILINE )
    script = statistics_soup.find('script', text=pattern)
    match = pattern.search(script.text)
    attribute_value = match.group(1)
    print(attribute_value)
    
    



pull_attribute_from_yahoo('FB', 'sharesOutstanding')
