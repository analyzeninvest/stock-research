#!/usr/bin/env python

MAX_TAX_RATE                = 0.35
LONG_TERM_GROWTH_RATE       = 0.025
BOND_RATE_10Y_US            = 0.0188
FD_RATE_INDIA               = 0.07
AVG_RETURN_OF_MARKET_US     = 0.10
AVG_RETURN_OF_MARKET_INDIA  = 0.12
DISCOUNT_FACTOR_INDIA       = 0.15
DISCOUNT_FACTOR_US          = 0.075
YEARS_TILL_STABLE_GROWTH    = 10

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
    import requests, re
    from bs4 import BeautifulSoup
    from datetime import date
    statistics_url        = 'https://finance.yahoo.com/quote/'+stock_ticker+'/key-statistics?p='+stock_ticker+''
    income_statement_url  = 'https://finance.yahoo.com/quote/'+stock_ticker+'/financials?p='+stock_ticker+''
    balance_sheet_url     = 'https://finance.yahoo.com/quote/'+stock_ticker+'/balance-sheet?p='+stock_ticker+''
    cash_flow_url         = 'https://finance.yahoo.com/quote/'+stock_ticker+'/cash-flow?p='+stock_ticker+''
    analysis_url          = 'https://finance.yahoo.com/quote/'+stock_ticker+'/analysis?p='+stock_ticker+''
    profile_url           = 'https://in.finance.yahoo.com/quote/'+stock_ticker+'/profile?p='+stock_ticker+''
    attribute_value       = []
    year_range            = []
    year_attribute        = {}
    today                 = date.today()
    current_year          = today.year
    if attribute in ['beta', 'marketCap', 'sharesOutstanding']:
        page          = requests.get(statistics_url)
        soup          = BeautifulSoup(page.text, 'html.parser')
        match_string  = '"'+attribute+'":{"raw":([-]?[0-9.]+),"fmt":"[0-9.]*[A-Z]*.*"}'
        pattern       = re.compile(match_string, re.MULTILINE )
        script        = soup.find('script', text=pattern)
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
    elif attribute in ['longName', 'symbol', 'sector', 'industry', 'regularMarketPrice']:
        page          = requests.get(profile_url)
        soup          = BeautifulSoup(page.text, 'html.parser')
        if attribute == 'regularMarketPrice':
            match_string  = '"'+attribute+'":{"raw":([0-9.]+),"fmt":".*?"}'
        elif attribute in ['longName', 'symbol', 'sector', 'industry'] :
            match_string  = '"'+attribute+'":"(.*?)"'
        pattern       = re.compile(match_string, re.MULTILINE )
        script        = soup.find('script', text=pattern)
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
    elif attribute in ['totalCurrentAssets', 'totalCurrentLiabilities', 'longTermDebt', 'totalStockholderEquity']:
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
    elif attribute in ['depreciation', 'netIncome', 'capitalExpenditures', 'dividendsPaid']:
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

#print(pull_attribute_from_yahoo('ENGINERSIN.NS', 'dividendsPaid'))
#print(pull_attribute_from_yahoo('ENGINERSIN.NS', 'netIncome'))
#print(pull_attribute_from_yahoo('RECLTD.NS', 'dividendsPaid'))
#print(pull_attribute_from_yahoo('RECLTD.NS', 'netIncome'))

#print(pull_attribute_from_yahoo('AAPL', 'totalStockholderEquity'))
# print(pull_attribute_from_yahoo('AAPL', 'longName'))
# print(pull_attribute_from_yahoo('AAPL', 'sector'))
# print(pull_attribute_from_yahoo('AAPL', 'industry'))
# print(pull_attribute_from_yahoo('AAPL', 'regularMarketPrice'))
# print(pull_attribute_from_yahoo('LT.NS', 'longTermDebt'))

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

# print_yahoo_financials_for_DCF('LT.NS')

