# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:57:49 2018

@author: amrul
"""

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import datasets
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
import numpy as np
import matplotlib.pyplot as plt

boston=datasets.load_boston()
X=boston.data
y=boston.target

X_train, X_test, y_train, y_test=train_test_split(X,y,test_size=0.3,random_state=42)

ols_reg=LinearRegression()
ols_reg.fit(X_train,y_train)
cv_results=cross_val_score(ols_reg,X_train,y_train,cv=5)
print("OLS score:",ols_reg.score(X_test,y_test))
print("OLS cross val:",cv_results)

ridge=Ridge(alpha=0.1,normalize=True)
ridge.fit(X_train,y_train)
cv_results=cross_val_score(ridge,X_train,y_train,cv=5)
print("Ridge score:",ridge.score(X_test,y_test))
print("Ridge cross val:",cv_results)

lasso=Lasso(alpha=0.1,normalize=True)
lasso.fit(X_train,y_train)
cv_results=cross_val_score(lasso,X_train,y_train,cv=5)
print("Lasso score:",lasso.score(X_test,y_test))
print("Lasso cross val:",cv_results)

#detecting important features with lasso
#you can verify that number of rooms is the most important feature
names=boston.feature_names
lasso_coef=lasso.coef_
plt.plot(range(len(names)),lasso_coef)
plt.xticks(range(len(names)),names,rotation=60)
plt.ylabel('Coefficients')
plt.show()