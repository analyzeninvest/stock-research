#!/usr/bin/env python

def pull_attribute_from_yahoo(stock_ticker, attribute):
    """
    This function is for pulling the data_range from yahoo finance.
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
    attribute_value = []
    year_range = []
    today = date.today()
    current_year = today.year
    if attribute in ['beta', 'marketCap', 'sharesOutstanding']:
        page = requests.get(statistics_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        match_string = '"'+attribute+'":{"raw":([-]?[0-9.]+),"fmt":"[0-9.]*[A-Z]*.*"}'
        pattern = re.compile(match_string, re.MULTILINE )
        script = soup.find('script', text=pattern)
        if script:
            match = pattern.search(script.text)
            if match:
                attribute_value.append(match.group(1))
            else:
                attribute_value.append(str(0))
        else:
            attribute_value.append(str(0))
        for value in attribute_value:
            print(stock_ticker + " has " +attribute + " of for year " + str(current_year) + " :  " + value)
    elif attribute in ['revenue', 'netIncome', 'ebit', 'interestExpense']:
        page = requests.get(income_statement_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        match_string = '"cashflowStatements":[[].*"'+attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+'":{"raw":([-]?[0-9.]+).*}.*[]]'
        #match_string = '"cashflowStatements":[[].*[]]'
        #print(match_string)
        pattern = re.compile(match_string, re.MULTILINE )
        #print(pattern)
        script = soup.find('script', text=pattern)
        if script:
            #print("script found")
            match = pattern.search(script.text)
            if match:
                #print("match found")
                attribute_value.append(match.group(1))
                attribute_value.append(match.group(2))
                attribute_value.append(match.group(3))
                attribute_value.append(match.group(4))
            else:
                #print("match not found")
                attribute_value.append(str(0))
                attribute_value.append(str(0))
                attribute_value.append(str(0))
                attribute_value.append(str(0))
        else:
            #print("script not found")
            attribute_value.append(str(0))
            attribute_value.append(str(0))
            attribute_value.append(str(0))
            attribute_value.append(str(0))
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -1) + " as :"  + attribute_value[0])
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -2) + " as :"  + attribute_value[1])
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -3) + " as :"  + attribute_value[2])
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -4) + " as :"  + attribute_value[3])
    elif attribute in ['incomeBeforeTax', 'incomeTaxExpense']:
        page = requests.get(income_statement_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        match_string = '"cashflowStatements":[[].*"'+attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+'":{"raw":([-]?[0-9.]+).*}.*[]]'
        #match_string = '"cashflowStatements":[[].*[]]'
        #print(match_string)
        pattern = re.compile(match_string, re.MULTILINE )
        #print(pattern)
        script = soup.find('script', text=pattern)
        if script:
            #print("script found")
            match = pattern.search(script.text)
            if match:
                #print("match found")
                attribute_value.append(match.group(1))
                attribute_value.append(match.group(2))
                attribute_value.append(match.group(3))
                attribute_value.append(match.group(4))
            else:
                #print("match not found")
                attribute_value.append(str(0))
                attribute_value.append(str(0))
                attribute_value.append(str(0))
                attribute_value.append(str(0))
        else:
            #print("script not found")
            attribute_value.append(str(0))
            attribute_value.append(str(0))
            attribute_value.append(str(0))
            attribute_value.append(str(0))
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -1) + " as :"  + attribute_value[0])
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -2) + " as :"  + attribute_value[1])
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -3) + " as :"  + attribute_value[2])
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -4) + " as :"  + attribute_value[3])
    elif attribute in ['totalCurrentAssets', 'totalCurrentLiabilities', 'longTermDebt']:
        page = requests.get(balance_sheet_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        match_string = '"cashflowStatements":[[].*"'+attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+'":{"raw":([-]?[0-9.]+).*}.*[]]'
        #match_string = '"cashflowStatements":[[].*[]]'
        #print(match_string)
        pattern = re.compile(match_string, re.MULTILINE )
        #print(pattern)
        script = soup.find('script', text=pattern)
        if script:
            #print("script found")
            match = pattern.search(script.text)
            if match:
                #print("match found")
                attribute_value.append(match.group(1))
                attribute_value.append(match.group(2))
                attribute_value.append(match.group(3))
                attribute_value.append(match.group(4))
            else:
                #print("match not found")
                attribute_value.append(str(0))
                attribute_value.append(str(0))
                attribute_value.append(str(0))
                attribute_value.append(str(0))
        else:
            #print("script not found")
            attribute_value.append(str(0))
            attribute_value.append(str(0))
            attribute_value.append(str(0))
            attribute_value.append(str(0))
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -1) + " as :"  + attribute_value[0])
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -2) + " as :"  + attribute_value[1])
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -3) + " as :"  + attribute_value[2])
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -4) + " as :"  + attribute_value[3])
    elif attribute in ['depreciation', 'capitalExpenditures']:
        page = requests.get(cash_flow_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        match_string = '"cashflowStatements":[[].*"'+attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+'":{"raw":([-]?[0-9.]+).*}.*[]]'
        #match_string = '"cashflowStatements":[[].*[]]'
        #print(match_string)
        pattern = re.compile(match_string, re.MULTILINE )
        #print(pattern)
        script = soup.find('script', text=pattern)
        if script:
            #print("script found")
            match = pattern.search(script.text)
            if match:
                #print("match found")
                attribute_value.append(match.group(1))
                attribute_value.append(match.group(2))
                attribute_value.append(match.group(3))
                attribute_value.append(match.group(4))
            else:
                #print("match not found")
                attribute_value.append(str(0))
                attribute_value.append(str(0))
                attribute_value.append(str(0))
                attribute_value.append(str(0))
        else:
            #print("script not found")
            attribute_value.append(str(0))
            attribute_value.append(str(0))
            attribute_value.append(str(0))
            attribute_value.append(str(0))
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -1) + " as :"  + attribute_value[0])
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -2) + " as :"  + attribute_value[1])
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -3) + " as :"  + attribute_value[2])
        print(stock_ticker + " has " +attribute + " for "+ str(current_year -4) + " as :"  + attribute_value[3])
                
    elif attribute in ['revenueEstimate']:
        page = requests.get(analysis_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        match_string = attribute+'.*'+attribute+'.*"'+attribute+'":{"avg":{"raw":([-]?[0-9.]+).*?"low":{"raw":([-]?[0-9.]+).*?"high":{"raw":([-]?[0-9.]+),.*'+attribute+ '":{"avg":{"raw":([-]?[0-9.]+).*"low":{"raw":([-]?[0-9.]+).*"high":{"raw":([-]?[0-9.]+),.*'+attribute+'.*'+attribute
        #print(match_string)
        pattern = re.compile(match_string, re.MULTILINE )
        #print(pattern)
        script = soup.find('script', text=pattern)
        if script:
            #print("script found")
            match = pattern.search(script.text)
            if match:
                #print("match found")
                attribute_value.append(match.group(1))
                attribute_value.append(match.group(2))
                attribute_value.append(match.group(3))
                attribute_value.append(match.group(4))
                attribute_value.append(match.group(5))
                attribute_value.append(match.group(6))
            else:
                #print("match not found")
                attribute_value.append(str(0))
                attribute_value.append(str(0))
                attribute_value.append(str(0))
                attribute_value.append(str(0))
                attribute_value.append(str(0))
                attribute_value.append(str(0))
        else:
            #print("script not found")
            attribute_value.append(str(0))
            attribute_value.append(str(0))
            attribute_value.append(str(0))
            attribute_value.append(str(0))
            attribute_value.append(str(0))
            attribute_value.append(str(0))
        print(stock_ticker + " has " +attribute + " of for "+ str(current_year) + " avg: "  + attribute_value[0])
        print(stock_ticker + " has " +attribute + " of for "+ str(current_year) + " low: "  + attribute_value[1])
        print(stock_ticker + " has " +attribute + " of for "+ str(current_year) + " high: " + attribute_value[2])
        next_year = current_year + 1
        print(stock_ticker + " has " +attribute + " of for "+ str(next_year) + " avg: "  + attribute_value[3])
        print(stock_ticker + " has " +attribute + " of for "+ str(next_year) + " low: "  + attribute_value[4])
        print(stock_ticker + " has " +attribute + " of for "+ str(next_year) + " high: " + attribute_value[5])



# testing the code :
pull_attribute_from_yahoo('AAPL', 'beta')
pull_attribute_from_yahoo('AAPL', 'marketCap')
pull_attribute_from_yahoo('AAPL', 'sharesOutstanding')
pull_attribute_from_yahoo('AAPL', 'revenue')
pull_attribute_from_yahoo('AAPL', 'netIncome')
pull_attribute_from_yahoo('AAPL', 'ebit')
pull_attribute_from_yahoo('AAPL', 'incomeBeforeTax')
pull_attribute_from_yahoo('AAPL', 'incomeTaxExpense')
pull_attribute_from_yahoo('AAPL', 'totalCurrentAssets')
pull_attribute_from_yahoo('AAPL', 'totalCurrentLiabilities')
pull_attribute_from_yahoo('AAPL', 'longTermDebt')
pull_attribute_from_yahoo('AAPL', 'depreciation')
pull_attribute_from_yahoo('AAPL', 'capitalExpenditures')
pull_attribute_from_yahoo('AAPL', 'revenueEstimate')

