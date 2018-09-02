# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 00:31:39 2018

@author: amrul
"""

from myfunctions import *

def load_mt4_fx_file(folder,file):
    fx_df=pd.read_csv(folder+file,header=-1,index_col=0,parse_dates=True)
    fx_df.drop(1,axis=1,inplace=True)
    cols=['open','high','low','close','volume']
    fx_df.columns=cols
    fx_df=add_ret_cols(fx_df,'close')
    return fx_df

folder=r'C:\Users\amrul\Downloads\mt4_downloads'
folder+='\\'
eurjpy_file=r'eurjpy_daily_20110802_to_20180831.csv'
usdjpy_file=r'usdjpy_20110704_to_20180831.csv'

eurjpy_df=load_mt4_fx_file(folder,eurjpy_file)
usdjpy_df=load_mt4_fx_file(folder,usdjpy_file)

#plt.subplot(2,2,1)
eurjpy_df.loc['2018-5':'2018-8','dly_ret_bps'].plot(label='eurjpy')
usdjpy_df.loc['2018-5':'2018-8','dly_ret_bps'].plot(label='usdjpy')
plt.xlabel('date')
plt.ylabel('daily return in bps')
plt.title('Daily return in bps')
plt.legend()
plt.show()

#plt.subplot(2,2,2)
#eurjpy_df.loc['2018-8','close'].plot(label='eurjpy')
#usdjpy_df.loc['2018-8','close'].plot(label='usdjpy')
#plt.xlabel('date')
#plt.ylabel('Close prices')
#plt.title('Close prices')
#plt.legend()
#plt.tight_layout()
#plt.show()
#
#plt.subplot(2,2,3)
#eurjpy_df.loc['2018-8','comp_ret'].plot(label='eurjpy')
#usdjpy_df.loc['2018-8','comp_ret'].plot(label='usdjpy')
#plt.xlabel('date')
#plt.ylabel('Compounded return')
#plt.title('Compounded return in decimals start with 1 unit of currency')
#plt.legend()
#plt.tight_layout()
#plt.show()
#
