# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 21:15:58 2018

@author: amrul
"""
import pandas as pd

folder=r'C:\Users\amrul\Documents\japan_sweets_business\costco_visa_spendings'
folder+='\\'
file='costco_visa_201812.xlsx'
df=pd.read_excel(folder+file)
df['amount']=df['ご利用金額'].str.replace('円','')
df['amount']=df['amount'].str.replace(',','')
df['amount']=pd.to_numeric(df['amount'])
print("Total:",df['amount'].sum())
#['ご利用日', 'ご利用先など', 'ご利', '支払', '支払.1', '支払開始', 'ご利用金額', '手数料・利息']

familyspendingfile=r'C:\Users\amrul\Documents\familyspending.xlsx'
family_df=pd.read_excel(familyspendingfile)

#['Month', 'Current Balance(Mitsubishi)', 'Current Balance(Saitama)',
#       'Solar to receive', 'Salary', 'metlife', 'Mortgage',
#       'saison lalaport visa', 'cosmos gasoline visa', 'edion visa',
#       'Costco old', 'Costco new', 'Yahoo', 'softbank', 'Solar',
#       'Rakuten Visa', 'proyezd', 'sadik', 'Denki', 'Gas', 'Suv',
#       'timur school', 'oyimizga pul', 'jidoushazei', 'home tax', 'Balance',
#       'yashashga', 'Saitama ginko(has to put)', 'Saitama(after balance)',
#       'Mitubishi balance', 'Mitsubishi after balance',
#       'Mitsubishi (has to remain)', 'Mitsubishi to pull total',
#       'Difference between mitsui balance and has to pull',
#       'difference between mitsu balance and has to remain']

visa_cols=[]