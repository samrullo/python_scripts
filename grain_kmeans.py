# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 19:25:18 2018

@author: amrul
"""

import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans

from scipy.cluster.hierarchy import linkage, dendrogram


url="""https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt"""
html=urlopen(url)
soup=BeautifulSoup(html,'lxml')
#print(soup.title)
#print(soup.get_text())
df=pd.read_csv(url,delimiter='\t',error_bad_lines=False,header=-1)
cols=['area','perimeter','compactness','length','width','asymmetry_coefficient','kernel_groove_length','label']
df.columns=cols
plt.scatter(df.width,df.length)
plt.show()

samples=df[['area','perimeter','compactness','length','width','asymmetry_coefficient','kernel_groove_length']]
targets=df['label']

ks=range(1,7)
inertias=[]
for k in ks:
    model=KMeans(n_clusters=k)
    model.fit(samples)
    inertias.append(model.inertia_)

plt.plot(ks,inertias,'-o')
plt.xlabel('number of clusters')
plt.ylabel('inertia')
plt.xticks(ks)
plt.show()

model=KMeans(n_clusters=3)
labels=model.fit_predict(samples)
df2=pd.DataFrame({'labels':labels,'targets':targets.values})
print(pd.crosstab(df2['labels'],df2['targets']))

#varieties=['Kama wheat',
# 'Kama wheat',
# 'Kama wheat',
# 'Kama wheat',
# 'Kama wheat',
# 'Kama wheat',
# 'Kama wheat',
# 'Kama wheat',
# 'Kama wheat',
# 'Kama wheat',
# 'Kama wheat',
# 'Kama wheat',
# 'Kama wheat',
# 'Kama wheat',
# 'Rosa wheat',
# 'Rosa wheat',
# 'Rosa wheat',
# 'Rosa wheat',
# 'Rosa wheat',
# 'Rosa wheat',
# 'Rosa wheat',
# 'Rosa wheat',
# 'Rosa wheat',
# 'Rosa wheat',
# 'Rosa wheat',
# 'Rosa wheat',
# 'Rosa wheat',
# 'Rosa wheat',
# 'Canadian wheat',
# 'Canadian wheat',
# 'Canadian wheat',
# 'Canadian wheat',
# 'Canadian wheat',
# 'Canadian wheat',
# 'Canadian wheat',
# 'Canadian wheat',
# 'Canadian wheat',
# 'Canadian wheat',
# 'Canadian wheat',
# 'Canadian wheat',
# 'Canadian wheat',
# 'Canadian wheat']
#
plt.figure()
mergings=linkage(samples, method='complete')
dendrogram(mergings, labels=targets.values, leaf_rotation=90,leaf_font_size=6)

#Try using t-SNE to plot 2D map of the 7 dimensional grain dataset
from sklearn.manifold import TSNE
model=TSNE(learning_rate=100)
transformed=model.fit_transform(samples)
plt.figure()
plt.scatter(transformed[:,0], transformed[:,1], c=targets, alpha=0.5)