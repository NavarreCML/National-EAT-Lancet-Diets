#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:48:33 2021

@author: nicolasnavarre
"""
from collections import defaultdict
import pickle
import pandas as pd

df_save = 'df/'
    
def save_data(POM_global, POM_data):

    df1 = POM_global
    df_dict = df1.to_dict(orient = 'index')
    dict_min_org = defaultdict(list)
    dict_min_new = defaultdict(list)
    dict_min_eat = defaultdict(list)
    
    for i in df_dict:
        #print(df_dict[i])
        temp_list = []
        test = df_dict[i]
        for j in test:
            temp_list.append(test[j])
            #print(test[j])
        if temp_list[0] == min(temp_list):
            dict_min_org[i].append(temp_list)
        else:
            dict_min_eat[i].append(temp_list)
            
    df_min_org = pd.DataFrame([[k] + v[0] for k, v in dict_min_org.items()], 
                       columns=['Area', 'Org', 'EAT'])
    
    df_min_eat = pd.DataFrame([[k] + v[0] for k, v in dict_min_eat.items()], 
                       columns=['Area', 'Org', 'EAT'])
    
    pickle.dump(df_min_org, open(df_save+"df_min_org_Prod_2", "wb"))
    pickle.dump(df_min_eat, open(df_save+"df_min_eat_Prod_2", "wb"))
    #pickle.dump(POM_global_avg, open("POM_global_avg", "wb"))
    pickle.dump(df_dict, open(df_save+"df_dict_Prod_2", "wb"))
    pickle.dump(POM_data, open(df_save+"Prod_data", "wb"))
    pickle.dump(POM_global, open(df_save+"Prod_global", "wb"))
    
    
def save_area_data(Meat_Area, FAO_all_crops_area, Feed_crops_area_sum, Weighted_final, FAO_pop, Total_Area, POM_data):
    
    Compare_Area = pd.merge(Meat_Area, FAO_all_crops_area, on = 'Area')
    Compare_Area = pd.merge(Compare_Area, Feed_crops_area_sum, on = 'Area')
    
    Compare_Area = Compare_Area.rename(columns = {"Org_x": "Org Meat & Dairy Area", "EAT_x":"EAT Meat & Dairy Area"})
    Compare_Area = Compare_Area.rename(columns = {"Org_y": "Org Crop Area", "EAT_y":"EAT Crop Area"})
    
    Compare_Area['Meat Share'] = (Compare_Area['EAT Meat & Dairy Area']/(Compare_Area['EAT Meat & Dairy Area']+Compare_Area['EAT Crop Area']))*100
    Compare_Area['Feed Share'] = (Compare_Area['Feed crop Area']/(Compare_Area['EAT Meat & Dairy Area']+Compare_Area['EAT Crop Area']))*100
    Compare_Area['IMAGEGROUP'] = Compare_Area['Meat Share']
    Compare_Area['pop'] = Compare_Area['Meat Share']
    for i in Weighted_final.index:
        Compare_Area.loc[Compare_Area.Area == Weighted_final.Area[i], 'IMAGEGROUP'] = Weighted_final.GROUP[i]
    for i in FAO_pop.index:
        Compare_Area.loc[Compare_Area.Area == FAO_pop.Area[i], 'pop'] = FAO_pop.Value[i]
        
    Compare_Area['meatha/p'] = Compare_Area['EAT Meat & Dairy Area']/(Compare_Area['pop']*1000)
    Compare_Area['cropha/p'] = Compare_Area['EAT Crop Area']/(Compare_Area['pop']*1000)
    Compare_Area['totha/p'] = (Compare_Area['EAT Meat & Dairy Area']+Compare_Area['EAT Crop Area'])/(Compare_Area['pop']*1000)
    
    #Total_Area = FAO_all_crops_area
    Area_Used = pd.DataFrame()
    Area_Used ["Org"] = Total_Area.groupby(["Area"]).apply(lambda x: x["Org"].sum())
    Area_Used ["EAT"] = Total_Area.groupby(["Area"]).apply(lambda x: x["EAT"].sum())
    
    
    for i in Area_Used.index:
        if Area_Used["Org"][i] == 0:
            Area_Used = Area_Used.drop([i])
    
    from collections import defaultdict
    df1 = Area_Used
    df_dict = df1.to_dict(orient = 'index')
    
    dict_min_org = defaultdict(list)
    dict_min_new = defaultdict(list)
    dict_min_eat = defaultdict(list)
    
    for i in df_dict:
        #print(df_dict[i])
        temp_list = []
        test = df_dict[i]
        for j in test:
            temp_list.append(test[j])
            #print(test[j])
        if temp_list[0] == min(temp_list):
            dict_min_org[i].append(temp_list)
        else:
            dict_min_eat[i].append(temp_list)
            
    df_min_org = pd.DataFrame([[k] + v[0] for k, v in dict_min_org.items()], 
                       columns=['Area', 'Org', 'EAT'])
    df_min_eat = pd.DataFrame([[k] + v[0] for k, v in dict_min_eat.items()], 
                       columns=['Area', 'Org', 'EAT'])
    
    total_org = df_min_org['Org'].sum() + df_min_eat['Org'].sum()
    total_eat = df_min_org['EAT'].sum() + df_min_eat['EAT'].sum()
    
    import pickle
    pickle.dump(df_min_org, open(df_save+"Area_min_org_Prod_2", "wb"))
    pickle.dump(df_min_eat, open(df_save+"Area_min_eat_Prod_2", "wb"))
    #pickle.dump(POM_global_avg, open("POM_global_avg", "wb"))
    pickle.dump(df_dict, open(df_save+"Area_dict_Prod_2", "wb"))
    pickle.dump(POM_data, open(df_save+"Area_Prod_data", "wb"))
    pickle.dump(Area_Used, open(df_save+"Prod_global_area", "wb"))