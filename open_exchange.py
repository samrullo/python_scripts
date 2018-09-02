# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 22:20:59 2018

@author: amrul
"""

"""
import urllib, json
url = "http://maps.googleapis.com/maps/api/geocode/json?address=google"
response = urllib.urlopen(url)
data = json.loads(response.read())
print data
"""

from myfunctions import *
from urllib.request import urlopen
import json
import datetime

app_id='bda2e8b480e043ed8993c58d36c73c98'

#latest_url='https://openexchangerates.org/api/latest.json?app_id={app_id}'.format(app_id=app_id)
hist_url_tmp='https://openexchangerates.org/api/historical/{date}.json?app_id={app_id}'
#response=urlopen(hist_url)
#data=json.loads(response.read())
#print(data)

dt_range=pd.date_range(start=datetime.date(2018,1,1),end=datetime.date.today())

fx_df=pd.DataFrame(index=dt_range)

for i,row in fx_df.iterrows():
    print(str(datetime.datetime.now())+' processing '+str(i))
    dt_str=str(i.year).zfill(4)+'-'+str(i.month).zfill(2)+'-'+str(i.day).zfill(2)
    hist_url=hist_url_tmp.format(date=dt_str,app_id=app_id)
    response=urlopen(hist_url)
    data=json.loads(response.read())
    if(len(data)!=0):
        rates=data['rates']
        for key,value in rates.items():
            fx_df.loc[i,key]=value

