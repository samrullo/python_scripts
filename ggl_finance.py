# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 16:38:10 2018

@author: amrul
"""

"""

Retrieve intraday stock data from Google Finance.

"""
import csv
import datetime
import re
import pandas as pd
import requests
import codecs
from myfunctions import *

from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARMA


def get_google_finance_intraday(ticker, period=60, days=1):

    """
    Retrieve intraday stock data from Google Finance.
    Parameters
    ----------
    ticker : str
        Company ticker symbol.
    period : int
        Interval between stock values in seconds.
    days : int
        Number of days of data to retrieve.
    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the opening price, high price, low price,
        closing price, and volume. The index contains the times associated with
        the retrieved price values.
    """
    uri = 'http://www.google.com/finance/getprices?i={period}&p={days}d&f=d,o,h,l,c,v&df=cpct&q={ticker}'.format(ticker=ticker,period=period,days=days)

    page = requests.get(uri)

    #reader = csv.reader(page.content.splitlines())
    reader = csv.reader(codecs.iterdecode(page.content.splitlines(), "utf-8"))

    columns = ['open', 'high', 'low', 'close', 'volume']
    

    rows = []

    times = []

    for row in reader:
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start+datetime.timedelta(seconds=period*int(row[0])))
            rows.append(map(float, row[1:]))
    if len(rows):
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'),columns=columns)
    else:
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))
    
ntt_df=get_google_finance_intraday('9437.T',period=60*5,days=1)
sft_df=get_google_finance_intraday('9984.T',period=60*5,days=1)

ntt_df=add_ret_cols(ntt_df,'close')
sft_df=add_ret_cols(sft_df,'close')

ntt_returns=ntt_df.dly_ret_bps
ntt_returns=ntt_returns.dropna()

sft_returns=sft_df.dly_ret_bps
sft_returns=sft_returns.dropna()


plot_acf(ntt_returns,lags=10)
mod=ARMA(ntt_returns,order=(0,1))
res_ntt=mod.fit()
print(res_ntt.params)

plot_acf(sft_returns,lags=10)
mod=ARMA(sft_returns,order=(0,1))
res_sft=mod.fit()
print(res_sft.params)