"""
This module sends HTTP requests to retrieve closing stock price (json file) of an S&P 500
company from Alpha Vantage API.
"""


import urllib.request, urllib.parse, urllib.error
import config
import json
import pandas as pd
import numpy as np


def get_data():
    """
    Function to generate stock prices and company symbol

    """

    # Enter Company Symbol
    
    SYMBOL = 'AAPL' 

    # Enter Alpha Vantage API URL

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + SYMBOL + '&outputsize=full&apikey='+ config.public_api_key

    # Extract JSON data 

    alpha_vantage_data = urllib.request.urlopen(url).read().decode()
    js = json.loads(alpha_vantage_data)
    

    close_price = list()
    dates = list()

    # Extract Close Prices 
    for item in js["Time Series (Daily)"]:
        dates.append(item)
        close_price.append(float(js['Time Series (Daily)'][item]['4. close']))

    # DataFrame of Close Prices

    stock_df = pd.DataFrame(data=close_price, index=dates)
    stock_df.index = pd.to_datetime(stock_df.index)
    stock_df = stock_df.sort_index(ascending=True)
    stock_df.columns = [SYMBOL]

    return stock_df, SYMBOL
