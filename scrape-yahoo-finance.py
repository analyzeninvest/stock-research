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


# testing    
# print_yahoo_financials_for_DCF('MOIL.NS')
# print(pull_attribute_from_yahoo('AAPL', 'marketCap'))


def DCF_valuation(stock_ticker):
    """
    DCF Valuation of the stock.
    This is based on the yahoo finance.
    """
    import pandas as pd
    import numpy as np


def wacc_of_stock(stock_ticker):
    """
    Get the WACC of a stock.
    WACC or Weighted Average Cost of Capital is calculated in the following way:
    r WACC Weighted Average Cost of Capital = w_d * r_d * (1-t) + w_e * r_e
    w_d = weight of debt = (last FY) = long term debt / total market cap
    r_d = rate of debt = (last FY) = intest expenses / long term debt
    t = last tax rate = (last FY) = income tax expense / income before tax
    w_e = weight of equity = 1 - w_d 
    r_e = rate of equity = calculated by CAPM model
    """
    from datetime import date
    today = date.today()
    current_year = today.year
    marketcap_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'marketCap')
    market_cap = int(marketcap_year_from_yahoo.get(str(current_year)))
    debt_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'longTermDebt')
    long_term_debt = int(debt_year_from_yahoo.get(str(current_year -1)))
    interst_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'interestExpense')
    interest_expense = -(int(interst_year_from_yahoo.get(str(current_year -1))))
    tax_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'incomeTaxExpense')
    tax = int(tax_year_from_yahoo.get(str(current_year -1)))
    income_before_tax_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'incomeBeforeTax')
    income_before_tax = int(income_before_tax_year_from_yahoo.get(str(current_year -1)))
    weight_of_debt = long_term_debt / market_cap
    rate_of_debt = interest_expense / long_term_debt
    tax_rate = tax / income_before_tax
    weight_of_equity = 1 - weight_of_debt
    rate_of_equity = rate_of_equity_of_stock(stock_ticker)
    weighted_average_cost_of_capital = (weight_of_debt * rate_of_debt * (1 - tax_rate)) + (weight_of_equity * rate_of_equity)
    return(weighted_average_cost_of_capital)

print(wacc_of_stock('AAPL'))

def rate_of_equity_of_stock(stock_ticker):
    """
    Get the rate of equity of the stock.  This is calculated based on
    the CAPM model.  CAPM or Capital Asset Pricing Model calculates
    the rate of equity in following way:
    r_e = R_f + beta * (R_m - R_f)
    where:
    r_e = rate of equity.
    beta is obtained from the statistics of the stock.
    R_m = Rate of Return of the market in general.
    R_f = Risk free rate of return.
    R_m = 10%   (general return of the SNP 500 index fund)
    R_f = 1.88% (10y US treasury bond yield)
    """
    from datetime import date
    today = date.today()
    current_year = today.year
    beta_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'beta')
    beta = float(beta_year_from_yahoo.get(str(current_year)))
    risk_free_rate = 0.0188
    return_of_market = 0.10
    rate_of_equity = risk_free_rate + (beta * (return_of_market - risk_free_rate))
    return(rate_of_equity)
    
# print(rate_of_equity_of_stock('AAPL'))
