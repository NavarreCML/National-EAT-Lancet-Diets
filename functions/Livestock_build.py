#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:25:39 2021

@author: nicolasnavarre
"""
import pandas as pd
from functions import fao_regions as regions

data = 'data/'

def livestock_pom(POM_data, FAO_animals, ls_proxie, diet_div_ls, diet_source_ls, FAO_pop):
    FAO_Livestock = pd.read_csv(data+"FAOSTAT_Livestock Production.csv")
    FAO_Livestock = FAO_Livestock.dropna(subset = ['Value'])
    FAO_Livestock.loc[FAO_Livestock.Area == "Cote d'Ivoire", "Area"] = "Côte d'Ivoire"
    FAO_Livestock.loc[FAO_Livestock.Area == "United Kingdom of Great Britain and Northern Ireland", "Area"] = "United Kingdom"
    FAO_Livestock ['group'] = FAO_Livestock.apply(lambda x: regions.group(x["Item Code"]), axis=1)
    FAO_Livestock.loc[FAO_Livestock.Unit == '1000 Head', 'Value'] *= 1000
    FAO_Livestock.loc[FAO_Livestock.Unit == '1000 Head', 'Unit'] = 'Head'
    
    FAO_Livestock_5 = pd.read_csv(data+"FAOSTAT_Livestock Production_5.csv")
    FAO_Livestock_5 = FAO_Livestock_5.dropna(subset = ['Value'])
    FAO_Livestock_5.loc[FAO_Livestock_5.Area == "Cote d'Ivoire", "Area"] = "Côte d'Ivoire"
    FAO_Livestock_5.loc[FAO_Livestock_5.Area == "United Kingdom of Great Britain and Northern Ireland", "Area"] = "United Kingdom"

    FAO_Livestock_5 ['group'] = FAO_Livestock_5.apply(lambda x: regions.group(x["Item Code (FAO)"]), axis=1)
    FAO_Livestock_5.loc[FAO_Livestock_5.Unit == '1000 Head', 'Value'] *= 1000
    FAO_Livestock_5.loc[FAO_Livestock_5.Unit == '1000 Head', 'Unit'] = 'Head'
    FAO_Livestock_5 = FAO_Livestock_5.groupby(['Area', 'Item']).mean().reset_index()

    FAO_Livestock = pd.merge(FAO_Livestock, FAO_Livestock_5[['Area', 'Item', 'Value']], on = ["Area", "Item"], how = 'left')
    FAO_Livestock['Value'] = FAO_Livestock['Value_y']
    FAO_Livestock = FAO_Livestock.drop(columns = ["Value_x", "Value_y"])

    
    FAO_Livestock = pd.merge(FAO_Livestock, FAO_animals[['Area', 'Item', 'Production', 'Unit']], on = ["Area", "Item"], how = 'left')
    FAO_Livestock = FAO_Livestock.dropna(subset = ['Production'])
    
    extra_nations = ['Puerto Rico', 'Palestine', 'Greenland', 'Falkland Islands (Malvinas)'\
                     'New Caledonia', 'China', 'China, Taiwan Province of' ]
    FAO_Livestock = FAO_Livestock[~FAO_Livestock['Area'].isin(extra_nations)]
    
    FAO_pop = FAO_pop.set_index("Area")
    

    if ls_proxie == True:
        for i,j in zip (diet_div_ls, diet_source_ls): 
            fao_fix = FAO_Livestock.loc[FAO_Livestock.Area == j]
            fao_fix['Area'] = i

            factor = FAO_pop['Value'][i] / FAO_pop['Value'][j]
            fao_fix['Value'] *= factor
            fao_fix['Production'] *= factor
            
            FAO_Livestock = FAO_Livestock[FAO_Livestock.Area != i]
            FAO_Livestock = pd.concat([FAO_Livestock,fao_fix])
    
    FAO_Livestock = FAO_Livestock.reset_index()
    
    
    FAO_Livestock["Prod/Hd"] = FAO_Livestock["Production"] / FAO_Livestock["Value"]
    
    FAO_Livestock = pd.merge(FAO_Livestock, POM_data[["Area", "Item", "GROUP"]], on = ["Area", "Item"], how = 'inner')
    FAO_Livestock['Prod/Hd Org'] = FAO_Livestock['Prod/Hd']
    
    return FAO_Livestock

def feed_demand(POM_data, FAO_Livestock, change_livestock_yields, livestock_standard, livestock_regions, livestock_countries):
    #adjust yields
    if change_livestock_yields == True:
        
        yield_avg = pd.DataFrame()
        yield_avg ["avg yield"] = FAO_Livestock.groupby(["Item", "GROUP"]).apply(lambda x: x["Prod/Hd"].mean())
        yield_avg = yield_avg.reset_index(level = ["Item", "GROUP"])


        yield_sub = yield_avg.loc[(yield_avg.GROUP == livestock_standard)]
        for j in yield_sub.index:
            for region_name in livestock_regions:
                for i in FAO_Livestock.loc[(FAO_Livestock.GROUP == region_name) & (FAO_Livestock.Item == yield_sub.Item[j])].index:
                    if yield_sub['avg yield'][j] > FAO_Livestock['Prod/Hd'][i]:
                        FAO_Livestock['Prod/Hd'][i] = yield_sub['avg yield'][j]
       
            for c_name in livestock_countries:
                for i in FAO_Livestock.loc[(FAO_Livestock.Area == c_name) & (FAO_Livestock.Item == yield_sub.Item[j])].index:
                    if yield_sub['avg yield'][j] > FAO_Livestock['Prod/Hd'][i]:
                        FAO_Livestock['Prod/Hd'][i] = yield_sub['avg yield'][j]
    
    FAO_Livestock['Value'] =  FAO_Livestock["Production"] / FAO_Livestock["Prod/Hd"]
    FAO_Livestock['Value Org'] =  FAO_Livestock["Production"] / FAO_Livestock["Prod/Hd Org"]
    FAO_Livestock = FAO_Livestock.drop(columns = ["Domain Code", "Domain", "Area Code", "Year Code", "Year", "Flag", "Flag Description"])
    

    POM_temp_feed = POM_data
    feed_list = ['grass', 'Maize', 'Soybeans', 'Wheat', 'Rapeseed', 'Oats', 'Peas, dry', 'Barley']
    feed_codes = [0, 56, 236, 15, 270, 75, 187, 44]
    feed_group_nf = ['rice wheat corn and other', 'rice wheat corn and other', 'soy foods', 'rice wheat corn and other', 'unsaturated oils', 'rice wheat corn and other', 'dry beans lentils and peas','rice wheat corn and other']
    feed_group = ['rice wheat corn and other', 'rice wheat corn and other', 'soy foods', 'rice wheat corn and other', 'unsaturated oils', 'rice wheat corn and other', 'dry beans lentils and peas', 'rice wheat corn and other']
    feed_group_eat = ['whole grains', 'whole grains','legumes', 'whole grains', 'added fats','whole grains', 'legumes', 'whole grains']
    for j in POM_data.Area.unique().tolist():
        for (i,z,a,b,c) in zip(feed_list, feed_codes, feed_group_nf, feed_group, feed_group_eat):
            if len(POM_data.loc[(POM_data['Area'] == j) & (POM_data['Item'] == i)]) == 0:
                temp_i = POM_data.loc[(POM_data['Area'] == j)]
                for k in temp_i.iterrows():
                    k = k[1]
                    for set_zero in k.index:
                        if set_zero == 'Area':
                            k[set_zero] = j
                        elif set_zero == 'Item':
                            k[set_zero] = i
                        elif set_zero == 'Item Code':
                            k[set_zero] = z
                        elif set_zero == 'group_nf':
                            k[set_zero] = a
                        elif set_zero == 'group':
                            k[set_zero] = b
                        elif set_zero == 'EAT_group':
                            k[set_zero] = c
                        elif set_zero in ['Population (2016), 1000person', 'GROUP', 'IMAGEGROUP', 'REGION']:
                            continue
                        else:
                            k[set_zero] = 0 
                    break
                POM_temp_feed = POM_temp_feed.append(k, ignore_index = True)
                
    POM_temp_feed.dropna(subset = ["Population (2016), 1000person"])
    POM_data = POM_temp_feed
    
    POM_test = POM_data
    POM_test = pd.merge(POM_test, FAO_Livestock[['Area', 'Item','Prod/Hd', 'Prod/Hd Org']], on = ['Area', 'Item'], how = 'left')
    POM_test['EAT (waste) hd'] =  POM_test['EAT POM (with waste)'] / POM_test['Prod/Hd'] 
    POM_test['Org (waste) hd'] =  POM_test['POM with waste'] / POM_test['Prod/Hd Org']
    POM_test ['feed group'] = POM_test ['group_nf']
    
    beef_items = [1108, 947, 1127, 867, 1097, 1158, 1111, 1166]
    beef_milk_items = [951, 1130, 882]
    lamb_items = [1163, 1017, 977]
    lamb_milk_items = [1020, 982]
    
    POM_test.loc[POM_test['Item Code'].isin(beef_items), "feed group"] = "beef"
    POM_test.loc[POM_test['Item Code'].isin(beef_milk_items), "feed group"] = "beef milk"
    POM_test.loc[POM_test['Item Code'].isin(lamb_items), "feed group"] = "lamb"
    POM_test.loc[POM_test['Item Code'].isin(lamb_milk_items), "feed group"] = "lamb milk"
    
    Animal_sys = pd.read_csv(data+"GLEAM_Data_csv.csv", sep = ";", header = 1, encoding='latin-1')
    Animal_sys.loc[Animal_sys['Animal species'] == 'Buffaloes', 'Animal species'] = 'Cattle'
    Animal_sys.loc[Animal_sys['Animal species'] == 'Sheep', 'Animal species'] = 'Goats'
    Animal_sys.loc[Animal_sys['Animal species'] == 'Chicken', 'Animal species'] = 'Chickens'
    Animal_sys.loc[Animal_sys['Commodity'] == 'Eggs', 'Animal species'] = 'eggs'
    Animal_sys.loc[(Animal_sys['Animal species'] == 'Cattle') & (Animal_sys['Commodity'] == 'Milk'), 'Animal species'] = 'beef milk'
    Animal_sys.loc[(Animal_sys['Animal species'] == 'Goats') & (Animal_sys['Commodity'] == 'Milk'), 'Animal species'] = 'lamb milk'
    
    Animal_sys = Animal_sys[["Region", "Animal species", "Production system", "Commodity", "kg protein"]]
    Animal_sys["kg protein"] = pd.to_numeric(Animal_sys["kg protein"], errors = "coerce")
    Animal_sys.dropna(subset = ["kg protein"], inplace = True)
    Animal_sys = Animal_sys.drop(Animal_sys[(Animal_sys['Production system'] == 'Aggregated') | (Animal_sys['Commodity'] == 'Aggregated')].index)
    Animal_sys = Animal_sys.reset_index(drop = True)
    
    feed_systems = ['Feedlots', 'Broilers', 'Industrial systems', 'Intermediate systems', 'Layers', 'Backyard systems', 'Mixed systems']#, 'Mixed systems'] assume mixed systems eat food waste.
    area_systems = ['Feedlots', 'Broilers', 'Industrial systems', 'Intermediate systems', 'Layers', 'Backyard systems']
    
    Percent_sys = pd.DataFrame()
    Percent_sys ["% of Sys"] = Animal_sys.groupby(["Region", "Animal species"]).apply(lambda x: x["kg protein"]/x["kg protein"].sum())
    Percent_sys = Percent_sys.reset_index(level = ["Region", "Animal species"])
    
    Animal_sys ["% of Sys"] = Percent_sys ["% of Sys"]
    
    Area_sys = Animal_sys
    Int_area = Animal_sys
    
    Area_sys = Area_sys[Area_sys['Production system'].isin(['Grassland systems'])]
    Animal_sys = Animal_sys[Animal_sys['Production system'].isin(feed_systems)]
    Int_area = Int_area[Int_area['Production system'].isin(area_systems)]
    
    Sum_area = pd.DataFrame()
    Sum_area['% feed'] = Area_sys.groupby(['Region','Animal species']).apply(lambda x: x['% of Sys'].sum())
    Sum_area = Sum_area.reset_index(level = ["Region", "Animal species"])
    
    Sum_species = pd.DataFrame()
    Temp_species = Animal_sys
    
    #Remove 20% from pig backyard systems feed demand and 40% for chickens and eggs. 
    Temp_species.loc[(Temp_species['Production system'] == 'Backyard systems') & (Temp_species['Animal species'] == 'Pigs'), '% of Sys'] *= 0.8
    Temp_species.loc[(Temp_species['Production system'] == 'Backyard systems') & (Temp_species['Animal species'] == 'Chickens'), '% of Sys'] *= 0.6
    Temp_species.loc[(Temp_species['Production system'] == 'Backyard systems') & (Temp_species['Animal species'] == 'eggs'), '% of Sys'] *= 0.6
    
    Sum_species['% feed'] = Temp_species.groupby(['Region','Animal species']).apply(lambda x: x['% of Sys'].sum())
    Sum_species = Sum_species.reset_index(level = ["Region", "Animal species"])
    
    Sum_area_int = pd.DataFrame()
    Sum_area_int['% feed'] = Int_area.groupby(['Region','Animal species']).apply(lambda x: x['% of Sys'].sum())
    Sum_area_int = Sum_area_int.reset_index(level = ["Region", "Animal species"])
    
    Sum_area = pd.merge(Sum_area, Sum_area_int[['Region', 'Animal species', '% feed']], on = ['Region', 'Animal species'], how = 'outer')
    Sum_area = Sum_area.rename(columns = {'% feed_x' : '% Grazing'})
    Sum_area = Sum_area.rename(columns = {'% feed_y' : '% int Land'})
    Sum_area = Sum_area.fillna(0)
    
    Sum_species = pd.merge(Sum_species, Sum_area[["Region", "Animal species", "% Grazing"]], on =["Region", "Animal species"], how ='left')
    Sum_species['% feed'] = 1 - Sum_species['% Grazing']
    
    Sum_species = Sum_species.drop(Sum_species[(Sum_species['Animal species'] == 'Buffaloes') | (Sum_species['Animal species'] == 'Sheep')].index)
    Sum_species.loc[Sum_species['Animal species'] == 'Cattle', 'Animal species'] = 'beef'
    Sum_species.loc[Sum_species['Animal species'] == 'Pigs', 'Animal species'] = 'pork'
    Sum_species.loc[Sum_species['Animal species'] == 'Goats', 'Animal species'] = 'lamb'
    Sum_species.loc[Sum_species['Animal species'] == 'Chickens', 'Animal species'] = 'chicken and other poultry'
    

    for i in POM_test.index:
        if POM_test['IMAGEGROUP'][i] == 'Brazil':
            POM_test['IMAGEGROUP'][i] = 'Latin America and the Caribbean'
        elif POM_test['IMAGEGROUP'][i] == 'Canada':
            POM_test['IMAGEGROUP'][i] = 'North America'
        elif POM_test['IMAGEGROUP'][i] == 'Central America':
            POM_test['IMAGEGROUP'][i] = 'Latin America and the Caribbean'
        elif POM_test['IMAGEGROUP'][i] == 'Central Asia':
            POM_test['IMAGEGROUP'][i] = 'Near East and North Africa'
        elif POM_test['IMAGEGROUP'][i] == 'China':
            POM_test['IMAGEGROUP'][i] = 'East Asia and Southeast Asia'
        elif POM_test['IMAGEGROUP'][i] == 'East Africa':
            POM_test['IMAGEGROUP'][i] = 'Sub-Saharan Africa'        
        elif POM_test['IMAGEGROUP'][i] == 'India':
            POM_test['IMAGEGROUP'][i] = 'South Asia'
        elif POM_test['IMAGEGROUP'][i] == 'Indonesia':
            POM_test['IMAGEGROUP'][i] = 'East Asia and Southeast Asia'
        elif POM_test['IMAGEGROUP'][i] == 'Japan':
            POM_test['IMAGEGROUP'][i] = 'East Asia and Southeast Asia'
        elif POM_test['IMAGEGROUP'][i] == 'Korea':
            POM_test['IMAGEGROUP'][i] = 'East Asia and Southeast Asia'
        elif POM_test['IMAGEGROUP'][i] == 'Mexico':
            POM_test['IMAGEGROUP'][i] = 'Latin America and the Caribbean'
        elif POM_test['IMAGEGROUP'][i] == 'Middle East':
            POM_test['IMAGEGROUP'][i] = 'Near East and North Africa'
        elif POM_test['IMAGEGROUP'][i] == 'North Africa':
            POM_test['IMAGEGROUP'][i] = 'Near East and North Africa'
        elif POM_test['IMAGEGROUP'][i] == 'Other':
            POM_test['IMAGEGROUP'][i] = 'East Asia and Southeast Asia'
        elif POM_test['IMAGEGROUP'][i] == 'South Africa':
            POM_test['IMAGEGROUP'][i] = 'Sub-Saharan Africa' 
        elif POM_test['IMAGEGROUP'][i] == 'South America':
            POM_test['IMAGEGROUP'][i] = 'Latin America and the Caribbean'
        elif POM_test['IMAGEGROUP'][i] == 'South East Asia':
            POM_test['IMAGEGROUP'][i] = 'East Asia and Southeast Asia'
        elif POM_test['IMAGEGROUP'][i] == 'Southern Africa':
            POM_test['IMAGEGROUP'][i] = 'Sub-Saharan Africa' 
        elif POM_test['IMAGEGROUP'][i] == 'Turkey':
            POM_test['IMAGEGROUP'][i] = 'Near East and North Africa' 
        elif POM_test['IMAGEGROUP'][i] == 'USA':
            POM_test['IMAGEGROUP'][i] = 'North America'     
        elif POM_test['IMAGEGROUP'][i] == 'Ukraine':
            POM_test['IMAGEGROUP'][i] = 'Eastern Europe' 
        elif POM_test['IMAGEGROUP'][i] == 'West Africa':
            POM_test['IMAGEGROUP'][i] = 'Sub-Saharan Africa'
        elif POM_test['IMAGEGROUP'][i] == 'Russia':
            POM_test['IMAGEGROUP'][i] = 'Russian Federation'
        elif POM_test['IMAGEGROUP'][i] == 'China, mainland':
            POM_test['IMAGEGROUP'][i] = 'East Asia and Southeast Asia'
               
    Org_food_hd = POM_test.groupby(["Area", "feed group", 'IMAGEGROUP']).apply(lambda x: x["Org (waste) hd"].sum())
    Org_food_hd = Org_food_hd.reset_index(level = ["Area", "feed group", 'IMAGEGROUP'])
    Org_food_hd = Org_food_hd.rename(columns = {0: "hds"})
    Org_food_hd["GROUP"] = Org_food_hd["hds"] 
    
    EAT_food_hd = POM_test.groupby(["Area", "feed group", 'IMAGEGROUP']).apply(lambda x: x["EAT (waste) hd"].sum())
    EAT_food_hd = EAT_food_hd.reset_index(level = ["Area", "feed group", 'IMAGEGROUP'])
    EAT_food_hd = EAT_food_hd.rename(columns = {0: "hds"})
    EAT_food_hd["GROUP"] = EAT_food_hd["hds"]
    
    for j in Sum_species.index:
        Org_food_hd.loc[(Org_food_hd['IMAGEGROUP'] == Sum_species['Region'][j]) & (Org_food_hd['feed group'] == Sum_species['Animal species'][j]), ['hds']] *= Sum_species['% feed'][j]
        EAT_food_hd.loc[(Org_food_hd['IMAGEGROUP'] == Sum_species['Region'][j]) & (EAT_food_hd['feed group'] == Sum_species['Animal species'][j]), ['hds']] *= Sum_species['% feed'][j]
    
    
    
    FAO_LSU_Coeffs = pd.read_csv(r'data/LSU_Coeffs_by_Country.csv', encoding='latin-1')
    FAO_LSU_Coeffs['IMAGEGROUP'] = FAO_LSU_Coeffs['ItemName']
    
    #POM_protein_feed = pd.DataFrame(columns = protein_columns)
    Temp_LSU_Coeffs = pd.DataFrame(columns = FAO_LSU_Coeffs.columns.tolist() )
    
    
    FAO_LSU_Coeffs.loc[FAO_LSU_Coeffs.Value == 0, 'Hd/Ha (max)'] = 0
    FAO_LSU_Coeffs.loc[FAO_LSU_Coeffs.Value != 0, 'Hd/Ha (max)'] = 10/FAO_LSU_Coeffs.Value
    
    
    for j in POM_test.Area.unique().tolist():
        FAO_LSU_Coeffs.loc[(FAO_LSU_Coeffs["AreaName"] == j), ["IMAGEGROUP"]] = POM_test.loc[POM_test.Area == j, ["IMAGEGROUP"]]["IMAGEGROUP"].unique()[0]
    
    for i in FAO_LSU_Coeffs.index:
        if FAO_LSU_Coeffs['IMAGEGROUP'][i] == FAO_LSU_Coeffs['ItemName'][i]:
            FAO_LSU_Coeffs = FAO_LSU_Coeffs.drop([i])
    FAO_LSU_Coeffs = FAO_LSU_Coeffs.reset_index(drop = True)
    
    
    count_new = 0
    for i in range(len(FAO_LSU_Coeffs)):
        if FAO_LSU_Coeffs['ItemName'][i] == 'Cattle':      
            Temp_LSU_Coeffs.loc[count_new] = FAO_LSU_Coeffs.loc[i]
            Temp_LSU_Coeffs['ItemName'][count_new] = 'beef milk'
            count_new += 1
            
        elif FAO_LSU_Coeffs['ItemName'][i] == 'Goats':
            Temp_LSU_Coeffs.loc[count_new] = FAO_LSU_Coeffs.loc[i]
            Temp_LSU_Coeffs['ItemName'][count_new] = 'lamb milk'
            count_new += 1
    
    FAO_LSU_Coeffs = pd.concat([FAO_LSU_Coeffs, Temp_LSU_Coeffs])
    FAO_LSU_Coeffs['% Grazing'] = FAO_LSU_Coeffs['IMAGEGROUP']
    FAO_LSU_Coeffs['% int Land'] = FAO_LSU_Coeffs['IMAGEGROUP']
    
    
    for i in Sum_area.index:
        FAO_LSU_Coeffs.loc[(FAO_LSU_Coeffs['IMAGEGROUP'] == Sum_area['Region'][i]) & (FAO_LSU_Coeffs['ItemName'] == Sum_area['Animal species'][i]), ['% Grazing']] = Sum_area['% Grazing'][i]
        FAO_LSU_Coeffs.loc[(FAO_LSU_Coeffs['IMAGEGROUP'] == Sum_area['Region'][i]) & (FAO_LSU_Coeffs['ItemName'] == Sum_area['Animal species'][i]), ['% int Land']] = Sum_area['% int Land'][i]
    
    FAO_LSU_Coeffs['Hd/Ha (max)'] = 10/FAO_LSU_Coeffs.Value
    FAO_LSU_Coeffs.loc[FAO_LSU_Coeffs.Value == 0, 'Hd/Ha (max)'] = 0
    
    for i in FAO_LSU_Coeffs.index:
        if isinstance(FAO_LSU_Coeffs['% Grazing'][i],str) == True:
            FAO_LSU_Coeffs = FAO_LSU_Coeffs.drop([i])
        elif isinstance(FAO_LSU_Coeffs['% int Land'][i],str) == True:
            FAO_LSU_Coeffs = FAO_LSU_Coeffs.drop([i])
    FAO_LSU_Coeffs = FAO_LSU_Coeffs.reset_index(drop = True)
    
    for i in FAO_LSU_Coeffs.index:
        if FAO_LSU_Coeffs['IMAGEGROUP'][i] == FAO_LSU_Coeffs['% Grazing'][i]:
            FAO_LSU_Coeffs = FAO_LSU_Coeffs.drop([i])
    
    FAO_LSU_Coeffs = FAO_LSU_Coeffs.reset_index(drop = True)
    
    
    food_hd = pd.DataFrame()
    food_hd = EAT_food_hd
    food_hd ["Org hds"] = Org_food_hd ["hds"]
    food_hd = food_hd.rename(columns = {'hds' : "EAT hds"})
    
    
    
    dairy_cow_dict = {"type": ["grass", "Maize", "Soybeans", "Barley", "Rapeseed"], ##"citrus pulp concentrate", "palm kernel meal concentrate", "rapeseed meal concentrate", "beet pulp concentrate", "wheat concentrate", "rest products"],
                   "gram": [41250, (13750 + (1250*0.86))*0.65, (750*0.8)*0.65, 250, 500]}##, 500, 500, 500, 250, 250, 1000]}
    dairy_cow_Lancet_diet_per_day = pd.DataFrame(dairy_cow_dict)
    dairy_cow_Lancet_diet_per_day = dairy_cow_Lancet_diet_per_day.set_index(["type"])
    dairy_cow_feed_per_hd = dairy_cow_Lancet_diet_per_day*365/(10**9)
    
    cow_dict = {"type": ["grass", "Maize", "Soybeans", "Barley"], ##"citrus pulp concentrate", "palm kernel meal concentrate", "rapeseed meal concentrate", "beet pulp concentrate", "wheat concentrate", "rest products"],
                   "gram": [0, 3550, (2720*0.8)*0.65, 15900]}##, 500, 500, 500, 250, 250, 1000]}
    cow_Lancet_diet_per_day = pd.DataFrame(cow_dict)
    cow_Lancet_diet_per_day = cow_Lancet_diet_per_day.set_index(["type"])
    cow_feed_per_hd = cow_Lancet_diet_per_day*365/(10**9)
    
    chicken_dict = {"type": ["Wheat", "Soybeans", "Rapeseed", "Oats", "Peas, dry"], ##"other"],
                   "gram": [(45.95)*0.65, (21.62*0.8)*0.65, 4.04*0.65, (23.15)*0.65, 9.7*0.65]} ##, 16.84]}
    chicken_Lancet_diet_per_day = pd.DataFrame(chicken_dict)
    chicken_Lancet_diet_per_day = chicken_Lancet_diet_per_day.set_index(["type"]) 
    chicken_feed_per_hd = chicken_Lancet_diet_per_day*365/(10**9)
    
    lamb_dict = {"type": ["grass", "Maize", "Soybeans", "Barley", "Rapeseed"], ##"citrus pulp concentrate", "palm kernel meal concentrate", "rapeseed meal concentrate", "beet pulp concentrate", "wheat concentrate", "rest products"],
                   "gram": [41250, (13750 + (1250*0.86))*0.65, (750*0.8)*0.65, 250, 500]} ##, 8.33, 8.33, 8.33, 4.15, 4.15, 16.66]}
    
    import numpy as np
    temp = np.array(lamb_dict['gram'])
    temp *= 900/60000
    
    lamb_dict['gram'] = temp

    
    
    lamb_Lancet_diet_per_day = pd.DataFrame(lamb_dict)
    lamb_Lancet_diet_per_day = lamb_Lancet_diet_per_day.set_index(["type"])
    lamb_feed_per_hd = lamb_Lancet_diet_per_day*365/(10**9)
    
    pig_dict = {"type": ["Maize", "Barley", "Wheat"], ##"swill", "molasses"],
                        "gram": [378.54*0.65, (525.75 + 147.21)*0.65, 630.9*0.65]} ##, 210.3, 210.3]}
    pig_Lancet_diet_per_day = pd.DataFrame(pig_dict)
    pig_Lancet_diet_per_day = pig_Lancet_diet_per_day.set_index(["type"])
    pig_feed_per_hd = pig_Lancet_diet_per_day*365/(10**9)
    
    POM_feed = POM_test[['Area', 'Item', 'feed group', 'IMAGEGROUP']]
    POM_feed['for feed EAT'] = 0
    POM_feed['for feed Org'] = 0
    
    
    protein_columns = ['Area', 'group'] + feed_list #+ ['grass']
    POM_protein_feed = pd.DataFrame(columns = protein_columns)
    #POM_protein_feed['Area'] = 0     
    #POM_protein_feed['group'] = 0 
    #POM_protein_feed['grass'] = 0 
    global_beef_milk_in = {}
    from collections import defaultdict
    feed_dict = defaultdict(list)
    feed_detail = pd.DataFrame(columns = ['Area', 'grass', "Maize", "Soybeans", "Barley", "Rapeseed"])
    feed_lamb = pd.DataFrame(columns = ['Area', 'grass', "Maize", "Soybeans", "Barley", "Rapeseed"])

  
    
    EAT_food_hd['Net'] = EAT_food_hd['hds']- EAT_food_hd['Org hds']
    
    count_p = 0 
    for i,z in zip(EAT_food_hd.index, Org_food_hd.index):
        if EAT_food_hd['hds'][i] > 0:
            if EAT_food_hd['feed group'][i] == 'beef':
                POM_protein_feed.loc[count_p] = 0
                for j in cow_feed_per_hd.index:
                    POM_feed.loc[(POM_feed['Area'] == EAT_food_hd["Area"][i]) & (POM_feed["Item"] == j), ['for feed EAT']] += cow_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                    feed_dict[EAT_food_hd["Area"][i]].append(cow_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i])
                    
                    POM_protein_feed['Area'][count_p] = EAT_food_hd["Area"][i]
                    POM_protein_feed['group'][count_p] = EAT_food_hd['feed group'][i]
                    POM_protein_feed[j][count_p] = cow_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                    
                count_p += 1

            if EAT_food_hd['feed group'][i] == 'beef milk':
                POM_protein_feed.loc[count_p] = 0
                for j in dairy_cow_feed_per_hd.index:
                    POM_feed.loc[(POM_feed['Area'] == EAT_food_hd["Area"][i]) & (POM_feed["Item"] == j), ['for feed EAT']] += dairy_cow_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                    feed_dict[EAT_food_hd["Area"][i]].append(dairy_cow_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i])
                    
                    POM_protein_feed['Area'][count_p] = EAT_food_hd["Area"][i]
                    POM_protein_feed['group'][count_p] = EAT_food_hd['feed group'][i]
                    POM_protein_feed[j][count_p] = dairy_cow_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                    if j not in global_beef_milk_in:
                        global_beef_milk_in[j] = 0
                    if j not in global_beef_milk_in:
                        global_beef_milk_in[j] = 0
                    
                    global_beef_milk_in[j] += dairy_cow_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                    feed_detail.loc[count_p, 'Area'] = EAT_food_hd["Area"][i]
                    feed_detail.loc[count_p, j] = dairy_cow_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                count_p += 1

            if EAT_food_hd['feed group'][i] == 'lamb milk':
                POM_protein_feed.loc[count_p] = 0
                for j in lamb_feed_per_hd.index:
                    POM_feed.loc[(POM_feed['Area'] == EAT_food_hd["Area"][i]) & (POM_feed["Item"] == j), ['for feed EAT']] += lamb_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                    feed_dict[EAT_food_hd["Area"][i]].append(lamb_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i])
    
                    POM_protein_feed['Area'][count_p] = EAT_food_hd["Area"][i]
                    POM_protein_feed['group'][count_p] = EAT_food_hd['feed group'][i]
                    POM_protein_feed[j][count_p] = lamb_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                    
                    feed_lamb.loc[count_p, 'Area'] = EAT_food_hd["Area"][i]
                    feed_lamb.loc[count_p, j] = lamb_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                    
                count_p += 1                   

            if EAT_food_hd['feed group'][i] == 'lamb':
                POM_protein_feed.loc[count_p] = 0
                for j in lamb_feed_per_hd.index:
                    POM_feed.loc[(POM_feed['Area'] == EAT_food_hd["Area"][i]) & (POM_feed["Item"] == j), ['for feed EAT']] += lamb_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                    feed_dict[EAT_food_hd["Area"][i]].append(lamb_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i])
    
                    POM_protein_feed['Area'][count_p] = EAT_food_hd["Area"][i]
                    POM_protein_feed['group'][count_p] = EAT_food_hd['feed group'][i]
                    POM_protein_feed[j][count_p] = lamb_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                count_p += 1
                
            if EAT_food_hd['feed group'][i] == 'pork':
                POM_protein_feed.loc[count_p] = 0
                for j in pig_feed_per_hd.index:
                    POM_feed.loc[(POM_feed['Area'] == EAT_food_hd["Area"][i]) & (POM_feed["Item"] == j), ['for feed EAT']] += pig_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                    feed_dict[EAT_food_hd["Area"][i]].append(pig_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i])
                    
                    POM_protein_feed['Area'][count_p] = EAT_food_hd["Area"][i]
                    POM_protein_feed['group'][count_p] = EAT_food_hd['feed group'][i]
                    POM_protein_feed[j][count_p] = pig_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                count_p += 1         

            if EAT_food_hd['feed group'][i] in ['eggs', 'chicken and other poultry']:
                POM_protein_feed.loc[count_p] = 0
                for j in chicken_feed_per_hd.index:
                    POM_feed.loc[(POM_feed['Area'] == EAT_food_hd["Area"][i]) & (POM_feed["Item"] == j), ['for feed EAT']] += chicken_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                    feed_dict[EAT_food_hd["Area"][i]].append(chicken_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i])
                    
                    POM_protein_feed['Area'][count_p] = EAT_food_hd["Area"][i]
                    POM_protein_feed['group'][count_p] = EAT_food_hd['feed group'][i]
                    POM_protein_feed[j][count_p] = chicken_feed_per_hd['gram'][j]*EAT_food_hd['hds'][i]
                count_p += 1
    
            if Org_food_hd['feed group'][i] == 'beef':
                for j in cow_feed_per_hd.index:
                    POM_feed.loc[(POM_feed['Area'] == Org_food_hd["Area"][i]) & (POM_feed["Item"] == j), ['for feed Org']] += cow_feed_per_hd['gram'][j]*Org_food_hd['hds'][i]
    
            if Org_food_hd['feed group'][i] == 'beef milk':
                for j in cow_feed_per_hd.index:
                    POM_feed.loc[(POM_feed['Area'] == Org_food_hd["Area"][i]) & (POM_feed["Item"] == j), ['for feed Org']] += cow_feed_per_hd['gram'][j]*Org_food_hd['hds'][i]
                            
            if Org_food_hd['feed group'][i] == 'lamb milk':
                for j in lamb_feed_per_hd.index:
                    POM_feed.loc[(POM_feed['Area'] == Org_food_hd["Area"][i]) & (POM_feed["Item"] == j), ['for feed Org']] += lamb_feed_per_hd['gram'][j]*Org_food_hd['hds'][i]
                    
            if Org_food_hd['feed group'][i] == 'lamb':
                for j in lamb_feed_per_hd.index:
                    POM_feed.loc[(POM_feed['Area'] == Org_food_hd["Area"][i]) & (POM_feed["Item"] == j), ['for feed Org']] += lamb_feed_per_hd['gram'][j]*Org_food_hd['hds'][i]
                    
            if Org_food_hd['feed group'][i] == 'pork':
                for j in pig_feed_per_hd.index:
                    POM_feed.loc[(POM_feed['Area'] == Org_food_hd["Area"][i]) & (POM_feed["Item"] == j), ['for feed Org']] += pig_feed_per_hd['gram'][j]*Org_food_hd['hds'][i]
                            
            if Org_food_hd['feed group'][i] in ['eggs', 'chicken and other poultry']:
                for j in chicken_feed_per_hd.index:
                    POM_feed.loc[(POM_feed['Area'] == Org_food_hd["Area"][i]) & (POM_feed["Item"] == j), ['for feed Org']] += chicken_feed_per_hd['gram'][j]*Org_food_hd['hds'][i]
    
    """*** Add in the FEED fraction of food to the total data ***"""
    POM_data = pd.merge(POM_data, POM_feed[['Area', 'Item', 'for feed EAT', 'for feed Org']], on = ['Area', 'Item'], how = 'outer')
    
    
    POM_data["POM Org (with waste & feed)"] = POM_data["POM"] + POM_data["for feed Org"]
    POM_data["POM EAT (with waste & feed)"] = POM_data["EAT POM (with waste)"] + POM_data["for feed EAT"]
    
    POM_data["Org per Capita (with waste & feed)"] = (POM_data["POM Org (with waste & feed)"]*1000)/(POM_data["Population (2016), 1000person"]*365)
    POM_data["EAT per Capita (with waste & feed)"] = (POM_data["POM EAT (with waste & feed)"]*1000)/(POM_data["Population (2016), 1000person"]*365)
    POM_data = POM_data.fillna(0)
    
    return POM_data, FAO_LSU_Coeffs, beef_items, beef_milk_items, lamb_items,\
        lamb_milk_items, feed_list, POM_protein_feed, global_beef_milk_in, feed_dict, feed_detail, feed_lamb
    
    