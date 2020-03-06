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

# print(pull_attribute_from_yahoo('AAPL', 'marketCap'))

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

# print_yahoo_financials_for_DCF('MOIL.NS')

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
    today = date.today()
    current_year = today.year
    financials_of_stock = {}
    financials_of_stock.update({'year':[
        str(current_year -4),
        str(current_year -3),
        str(current_year -2),
        str(current_year -1)]})
    longTermDebt_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'longTermDebt')
    longTermDebt_year_1 = abs(int(longTermDebt_year_from_yahoo.get(str(current_year -4))))
    longTermDebt_year_2 = abs(int(longTermDebt_year_from_yahoo.get(str(current_year -3))))
    longTermDebt_year_3 = abs(int(longTermDebt_year_from_yahoo.get(str(current_year -2))))
    longTermDebt_year_4 = abs(int(longTermDebt_year_from_yahoo.get(str(current_year -1))))
    totalCurrentLiabilities_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'totalCurrentLiabilities')
    totalCurrentLiabilities_year_1 = abs(int(totalCurrentLiabilities_year_from_yahoo.get(str(current_year -4))))
    totalCurrentLiabilities_year_2 = abs(int(totalCurrentLiabilities_year_from_yahoo.get(str(current_year -3))))
    totalCurrentLiabilities_year_3 = abs(int(totalCurrentLiabilities_year_from_yahoo.get(str(current_year -2))))
    totalCurrentLiabilities_year_4 = abs(int(totalCurrentLiabilities_year_from_yahoo.get(str(current_year -1))))
    totalCurrentAssets_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'totalCurrentAssets')
    totalCurrentAssets_year_1 = abs(int(totalCurrentAssets_year_from_yahoo.get(str(current_year -4))))
    totalCurrentAssets_year_2 = abs(int(totalCurrentAssets_year_from_yahoo.get(str(current_year -3))))
    totalCurrentAssets_year_3 = abs(int(totalCurrentAssets_year_from_yahoo.get(str(current_year -2))))
    totalCurrentAssets_year_4 = abs(int(totalCurrentAssets_year_from_yahoo.get(str(current_year -1))))
    incomeTaxExpense_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'incomeTaxExpense')
    incomeTaxExpense_year_1 = abs(int(incomeTaxExpense_year_from_yahoo.get(str(current_year -4))))
    incomeTaxExpense_year_2 = abs(int(incomeTaxExpense_year_from_yahoo.get(str(current_year -3))))
    incomeTaxExpense_year_3 = abs(int(incomeTaxExpense_year_from_yahoo.get(str(current_year -2))))
    incomeTaxExpense_year_4 = abs(int(incomeTaxExpense_year_from_yahoo.get(str(current_year -1))))
    totalRevenue_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'totalRevenue')
    Revenue_year_1 = abs(int(totalRevenue_year_from_yahoo.get(str(current_year -4))))
    Revenue_year_2 = abs(int(totalRevenue_year_from_yahoo.get(str(current_year -3))))
    Revenue_year_3 = abs(int(totalRevenue_year_from_yahoo.get(str(current_year -2))))
    Revenue_year_4 = abs(int(totalRevenue_year_from_yahoo.get(str(current_year -1))))
    netIncome_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'netIncome')
    netIncome_year_1 = abs(int(netIncome_year_from_yahoo.get(str(current_year -4))))
    netIncome_year_2 = abs(int(netIncome_year_from_yahoo.get(str(current_year -3))))
    netIncome_year_3 = abs(int(netIncome_year_from_yahoo.get(str(current_year -2))))
    netIncome_year_4 = abs(int(netIncome_year_from_yahoo.get(str(current_year -1))))
    incomeBeforeTax_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'incomeBeforeTax')
    incomeBeforeTax_year_1 = abs(int(incomeBeforeTax_year_from_yahoo.get(str(current_year -4))))
    incomeBeforeTax_year_2 = abs(int(incomeBeforeTax_year_from_yahoo.get(str(current_year -3))))
    incomeBeforeTax_year_3 = abs(int(incomeBeforeTax_year_from_yahoo.get(str(current_year -2))))
    incomeBeforeTax_year_4 = abs(int(incomeBeforeTax_year_from_yahoo.get(str(current_year -1))))
    depreciation_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'depreciation')
    D_n_A_year_1 = abs(int(depreciation_year_from_yahoo.get(str(current_year -4))))
    D_n_A_year_2 = abs(int(depreciation_year_from_yahoo.get(str(current_year -3))))
    D_n_A_year_3 = abs(int(depreciation_year_from_yahoo.get(str(current_year -2))))
    D_n_A_year_4 = abs(int(depreciation_year_from_yahoo.get(str(current_year -1))))
    interestExpense_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'interestExpense')
    interestExpense_year_1 = abs(int(interestExpense_year_from_yahoo.get(str(current_year -4))))
    interestExpense_year_2 = abs(int(interestExpense_year_from_yahoo.get(str(current_year -3))))
    interestExpense_year_3 = abs(int(interestExpense_year_from_yahoo.get(str(current_year -2))))
    interestExpense_year_4 = abs(int(interestExpense_year_from_yahoo.get(str(current_year -1))))
    capitalExpenditures_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'capitalExpenditures')
    capitalExpenditures_year_1 = abs(int(capitalExpenditures_year_from_yahoo.get(str(current_year -4))))
    capitalExpenditures_year_2 = abs(int(capitalExpenditures_year_from_yahoo.get(str(current_year -3))))
    capitalExpenditures_year_3 = abs(int(capitalExpenditures_year_from_yahoo.get(str(current_year -2))))
    capitalExpenditures_year_4 = abs(int(capitalExpenditures_year_from_yahoo.get(str(current_year -1))))
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
    df_financial = pd.DataFrame(data = financials_of_stock)
    df_financial['EBIT'] = df_financial['Net Income'] + df_financial['Income Tax Expenses'] + df_financial['Interest Expenses']
    df_financial['Net Working Capital'] = df_financial['Current Assets'] - df_financial['Current Liabilities']
    df_financial['Tax Rate'] = df_financial['Income Tax Expenses'] / df_financial['Income Before Tax']
    df_financial['Free Cash Flow'] = df_financial['EBIT'] * (1 - df_financial['Tax Rate']) + df_financial['Net Working Capital'] + df_financial['Depreciation and Amortization'] - df_financial['Capital Expenditures']
    df_financial['FCF/Net Income'] = df_financial['Free Cash Flow'] / df_financial['Net Income']
    df_financial['Net Income Margin'] = df_financial['Net Income'] / df_financial['Total Revenue']
    df_financial['Revenue Growth Rate'] = df_financial['Total Revenue'].pct_change()
    return(df_financial)

