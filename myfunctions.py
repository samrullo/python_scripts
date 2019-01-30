# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 21:30:17 2018

@author: amrul
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def add_ret_cols(df,col):
    df['dly_ret']=df[col].pct_change()
    df['dly_ret_bps']=df['dly_ret']*10000
    df['comp_ret']=np.cumprod(1+df['dly_ret'])
    df['up']=df['dly_ret_bps'].map(lambda x: x>0)
    return df