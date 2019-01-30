# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 19:01:23 2018

@author: amrul
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from urllib.request import urlopen
from bs4 import BeautifulSoup

url="https://my.orico.co.jp/eorico/KAL1B40000.do"
html=urlopen(url)
soup=BeautifulSoup(html,'lxml')

print(soup.title)