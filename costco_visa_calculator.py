    # -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 21:15:58 2018

@author: amrul
"""
import pandas as pd

folder=r'C:\Users\amrul\Documents\japan_sweets_business\costco_visa_spendings'
folder+='\\'
file='costco_visa_201901.xlsx'
df=pd.read_excel(folder+file)
df['amount']=df['ご利用金額'].str.replace('円','')
df['amount']=df['amount'].str.replace(',','')
df['amount']=pd.to_numeric(df['amount'])
print("Total:",df['amount'].sum())
#['ご利用日', 'ご利用先など', 'ご利', '支払', '支払.1', '支払開始', 'ご利用金額', '手数料・利息']
#Index(['利用日', 'ご利用先など', 'ご利', '今回', 'ご利用金額', '手数料・利息', 'その他', '当月', 'amount'], dtype='object')
print("Total(family spent):{}".format(df.loc[df['ご利']=='家族','amount'].sum()))