def Create_Financial_Statements_DataFrame_for_DCF(stock_ticker):
    """
    This will give out the Financial Statement Data Frame needed for DCF Valuation.
    Following are derived:
    1. EBITDA = Net Income + Tax + Interest Expenses + Depreciation and Amortization 
    2. NWC Net Working Capital = Current Assets - Current Liabilities
    3. t tax Rate = Tax / Income Before Tax
    4. FCF Free Cash Flow = EBIT * (1 - t) + NWC + D&A - CapEx
    5. FCF / Net Income 
    6. Net Income Margin = Net Income / Total Revenue
    """
    import pandas as pd
    from datetime import date
    today                                    = date.today()
    current_year                             = today.year
    financials_of_stock                      = {}
    longTermDebt_year_from_yahoo             = pull_attribute_from_yahoo(stock_ticker, 'longTermDebt')
    longTermDebt_year_1                      = abs(int(longTermDebt_year_from_yahoo.get(str(current_year -4))))
    longTermDebt_year_2                      = abs(int(longTermDebt_year_from_yahoo.get(str(current_year -3))))
    longTermDebt_year_3                      = abs(int(longTermDebt_year_from_yahoo.get(str(current_year -2))))
    longTermDebt_year_4                      = abs(int(longTermDebt_year_from_yahoo.get(str(current_year -1))))
    totalCurrentLiabilities_year_from_yahoo  = pull_attribute_from_yahoo(stock_ticker, 'totalCurrentLiabilities')
    totalCurrentLiabilities_year_1           = abs(int(totalCurrentLiabilities_year_from_yahoo.get(str(current_year -4))))
    totalCurrentLiabilities_year_2           = abs(int(totalCurrentLiabilities_year_from_yahoo.get(str(current_year -3))))
    totalCurrentLiabilities_year_3           = abs(int(totalCurrentLiabilities_year_from_yahoo.get(str(current_year -2))))
    totalCurrentLiabilities_year_4           = abs(int(totalCurrentLiabilities_year_from_yahoo.get(str(current_year -1))))
    totalCurrentAssets_year_from_yahoo       = pull_attribute_from_yahoo(stock_ticker, 'totalCurrentAssets')
    totalCurrentAssets_year_1                = abs(int(totalCurrentAssets_year_from_yahoo.get(str(current_year -4))))
    totalCurrentAssets_year_2                = abs(int(totalCurrentAssets_year_from_yahoo.get(str(current_year -3))))
    totalCurrentAssets_year_3                = abs(int(totalCurrentAssets_year_from_yahoo.get(str(current_year -2))))
    totalCurrentAssets_year_4                = abs(int(totalCurrentAssets_year_from_yahoo.get(str(current_year -1))))
    incomeTaxExpense_year_from_yahoo         = pull_attribute_from_yahoo(stock_ticker, 'incomeTaxExpense')
    incomeTaxExpense_year_1                  = abs(int(incomeTaxExpense_year_from_yahoo.get(str(current_year -4))))
    incomeTaxExpense_year_2                  = abs(int(incomeTaxExpense_year_from_yahoo.get(str(current_year -3))))
    incomeTaxExpense_year_3                  = abs(int(incomeTaxExpense_year_from_yahoo.get(str(current_year -2))))
    incomeTaxExpense_year_4                  = abs(int(incomeTaxExpense_year_from_yahoo.get(str(current_year -1))))
    totalRevenue_year_from_yahoo             = pull_attribute_from_yahoo(stock_ticker, 'totalRevenue')
    Revenue_year_1                           = abs(int(totalRevenue_year_from_yahoo.get(str(current_year -4))))
    Revenue_year_2                           = abs(int(totalRevenue_year_from_yahoo.get(str(current_year -3))))
    Revenue_year_3                           = abs(int(totalRevenue_year_from_yahoo.get(str(current_year -2))))
    Revenue_year_4                           = abs(int(totalRevenue_year_from_yahoo.get(str(current_year -1))))
    netIncome_year_from_yahoo                = pull_attribute_from_yahoo(stock_ticker, 'netIncome')
    netIncome_year_1                         = abs(int(netIncome_year_from_yahoo.get(str(current_year -4))))
    netIncome_year_2                         = abs(int(netIncome_year_from_yahoo.get(str(current_year -3))))
    netIncome_year_3                         = abs(int(netIncome_year_from_yahoo.get(str(current_year -2))))
    netIncome_year_4                         = abs(int(netIncome_year_from_yahoo.get(str(current_year -1))))
    incomeBeforeTax_year_from_yahoo          = pull_attribute_from_yahoo(stock_ticker, 'incomeBeforeTax')
    incomeBeforeTax_year_1                   = abs(int(incomeBeforeTax_year_from_yahoo.get(str(current_year -4))))
    incomeBeforeTax_year_2                   = abs(int(incomeBeforeTax_year_from_yahoo.get(str(current_year -3))))
    incomeBeforeTax_year_3                   = abs(int(incomeBeforeTax_year_from_yahoo.get(str(current_year -2))))
    incomeBeforeTax_year_4                   = abs(int(incomeBeforeTax_year_from_yahoo.get(str(current_year -1))))
    depreciation_year_from_yahoo             = pull_attribute_from_yahoo(stock_ticker, 'depreciation')
    D_n_A_year_1                             = abs(int(depreciation_year_from_yahoo.get(str(current_year -4))))
    D_n_A_year_2                             = abs(int(depreciation_year_from_yahoo.get(str(current_year -3))))
    D_n_A_year_3                             = abs(int(depreciation_year_from_yahoo.get(str(current_year -2))))
    D_n_A_year_4                             = abs(int(depreciation_year_from_yahoo.get(str(current_year -1))))
    interestExpense_year_from_yahoo          = pull_attribute_from_yahoo(stock_ticker, 'interestExpense')
    interestExpense_year_1                   = abs(int(interestExpense_year_from_yahoo.get(str(current_year -4))))
    interestExpense_year_2                   = abs(int(interestExpense_year_from_yahoo.get(str(current_year -3))))
    interestExpense_year_3                   = abs(int(interestExpense_year_from_yahoo.get(str(current_year -2))))
    interestExpense_year_4                   = abs(int(interestExpense_year_from_yahoo.get(str(current_year -1))))
    capitalExpenditures_year_from_yahoo      = pull_attribute_from_yahoo(stock_ticker, 'capitalExpenditures')
    capitalExpenditures_year_1               = abs(int(capitalExpenditures_year_from_yahoo.get(str(current_year -4))))
    capitalExpenditures_year_2               = abs(int(capitalExpenditures_year_from_yahoo.get(str(current_year -3))))
    capitalExpenditures_year_3               = abs(int(capitalExpenditures_year_from_yahoo.get(str(current_year -2))))
    capitalExpenditures_year_4               = abs(int(capitalExpenditures_year_from_yahoo.get(str(current_year -1))))
    financials_of_stock.update({'Total Revenue':[Revenue_year_1, Revenue_year_2, Revenue_year_3, Revenue_year_4]})
    financials_of_stock.update({'Net Income':[netIncome_year_1, netIncome_year_2, netIncome_year_3, netIncome_year_4]})
    financials_of_stock.update({'Income Before Tax':[incomeBeforeTax_year_1, incomeBeforeTax_year_2, incomeBeforeTax_year_3, incomeBeforeTax_year_4]})
    financials_of_stock.update({'Income Tax Expenses':[incomeTaxExpense_year_1, incomeTaxExpense_year_2, incomeTaxExpense_year_3, incomeTaxExpense_year_4]})
    financials_of_stock.update({'Interest Expenses':[interestExpense_year_1, interestExpense_year_2, interestExpense_year_3, interestExpense_year_4]})
    financials_of_stock.update({'Long Term Debt':[longTermDebt_year_1, longTermDebt_year_2, longTermDebt_year_3, longTermDebt_year_4]})
    financials_of_stock.update({'Current Assets':[totalCurrentAssets_year_1, totalCurrentAssets_year_2, totalCurrentAssets_year_3, totalCurrentAssets_year_4]})
    financials_of_stock.update({'Current Liabilities':[totalCurrentLiabilities_year_1, totalCurrentLiabilities_year_2, totalCurrentLiabilities_year_3, totalCurrentLiabilities_year_4]})
    financials_of_stock.update({'Capital Expenditures':[capitalExpenditures_year_1, capitalExpenditures_year_2, capitalExpenditures_year_3, capitalExpenditures_year_4]})
    financials_of_stock.update({'Depreciation and Amortization':[D_n_A_year_1, D_n_A_year_2, D_n_A_year_3, D_n_A_year_4]})
    df_financial          = pd.DataFrame(data = financials_of_stock,index=[ str(current_year -4), str(current_year -3), str(current_year -2), str(current_year -1)])
    df_financial['EBIT']  = df_financial['Net Income'] + df_financial['Income Tax Expenses'] + df_financial['Interest Expenses']
    df_financial['Net Working Capital'] = df_financial['Current Assets'] - df_financial['Current Liabilities']
    df_financial['Tax Rate'] = df_financial['Income Tax Expenses'] / df_financial['Income Before Tax']
    df_financial.loc[df_financial['Tax Rate'] > MAX_TAX_RATE, 'Tax Rate']  = MAX_TAX_RATE
    df_financial['Free Cash Flow'] = df_financial['EBIT'] * (1 - df_financial['Tax Rate']) + df_financial['Net Working Capital'] + df_financial['Depreciation and Amortization'] - df_financial['Capital Expenditures']
    df_financial['FCF/Net Income']       = df_financial['Free Cash Flow'] / df_financial['Net Income']
    df_financial['Net Income Margin']    = df_financial['Net Income'] / df_financial['Total Revenue']
    df_financial['Revenue Growth Rate']  = df_financial['Total Revenue'].pct_change()
    df_financial = df_financial[['Free Cash Flow', 'FCF/Net Income', 'Net Income Margin', 'Total Revenue', 'Revenue Growth Rate', 'Tax Rate', 'Income Tax Expenses', 'Income Before Tax', 'Net Working Capital', 'Current Assets' , 'Current Liabilities', 'EBIT', 'Net Income', 'Interest Expenses', 'Long Term Debt', 'Depreciation and Amortization', 'Capital Expenditures']]
    print(df_financial)
    return(df_financial)

