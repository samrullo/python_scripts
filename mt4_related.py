# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 19:33:31 2018

@author: amrul
"""

from myfunctions import *

def load_mt4_series(folder,file,ma1=11,ma2=31):
    header=['date','time','open','high','low','close','volume']
    df=pd.read_csv(folder+'\\'+file,header=-1,names=header)
    df['inx_time']=pd.to_datetime(df.date+' '+df.time)
    df.index=df['inx_time']
    df['ma_1']=df.close.rolling(window=ma1).mean()
    df['ma_2']=df.close.rolling(window=ma2).mean()
    return df[['open','high','low','close','volume','ma_1','ma_2']]

folder=r'C:\Users\amrul\Downloads\mt4_downloads'
file='EURUSD-cd15_20180627_to_20180727.csv'
eurusd_m15_df=load_mt4_series(folder,file)