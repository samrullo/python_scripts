# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 20:20:06 2018

@author: amrul
"""

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd

url="""https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt"""
df=pd.read_csv(url,delimiter='\t',error_bad_lines=False,header=-1)
cols=['area','perimeter','compactness','length','width','asymmetry_coefficient','kernel_groove_length','label']
df.columns=cols
plt.scatter(df.width,df.length)
plt.show()

samples=df[['area','perimeter','compactness','length','width','asymmetry_coefficient','kernel_groove_length']]
targets=df['label']
grains=samples[['width','length']].as_matrix()

model=PCA()
pca_features=model.fit_transform(grains)
plt.figure()
plt.scatter(pca_features[:,0],pca_features[:,1])
plt.show()