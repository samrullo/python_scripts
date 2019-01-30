# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 18:47:51 2018

@author: amrul
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date

from lxml.html import parse
from urllib.request import urlopen

from myfunctions import *

def _unpack(row,kind='td'):
    cells=row.findall('.//%s'%kind)
    vals=[val.text for val in cells]
    return vals


def getTopixSeries(url,prices):
    parsed=parse(urlopen(url))
    doc=parsed.getroot()
    
    tables=doc.findall('.//table')
    topix=tables[1]
    
    rows=topix.findall('.//tr')
    for row in rows:
        if row.getchildren()[0].tag!='th':
            arr=_unpack(row,kind='td')
            if len(arr)!=0:
                arr[0]=arr[0].replace('年','-')
                arr[0]=arr[0].replace('月','-')
                arr[0]=arr[0].replace('日','')
                prices.append(arr)
    pass


def get_px_series(px_rows):
    px_df=pd.DataFrame(columns=['close','high','low','open'])
    for row in px_rows:
        if row.getchildren()[0].tag!='th':
            arr=_unpack(row,kind='td')
            if len(arr)!=0:
                arr[0]=arr[0].replace('年','-')
                arr[0]=arr[0].replace('月','-')
                arr[0]=arr[0].replace('日','')
            df=pd.DataFrame(index=[arr[0]],data=[arr[1:5]],columns=['open','high','low','close'])
            px_df=pd.concat([px_df,df])
    return px_df



#################getting header#################
url='https://info.finance.yahoo.co.jp/history/?code=998405.T&sy=1983&sm=2&sd=20&ey=2018&em=3&ed=22&tm=d&p=1'
parsed=parse(urlopen(url))
doc=parsed.getroot()
tables=doc.findall('.//table')
topix=tables[1]
rows=topix.findall('.//tr')
header=np.array(_unpack(rows[0],kind='th'))
header_eng=['date','open','high','low','close','volume','px_aft_adj']
#################getting header#################

def getYahooSeries(ticker,start=date(2017,12,31),end=datetime.today(),inv_amt=10000):
    #loading data from 300 urls pages
    px_df=pd.DataFrame(columns=['close','high','low','open'])
    url_template='https://info.finance.yahoo.co.jp/history/?code={ticker}&sy={start_year}&sm={start_month}&sd={start_day}&ey={end_year}&em={end_month}&ed={end_day}&tm=d&p={page_numb}'
    #url_template='https://info.finance.yahoo.co.jp/history/?code=USDJPY=X&sy=2005&sm=1&sd=1&ey=2018&em=7&ed=15&tm=d&p=1'
    hasPX=True
    page=1
    while(hasPX):
        url=url_template.format(ticker=ticker,start_year=start.year,start_month=start.month,start_day=start.day,end_year=end.year,end_month=end.month,end_day=end.day,page_numb=str(page))
        print(url)
        page+=1
        parsed=parse(urlopen(url))
        doc=parsed.getroot()    
        tables=doc.findall('.//table')
        if len(tables)>2:
            px_tbl=tables[1]    
            rows=px_tbl.findall('.//tr')
            if len(rows)!=0:
                df=get_px_series(rows)
                if len(df)!=0:
                    px_df=pd.concat([px_df,df])
                else:
                    hasPX=False
            else:
                hasPX=False
        else:
            hasPX=False
    if len(px_df)!=0:
        px_df.index=pd.to_datetime(px_df.index)
        for col in px_df.columns.values:
            px_df[col]=px_df[col].str.replace(',','')
            px_df[col]=pd.to_numeric(px_df[col])
        px_df.sort_index(inplace=True)
        px_df['dly_ret']=px_df['close'].pct_change()
        px_df['dly_ret_bps']=px_df['dly_ret']*10000
        px_df['comp_ret']=inv_amt*np.cumprod(1+px_df.dly_ret)        
    return px_df

def load_fx_from_file(folder='C:\\Users\\amrul\\Documents\\investment_analysis\\',file='open_ex_fx_2007-01-01_to_2017-06-18.xlsx'):
    df=pd.read_excel(folder+file,index_col='date',parse_dates=True)
    df.columns=df.columns.map(lambda x:x.lower())
    usdjpy_df=df[['jpy']]
    eurusd_df=1/df[['eur']]
    gbpusd_df=1/df[['gbp']]
    usdcad_df=df[['cad']]
    df_tpl=(usdjpy_df,eurusd_df,gbpusd_df,usdcad_df)
    for tmp_df in df_tpl:
        tmp_df.columns=['fxspot']
        tmp_df=add_ret_cols(tmp_df,'fxspot')
    
    return df,usdjpy_df,eurusd_df,gbpusd_df,usdcad_df

def load_tpx_from_file(folder='C:\\Users\\amrul\\Documents\\investment_analysis\\',file='topix_ts_19910104_to_20180427.xlsx'):
    df=pd.read_excel(folder+file,index_col='date',parse_dates=True)
    df.columns=df.columns.map(lambda x:x.lower())
    df=add_ret_cols(df,'close')
    return df

def join_two_df(df1,df2,suffixes=('_usdjpy','_tpx')):
    df_merged=df1.join(df2,how='inner',rsuffix=suffixes[0],lsuffix=suffixes[1])
    return df_merged

main_folder='C:\\Users\\amrul\\Documents\\investment_analysis\\'
start=date(2018,3,31)
end=date(2018,11,24)
#ticker='USDJPY%3DX'
#file=ticker+'_'+start.isoformat()+'_to_'+end.isoformat()+'.xlsx'
#cols=['date','close','high','low','open','daily_ret']
#prices_df[cols].to_excel(main_folder+file,index=False)
#monthly_ret_df=((1+prices_df['daily_ret']/10000).resample('M').prod()-1)*10000

#usdjpy_df=getYahooSeries('USDJPY%3DX',start=start,end=end)
#eurjpy_df=getYahooSeries('EURJPY%3DX',start=start,end=end)
softbank_df=getYahooSeries('9984.T',start=start,end=end)
#df.to_excel(main_folder+file)
#fx_all_df,usdjpy_df,eurusd_df,gbpusd_df,usdcad_df=load_fx_from_file()
#tpx_df=load_tpx_from_file()
#usdjpy_tpx_mrg_df=join_two_df(usdjpy_df,tpx_df,suffixes=('_usdjpy','_tpx'))


#----------------------------------------------------------------------------
#Check if usd/jpy fx rates are a random walk with adfuller
#----------------------------------------------------------------------------
#from statsmodels.tsa.stattools import adfuller
