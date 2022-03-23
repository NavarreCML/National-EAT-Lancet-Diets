#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:38:36 2021

@author: nicolasnavarre
"""
import pandas as pd

def feed_eff_conv(feed_detail, feed_lamb, POM_data, FAO_Livestock, feed_conv_adj_lamb, feed_conv_nat_lamb, feed_conv_adj_cow, feed_conv_nat_cow):
    feed_detail['fraction'] = 0
    for i in feed_detail.Area.tolist():
        feed_detail.loc[feed_detail.Area == i, 'fraction'] = 1 - float(FAO_Livestock.loc[(FAO_Livestock.Area == i) & (FAO_Livestock['Item Code'] == 882), '% Grazing'])
    
    POM_p_balance = POM_data.loc[POM_data.Item.isin(['Milk, whole fresh cow'])]
    feed_detail['prod'] = 0
    feed_detail = pd.merge(feed_detail, POM_p_balance[['Area', 'EAT POM (with waste)', 'GROUP']], left_on = 'Area', right_on = 'Area' )
    
    
    for i in feed_detail.Area.tolist():
        feed_detail.loc[feed_detail.Area == i, 'prod'] = float(POM_p_balance.loc[POM_p_balance.Area == i, 'EAT POM (with waste)'])
    
    feed_detail['prod'] *= feed_detail['fraction'] 
    feed_detail['ratio'] = feed_detail['prod']/(feed_detail['grass']*0.17 + feed_detail['Maize']*0.325 + feed_detail['Soybeans']*0.88)
    feed_detail['adjustment'] = 1
        
    #https://www.sciencedirect.com/science/article/pii/S0022030215002180
    feed_detail.loc[feed_detail['ratio']>1.82, 'adjustment'] = feed_detail['ratio'] / 1.82
    feed_detail.loc[feed_detail['ratio']<1.03, 'adjustment'] = feed_detail['ratio'] / 1.03 
    
    for i,j in zip(feed_conv_adj_cow, feed_conv_nat_cow):
        feed_detail.loc[feed_detail.Area == j, 'adjustment'] = feed_detail.loc[feed_detail.Area == j, 'ratio'] / i
    
    feed_detail['new Maize'] = feed_detail['Maize'] * feed_detail['adjustment']
    feed_detail['new Soybean'] = feed_detail['Soybeans'] * feed_detail['adjustment']
    
    feed_lamb['fraction'] = 0
    for i in feed_lamb.Area.tolist():
        if len(FAO_Livestock.loc[(FAO_Livestock.Area == i) & (FAO_Livestock['Item Code'] == 1020)]) > 0:
            feed_lamb.loc[feed_lamb.Area == i, 'fraction'] = 1 - float(FAO_Livestock.loc[(FAO_Livestock.Area == i) & (FAO_Livestock['Item Code'] == 1020), '% Grazing'])
    
    POM_p_balance = POM_data.loc[POM_data.Item.isin(['Milk, whole fresh goat', 'Milk, whole fresh sheep'])]
    POM_p_balance = POM_p_balance[['Area', 'EAT POM (with waste)', 'GROUP']]
    POM_p_temp = pd.DataFrame(POM_p_balance.groupby(['Area']).apply(lambda x:x['EAT POM (with waste)'].sum()))
    POM_p_temp = POM_p_temp.rename(columns = {0:'EAT POM (with waste)'})
    POM_p_balance = POM_p_temp.reset_index()
    feed_lamb['prod'] = 0
    feed_lamb = pd.merge(feed_lamb, POM_p_balance[['Area', 'EAT POM (with waste)']], left_on = 'Area', right_on = 'Area' )
    
    for i in feed_lamb.Area.tolist():
        feed_lamb.loc[feed_lamb.Area == i, 'prod'] = float(POM_p_balance.loc[POM_p_balance.Area == i, 'EAT POM (with waste)'])
    
    feed_lamb['prod'] *= feed_lamb['fraction'] 
    feed_lamb['ratio'] = feed_lamb['prod']/(feed_lamb['grass']*0.17 + feed_lamb['Maize']*0.325 + feed_lamb['Soybeans']*0.88)
    feed_lamb['adjustment'] = 1
    #https://www.scielo.br/pdf/rbz/v43n10/1516-3598-rbz-43-10-00524.pdf
    feed_lamb.loc[feed_lamb['ratio']>1.44, 'adjustment'] = feed_lamb['ratio'] / 1.44
    feed_lamb.loc[feed_lamb['ratio']<0.74, 'adjustment'] = feed_lamb['ratio'] / 0.74 
    
    
    for i,j in zip(feed_conv_adj_lamb, feed_conv_nat_lamb):
        feed_lamb.loc[feed_lamb.Area == j, 'adjustment'] = feed_lamb.loc[feed_lamb.Area == j, 'ratio'] / i

    
    feed_lamb['new Maize'] = feed_lamb['Maize'] * feed_lamb['adjustment']
    feed_lamb['new Soybean'] = feed_lamb['Soybeans'] * feed_lamb['adjustment']
    
    
    for i in feed_detail.Area.tolist():
        POM_data.loc[(POM_data.Area == i) & (POM_data.Item == 'Maize'), 'for feed EAT'] +=\
            float(feed_detail.loc[feed_detail.Area == i, 'new Maize']) - float(feed_detail.loc[feed_detail.Area == i, 'Maize'])
        POM_data.loc[(POM_data.Area == i) & (POM_data.Item == 'Soybeans'), 'for feed EAT'] +=\
            float(feed_detail.loc[feed_detail.Area == i, 'new Soybean']) - float(feed_detail.loc[feed_detail.Area == i, 'Soybeans'])
        POM_data.loc[(POM_data.Area == i) & (POM_data.Item == 'Maize'), 'POM EAT (with waste & feed)'] +=\
            float(feed_detail.loc[feed_detail.Area == i, 'new Maize']) - float(feed_detail.loc[feed_detail.Area == i, 'Maize'])
        POM_data.loc[(POM_data.Area == i) & (POM_data.Item == 'Soybeans'), 'POM EAT (with waste & feed)'] +=\
            float(feed_detail.loc[feed_detail.Area == i, 'new Soybean']) - float(feed_detail.loc[feed_detail.Area == i, 'Soybeans'])
    
    for i in feed_lamb.Area.tolist():
        POM_data.loc[(POM_data.Area == i) & (POM_data.Item == 'Maize'), 'for feed EAT'] +=\
            float(feed_lamb.loc[feed_lamb.Area == i, 'new Maize']) - float(feed_lamb.loc[feed_lamb.Area == i, 'Maize'])
        POM_data.loc[(POM_data.Area == i) & (POM_data.Item == 'Soybeans'), 'for feed EAT'] +=\
            float(feed_lamb.loc[feed_lamb.Area == i, 'new Soybean']) - float(feed_lamb.loc[feed_lamb.Area == i, 'Soybeans'])
        POM_data.loc[(POM_data.Area == i) & (POM_data.Item == 'Maize'), 'POM EAT (with waste & feed)'] +=\
            float(feed_lamb.loc[feed_lamb.Area == i, 'new Maize']) - float(feed_lamb.loc[feed_lamb.Area == i, 'Maize'])
        POM_data.loc[(POM_data.Area == i) & (POM_data.Item == 'Soybeans'), 'POM EAT (with waste & feed)'] +=\
            float(feed_lamb.loc[feed_lamb.Area == i, 'new Soybean']) - float(feed_lamb.loc[feed_lamb.Area == i, 'Soybeans'])
    return POM_data