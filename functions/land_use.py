#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:25:53 2020

@author: nicolasnavarre
"""
import pickle
import pandas as pd

def Area_data():
    data = 'data/'
    df_save = 'df/'
    df_plot_org_prod = pickle.load(open(df_save+"Area_min_org_Prod_2", "rb" ))
    df_plot_eat_prod = pickle.load(open(df_save+"Area_min_eat_Prod_2", "rb" ))
    df_dict_prod = pickle.load(open(df_save+"Area_dict_Prod_2", "rb"))
    POM_prod = pickle.load(open(df_save+"Area_Prod_data", "rb"))
    
    df_plot_org_prod = df_plot_org_prod.set_index("Area")
    df_plot_eat_prod = df_plot_eat_prod.set_index("Area")
    
    current_land = pd.read_csv(data+"FAOSTAT_Ag Land.csv")
    forest_land = pd.read_csv(data+"FAOSTAT_Forest_Land.csv")
    
    total_land = pd.merge(current_land, forest_land[['Area', 'Value']], on = ['Area'], how = 'left')
    total_land = total_land.fillna(0)
    
    for i in current_land.index:
        if current_land["Area"][i] == "C√¥te d'Ivoire":
            current_land["Area"][i] = "Côte d'Ivoire"
    
    total_land['Value'] = total_land['Value_x'] + total_land['Value_y'] 
    
    current_land = total_land[["Area", "Value"]]
    current_land["Value"] *= 1000
    
    final_df = pd.DataFrame()
    final_keys = []
    final_values = []
    final_color = []
    org_check = []
    final_org = []

    for i in df_dict_prod:

        org_check.append(df_dict_prod[i]['Org'])
        del df_dict_prod[i]['Org']
    
    count = 0 
    for i in df_dict_prod:
        temp_list = []
        test = df_dict_prod[i]
        for j in test:
            temp_list.append(test[j])
        #del temp_list[2]
        if min(temp_list) == 0:
            count += 1

            continue
        if temp_list[0] == min(temp_list):
            final_color.append("g")

        final_keys.append(i)
        final_values.append(min(temp_list))
        final_org.append(org_check[count])
        count += 1
    
    
    final_df["Countries"] = final_keys
    final_df["Ha"] = final_values
    final_df["final_color"] = final_color
    final_df["Org area"] = final_org
    
    final_df = final_df.sort_values(by=['Countries'])
    POM_prod = POM_prod.sort_values(by=['Area'])
    
    
    final_df ["IMAGEGROUP"] = final_df["Countries"]
    final_df["Population"] = final_df["Countries"]
    
    for j in final_df.index:
        for i in POM_prod.index:
            if POM_prod["Area"][i] == final_df["Countries"][j]:
                final_df["IMAGEGROUP"][j] = POM_prod["GROUP"][i]
                final_df["Population"][j] = POM_prod["Population (2016), 1000person"][i]
                break
    
            
    final_df = pd.merge(final_df, current_land, left_on = "Countries", right_on = "Area", how = 'left')
    final_df = final_df.drop(columns = "Area")
    final_df = final_df.sort_values(by=["Ha"])
    
    pickle.dump(final_df, open(df_save+"final_df", "wb"))
 