#print("\n")
#print(Create_Financial_Statements_DataFrame_for_DCF('AAPL'))


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
    if long_term_debt != 0:
        rate_of_debt = interest_expense / long_term_debt
    else:
        rate_of_debt = 0
    tax_rate = tax / income_before_tax
    weight_of_equity = 1 - weight_of_debt
    rate_of_equity = rate_of_equity_of_stock(stock_ticker)
    weighted_average_cost_of_capital = (weight_of_debt * rate_of_debt * (1 - tax_rate)) + (weight_of_equity * rate_of_equity)
    return(weighted_average_cost_of_capital)

# print(wacc_of_stock('AAPL'))

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


def Create_Financial_Estimation_DataFrame_for_DCF(stock_ticker):
    """
    This function will create the Estimation DataFrame for DCF Valuation. 
    """
    import pandas  as pd
    from datetime import date
    today = date.today()
    current_year = today.year
    financial_estimation_of_stock = {}
    revenue_estimation_year_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'revenueEstimate')
    revenue_estimation_year_1_avg   = abs(int(revenue_estimation_year_from_yahoo.get(str(current_year   )+'_avg' )))
    revenue_estimation_year_1_high  = abs(int(revenue_estimation_year_from_yahoo.get(str(current_year   )+'_high')))
    revenue_estimation_year_1_low   = abs(int(revenue_estimation_year_from_yahoo.get(str(current_year   )+'_low' )))
    revenue_estimation_year_2_avg   = abs(int(revenue_estimation_year_from_yahoo.get(str(current_year +1)+'_avg' )))
    revenue_estimation_year_2_high  = abs(int(revenue_estimation_year_from_yahoo.get(str(current_year +1)+'_high')))
    revenue_estimation_year_2_low   = abs(int(revenue_estimation_year_from_yahoo.get(str(current_year +1)+'_low' )))
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
    df_financial_estimate = pd.DataFrame(data = financial_estimation_of_stock)
    df_financial_estimate['Estimated Revenue Growth'] = df_financial_estimate['Revenue Estimate'].pct_change()
    projected_revenue_year_1 = [
        df_financial_estimate.loc[0,'Revenue Estimate'],
        df_financial_estimate.loc[2,'Revenue Estimate'],
        df_financial_estimate.loc[4,'Revenue Estimate']]
    projected_revenue_growth = [
        df_financial_estimate.loc[1,'Estimated Revenue Growth'],
        df_financial_estimate.loc[3,'Estimated Revenue Growth'],
        df_financial_estimate.loc[5,'Estimated Revenue Growth']]
    df_actual_finance_of_stock = Create_Financial_Statements_DataFrame_for_DCF(stock_ticker)
    actual_revenue_growth_average = df_actual_finance_of_stock['Revenue Growth Rate'].mean()
    last_year_revenue = df_actual_finance_of_stock.loc[3,'Total Revenue']
    projected_revenue_growth_year_1_avg = (projected_revenue_year_1[0] - last_year_revenue)/last_year_revenue
    projected_revenue_growth_year_1_high = (projected_revenue_year_1[1] - last_year_revenue)/last_year_revenue
    projected_revenue_growth_year_1_low = (projected_revenue_year_1[2] - last_year_revenue)/last_year_revenue
    # print(projected_revenue_growth_year_1_avg)
    # print(projected_revenue_growth_year_1_high)
    # print(projected_revenue_growth_year_1_low)
    revenue_growth_avg = (projected_revenue_growth_year_1_avg + actual_revenue_growth_average + projected_revenue_growth[0])/3
    revenue_growth_high = (projected_revenue_growth_year_1_high + actual_revenue_growth_average + projected_revenue_growth[1])/3
    revenue_growth_low = (projected_revenue_growth_year_1_low + actual_revenue_growth_average + projected_revenue_growth[2])/3
    # print(revenue_growth_avg)
    # print(revenue_growth_high)
    # print(revenue_growth_low)
    last_year_net_income = df_actual_finance_of_stock.loc[3,'Net Income']
    last_year_free_cash_flow = df_actual_finance_of_stock.loc[3,'Free Cash Flow']
    min_net_income_margin = df_actual_finance_of_stock['Net Income Margin'].min()
    min_fcf_over_net_income = df_actual_finance_of_stock['FCF/Net Income'].min()
    # print(min_net_income_margin)
    # print(min_fcf_over_net_income)
    df_financial_estimate = df_financial_estimate.drop(columns=['Estimated Revenue Growth'])
    df_financial_estimate = df_financial_estimate.reindex([2, 0, 4, 3, 1, 5])
    financial_projection_of_stock = {}
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
    revenue_estimation_year_3_high = revenue_estimation_year_2_high * (1 + revenue_growth_high)
    revenue_estimation_year_3_avg = revenue_estimation_year_2_avg * (1 + revenue_growth_avg)
    revenue_estimation_year_3_low = revenue_estimation_year_2_low * (1 + revenue_growth_low)
    revenue_estimation_year_4_high = revenue_estimation_year_3_high * (1 + revenue_growth_high)
    revenue_estimation_year_4_avg = revenue_estimation_year_3_avg * (1 + revenue_growth_avg)
    revenue_estimation_year_4_low = revenue_estimation_year_3_low * (1 + revenue_growth_low)
    revenue_estimation_year_5_high = revenue_estimation_year_4_high * (1 + revenue_growth_high)
    revenue_estimation_year_5_avg = revenue_estimation_year_4_avg * (1 + revenue_growth_avg)
    revenue_estimation_year_5_low = revenue_estimation_year_4_low * (1 + revenue_growth_low)
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
    df_financial_projection = pd.DataFrame(data=financial_projection_of_stock)
    df_financial_estimate = df_financial_estimate.append(df_financial_projection)
    df_financial_estimate = df_financial_estimate[['Year','Revenue Estimate']]
    df_financial_estimate['Net Income Estimate'] = df_financial_estimate['Revenue Estimate'] * min_net_income_margin
    df_financial_estimate['Free Cash Flow Estimate'] = df_financial_estimate['Net Income Estimate'] * min_fcf_over_net_income
    df_financial_estimate = df_financial_estimate.reset_index(drop = True)
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
    r = wacc_of_stock(stock_ticker)
    g = 0.025
    if r > g:
        terminal_value = last_FCF * (1 + g) / (r - g)
    else:
        terminal_value = last_FCF * (1 + g) / g
    return(terminal_value)


