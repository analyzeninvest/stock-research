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
    year_attribute = {}
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
            #print(stock_ticker + " has " +attribute + " of for year " + str(current_year) + " :  " + value)
            year_attribute.update({str(current_year):value})
    elif attribute in ['totalRevenue', 'interestExpense', 'incomeBeforeTax', 'incomeTaxExpense']:
        page = requests.get(income_statement_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        match_string = '"incomeStatementHistory":[[].*"'+attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+ '":{"raw":([-]?[0-9.]+).*},"' +attribute+'":{"raw":([-]?[0-9.]+).*}.*[]]'
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
        # print(stock_ticker + " has " +attribute + " for "+ str(current_year -1) + " as :"  + attribute_value[0])
        # print(stock_ticker + " has " +attribute + " for "+ str(current_year -2) + " as :"  + attribute_value[1])
        # print(stock_ticker + " has " +attribute + " for "+ str(current_year -3) + " as :"  + attribute_value[2])
        # print(stock_ticker + " has " +attribute + " for "+ str(current_year -4) + " as :"  + attribute_value[3])
        for value in attribute_value:
            year_attribute.update({str(current_year-1):value})
            current_year -= 1
    elif attribute in ['totalCurrentAssets', 'totalCurrentLiabilities', 'longTermDebt']:
        page = requests.get(balance_sheet_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        match_string = '"balanceSheetHistory":."balanceSheetStatements":[[].*"'+attribute+ '":."raw":([-]?[0-9.]+).*"' +attribute+ '":."raw":([-]?[0-9.]+).*"' +attribute+ '":."raw":([-]?[0-9.]+).*,"' +attribute+'":."raw":([-]?[0-9.]+).*[]]'
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
        # print(stock_ticker + " has " +attribute + " for "+ str(current_year -1) + " as :"  + attribute_value[0])
        # print(stock_ticker + " has " +attribute + " for "+ str(current_year -2) + " as :"  + attribute_value[1])
        # print(stock_ticker + " has " +attribute + " for "+ str(current_year -3) + " as :"  + attribute_value[2])
        # print(stock_ticker + " has " +attribute + " for "+ str(current_year -4) + " as :"  + attribute_value[3])
        for value in attribute_value:
            year_attribute.update({str(current_year-1):value})
            current_year -= 1
    elif attribute in ['depreciation', 'netIncome', 'capitalExpenditures']:
        page = requests.get(cash_flow_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        match_string = '"cashflowStatementHistory":."cashflowStatements":[[].*?"'+attribute+ '":{"raw":([-]?[0-9.]+).*?},"' +attribute+ '":{"raw":([-]?[0-9.]+).*?},"' +attribute+ '":{"raw":([-]?[0-9.]+).*?},"' +attribute+'":{"raw":([-]?[0-9.]+).*}.*[]]'
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
                #print(match.group(0))
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
        for value in attribute_value:
            year_attribute.update({str(current_year-1):value})
            current_year -= 1
        # print(stock_ticker + " has " +attribute + " for "+ str(current_year -1) + " as :"  + attribute_value[0])
        # print(stock_ticker + " has " +attribute + " for "+ str(current_year -2) + " as :"  + attribute_value[1])
        # print(stock_ticker + " has " +attribute + " for "+ str(current_year -3) + " as :"  + attribute_value[2])
        # print(stock_ticker + " has " +attribute + " for "+ str(current_year -4) + " as :"  + attribute_value[3])
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
        year_attribute.update({str(current_year)+'_avg':attribute_value[0]})
        year_attribute.update({str(current_year)+'_low':attribute_value[1]})
        year_attribute.update({str(current_year)+'_high':attribute_value[2]})
        year_attribute.update({str(current_year +1)+'_avg':attribute_value[3]})
        year_attribute.update({str(current_year +1)+'_low':attribute_value[4]})
        year_attribute.update({str(current_year +1)+'_high':attribute_value[5]})

        # print(stock_ticker + " has " +attribute + " of for "+ str(current_year) + " avg: "  + attribute_value[0])
        # print(stock_ticker + " has " +attribute + " of for "+ str(current_year) + " low: "  + attribute_value[1])
        # print(stock_ticker + " has " +attribute + " of for "+ str(current_year) + " high: " + attribute_value[2])
        # next_year = current_year + 1
        # print(stock_ticker + " has " +attribute + " of for "+ str(next_year) + " avg: "  + attribute_value[3])
        # print(stock_ticker + " has " +attribute + " of for "+ str(next_year) + " low: "  + attribute_value[4])
        # print(stock_ticker + " has " +attribute + " of for "+ str(next_year) + " high: " + attribute_value[5])
    return(year_attribute)

def print_yahoo_financials_for_DCF(stock_ticker):

    print(pull_attribute_from_yahoo(stock_ticker, 'beta'))
    print(pull_attribute_from_yahoo(stock_ticker, 'marketCap'))
    print(pull_attribute_from_yahoo(stock_ticker, 'sharesOutstanding'))
    print(pull_attribute_from_yahoo(stock_ticker, 'totalRevenue'))
    print(pull_attribute_from_yahoo(stock_ticker, 'netIncome'))
    print(pull_attribute_from_yahoo(stock_ticker, 'incomeBeforeTax'))
    print(pull_attribute_from_yahoo(stock_ticker, 'incomeTaxExpense'))
    print(pull_attribute_from_yahoo(stock_ticker, 'totalCurrentAssets'))
    print(pull_attribute_from_yahoo(stock_ticker, 'totalCurrentLiabilities'))
    print(pull_attribute_from_yahoo(stock_ticker, 'longTermDebt'))
    print(pull_attribute_from_yahoo(stock_ticker, 'interestExpense'))
    print(pull_attribute_from_yahoo(stock_ticker, 'depreciation'))
    print(pull_attribute_from_yahoo(stock_ticker, 'capitalExpenditures'))
    print(pull_attribute_from_yahoo(stock_ticker, 'revenueEstimate'))

print_yahoo_financials_for_DCF('MOIL.NS')
#print(pull_attribute_from_yahoo('AAPL', 'revenueEstimate'))
