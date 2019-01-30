# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:37:14 2018

@author: amrul
"""

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import datasets
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

boston=datasets.load_boston()
X_rooms=boston.data[:,5].reshape(-1,1)
y=boston.target

reg=LinearRegression()
reg.fit(X_rooms,y)
y_pred=reg.predict(X_rooms)
plt.scatter(X_rooms,y,color='blue',alpha=0.5)
plt.plot(X_rooms,y_pred,color='black',linewidth=3)
plt.xlabel('Number of rooms')
plt.ylabel('Boston House price')
plt.show()

cv_results=cross_val_score(reg,X_rooms,y,cv=5)
print(cv_results)