def DCF_valuation_of_a_stock(stock_ticker):
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
    today = date.today()
    current_year = today.year
    df_financial_projection_of_stock = Create_Financial_Estimation_DataFrame_for_DCF(stock_ticker)
    #print(df_financial_projection_of_stock)
    FCF_high_projection_year_1 = df_financial_projection_of_stock.loc[0,'Free Cash Flow Estimate'] 
    FCF_high_projection_year_2 = df_financial_projection_of_stock.loc[3,'Free Cash Flow Estimate'] 
    FCF_high_projection_year_3 = df_financial_projection_of_stock.loc[6,'Free Cash Flow Estimate'] 
    FCF_high_projection_year_4 = df_financial_projection_of_stock.loc[9,'Free Cash Flow Estimate'] 
    FCF_high_projection_year_5 = df_financial_projection_of_stock.loc[12,'Free Cash Flow Estimate']
    FCF_avg_projection_year_1 = df_financial_projection_of_stock.loc[1,'Free Cash Flow Estimate'] 
    FCF_avg_projection_year_2 = df_financial_projection_of_stock.loc[4,'Free Cash Flow Estimate'] 
    FCF_avg_projection_year_3 = df_financial_projection_of_stock.loc[7,'Free Cash Flow Estimate'] 
    FCF_avg_projection_year_4 = df_financial_projection_of_stock.loc[10,'Free Cash Flow Estimate'] 
    FCF_avg_projection_year_5 = df_financial_projection_of_stock.loc[13,'Free Cash Flow Estimate']
    FCF_low_projection_year_1 = df_financial_projection_of_stock.loc[2,'Free Cash Flow Estimate'] 
    FCF_low_projection_year_2 = df_financial_projection_of_stock.loc[5,'Free Cash Flow Estimate'] 
    FCF_low_projection_year_3 = df_financial_projection_of_stock.loc[8,'Free Cash Flow Estimate'] 
    FCF_low_projection_year_4 = df_financial_projection_of_stock.loc[11,'Free Cash Flow Estimate'] 
    FCF_low_projection_year_5 = df_financial_projection_of_stock.loc[14,'Free Cash Flow Estimate']
    last_FCF_estimate_high = df_financial_projection_of_stock.loc[12,'Free Cash Flow Estimate']
    last_FCF_estimate_avg = df_financial_projection_of_stock.loc[13,'Free Cash Flow Estimate']
    last_FCF_estimate_low = df_financial_projection_of_stock.loc[14,'Free Cash Flow Estimate']
    Terminal_value_high = terminal_value_of_stock_perpetual_growth_model(stock_ticker, last_FCF_estimate_high)
    Terminal_value_avg = terminal_value_of_stock_perpetual_growth_model(stock_ticker, last_FCF_estimate_avg)
    Terminal_value_low = terminal_value_of_stock_perpetual_growth_model(stock_ticker, last_FCF_estimate_low)
    # print(Terminal_value_high)
    # print(Terminal_value_avg)
    # print(Terminal_value_low)
    r = wacc_of_stock(stock_ticker)
    # print(r)
    Present_value_of_business_high = (FCF_high_projection_year_1 / (pow((1+r),1))) + (FCF_high_projection_year_2 / (pow((1+r),2))) + (FCF_high_projection_year_3 / (pow((1+r),3))) + (FCF_high_projection_year_4 / (pow((1+r),4))) + (FCF_high_projection_year_5 / (pow((1+r),5))) + (Terminal_value_high/ (pow((1+r),5)))
    Present_value_of_business_avg = (FCF_avg_projection_year_1 / (pow((1+r),1))) + (FCF_avg_projection_year_2 / (pow((1+r),2))) + (FCF_avg_projection_year_3 / (pow((1+r),3))) + (FCF_avg_projection_year_4 / (pow((1+r),4))) + (FCF_avg_projection_year_5 / (pow((1+r),5))) + (Terminal_value_avg/ (pow((1+r),5)))
    Present_value_of_business_low = (FCF_low_projection_year_1 / (pow((1+r),1))) + (FCF_low_projection_year_2 / (pow((1+r),2))) + (FCF_low_projection_year_3 / (pow((1+r),3))) + (FCF_low_projection_year_4 / (pow((1+r),4))) + (FCF_low_projection_year_5 / (pow((1+r),5))) + (Terminal_value_low/ (pow((1+r),5)))
    shares_outstanding_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'sharesOutstanding')
    shares = int(shares_outstanding_from_yahoo.get(str(current_year)))
    # print(shares)
    DCF_valuation_high = Present_value_of_business_high / shares
    DCF_valuation_avg = Present_value_of_business_avg / shares
    DCF_valuation_low = Present_value_of_business_low / shares
    # print(DCF_valuation_high)
    # print(DCF_valuation_avg)
    # print(DCF_valuation_low)
    DCF_valuation = [DCF_valuation_high, DCF_valuation_avg, DCF_valuation_low]
    return(DCF_valuation)

# testing
# print("\n")
# print(DCF_valuation_of_a_stock('AAPL'))
# print(DCF_valuation_of_a_stock('FB'))
# print(DCF_valuation_of_a_stock('NFLX'))
# print(DCF_valuation_of_a_stock('GOOG'))
# print(DCF_valuation_of_a_stock('AMZN'))
