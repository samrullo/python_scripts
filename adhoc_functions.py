# -*- coding: utf-8 -*-
"""
Created on Thu May 24 17:52:16 2018

@author: amrul
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

folder='C:\\Users\\amrul\\Documents\\rakuten_card\\'
file='rakuten_card_may.csv'

cols=['used_date','shinkisign','user','used_place','payment_method','amount','fee','total_amount','payment_times','tougetsuseikyugaku','yokugetukurikoshizan']
df=pd.read_csv(folder+file,error_bad_lines=False,encoding = "UTF-8")
df.columns=cols