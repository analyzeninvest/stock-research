#!/usr/bin/env python

EXCEL_PATH            = '/home/aritra/analyzeninvest-projects/stock-research/save_valuation.xlsx'
COMPANY_LISTED_INDIA  = '/home/aritra/analyzeninvest-projects/stock-research/Equity-India-filtered.csv'
COMPANY_LISTED_US     = '/home/aritra/analyzeninvest-projects/stock-research/Equity-US-filtered.csv'
IMAGE_PATH            = '/home/aritra/analyzeninvest-projects/stock-research/images/'

def stock_research(stock_ticker, us_or_india, excel_path = EXCEL_PATH):
    import pandas as pd
    import scrape_moneycontrol_data as moneycontrol
    import scrape_yahoo_finance as yahoo
    """ 
    This function calculates the valuation of a stock based on the
    yahoo finance. Then it also prints the max past 20 years of the
    stock performance.  
    """
    if us_or_india:
        stock_end = ".NS"
    else:
        stock_end = ""
    stock_name = stock_ticker + stock_end
    print("Staring the Valuation for " + stock_name)
    yahoo.Valuation_of_stock(stock_name)
    moneycontrol.Historical_Performance_of_stock(stock_ticker)

#stock_research('SBIN', True)    
#stock_research('CDNS', False)    
    
def get_factor_of_the_stock(stock_ticker, factor):
    """
    This function will get the factor of the stock. The factor may be
    calculated or directly obtained from yahoo finanace.
    Supported Factors:
    1. ROE = Net Income / Total Shareholder's Equity
    2. Revenue
    """
    from scrape_yahoo_finance import pull_attribute_from_yahoo 
    from datetime import date
    today = date.today()
    current_year = today.year
    if factor == 'ROE':
        netIncome_paid_year_from_yahoo      = pull_attribute_from_yahoo(stock_ticker, 'netIncome')
        net_income                          = float(netIncome_paid_year_from_yahoo.get(str(current_year -1)))
        shareholder_equity_year_from_yahoo  = pull_attribute_from_yahoo(stock_ticker, 'totalStockholderEquity')
        shareholder_equity                  = float(shareholder_equity_year_from_yahoo.get(str(current_year -1)))
        if shareholder_equity == 0:
            roe = 0
        else:
            roe                                 = net_income / shareholder_equity
        print(roe)
        return(roe)
    elif factor == "Revenue":
        total_revenue_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'totalRevenue')
        revenue = int(total_revenue_from_yahoo.get(str(current_year -1)))
        print(revenue)
        return(revenue)
    elif factor == "PE":
        trailingPE_from_yahoo = pull_attribute_from_yahoo(stock_ticker, 'trailingPE')
        trailingPE = float(trailingPE_from_yahoo.get(str(current_year)))
        print(trailingPE)
        return(trailingPE)

#get_factor_of_the_stock("ITC.NS", "ROE")
#get_factor_of_the_stock("ITC.NS", "Revenue")


def plot_sector_by_3_factors(sector, factor_x, factor_y, factor_z, us_or_india):
    """
    This is a function that will plot the equity of the sector by
    factor_x and factor_y.  
    This is a good way of evaluating all the
    equities from a given sector & find the stocks which are
    overvalued or undervalued.
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    if us_or_india:
        stock_end                = ".NS"
        stock_name_industry_csv  = COMPANY_LISTED_INDIA
        region_name = "India"
    else:
        stock_end                = ""
        stock_name_industry_csv  = COMPANY_LISTED_US
        region_name = "US"
    df_company_list    = pd.read_csv(stock_name_industry_csv)
    df_stock_industry  = df_company_list[df_company_list.Industry.isin([sector])].reset_index(drop=True)
    factor_x_array = []
    factor_y_array = []    
    factor_z_array = []    
    for stock in df_stock_industry.Symbol:
        stock_name = stock + stock_end
        print(stock_name)
        factor_x_array.append(get_factor_of_the_stock(stock_name, factor_x))
        factor_y_array.append(get_factor_of_the_stock(stock_name, factor_y))
        factor_z_array.append(get_factor_of_the_stock(stock_name, factor_z))
    df_stock_industry[factor_x] = factor_x_array
    df_stock_industry[factor_y] = factor_y_array
    df_stock_industry[factor_z] = factor_z_array
    print(df_stock_industry)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #df_stock_industry.plot(kind='scatter',x=factor_x,y=factor_y,color='red')
    ax.scatter(df_stock_industry[factor_x],df_stock_industry[factor_y],df_stock_industry[factor_z])
    ax.set_title(sector)
    for i,text in enumerate(df_stock_industry.Symbol):
        label = '(%d, %d, %d), %s' % (df_stock_industry[factor_x][i], df_stock_industry[factor_y][i], df_stock_industry[factor_z][i], text)
        ax.text(df_stock_industry[factor_x][i], df_stock_industry[factor_y][i], df_stock_industry[factor_z][i], label)
    # plt.xlabel(factor_x)
    # plt.ylabel(factor_y)
    # plt.ylabel(factor_z)
    ax.set_xlabel(factor_x)
    ax.set_ylabel(factor_y)
    ax.set_zlabel(factor_z)
    sector_name = sector.replace("/", "_")
    plt.savefig(IMAGE_PATH + sector_name + '_' + factor_x + '_' + factor_y + '_' + factor_z + '_' + region_name + '.png', dpi=1000)
    plt.show()

def plot_sector_by_2_factors(sector, factor_x, factor_y, us_or_india):
    """
    This is a function that will plot the equity of the sector by
    factor_x and factor_y.  
    This is a good way of evaluating all the
    equities from a given sector & find the stocks which are
    overvalued or undervalued.
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    if us_or_india:
        stock_end                = ".NS"
        stock_name_industry_csv  = COMPANY_LISTED_INDIA
        region_name = "India"
    else:
        stock_end                = ""
        stock_name_industry_csv  = COMPANY_LISTED_US
        region_name = "US"
    df_company_list    = pd.read_csv(stock_name_industry_csv)
    df_stock_industry  = df_company_list[df_company_list.Industry.isin([sector])].reset_index(drop=True)
    factor_x_array = []
    factor_y_array = []    
    factor_z_array = []    
    for stock in df_stock_industry.Symbol:
        stock_name = stock + stock_end
        print(stock_name)
        factor_x_array.append(get_factor_of_the_stock(stock_name, factor_x))
        factor_y_array.append(get_factor_of_the_stock(stock_name, factor_y))
    df_stock_industry[factor_x] = factor_x_array
    df_stock_industry[factor_y] = factor_y_array
    print(df_stock_industry)
    df_stock_industry.plot(kind='scatter',x=factor_x,y=factor_y,color='red')
    for i,text in enumerate(df_stock_industry.Symbol):
        plt.annotate(text, (df_stock_industry[factor_x][i], df_stock_industry[factor_y][i]))
    plt.xlabel(factor_x)
    plt.ylabel(factor_y)
    sector_name = sector.replace("/", "_")
    plt.savefig(IMAGE_PATH + sector_name + '_' + factor_x + '_' + factor_y + '_' + region_name + '.png', dpi=1000)
    plt.show()


    
#plot_sector_by_2_factors('Cement & Cement Products', 'ROE', 'Revenue', True)
#plot_sector_by_2_factors('Cement & Cement Products', 'PE', 'Revenue', True)
#plot_sector_by_3_factors('Cement & Cement Products', 'ROE', 'PE', 'Revenue', True)
#plot_sector_by_3_factors('2/3 Wheelers', 'ROE', 'PE', 'Revenue', True)
