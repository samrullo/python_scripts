# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 00:31:39 2018

@author: amrul
"""

from myfunctions import *
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score


def calc_profit(beg_rate, end_rate, lots):
    print("Pips earned:", (end_rate - beg_rate) * 100)
    return (end_rate - beg_rate) * lots * 100000


def calc_sl(risk, open_rate, lots):
    """
    Calculate stop loss, given maximum amount that one is ready to lose
    :param risk:
    :param open_rate:
    :param lots:
    :return:
    """
    sl_rate = open_rate - risk / (lots * 10 ** 5)
    print("Pips to lose:", (open_rate - sl_rate) * 100)
    print("SL rate:", sl_rate)
    return sl_rate


def load_mt4_fx_file(folder, file):
    fx_df = pd.read_csv(folder + file, header=-1, index_col=0, parse_dates=True)
    fx_df.drop(1, axis=1, inplace=True)
    cols = ['open', 'high', 'low', 'close', 'volume']
    fx_df.columns = cols
    fx_df = add_ret_cols(fx_df, 'close')
    return fx_df


def feature_target_maker(usdjpy_df, n_features, inx_feature, inx_target):
    targets = []
    predictors = []
    for i in range(len(usdjpy_df) - 1):
        if i > n_features:
            sample_predictors = []
            for i2 in range(n_features):
                sample_predictors.append(usdjpy_df.iloc[i - i2, inx_feature])
            predictors.append(sample_predictors)
            targets.append(usdjpy_df.iloc[i + 1, inx_target] > 0)
        else:
            continue
    X = np.array(predictors)
    y = np.array(targets)
    return X, y


def feature_target_maker2(df, inx_target):
    targets = []
    predictors = []
    for i in range(len(df)):
        if i > 1:
            predictors.append(
                [df.iloc[i - 1, 0], df.iloc[i - 1, 1], df.iloc[i - 1, 2], df.iloc[i - 1, 3], df.iloc[i - 1, 4]])
            targets.append(df.iloc[i, inx_target])
        else:
            continue
    X = np.array(predictors)
    y = np.array(targets)
    return X, y


folder = r'C:\Users\amrul\Downloads\mt4_downloads'
folder += '\\'
eurjpy_file = r'eurjpy_daily_20110802_to_20180831.csv'
usdjpy_file = r'usdjpy_20180622_0645_to_20190104_2345'
eurusd_file = r'eurusd_daily_20180910 .csv'
audjpy_file = r'audjpy_daily.csv'
# eurjpy_df=load_mt4_fx_file(folder,eurjpy_file)
usdjpy_df = load_mt4_fx_file(folder, usdjpy_file)
# audjpy_df = load_mt4_fx_file(folder, audjpy_file)

### trying LinearRegression with features 5 recent close fx rates to predict 6th day's fx rate ###
# X,y=feature_target_maker(usdjpy_df,5,3,3)
#
# X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=42)
#
# ols_reg=LinearRegression()
# ols_reg.fit(X_train,y_train)
# print("OLS score:",ols_reg.score(X_test,y_test))
# cv_result=cross_val_score(ols_reg,X_train,y_train,cv=5)
# print("OLS cross val:",cv_result)
#
# ridge=Ridge(alpha=0.1,normalize=True)
# ridge.fit(X_train,y_train)
# print("Ridge score:",ridge.score(X_test,y_test))
# cv_result=cross_val_score(ridge,X_train,y_train,cv=5)
# print("Ridge cross val:",cv_result)


### Building k-NearestNeighbor model to predit FX rate based on last 5 days rates ###
# X,y=feature_target_maker(usdjpy_df,6,3,8)
# #X,y=feature_target_maker2(usdjpy_df,8)
# X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=42)
# knn=KNeighborsClassifier(n_neighbors=7)
# knn.fit(X_train,y_train)
# print("knn score:",knn.score(X_test,y_test))
#
#
# logreg=LogisticRegression()
# logreg.fit(X_train,y_train)
# y_pred=logreg.predict(X_test)
# y_pred_prob=logreg.predict_proba(X_test)[:,1]
# print("logreg score:",logreg.score(X_test,y_test))
# print(confusion_matrix(y_test,y_pred))
# print(classification_report(y_test,y_pred))
# fpr,tpr,thresholds=roc_curve(y_test,y_pred_prob)
# plt.plot([0,1],[0,1],'k--')
# plt.plot(fpr,tpr,label='Logistic Regression')
# plt.xlabel("False positive rate")
# plt.ylabel("True positive rate")
# plt.title("Logistic Regression ROC curve")
# plt.show()
#
# cv_score=cross_val_score(logreg,X,y,cv=5,scoring='roc_auc')
# print("Roc AUC score:",roc_auc_score(y_test,y_pred_prob))
# print("ROC AUC cross val score:",cv_score)
#
#
#
#
# #eurusd_df=load_mt4_fx_file(folder,eurusd_file)
#
# #plt.subplot(2,2,1)
# #eurjpy_df.loc['2018-5':'2018-8','dly_ret_bps'].plot(label='eurjpy')
# #usdjpy_df.loc['2018-5':'2018-8','dly_ret_bps'].plot(label='usdjpy')
# #plt.xlabel('date')
# #plt.ylabel('daily return in bps')
# #plt.title('Daily return in bps')
# #plt.legend()
# #plt.show()
#
# #plt.subplot(2,2,2)
# #eurjpy_df.loc['2018-8','close'].plot(label='eurjpy')
# #usdjpy_df.loc['2018-8','close'].plot(label='usdjpy')
# #plt.xlabel('date')
# #plt.ylabel('Close prices')
# #plt.title('Close prices')
# #plt.legend()
# #plt.tight_layout()
# #plt.show()
# #
# #plt.subplot(2,2,3)
# #eurjpy_df.loc['2018-8','comp_ret'].plot(label='eurjpy')
# #usdjpy_df.loc['2018-8','comp_ret'].plot(label='usdjpy')
# #plt.xlabel('date')
# #plt.ylabel('Compounded return')
# #plt.title('Compounded return in decimals start with 1 unit of currency')
# #plt.legend()
# #plt.tight_layout()
# #plt.show()
# #
