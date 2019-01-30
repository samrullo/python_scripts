# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 05:38:23 2018

@author: amrul
The fish dataset is 6-dimensional. But what is its intrinsic dimension? 
Make a plot of the variances of the PCA features to find out. 
As before, samples is a 2D array, where each row represents a fish. 
You'll need to standardize the features first.
"""

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
import pandas as pd

url="""http://jse.amstat.org/datasets/fishcatch.dat.txt"""
df=pd.read_csv(url,delimiter='\t',error_bad_lines=False,header=-1)
cols=['obs_numb','species','weight','length1','length2','length3','height_pct','width_pct','sex']
fish_df=pd.DataFrame(columns=cols)

for i,row in df.iterrows():
    fish_df.loc[i,:]=row.values[0].split()

sample_cols=['weight','length1','length2','length3','height_pct','width_pct']
fish_df.fillna(0,inplace=True)
for col in sample_cols:
    fish_df[col]=pd.to_numeric(fish_df[col],errors='coerce')
fish_df.fillna(value=10e-7,inplace=True)
samples=fish_df[sample_cols].as_matrix()

# Create scaler: scaler
scaler = StandardScaler()

# Create a PCA instance: pca
pca = PCA()

# Create pipeline: pipeline
pipeline = make_pipeline(scaler,pca)

# Fit the pipeline to 'samples'
pipeline.fit(samples)

# Plot the explained variances
features = range(pca.n_components_)
plt.bar(features, pca.explained_variance_)
plt.xlabel('PCA feature')
plt.ylabel('variance')
plt.xticks(features)
plt.show()
