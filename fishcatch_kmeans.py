# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 20:17:58 2018

@author: amrul
"""

import pandas as pd

url="""http://jse.amstat.org/datasets/fishcatch.dat.txt"""
df=pd.read_csv(url,header=-1,error_bad_lines=False)