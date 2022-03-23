#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:54:27 2021

@author: nicolasnavarre
"""
import pandas as pd


data = 'data/'

def livestock_area(FAO_Livestock, FAO_LSU_Coeffs, POM_data, beef_items, beef_milk_items, lamb_items, lamb_milk_items, ls_proxie, diet_div_ls, diet_source_ls):
    FAO_Livestock['Value'] =  FAO_Livestock["Production"] / FAO_Livestock["Prod/Hd"]
    FAO_Livestock['Value Org'] =  FAO_Livestock["Production"] / FAO_Livestock["Prod/Hd Org"]

    FAO_Livestock_landuse = pd.read_csv(data+'Livestock_Paterns.csv')
    FAO_Livestock_landuse = FAO_Livestock_landuse.rename(columns = {"Value" : "LSU/Ha"})
    FAO_Livestock_landuse.loc[FAO_Livestock_landuse.Area ==\
                              'United Kingdom of Great Britain and Northern Ireland', 'Area'] = 'United Kingdom'
    
    #FAO_LSU_Coeffs = pd.read_csv(r'LSU_Coeffs_by_Country.csv', encoding='latin-1')
    FAO_LSU_Coeffs = FAO_LSU_Coeffs.rename(columns = {"Value" : "LSU Coeff", "AreaName" : "Area", "ItemName" :"Item"})
    
    if ls_proxie == True:
        for i,j in zip (diet_div_ls, diet_source_ls): 
            fao_fix = FAO_Livestock_landuse.loc[FAO_Livestock_landuse.Area == j]
            fao_fix['Area'] = i
            
            FAO_Livestock_landuse = FAO_Livestock_landuse[FAO_Livestock_landuse.Area != i]
            FAO_Livestock_landuse = pd.concat([FAO_Livestock_landuse,fao_fix])
    
    FAO_Livestock_landuse = FAO_Livestock_landuse.reset_index()
    
    FAO_Livestock_landuse = pd.merge(FAO_Livestock_landuse, FAO_LSU_Coeffs, on = ["Area", "Item"], how = 'left')
    FAO_Livestock_landuse['Value'] = FAO_Livestock_landuse['Hd/Ha (max)']
    
    


    
    FAO_Livestock['Hd/Ha'] = FAO_Livestock['Item']
    FAO_Livestock['% Grazing'] = FAO_Livestock['Item']
    FAO_Livestock['% int Land'] = FAO_Livestock['Item']
    animal_species = ['Asses', 'Buffaloes', 'Camels', 'Cattle', 'Chickens',\
                      'Goats','Horses', 'Mules', 'Pigs', 'Sheep']
    for i in FAO_Livestock_landuse.index:
        if FAO_Livestock_landuse['Item'][i] == 'Asses':
            for j in FAO_Livestock.index:
                if FAO_Livestock['Area'][j] == FAO_Livestock_landuse['Area'][i] and FAO_Livestock['Item'][j] in ['Meat, ass']:
                    FAO_Livestock['Hd/Ha'][j] = FAO_Livestock_landuse['Value'][i]   
                    FAO_Livestock['% Grazing'][j] = FAO_Livestock_landuse['% Grazing'][i]
                    FAO_Livestock['% int Land'][j] = FAO_Livestock_landuse['% int Land'][i]
        
        if FAO_Livestock_landuse['Item'][i] == 'Buffaloes':
            for j in FAO_Livestock.index:
                if FAO_Livestock['Area'][j] == FAO_Livestock_landuse['Area'][i] and FAO_Livestock['Item'][j] in ['Meat, buffalo', 'Milk, whole fresh buffalo']:
                    FAO_Livestock['Hd/Ha'][j] = FAO_Livestock_landuse['Value'][i]  
                    FAO_Livestock['% Grazing'][j] = FAO_Livestock_landuse['% Grazing'][i]
                    FAO_Livestock['% int Land'][j] = FAO_Livestock_landuse['% int Land'][i]
                    
        if FAO_Livestock_landuse['Item'][i] == 'Camels':
            for j in FAO_Livestock.index:
                if FAO_Livestock['Area'][j] == FAO_Livestock_landuse['Area'][i] and FAO_Livestock['Item'][j] in ['Meat, camel', 'Milk, whole fresh camel', 'Meat, other camelids']:
                    FAO_Livestock['Hd/Ha'][j] = FAO_Livestock_landuse['Value'][i]  
                    FAO_Livestock['% Grazing'][j] = FAO_Livestock_landuse['% Grazing'][i]
                    FAO_Livestock['% int Land'][j] = FAO_Livestock_landuse['% int Land'][i]
                    
        if FAO_Livestock_landuse['Item'][i] == 'Cattle':
            for j in FAO_Livestock.index:
                if FAO_Livestock['Area'][j] == FAO_Livestock_landuse['Area'][i] and FAO_Livestock['Item'][j] in ['Meat, cattle', 'Milk, whole fresh cow']:
                    FAO_Livestock['Hd/Ha'][j] = FAO_Livestock_landuse['Value'][i]   
                    FAO_Livestock['% Grazing'][j] = FAO_Livestock_landuse['% Grazing'][i]
                    FAO_Livestock['% int Land'][j] = FAO_Livestock_landuse['% int Land'][i]
                    
        if FAO_Livestock_landuse['Item'][i] == 'Chickens':
            for j in FAO_Livestock.index:
                if FAO_Livestock['Area'][j] == FAO_Livestock_landuse['Area'][i] and FAO_Livestock['group'][j] in ['chicken and other poultry', 'eggs', 'rabbit', 'other']:#, 'Eggs, other bird, in shell','Meat, goose and guinea fowl', 'Meat, other rodents', 'Meat, rabbit', 'Meat, turkey', 'Meat, duck']:
                    FAO_Livestock['Hd/Ha'][j] = FAO_Livestock_landuse['Value'][i]
                    FAO_Livestock['% Grazing'][j] = FAO_Livestock_landuse['% Grazing'][i]
                    FAO_Livestock['% int Land'][j] = FAO_Livestock_landuse['% int Land'][i]
                    
        if FAO_Livestock_landuse['Item'][i] == 'Goats':
            for j in FAO_Livestock.index:
                if FAO_Livestock['Area'][j] == FAO_Livestock_landuse['Area'][i] and FAO_Livestock['Item'][j] in ['Meat, goat', 'Milk, whole fresh goat']:
                    FAO_Livestock['Hd/Ha'][j] = FAO_Livestock_landuse['Value'][i] 
                    FAO_Livestock['% Grazing'][j] = FAO_Livestock_landuse['% Grazing'][i]
                    FAO_Livestock['% int Land'][j] = FAO_Livestock_landuse['% int Land'][i]
        
        if FAO_Livestock_landuse['Item'][i] == 'Horses':
            for j in FAO_Livestock.index:
                if FAO_Livestock['Area'][j] == FAO_Livestock_landuse['Area'][i] and FAO_Livestock['Item'][j] in ['Meat, horse']:
                    FAO_Livestock['Hd/Ha'][j] = FAO_Livestock_landuse['Value'][i] 
                    FAO_Livestock['% Grazing'][j] = FAO_Livestock_landuse['% Grazing'][i]
                    FAO_Livestock['% int Land'][j] = FAO_Livestock_landuse['% int Land'][i]
        
        if FAO_Livestock_landuse['Item'][i] == 'Mules':
            for j in FAO_Livestock.index:
                if FAO_Livestock['Area'][j] == FAO_Livestock_landuse['Area'][i] and FAO_Livestock['Item'][j] in ['Meat, mule']:
                    FAO_Livestock['Hd/Ha'][j] = FAO_Livestock_landuse['Value'][i] 
                    FAO_Livestock['% Grazing'][j] = FAO_Livestock_landuse['% Grazing'][i]
                    FAO_Livestock['% int Land'][j] = FAO_Livestock_landuse['% int Land'][i]
         
        if FAO_Livestock_landuse['Item'][i] == 'Pigs':
            for j in FAO_Livestock.index:
                if FAO_Livestock['Area'][j] == FAO_Livestock_landuse['Area'][i] and FAO_Livestock['Item'][j] in ['Meat, pig']:
                    FAO_Livestock['Hd/Ha'][j] = FAO_Livestock_landuse['Value'][i]  
                    FAO_Livestock['% Grazing'][j] = FAO_Livestock_landuse['% Grazing'][i]
                    FAO_Livestock['% int Land'][j] = FAO_Livestock_landuse['% int Land'][i]
    
        if FAO_Livestock_landuse['Item'][i] == 'Sheep':
            for j in FAO_Livestock.index:
                if FAO_Livestock['Area'][j] == FAO_Livestock_landuse['Area'][i] and FAO_Livestock['Item'][j] in ['Meat, sheep', 'Milk, whole fresh sheep']:
                    FAO_Livestock['Hd/Ha'][j] = FAO_Livestock_landuse['Value'][i]  
                    FAO_Livestock['% Grazing'][j] = FAO_Livestock_landuse['% Grazing'][i]
                    FAO_Livestock['% int Land'][j] = FAO_Livestock_landuse['% int Land'][i]
         
    FAO_Livestock.dropna(subset = ['% Grazing'])
    FAO_Livestock = FAO_Livestock.reset_index(drop = True)
    
    
    
    
    for i in FAO_Livestock.index:
        if isinstance(FAO_Livestock['Hd/Ha'][i], float) == False:
            FAO_Livestock = FAO_Livestock.drop([i])
        elif isinstance(FAO_Livestock['% Grazing'][i], str) == True:
            FAO_Livestock = FAO_Livestock.drop([i])
    FAO_Livestock = FAO_Livestock.reset_index(drop = True)
    
        
    FAO_Livestock['% Mixed'] = 1 - FAO_Livestock['% Grazing'] - FAO_Livestock['% int Land']
    
    FAO_Livestock["Area (Prod/Ha)"] = FAO_Livestock["Hd/Ha"]*FAO_Livestock["Prod/Hd"]
    FAO_Livestock["Area (Ha/Hd) int"] = FAO_Livestock['Area']
    

    
    FAO_Livestock ['feed group'] = FAO_Livestock ['group']
    FAO_Livestock.loc[FAO_Livestock['Item Code'].isin(beef_items), "group"] = "beef"
    FAO_Livestock.loc[FAO_Livestock['Item Code'].isin(beef_milk_items), "group"] = "beef milk"
    FAO_Livestock.loc[FAO_Livestock['Item Code'].isin(lamb_items), "group"] = "lamb"
    FAO_Livestock.loc[FAO_Livestock['Item Code'].isin(lamb_milk_items), "group"] = "lamb milk"
    
    FAO_Livestock.loc[FAO_Livestock['feed group'].isin(['eggs', 'chicken and other poultry', 'pork']), '% Mixed'] = 0
    
    FAO_Livestock.loc[FAO_Livestock.group == 'eggs', "Area (Ha/Hd) int"] = 0.0000056
    FAO_Livestock.loc[FAO_Livestock.group == 'chicken and other poultry', "Area (Ha/Hd) int"] = 0.0000056
    FAO_Livestock.loc[FAO_Livestock.group == 'beef', "Area (Ha/Hd) int"] = 0.0045
    FAO_Livestock.loc[FAO_Livestock.group == 'beef milk', "Area (Ha/Hd) int"] = 0.0045
    FAO_Livestock.loc[FAO_Livestock.group == 'lamb', "Area (Ha/Hd) int"] = 0.00037
    FAO_Livestock.loc[FAO_Livestock.group == 'lamb milk', "Area (Ha/Hd) int"] = 0.00037
    #FAO_Livestock.loc[FAO_Livestock.group == 'whole milk or derivative equivalents', "Area (Ha/Hd) int"] = 0.0045
    FAO_Livestock.loc[FAO_Livestock.group == 'pork', "Area (Ha/Hd) int"] = 0.001
    FAO_Livestock.loc[FAO_Livestock.group == 'other', "Area (Ha/Hd) int"] = 0.0001
    
    FAO_Livestock = pd.merge(FAO_Livestock, POM_data[['Area','Item', 'POM Org (with waste & feed)', 'POM EAT (with waste & feed)', 'Population (2016), 1000person', 'POM', 'EAT_group', '% Protein']], on = ["Area", "Item"], how = 'left')
    FAO_Livestock = FAO_Livestock.dropna(subset = ["Prod/Hd", "Hd/Ha"])
    
    
    FAO_Livestock['Prod_P/Hd'] = FAO_Livestock['Prod/Hd']*(FAO_Livestock['% Protein']/100)
    FAO_Livestock['Prod_P/Hd Org'] = FAO_Livestock['Prod/Hd Org']*(FAO_Livestock['% Protein']/100)
    
    FAO_Livestock["1000T P Org int"] = FAO_Livestock["POM Org (with waste & feed)"]*(FAO_Livestock["% Protein"]/100)*(FAO_Livestock['% int Land']+FAO_Livestock['% Mixed'])
    FAO_Livestock["1000T P EAT int"] = FAO_Livestock["POM EAT (with waste & feed)"]*(FAO_Livestock["% Protein"]/100)*(FAO_Livestock['% int Land']+FAO_Livestock['% Mixed'])
    
    FAO_Livestock["1000T P Org ext"] = FAO_Livestock["POM Org (with waste & feed)"]*(FAO_Livestock["% Protein"]/100)*(FAO_Livestock['% Grazing'])
    FAO_Livestock["1000T P EAT ext"] = FAO_Livestock["POM EAT (with waste & feed)"]*(FAO_Livestock["% Protein"]/100)*(FAO_Livestock['% Grazing'])
    
    FAO_Livestock['POM Org Area (Ha) int'] = FAO_Livestock["1000T P Org int"]/FAO_Livestock['Prod_P/Hd Org']*FAO_Livestock['Area (Ha/Hd) int']
    FAO_Livestock['POM EAT Area (Ha) int'] = FAO_Livestock["1000T P EAT int"]/FAO_Livestock['Prod_P/Hd']*FAO_Livestock['Area (Ha/Hd) int']
    
    FAO_Livestock['POM Org Area (Ha) ext'] = FAO_Livestock["1000T P Org ext"]/FAO_Livestock['Prod_P/Hd Org']/FAO_Livestock['Hd/Ha']
    FAO_Livestock['POM EAT Area (Ha) ext'] = FAO_Livestock["1000T P EAT ext"]/FAO_Livestock['Prod_P/Hd']/FAO_Livestock['Hd/Ha']
    
    
    FAO_Livestock.loc[FAO_Livestock['Hd/Ha'] == 0, ['POM Org Area (Ha) ext', 'POM EAT Area (Ha) ext']] = 0
    
    FAO_Livestock['POM Org Area (Ha)'] = FAO_Livestock["POM Org Area (Ha) int"] + FAO_Livestock["POM Org Area (Ha) ext"]
    FAO_Livestock['POM EAT Area (Ha)'] = FAO_Livestock["POM EAT Area (Ha) int"] + FAO_Livestock["POM EAT Area (Ha) ext"]
    
    FAO_Livestock['1000T P Org (Ha)'] = FAO_Livestock["1000T P Org int"]+ FAO_Livestock["1000T P Org ext"]
    FAO_Livestock['1000T P EAT (Ha)'] = FAO_Livestock["1000T P EAT int"]+ FAO_Livestock["1000T P EAT ext"]
    
    FAO_Livestock ['feed group'] = FAO_Livestock ['group']
    FAO_Livestock.loc[FAO_Livestock['Item Code'].isin(beef_items), "feed group"] = "beef"
    FAO_Livestock.loc[FAO_Livestock['Item Code'].isin(beef_milk_items), "feed group"] = "beef milk"
    FAO_Livestock.loc[FAO_Livestock['Item Code'].isin(lamb_items), "feed group"] = "lamb"
    FAO_Livestock.loc[FAO_Livestock['Item Code'].isin(lamb_milk_items), "feed group"] = "lamb milk"
    
    Meat_Area = pd.DataFrame() 
    Meat_Area ["Org"] = FAO_Livestock.groupby(["Area"]).apply(lambda x: x["POM Org Area (Ha)"].sum())
    Meat_Area ["EAT"] = FAO_Livestock.groupby(["Area"]).apply(lambda x: x["POM EAT Area (Ha)"].sum())
    
    Meat_Area_group = pd.DataFrame()
    Meat_Area_group ["EAT"] = FAO_Livestock.groupby(["Area", "group"]).apply(lambda x: x["POM EAT Area (Ha)"].sum())
    
    Meat_group = pd.DataFrame() 
    Meat_group ["Org"] = FAO_Livestock.groupby(["EAT_group"]).apply(lambda x: x["POM Org Area (Ha)"].sum())
    Meat_group ["EAT"] = FAO_Livestock.groupby(["EAT_group"]).apply(lambda x: x["POM EAT Area (Ha)"].sum())
    
    Meat_group = Meat_group.reset_index()
    
    return FAO_Livestock, Meat_Area, Meat_Area_group, Meat_group