# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 18:47:51 2018

@author: amrul
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date

from lxml.html import parse
from urllib.request import urlopen
import urllib

def getProductInfo(url='https://melonpanda.com/catalog/chocolate',folder='C:\\Users\\amrul\\Documents\\japan_sweets_business\\japan_panda_webpage\\',file='chocolates_catalog.xlsx',category='food'):
    parsed=parse(urlopen(url))
    doc=parsed.getroot()
    products=doc.find_class('product')
    product_id_arr=[]
    product_price_arr=[]
    product_name_eng_arr=[]
    product_name_rus_arr=[]
    product_img_src_arr=[]
    for product in products:
        product_id_arr.append(product.attrib['id'].strip())
        links=product.findall('.//a')
        product_name_eng_arr.append(links[1].attrib['href'].strip())
        product_name_rus_arr.append(links[1].text)
        img=product.find('.//img')
        product_img_src_arr.append(img.attrib['src'].strip())
        price=product.find_class('price price_yen')
        price_int=int(price[0].text.replace(' ',''))
        product_price_arr.append(price_int)
    data={'product_id':product_id_arr,'product_price':product_price_arr,'product_name_eng':product_name_eng_arr,'product_name_rus':product_name_rus_arr,'product_img':product_img_src_arr}
    df=pd.DataFrame(data=data)
    df['category']=category
    df.to_excel(folder+file,index=False)
    return df

def getCategories(url='https://melonpanda.com',folder='C:\\Users\\amrul\\Documents\\japan_sweets_business\\japan_panda_webpage\\catalog\\',file='categories.xlsx'):
    category_href_arr=[]
    subcategory_href_arr=[]
    category_text_arr=[]
    subcategory_text_arr=[]
    parsed=parse(urlopen(url))
    doc=parsed.getroot()
    categories=doc.find_class('side-menu__elem')
    product_df_arr=[]
    for category in categories:
        link=category.find('.//a')
        category_href=link.attrib['href']
        category_text=link.text.strip()
        subcategories=category.find_class('side-submenu__elem')
        for subcategory in subcategories:
            link=subcategory.find('.//a')
            subcategory_href=link.attrib['href']
            subcategory_text=link.text.strip()
            category_href_arr.append(category_href)
            subcategory_href_arr.append(subcategory_href)
            category_text_arr.append(category_text)
            subcategory_text_arr.append(subcategory_text)
            product_df=getProductInfo(url=url+subcategory_href,folder=folder,category=subcategory_href.split('/')[-1],file=subcategory_href.replace('/','_')+'.xlsx')
            product_df_arr.append(product_df)
    data={'category_href':category_href_arr,'subcategory_href':subcategory_href_arr,'category_text':category_text_arr,'subcategory_text':subcategory_text_arr}
    df=pd.DataFrame(data=data)
    df.to_excel(folder+file,index=False)
    product_agg_df=pd.concat(product_df_arr)
    product_agg_df.to_excel(folder+'all_products.xlsx',index=False)
    return df,product_df_arr

def make_sql_files(folder,file):
    df=pd.read_excel(folder+file)
    content_sql=""" INSERT INTO `content` (`ID`,`current_revision`,`active`,`secure`,`parent`,`order`,`author`,`type`,`path`) VALUES """
    content_sql_row=""" ({ID},{current_revision},{active},{secure},{parent},{order},{author},{type},'{path}') """
    content_versions_sql=""" INSERT INTO `content_versions` (`ID`,`title`,`name`,`heading`,`author`) VALUES """
    content_versions_sql_row=""" ({ID},'{title}','{name}','{heading}',{author}) """
    content_types_products_sql=""" INSERT INTO `content_types_products` (`ID`,`content_version`,`price`,`image`) VALUES """
    content_types_products_sql_row=""" ({ID},{content_version},{price},'{image}') """
    
    for i,row in df.iterrows():
        content_sql_record=content_sql_row.format(ID=row['ID'],current_revision=row['ID'],active=1,secure=1,parent=0,order=0,author=2,type=2,path=row['path'])
        content_sql+=content_sql_record+','
        content_versions_record=content_versions_sql_row.format(ID=row['ID'],title=row['path'],name=row['product_name_rus'],heading=row['product_name_rus'],author=2)
        content_versions_sql+=content_versions_record+""","""
        content_types_products_record=content_types_products_sql_row.format(ID=row['ID'],content_version=row['ID'],price=row['product_price'],image=row['product_img'])
        content_types_products_sql+=content_types_products_record+""","""
        
    content_sql=content_sql[:-1]+';'
    content_versions_sql=content_versions_sql[:-1]+';'
    content_types_products_sql=content_types_products_sql[:-1]+';'
    
    content_fh=open(folder+'content.sql','w',encoding='utf-8')
    content_fh.write(content_sql)
    content_fh.close()
    
    content_versions_fh=open(folder+'content_versions.sql','w',encoding='utf-8')
    content_versions_fh.write(content_versions_sql)
    content_versions_fh.close()
    
    content_types_products_fh=open(folder+'content_types_products.sql','w',encoding='utf-8')
    content_types_products_fh.write(content_types_products_sql)
    content_types_products_fh.close()
    return (content_versions_sql,content_sql,content_types_products_sql)

