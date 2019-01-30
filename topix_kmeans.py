# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 19:04:58 2018

@author: amrul
"""
from datetime import date
import pandas as pd
from pandas_datareader import data

tpx_weights_file=r'C:\Users\amrul\Documents\finance_related\TOPIX_weight_jp.xlsx'
tpx_df=pd.read_excel(tpx_weights_file)

#Index(['日付', '銘柄名', 'コード', '業種', 'TOPIXに占める個別銘柄のウェイト', 'ニューインデックス区分','調整係数対象銘柄'],dtype='object')
cols=['date', 'sec_desc','ticker','industry','weight','new_index_sector','adjustment_target']
tpx_df.columns=cols

start=date(2016,12,31)
end=date(2017,12,31)

inx=270
ticker=str(tpx_df.loc[inx,'ticker'])+'.T'
print("processing ",tpx_df.loc[inx,'ticker'],tpx_df.loc[inx, 'sec_desc'])
stock_df=data.DataReader(ticker,'yahoo',start.isoformat(),end.isoformat())
stock_df['dly_ret']=stock_df['Adj Close'].pct_change()
tpx_df.loc[1,'dly_mean']=stock_df.dly_ret.mean()
tpx_df.loc[1,'dly_std']=stock_df.dly_ret.std()
#print("Total number of stocks:",len(tpx_df))
#for i,row in tpx_df.iterrows():
#    ticker=str(row['ticker'])+'.T'
#    print(i+1,":processing ",row['ticker'],row['sec_desc'])
#    stock_df=data.DataReader(ticker,'yahoo',start.isoformat(),end.isoformat())
#    stock_df['dly_ret']=stock_df['Adj Close'].pct_change()
#    tpx_df.loc[i,'dly_mean']=stock_df.dly_ret.mean()
#    tpx_df.loc[i,'dly_std']=stock_df.dly_ret.std()