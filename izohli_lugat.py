# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 21:01:41 2018

@author: amrul
"""

import pandas as pd

folder=r'C:\Users\amrul\Documents\various\izholi_lugat\A'
folder+='\\'
count=0
df=pd.DataFrame(columns=['word','meaning','img'])
for i in range(11):
    file=folder+'izohli_lugat_a_'+str(i)+'.txt'
    fh=open(file,'r',encoding='utf-8')
    ftext=fh.readlines()
    fh.close()    
    for line in ftext:
        if line.split() != '' and len(line.split()) != 0 and  line.split()[0][0] == 'А' and line.split()[0].isupper():
#            print(line.split()[0])
#            print(line.split()[1:])            
            count+=1
            df.loc[count,'word']=line.split()[0]
            df.loc[count,'img']='izohli_lugat_a_'+str(i)+'.jpg'
            df.loc[count,'meaning']=str(df.loc[count,'meaning'])+' '.join(line.split()[1:])            
        else:
            df.loc[count,'meaning']=str(df.loc[count,'meaning'])+' '+line
            print(df)
        