#print("\n")
#print(Create_Financial_Statements_DataFrame_for_DCF('AAPL'))

def rate_of_equity_of_stock_CAPM(stock_ticker):
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
    today                 = date.today()
    current_year          = today.year
    beta_year_from_yahoo  = pull_attribute_from_yahoo(stock_ticker, 'beta')
    beta                  = float(beta_year_from_yahoo.get(str(current_year)))
    stock_end = stock_ticker.split(".")
    if len(stock_end)==2:
        if stock_end[1] == "NS" or stock_end[1] == "BO":
            risk_free_rate        = FD_RATE_INDIA
            return_of_market      = AVG_RETURN_OF_MARKET_US
    else:
        risk_free_rate        = BOND_RATE_10Y_US
        return_of_market      = AVG_RETURN_OF_MARKET_INDIA
    rate_of_equity        = risk_free_rate + (beta * (return_of_market - risk_free_rate))
    return(rate_of_equity)
    
# print(rate_of_equity_of_stock_CAPM('AAPL'))

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
    set tax rate to 25% if the last value is greater than 25%. 
    There can be such cases when :
    there is any income tax refund / tax paid more for some pending tax.
    But this will not happen in the future.
    25% is a value that is universally true for most companies.
    """
    from datetime import date
    today                              = date.today()
    current_year                       = today.year
    marketcap_year_from_yahoo          = pull_attribute_from_yahoo(stock_ticker, 'marketCap')
    market_cap                         = int(marketcap_year_from_yahoo.get(str(current_year)))
    debt_year_from_yahoo               = pull_attribute_from_yahoo(stock_ticker, 'longTermDebt')
    long_term_debt                     = int(debt_year_from_yahoo.get(str(current_year -1)))
    interst_year_from_yahoo            = pull_attribute_from_yahoo(stock_ticker, 'interestExpense')
    interest_expense                   = -(int(interst_year_from_yahoo.get(str(current_year -1))))
    tax_year_from_yahoo                = pull_attribute_from_yahoo(stock_ticker, 'incomeTaxExpense')
    tax                                = int(tax_year_from_yahoo.get(str(current_year -1)))
    income_before_tax_year_from_yahoo  = pull_attribute_from_yahoo(stock_ticker, 'incomeBeforeTax')
    income_before_tax                  = int(income_before_tax_year_from_yahoo.get(str(current_year -1)))
    weight_of_debt                     = long_term_debt / market_cap
    if long_term_debt != 0:
        rate_of_debt                   = interest_expense / long_term_debt
    else:
        rate_of_debt                   = 0
    tax_rate                           = tax / income_before_tax
    if tax_rate > MAX_TAX_RATE:
        tax_rate                       = MAX_TAX_RATE
    weight_of_equity                   = 1 - weight_of_debt
    rate_of_equity                     = rate_of_equity_of_stock_CAPM(stock_ticker)
    # print("weight of debt " + str(weight_of_debt))
    # print("rate of debt " + str(rate_of_debt))
    # print("tax rate " + str(tax_rate))
    # print("weight of eq " + str(weight_of_equity))
    # print("rate of eq " + str(rate_of_equity))
    weighted_average_cost_of_capital   = (weight_of_debt * rate_of_debt * (1 - tax_rate)) + (weight_of_equity * rate_of_equity)
    return(weighted_average_cost_of_capital)

# print(wacc_of_stock('RELAXO.NS'))

def Create_Financial_Estimation_DataFrame_for_DCF(stock_ticker, df_actual_finance_of_stock):
    """
    This function will create the Estimation DataFrame for DCF Valuation. 
    """
    import pandas  as pd
    from datetime import date
    today                               = date.today()
    current_year                        = today.year
    financial_estimation_of_stock       = {}
    revenue_estimation_year_from_yahoo  = pull_attribute_from_yahoo(stock_ticker, 'revenueEstimate')
    revenue_estimation_year_1_avg       = abs(int(revenue_estimation_year_from_yahoo.get(str(current_year   )+'_avg' )))
    revenue_estimation_year_1_high      = abs(int(revenue_estimation_year_from_yahoo.get(str(current_year   )+'_high')))
    revenue_estimation_year_1_low       = abs(int(revenue_estimation_year_from_yahoo.get(str(current_year   )+'_low' )))
    revenue_estimation_year_2_avg       = abs(int(revenue_estimation_year_from_yahoo.get(str(current_year +1)+'_avg' )))
    revenue_estimation_year_2_high      = abs(int(revenue_estimation_year_from_yahoo.get(str(current_year +1)+'_high')))
    revenue_estimation_year_2_low       = abs(int(revenue_estimation_year_from_yahoo.get(str(current_year +1)+'_low' )))
    actual_revenue_growth_average       = df_actual_finance_of_stock['Revenue Growth Rate'].mean()
    last_year_revenue                   = df_actual_finance_of_stock.loc[str(current_year -1),'Total Revenue']
    if revenue_estimation_year_1_high  == 0.0:
        revenue_estimation_year_1_high  = last_year_revenue * (1 + actual_revenue_growth_average)
    if revenue_estimation_year_1_avg   == 0.0:
        revenue_estimation_year_1_avg   = last_year_revenue * (1 + actual_revenue_growth_average)
    if revenue_estimation_year_1_low   == 0.0:
        revenue_estimation_year_1_low   = last_year_revenue * (1 + actual_revenue_growth_average)
    if revenue_estimation_year_2_high  == 0.0:
        revenue_estimation_year_2_high  = revenue_estimation_year_1_high * (1 + actual_revenue_growth_average)
    if revenue_estimation_year_2_avg   == 0.0:
        revenue_estimation_year_2_avg   = revenue_estimation_year_1_avg * (1 + actual_revenue_growth_average)
    if revenue_estimation_year_2_low   == 0.0:
        revenue_estimation_year_2_low   = revenue_estimation_year_1_low * (1 + actual_revenue_growth_average)
    financial_estimation_of_stock.update({'Year':[
        str(current_year   )+'_avg' ,
        str(current_year +1)+'_avg' ,
        str(current_year   )+'_high',
        str(current_year +1)+'_high',
        str(current_year   )+'_low' ,
        str(current_year +1)+'_low']})
    financial_estimation_of_stock.update({'Revenue Estimate':[
        revenue_estimation_year_1_avg,
        revenue_estimation_year_2_avg,
        revenue_estimation_year_1_high,
        revenue_estimation_year_2_high,
        revenue_estimation_year_1_low,
        revenue_estimation_year_2_low]})
    df_financial_estimate                              = pd.DataFrame(data = financial_estimation_of_stock)
    df_financial_estimate['Estimated Revenue Growth']  = df_financial_estimate['Revenue Estimate'].pct_change()
    projected_revenue_year_1                           = [
        df_financial_estimate.loc[0,'Revenue Estimate'],
        df_financial_estimate.loc[2,'Revenue Estimate'],
        df_financial_estimate.loc[4,'Revenue Estimate']]
    projected_revenue_growth                           = [
        df_financial_estimate.loc[1,'Estimated Revenue Growth'],
        df_financial_estimate.loc[3,'Estimated Revenue Growth'],
        df_financial_estimate.loc[5,'Estimated Revenue Growth']]
    # df_actual_finance_of_stock          = Create_Financial_Statements_DataFrame_for_DCF(stock_ticker)
    projected_revenue_growth_year_1_avg   = (projected_revenue_year_1[0] - last_year_revenue)/last_year_revenue
    projected_revenue_growth_year_1_high  = (projected_revenue_year_1[1] - last_year_revenue)/last_year_revenue
    projected_revenue_growth_year_1_low   = (projected_revenue_year_1[2] - last_year_revenue)/last_year_revenue
    # print(projected_revenue_growth_year_1_avg)
    # print(projected_revenue_growth_year_1_high)
    # print(projected_revenue_growth_year_1_low)
    revenue_growth_avg                    = (projected_revenue_growth_year_1_avg + actual_revenue_growth_average + projected_revenue_growth[0])/3
    revenue_growth_high                   = (projected_revenue_growth_year_1_high + actual_revenue_growth_average + projected_revenue_growth[1])/3
    revenue_growth_low                    = (projected_revenue_growth_year_1_low + actual_revenue_growth_average + projected_revenue_growth[2])/3
    # print(revenue_growth_avg)
    # print(revenue_growth_high)
    # print(revenue_growth_low)
    last_year_net_income                  = df_actual_finance_of_stock.loc[str(current_year -1),'Net Income']
    last_year_free_cash_flow              = df_actual_finance_of_stock.loc[str(current_year -1),'Free Cash Flow']
    min_net_income_margin                 = df_actual_finance_of_stock['Net Income Margin'].min()
    min_fcf_over_net_income               = df_actual_finance_of_stock['FCF/Net Income'].min()
    # print(min_net_income_margin)
    # print(min_fcf_over_net_income)
    df_financial_estimate                 = df_financial_estimate.drop(columns=['Estimated Revenue Growth'])
    df_financial_estimate                 = df_financial_estimate.reindex([2, 0, 4, 3, 1, 5])
    financial_projection_of_stock         = {}
    financial_projection_of_stock.update({'Year':[
        str(current_year +2)+'_high',
        str(current_year +2)+'_avg' ,
        str(current_year +2)+'_low' ,
        str(current_year +3)+'_high',
        str(current_year +3)+'_avg' ,
        str(current_year +3)+'_low' ,
        str(current_year +4)+'_high',
        str(current_year +4)+'_avg' ,
        str(current_year +4)+'_low']})
    revenue_estimation_year_3_high  = revenue_estimation_year_2_high * (1 + revenue_growth_high)
    revenue_estimation_year_3_avg   = revenue_estimation_year_2_avg * (1 + revenue_growth_avg)
    revenue_estimation_year_3_low   = revenue_estimation_year_2_low * (1 + revenue_growth_low)
    revenue_estimation_year_4_high  = revenue_estimation_year_3_high * (1 + revenue_growth_high)
    revenue_estimation_year_4_avg   = revenue_estimation_year_3_avg * (1 + revenue_growth_avg)
    revenue_estimation_year_4_low   = revenue_estimation_year_3_low * (1 + revenue_growth_low)
    revenue_estimation_year_5_high  = revenue_estimation_year_4_high * (1 + revenue_growth_high)
    revenue_estimation_year_5_avg   = revenue_estimation_year_4_avg * (1 + revenue_growth_avg)
    revenue_estimation_year_5_low   = revenue_estimation_year_4_low * (1 + revenue_growth_low)
    financial_projection_of_stock.update({'Revenue Estimate':[
        revenue_estimation_year_3_high,
        revenue_estimation_year_3_avg,
        revenue_estimation_year_3_low,
        revenue_estimation_year_4_high,
        revenue_estimation_year_4_avg,
        revenue_estimation_year_4_low,
        revenue_estimation_year_5_high,
        revenue_estimation_year_5_avg,
        revenue_estimation_year_5_low,]})
    df_financial_projection                           = pd.DataFrame(data=financial_projection_of_stock)
    df_financial_estimate                             = df_financial_estimate.append(df_financial_projection)
    df_financial_estimate                             = df_financial_estimate[['Year','Revenue Estimate']]
    df_financial_estimate['Net Income Estimate']      = df_financial_estimate['Revenue Estimate'] * min_net_income_margin
    df_financial_estimate['Free Cash Flow Estimate']  = df_financial_estimate['Net Income Estimate'] * min_fcf_over_net_income
    df_financial_estimate                             = df_financial_estimate.reset_index(drop = True)
    print(df_financial_estimate)
    return(df_financial_estimate)

# print("\n")
# print(Create_Financial_Estimation_DataFrame_for_DCF('AAPL'))

def terminal_value_of_stock_perpetual_growth_model(stock_ticker, last_FCF):
    """
    This function finds the terminal value of for the last estimated
    revenue. The Calculation is made using the perpetual growth model.
    Terminal Value = Last Revenue * (1 + g)/(r- g)
    r = required rate of return, this is calculated using the WACC
    g = perpetual growth rate, this is considered to be 2.5%
    """
    r                   = wacc_of_stock(stock_ticker)
    g                   = LONG_TERM_GROWTH_RATE
    if r > g:
        terminal_value  = last_FCF * (1 + g) / (r - g)
    else:
        terminal_value  = last_FCF * (1 + g) / g
    return(terminal_value)


def present_value_by_discount(FCF_1, FCF_2, FCF_3, FCF_4, FCF_5, TV, r):
    """
    Intrinsic Value of the business = FCF_1 / (1+r)^1 + FCF_2 / (1+r)^2 + FCF_3 / (1+r)^3 + FCF_4 / (1+r)^4 + FCF_5 / (1+r)^5 + FCF_5*(1+g)/(r-g)    
    """
    Present_value = (FCF_1 / (pow((1+r),1))) + (FCF_2 / (pow((1+r),2))) + (FCF_3 / (pow((1+r),3))) + (FCF_4 / (pow((1+r),4))) + (FCF_5 / (pow((1+r),5))) + (TV/ (pow((1+r),5)))
    return(Present_value)


def DCF_valuation_of_stock(stock_ticker, df_actual_financials_of_stock, df_financial_projection_of_stock):
    """
    This function calculcates the DCF valuation of a stock.
    DCF Valuation is calculated using the following method:
    Intrinsic Value of the business = FCF_1 / (1+r)^1 + FCF_2 / (1+r)^2 + FCF_3 / (1+r)^3 + FCF_4 / (1+r)^4 + FCF_5 / (1+r)^5 + FCF_5*(1+g)/(r-g)
    Intrinsic Value of Stock = Intrinsic Value of the Business / shares Outstanding
    The valuation is based on the yahoo Finance.
    Since the yahoo Finance estimates 3 range of values for a stock, this method will give out 3 DCF value of the stock.
    """
    import pandas as pd
    from datetime import date
    today                             = date.today()
    current_year                      = today.year
    # print(df_financial_projection_of_stock)
    FCF_high_projection_year_1  = df_financial_projection_of_stock.loc[0,'Free Cash Flow Estimate'] 
    FCF_high_projection_year_2  = df_financial_projection_of_stock.loc[3,'Free Cash Flow Estimate'] 
    FCF_high_projection_year_3  = df_financial_projection_of_stock.loc[6,'Free Cash Flow Estimate'] 
    FCF_high_projection_year_4  = df_financial_projection_of_stock.loc[9,'Free Cash Flow Estimate'] 
    FCF_high_projection_year_5  = df_financial_projection_of_stock.loc[12,'Free Cash Flow Estimate']
    FCF_avg_projection_year_1   = df_financial_projection_of_stock.loc[1,'Free Cash Flow Estimate'] 
    FCF_avg_projection_year_2   = df_financial_projection_of_stock.loc[4,'Free Cash Flow Estimate'] 
    FCF_avg_projection_year_3   = df_financial_projection_of_stock.loc[7,'Free Cash Flow Estimate'] 
    FCF_avg_projection_year_4   = df_financial_projection_of_stock.loc[10,'Free Cash Flow Estimate'] 
    FCF_avg_projection_year_5   = df_financial_projection_of_stock.loc[13,'Free Cash Flow Estimate']
    FCF_low_projection_year_1   = df_financial_projection_of_stock.loc[2,'Free Cash Flow Estimate'] 
    FCF_low_projection_year_2   = df_financial_projection_of_stock.loc[5,'Free Cash Flow Estimate'] 
    FCF_low_projection_year_3   = df_financial_projection_of_stock.loc[8,'Free Cash Flow Estimate'] 
    FCF_low_projection_year_4   = df_financial_projection_of_stock.loc[11,'Free Cash Flow Estimate'] 
    FCF_low_projection_year_5   = df_financial_projection_of_stock.loc[14,'Free Cash Flow Estimate']
    last_FCF_estimate_high      = df_financial_projection_of_stock.loc[12,'Free Cash Flow Estimate']
    last_FCF_estimate_avg       = df_financial_projection_of_stock.loc[13,'Free Cash Flow Estimate']
    last_FCF_estimate_low       = df_financial_projection_of_stock.loc[14,'Free Cash Flow Estimate']
    Terminal_value_high         = terminal_value_of_stock_perpetual_growth_model(stock_ticker, last_FCF_estimate_high)
    Terminal_value_avg          = terminal_value_of_stock_perpetual_growth_model(stock_ticker, last_FCF_estimate_avg)
    Terminal_value_low          = terminal_value_of_stock_perpetual_growth_model(stock_ticker, last_FCF_estimate_low)
    # print(Terminal_value_high)
    # print(Terminal_value_avg)
    # print(Terminal_value_low)
    stock_end = stock_ticker.split(".")
    if len(stock_end)==2:
        if stock_end[1] == "NS" or stock_end[1] == "BO":
            r_fixed = DISCOUNT_FACTOR_INDIA
    else:
        r_fixed = DISCOUNT_FACTOR_US
    r = wacc_of_stock(stock_ticker)
    # print(r)
    Present_value_of_business_wacc_high =  present_value_by_discount(
        FCF_high_projection_year_1,
        FCF_high_projection_year_2,
        FCF_high_projection_year_3,
        FCF_high_projection_year_4,
        FCF_high_projection_year_5,
        Terminal_value_high,
        r)
    Present_value_of_business_wacc_avg = present_value_by_discount(
        FCF_avg_projection_year_1,
        FCF_avg_projection_year_2,
        FCF_avg_projection_year_3,
        FCF_avg_projection_year_4,
        FCF_avg_projection_year_5,
        Terminal_value_avg,
        r)
    Present_value_of_business_wacc_low = present_value_by_discount(
        FCF_low_projection_year_1,
        FCF_low_projection_year_2,
        FCF_low_projection_year_3,
        FCF_low_projection_year_4,
        FCF_low_projection_year_5,
        Terminal_value_low,
        r)
    Present_value_of_business_fixed_high =  present_value_by_discount(
        FCF_high_projection_year_1,
        FCF_high_projection_year_2,
        FCF_high_projection_year_3,
        FCF_high_projection_year_4,
        FCF_high_projection_year_5,
        Terminal_value_high,
        r_fixed)
    Present_value_of_business_fixed_avg = present_value_by_discount(
        FCF_avg_projection_year_1,
        FCF_avg_projection_year_2,
        FCF_avg_projection_year_3,
        FCF_avg_projection_year_4,
        FCF_avg_projection_year_5,
        Terminal_value_avg,
        r_fixed)
    Present_value_of_business_fixed_low = present_value_by_discount(
        FCF_low_projection_year_1,
        FCF_low_projection_year_2,
        FCF_low_projection_year_3,
        FCF_low_projection_year_4,
        FCF_low_projection_year_5,
        Terminal_value_low,
        r_fixed)
    shares_outstanding_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'sharesOutstanding')
    shares = int(shares_outstanding_from_yahoo.get(str(current_year)))
    # print(shares)
    DCF_valuation_wacc_high   = Present_value_of_business_wacc_high / shares
    DCF_valuation_wacc_avg    = Present_value_of_business_wacc_avg / shares
    DCF_valuation_wacc_low    = Present_value_of_business_wacc_low / shares
    DCF_valuation_fixed_high  = Present_value_of_business_fixed_high / shares
    DCF_valuation_fixed_avg   = Present_value_of_business_fixed_avg / shares
    DCF_valuation_fixed_low   = Present_value_of_business_fixed_low / shares
    # print(DCF_valuation_wacc_high)
    # print(DCF_valuation_wacc_avg)
    # print(DCF_valuation_wacc_low)
    DCF_valuation = {}
    DCF_valuation.update({"Rate of Return (wacc)":r})
    DCF_valuation.update({"Rate of Return (fixed)":r_fixed})
    DCF_valuation.update({"Total Shares Outstanding":shares})
    DCF_valuation.update({str(current_year  )+" FCF":[FCF_high_projection_year_1,FCF_avg_projection_year_1,FCF_low_projection_year_1]})
    DCF_valuation.update({str(current_year+1)+" FCF":[FCF_high_projection_year_2,FCF_avg_projection_year_2,FCF_low_projection_year_2]})
    DCF_valuation.update({str(current_year+2)+" FCF":[FCF_high_projection_year_3,FCF_avg_projection_year_3,FCF_low_projection_year_3]})
    DCF_valuation.update({str(current_year+3)+" FCF":[FCF_high_projection_year_4,FCF_avg_projection_year_4,FCF_low_projection_year_4]})
    DCF_valuation.update({str(current_year+4)+" FCF":[FCF_high_projection_year_5,FCF_avg_projection_year_5,FCF_low_projection_year_5]})
    DCF_valuation.update({"Terminal Value":[Terminal_value_high, Terminal_value_avg, Terminal_value_low]})
    DCF_valuation.update({"Present Value of Business (wacc)":[Present_value_of_business_wacc_high, Present_value_of_business_wacc_avg, Present_value_of_business_wacc_low]})
    DCF_valuation.update({"Present Value of Business (fixed)":[Present_value_of_business_fixed_high, Present_value_of_business_fixed_avg, Present_value_of_business_fixed_low]})
    DCF_valuation.update({"DCF Valuation (wacc)":[DCF_valuation_wacc_high, DCF_valuation_wacc_avg, DCF_valuation_wacc_low]})
    DCF_valuation.update({"DCF Valuation (fixed)":[DCF_valuation_fixed_high, DCF_valuation_fixed_avg, DCF_valuation_fixed_low]})
    df_DCF_valuation = pd.DataFrame(data=DCF_valuation,index=['high','average','low'])
    df_DCF_valuation = df_DCF_valuation[[
        'DCF Valuation (wacc)',
        'DCF Valuation (fixed)',
        'Present Value of Business (wacc)',
        'Present Value of Business (fixed)',
        'Rate of Return (wacc)',
        'Rate of Return (fixed)',
        'Total Shares Outstanding',
        str(current_year  )+" FCF",
        str(current_year+1)+" FCF",
        str(current_year+2)+" FCF",
        str(current_year+3)+" FCF",
        str(current_year+4)+" FCF",
        "Terminal Value"]]
    print(df_DCF_valuation)
    return(df_DCF_valuation)

def DDM_Valuation_of_stock(stock_ticker):
    """
    This function will calculate Dividend Discount Model of the stock_ticker.
    Share Price = Current Dividend Per Share * ( 1 + g) / (r -g)
    r = rate of Equity
    g = (1 - dividend payout ratio) * ROE
    ROE = Net Income / Total Shareholder's Equity
    dividend payout ratio = Dividend Paid / Net Income  
    """
    from datetime import date
    import pandas as pd
    today                               = date.today()
    current_year                        = today.year
    r                                   = rate_of_equity_of_stock_CAPM(stock_ticker)
    dividend_paid_year_from_yahoo       = pull_attribute_from_yahoo(stock_ticker, 'dividendsPaid')
    dividend                            = abs(float(dividend_paid_year_from_yahoo.get(str(current_year -1))))
    shareholder_equity_year_from_yahoo  = pull_attribute_from_yahoo(stock_ticker, 'totalStockholderEquity')
    shareholder_equity                  = float(shareholder_equity_year_from_yahoo.get(str(current_year -1)))
    netIncome_paid_year_from_yahoo      = pull_attribute_from_yahoo(stock_ticker, 'netIncome')
    net_income                          = float(netIncome_paid_year_from_yahoo.get(str(current_year -1)))
    shares_outstanding_from_yahoo       = pull_attribute_from_yahoo(stock_ticker, 'sharesOutstanding')
    shares                              = int(shares_outstanding_from_yahoo.get(str(current_year)))
    dividend_payout_ratio               = dividend / net_income
    roe                                 = net_income / shareholder_equity
    g                                   = (1 - dividend_payout_ratio) * roe
    dividend_per_share                  = dividend / shares
    g_l = LONG_TERM_GROWTH_RATE
    h = YEARS_TILL_STABLE_GROWTH
    Intrisic_value_of_share_DDM         = dividend_per_share * ( 1 + g) / (r - g)
    Intrisic_value_of_share_DDM_H_model = (dividend_per_share * ( 1 + g_l) / (r - g_l)) + (dividend_per_share * (h/2) * (1 + g)/(r - g_l))
    ddm_valuation = {}
    ddm_valuation.update({"Current Dividend"      :dividend})
    ddm_valuation.update({"Rate of Return"        :r})
    ddm_valuation.update({"Growth Rate"           :g})
    ddm_valuation.update({"Shareholders' Equity"  :shareholder_equity})
    ddm_valuation.update({"Net Income"            :net_income})
    ddm_valuation.update({"Shares"                :shares})
    ddm_valuation.update({"Dividend Payout Ratio" :dividend_payout_ratio})
    ddm_valuation.update({"Return On Equity"      :roe})
    ddm_valuation.update({"Dividend Per Share"    :dividend_per_share})
    ddm_valuation.update({"DDM Valuation"         :Intrisic_value_of_share_DDM})
    ddm_valuation.update({"DDM Valuation H model" :Intrisic_value_of_share_DDM_H_model})
    df_ddm_valuation = pd.DataFrame(data=ddm_valuation, index=[current_year])
    df_ddm_valuation = df_ddm_valuation[[
        "DDM Valuation"         ,
        "DDM Valuation H model" ,
        "Rate of Return"        ,
        "Growth Rate"           ,
        "Dividend Payout Ratio" ,
        "Dividend Per Share"    ,
        "Current Dividend"      ,
        "Shareholders' Equity"  ,
        "Net Income"            ,
        "Shares"                ,
        "Return On Equity"      
    ]]
    print(df_ddm_valuation)
    return(df_ddm_valuation)

# print(DDM_Valuation_of_stock('AAPL'))

def Stock_details(stock_ticker):
    """
    This function give general info about the stock.
    """
    from datetime import date
    import pandas as pd
    today                               = date.today()
    current_year                        = today.year
    beta_year_from_yahoo                = pull_attribute_from_yahoo(stock_ticker, 'beta')
    beta                                = float(beta_year_from_yahoo.get(str(current_year)))
    marketcap_year_from_yahoo           = pull_attribute_from_yahoo(stock_ticker, 'marketCap')
    market_cap                          = int(marketcap_year_from_yahoo.get(str(current_year)))
    symbol_year_from_yahoo              = pull_attribute_from_yahoo(stock_ticker, 'symbol')
    symbol                              = str(symbol_year_from_yahoo.get(str(current_year)))
    longName_year_from_yahoo            = pull_attribute_from_yahoo(stock_ticker, 'longName')
    StockName                           = str(longName_year_from_yahoo.get(str(current_year)))
    sector_year_from_yahoo              = pull_attribute_from_yahoo(stock_ticker, 'sector')
    sector                              = str(sector_year_from_yahoo.get(str(current_year)))
    industry_year_from_yahoo            = pull_attribute_from_yahoo(stock_ticker, 'industry')
    industry                            = str(industry_year_from_yahoo.get(str(current_year)))
    regularMarketPrice_year_from_yahoo  = pull_attribute_from_yahoo(stock_ticker, 'regularMarketPrice')
    currentMarketPrice                  = float(regularMarketPrice_year_from_yahoo.get(str(current_year)))
    shares_outstanding_from_yahoo       = pull_attribute_from_yahoo(stock_ticker, 'sharesOutstanding')
    shares                              = int(shares_outstanding_from_yahoo.get(str(current_year)))
    stock_details = {}
    stock_details.update({"Total Shares Outstanding":shares})
    stock_details.update({"Total Market Cap":market_cap})
    stock_details.update({"beta":beta})
    stock_details.update({"Current Share Price":currentMarketPrice})
    stock_details.update({"Ticker Symbol":symbol})
    stock_details.update({"Stock Name":StockName})
    stock_details.update({"Sector":sector})
    stock_details.update({"Industry":industry})
    df_stock_details = pd.DataFrame(data=stock_details,index=[current_year])
    df_stock_details = df_stock_details[[
        'Stock Name',
        'Ticker Symbol',
        'Current Share Price',
        'Total Shares Outstanding',
        'Total Market Cap',
        'Sector',
        'Industry',
        'beta'
    ]]
    print(df_stock_details)
    return(df_stock_details)

#print(Stock_details('AAPL'))

def Valuation_of_stock(stock_ticker):
    """
    This is the main function for the valuation. 
    The valuations will include:
    1. DCF Discounted Cash Flow
    1.a. perpetual growth model
    1.b. rate of return with wacc
    1.c. fixed rate of return
    2. DDM Dividend Discount model
    2.b grodon growth model
    After calculating the valuation, will write to an xlsx
    """
    import pandas as pd
    from openpyxl import load_workbook
    from datetime import date
    today                             = date.today()
    current_year                      = today.year
    excel_path                        = '/home/aritra/analyzeninvest-projects/stock-research/save_valuation.xlsx'
    writer                            = pd.ExcelWriter(excel_path, engine = 'openpyxl')
    writer.book                       = load_workbook(excel_path)
    writer.sheets                     = dict((ws.title, ws) for ws in writer.book.worksheets)
    df_actual_financials_of_stock     = Create_Financial_Statements_DataFrame_for_DCF(stock_ticker)
    df_financial_projection_of_stock  = Create_Financial_Estimation_DataFrame_for_DCF(stock_ticker,
                                                                                      df_actual_financials_of_stock)
    df_DCF_valuation                  = DCF_valuation_of_stock(stock_ticker,
                                                               df_actual_financials_of_stock,
                                                               df_financial_projection_of_stock)
    df_DDM_valuation                  = DDM_Valuation_of_stock(stock_ticker)
    df_stock_details                  = Stock_details(stock_ticker)
    df_stock_details.to_excel(writer                 , sheet_name=stock_ticker,float_format="%.2f",index=False)
    df_DCF_valuation.to_excel(writer                 , sheet_name=stock_ticker,float_format="%.2f",index=True, startrow=5)
    df_DDM_valuation.to_excel(writer                 , sheet_name=stock_ticker,float_format="%.2f",index=True, startrow=12)
    df_actual_financials_of_stock.to_excel(writer    , sheet_name=stock_ticker,float_format="%.2f",index=True, startrow=18)
    df_financial_projection_of_stock.to_excel(writer , sheet_name=stock_ticker,float_format="%.2f",index=False, startrow=25)
    writer.save()
    writer.close()


#Valuation_of_stock('ITC.NS')
#Valuation_of_stock('COCHINSHIP.NS')
#Valuation_of_stock('CONTROLPR.NS')
#Valuation_of_stock('ENGINERSIN.NS')
#Valuation_of_stock('PAPERPROD.NS')
#Valuation_of_stock('KSCL.NS')
#Valuation_of_stock('IOC.NS')
#Valuation_of_stock('GAIL.NS')
#Valuation_of_stock('COALINDIA.NS')
#Valuation_of_stock('BAJAJCON.NS')
#Valuation_of_stock('SJVN.NS')
#Valuation_of_stock('POWERGRID.NS')
#Valuation_of_stock('NTPC.NS')
#Valuation_of_stock('MOIL.NS')
#Valuation_of_stock('INFRATEL.NS')
#Valuation_of_stock('SUNTV.NS')
#Valuation_of_stock('NMDC.NS')
#Valuation_of_stock('NESCO.NS')
#Valuation_of_stock('MCX.NS')
# Valuation_of_stock('ZEEL.NS')
# Valuation_of_stock('ABB.NS')
# Valuation_of_stock('GOOG')
# Valuation_of_stock('FB')
# Valuation_of_stock('AMZN')
# Valuation_of_stock('NFLX')