def make_categories_sql_file(folder,file):
    df=pd.read_excel(folder+file)
    categories_insert_sql=""" INSERT INTO `categories` (`id`,`name_eng`,`name`,`parent`) VALUES """
    
    categories_insert_sql_row=""" ({id},'{name_eng}','{name}',{parent}) """

    for i,row in df.iterrows():
        categories_insert_sql_record=categories_insert_sql_row.format(id=row['ID'],name_eng=row['subcategory_eng'],name=row['subcategory_rus'],parent=row['parent_id'])
        categories_insert_sql+=categories_insert_sql_record+""" , """
    
    categories_insert_sql=categories_insert_sql[:-1]+';'
    categories_fh=open(folder+'sub_categories.sql','w',encoding='utf-8')
    categories_fh.write(categories_insert_sql)
    categories_fh.close()
    return (df,categories_insert_sql)


def make_products_sql_file(folder,file):
    df=pd.read_excel(folder+file)
    products_insert_sql=""" INSERT INTO `products` (`id`,`name`,`description`,`price`,`category`,`image`) VALUES """
    products_insert_sql_row=""" ({id},'{name}','{description}',{price},{category},'{image}')"""

    for i,row in df.iterrows():
        products_insert_sql_record=products_insert_sql_row.format(id=row['id'],name=row['name'],description=row['description'],price=row['price'],category=row['category'],image=row['image'])
        products_insert_sql+=products_insert_sql_record+""" , """
    
    products_insert_sql=products_insert_sql[:-1]+';'
    products_fh=open(folder+'products.sql','w',encoding='utf-8')
    products_fh.write(products_insert_sql)
    products_fh.close()
    return (df,products_insert_sql)

def make_update_products_sql(folder,file):
    df=pd.read_excel(folder+file)
    update_sql=""" UPDATE `products` SET `price`='{price}' WHERE `id`='{id}'"""
    update_sql_fh=open(folder+'products_update.sql','w',encoding='utf-8')
    for i,row in df.iterrows():
        update_sql_record=update_sql.format(price=row['price'],id=row['id'])+';'
        update_sql_fh.write(update_sql_record)
    
    update_sql_fh.close()
    return df


folder=r'C:\Users\amrul\Documents\japan_sweets_business\japan_panda_webpage\catalog'
folder+='\\'
file='ecommerce_products_tousd.xlsx'
ret=make_update_products_sql(folder,file)

#df=getProductInfo()
#menu_df,product_df_arr=getCategories()
    
"""
folder='C:\\Users\\amrul\\Documents\\japan_sweets_business\\japan_panda_webpage\\catalog\\'
img_folder='C:\\Users\\amrul\\Documents\\japan_sweets_business\\japan_panda_webpage\\catalog\\product_images\\'
categories_file='categories.xlsx'
product_category_file='all_products_v0.0.xlsx'
products_file='all_products_v0.4.xlsx'

categoried_df=pd.read_excel(folder+categories_file)
product_category_df=pd.read_excel(folder+product_category_file)
products_df=pd.read_excel(folder+products_file)

categoried_df['category']=categoried_df['subcategory_eng']
categoried_df['category_id']=categoried_df['ID']


prd_cat_df=pd.merge(left=product_category_df,right=products_df,on='product_id',how='left')
prd_cat_df['product_id']=prd_cat_df['ID']

prd_cat_all_df=pd.merge(left=prd_cat_df,right=categoried_df,on='category',how='left')

prd_cat_final_df=prd_cat_all_df[['product_id','category_id','path','category']]

"""
#prd_cat_sql=""" INSERT INTO `product_category` (`ID`,`product_id`,`category_id`) VALUES """
#prd_cat_row=""" ({ID},{product_id},{category_id})"""
"""

for i,row in prd_cat_final_df.iterrows():
    prd_cat_record=prd_cat_row.format(ID=i,product_id=row['product_id'],category_id=row['category_id'])
    prd_cat_sql+=prd_cat_record+""","""

prd_cat_sql=prd_cat_sql[:-1]+';'
prd_cat_fh=open(folder+'prd_cat.sql','w',encoding='utf-8')
prd_cat_fh.write(prd_cat_sql)
prd_cat_fh.close()
#tmp=make_sql_files(folder,file)

#ret=make_categories_sql_file(folder,file)

#urllib.urlretrieve(df.iloc[0,'product_img'], df.iloc[0,'path']+".jpg")

"""
#downloading each image from url and saving it into file
"""
for i,row in df.iterrows():
    fh=open(img_folder+row['path']+'.jpg','wb')
    fh.write(urlopen(row['product_img']).read())
    fh.close()
"""




"""
cols=['product_id', 'product_name_eng', 'product_name_rus','product_price','path']
new_df=pd.DataFrame(columns=cols)
for col in cols:
    new_df[col]=df[col].unique()

id_index=np.arange(len(df))+1000
df['ID']=id_index
#df['path']=df['product_name_eng'].apply(lambda x:'-'.join(x.split('/')[-1].split('-')[1:]))
df.to_excel(folder+'all_products.xlsx',index=False)

df=pd.read_excel(folder+file)
df['category_href']=df['category_href'].apply(lambda x:x.split('/')[-1])
df['subcategory_href']=df['subcategory_href'].apply(lambda x:x.split('/')[-1])
df.to_excel(folder+'categories.xlsx',index=False,header=['category_eng','category_rus','subcategory_eng','subcategory_rus'])
"""