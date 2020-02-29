#!/usr/bin/env python

def DCF_valuation_of_stock():
    from scrape-yahoo-finance import pull_attribute_from_yahoo
    from write-to-googlesheet import write_to_google_sheet
    import pandas as pd
    import numpy as np
    """ 
    This function calculates the DCF valuation of a stock based on the
    yahoo finance. 
    """

    

