#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 16:13:16 2021

@author: nicolasnavarre
"""
import pandas as pd
import math

data = 'data/'

def crop_yield(POM_data, fish_products, meat_products, feed_list, crop_proxie, diet_div_crop, diet_source_crop):
    POM_crop_data = POM_data[~POM_data.Item.isin(fish_products)]
    POM_crop_data = POM_crop_data[~POM_crop_data.group.isin(meat_products)]
    
    FAO_Crop_yield = pd.read_csv(data+"FAOSTAT_crop Yield.csv")
    FAO_Crop_yield.loc[FAO_Crop_yield.Area == "Cote d'Ivoire", "Area"] = "Côte d'Ivoire"
    FAO_Crop_yield.loc[FAO_Crop_yield.Area == "United Kingdom of Great Britain and Northern Ireland", "Area"] = "United Kingdom"

    FAO_Crop_yield["Value"] = FAO_Crop_yield["Value"] / 10000 / 1000 #convert to 1000 tons/ha
    FAO_Crop_yield["Unit"] = "1000 tons/ha"
    
    FAO_Crop_yield_5 = pd.read_csv(data+"FAOSTAT_crop Yield_5.csv")
    FAO_Crop_yield_5.loc[FAO_Crop_yield_5.Area == "Cote d'Ivoire", "Area"] = "Côte d'Ivoire"
    FAO_Crop_yield_5.loc[FAO_Crop_yield_5.Area == "United Kingdom of Great Britain and Northern Ireland", "Area"] = "United Kingdom"

    FAO_Crop_yield_5["Value"] = FAO_Crop_yield_5["Value"] / 10000 / 1000 #convert to 1000 tons/ha
    FAO_Crop_yield_5["Unit"] = "1000 tons/ha"
    FAO_Crop_yield_5 = FAO_Crop_yield_5.groupby(['Area', 'Item']).mean().reset_index()

    FAO_Crop_yield = pd.merge(FAO_Crop_yield, FAO_Crop_yield_5[['Area', 'Item', 'Value']], on = ["Area", "Item"], how = 'left')
    FAO_Crop_yield['Value'] = FAO_Crop_yield['Value_y']
    FAO_Crop_yield = FAO_Crop_yield.drop(columns = ["Value_x", "Value_y"])
    
    if crop_proxie == True:
        for i,j in zip (diet_div_crop, diet_source_crop): 
            fao_fix = FAO_Crop_yield.loc[FAO_Crop_yield.Area == j]
            fao_fix['Area'] = i

            FAO_Crop_yield = FAO_Crop_yield[FAO_Crop_yield.Area != i]
            FAO_Crop_yield = pd.concat([FAO_Crop_yield,fao_fix])
    
    FAO_Crops = pd.merge(FAO_Crop_yield, POM_data, on = ["Area", "Item"], how = "left")
    POM_data.loc[POM_data.Area == 'China, mainland', 'REGION'] = 'CHN'
    extra_nations = ['Puerto Rico', 'Palestine', 'Greenland', 'Falkland Islands (Malvinas)'\
                 'New Caledonia', 'China', 'China, Taiwan Province of' ]
    FAO_Crops = FAO_Crops[~FAO_Crops['Area'].isin(extra_nations)]

    
    
    FAO_Crops = FAO_Crops.reset_index()
    
    yield_avg = pd.DataFrame()
    yield_avg ["avg yield"] = FAO_Crops.groupby(["Item", "GROUP"]).apply(lambda x: x["Value"].mean())
    yield_avg = yield_avg.reset_index(level = ["Item", "GROUP"])
    yield_avg_feed = yield_avg[yield_avg.Item.isin(feed_list)]
    yield_avg_crop = yield_avg[~yield_avg.Item.isin(feed_list)]
    
    Feed_crops = POM_data[POM_data.Item.isin(feed_list)]
    FAO_Crops = pd.concat([FAO_Crops, Feed_crops]).drop_duplicates(subset=['Area', 'Item'], keep='first').reset_index(drop=True)
    FAO_Crops['Element'] = 'Yield'
    FAO_Crops['Unit_x'] = '1000 tons/ha'
    
    global_avg = yield_avg.groupby(['Item']).apply(lambda x: x['avg yield'].mean())
    global_avg = pd.DataFrame(global_avg)
    global_avg = global_avg.rename(columns = {0: "avg yield"})
    
    
    #Fill in missing values with the nation's imagegroup average
    for i in FAO_Crops.index:
        if math.isnan(FAO_Crops['Value'][i]) == True:
            for j in yield_avg.index:
                if FAO_Crops['Item'][i] == yield_avg['Item'][j] and FAO_Crops['GROUP'][i] == yield_avg['GROUP'][j]:
                    FAO_Crops['Value'][i] = yield_avg['avg yield'][j]
    for i in FAO_Crops.index:
        if math.isnan(FAO_Crops['Value'][i]) == True:
            if FAO_Crops['Item'][i] in feed_list:
                if FAO_Crops['Item'][i] == 'grass':
                    FAO_Crops['Value'][i] = (6800/0.17)/1000/1000
                else: 
                    FAO_Crops['Value'][i] = global_avg["avg yield"][str(FAO_Crops['Item'][i])]
        
    
    FAO_Crops = FAO_Crops.dropna(subset = ['for feed EAT'])
    FAO_Crops['Value Org'] = FAO_Crops['Value']
    
    global_avg = global_avg.reset_index(level = 'Item')
    global_avg_feed = global_avg[global_avg['Item'].isin(feed_list)]
    global_avg_crop = global_avg[~global_avg['Item'].isin(feed_list)]
    
    return FAO_Crops, FAO_Crop_yield, yield_avg_feed, yield_avg_crop, global_avg_feed, global_avg_crop


def crop_area(FAO_Crops, yield_avg_feed, change_feed_yields,regional_change_feed,feed_standard,feed_regions,\
              feed_countries,global_avg_feed,change_crop_yields,regional_change_crop,yield_avg_crop,crop_standard,\
                  cr_y_regions,cr_y_countries,global_avg_crop):
    
    if change_feed_yields == True:
        if regional_change_feed == True:
            yield_avg_feeds = yield_avg_feed.loc[(yield_avg_feed.GROUP == feed_standard)]
            for j in yield_avg_feeds.index:
                for region_name in feed_regions:
                    for i in FAO_Crops.loc[(FAO_Crops.GROUP == region_name) & (FAO_Crops.Item == yield_avg_feed.Item[j])].index:
                        if yield_avg_feed['avg yield'][j] > FAO_Crops.Value[i]:
                            FAO_Crops.Value[i] = yield_avg_feed['avg yield'][j]
                for c_name in feed_countries:
                    for i in FAO_Crops.loc[(FAO_Crops.Area == c_name) & (FAO_Crops.Item == yield_avg_feed.Item[j])].index:
                        if yield_avg_feed['avg yield'][j] > FAO_Crops.Value[i]:
                            FAO_Crops.Value[i] = yield_avg_feed['avg yield'][j]
        else:
            #global average
            for j in global_avg_feed.index:
                for region_name in feed_regions:
                    for i in FAO_Crops.loc[(FAO_Crops.GROUP == region_name) & (FAO_Crops.Item == global_avg_feed.Item[j])].index:
                        if global_avg_feed['avg yield'][j] > FAO_Crops.Value[i]:
                            FAO_Crops.Value[i] = global_avg_feed['avg yield'][j]
    
                for c_name in feed_countries:
                    for i in FAO_Crops.loc[(FAO_Crops.Area == c_name) & (FAO_Crops.Item == global_avg_feed.Item[j])].index:
                        if global_avg_feed['avg yield'][j] > FAO_Crops.Value[i]:
                            FAO_Crops.Value[i] = global_avg_feed['avg yield'][j]


    if change_crop_yields == True:
        if regional_change_crop == True:
            #imagegroup based averages
            yield_avg_sub = yield_avg_crop.loc[(yield_avg_crop.GROUP == crop_standard)]
            for j in yield_avg_sub.index:
                for region_name in cr_y_regions:
                    for i in FAO_Crops.loc[(FAO_Crops.GROUP == region_name) & (FAO_Crops.Item == yield_avg_sub.Item[j])].index:
                        if yield_avg_sub['avg yield'][j] > FAO_Crops.Value[i]:
                            FAO_Crops.Value[i] = yield_avg_sub['avg yield'][j]
    
                for c_name in cr_y_countries:
                    for i in FAO_Crops.loc[(FAO_Crops.Area == c_name) & (FAO_Crops.Item == yield_avg_sub.Item[j])].index:
                        if yield_avg_sub['avg yield'][j] > FAO_Crops.Value[i]:
                            FAO_Crops.Value[i] = yield_avg_sub['avg yield'][j]
                                
        else:
            #global average
            for j in global_avg_crop.index:
                for region_name in cr_y_regions:
                    for i in FAO_Crops.loc[(FAO_Crops.GROUP == region_name) & (FAO_Crops.Item == global_avg_crop.Item[j])].index:
                        if global_avg_crop['avg yield'][j] > FAO_Crops.Value[i]:
                            FAO_Crops.Value[i] = global_avg_crop['avg yield'][j]
    
                for c_name in cr_y_countries:
                    for i in FAO_Crops.loc[(FAO_Crops.Area == c_name) & (FAO_Crops.Item == global_avg_crop.Item[j])].index:
                        if global_avg_crop['avg yield'][j] > FAO_Crops.Value[i]:
                            FAO_Crops.Value[i] = global_avg_crop['avg yield'][j]
    
    
    
    
    FAO_all_crops = FAO_Crops
    FAO_all_crops['POM Org Area'] = FAO_all_crops['POM Org (with waste & feed)']/FAO_all_crops['Value Org']
    FAO_all_crops['POM EAT Area'] = FAO_all_crops['POM EAT (with waste & feed)']/FAO_all_crops['Value']
    
    average_yield_nat = FAO_all_crops.groupby(['Area']).apply(lambda x: x['EAT POM'].sum()/x['POM EAT Area'].sum())
    average_yield_group_nat = FAO_all_crops.groupby(['Area', 'EAT_group']).apply(lambda x: x['EAT POM'].sum()/x['POM EAT Area'].sum())
    
    Crop_Area_only = FAO_all_crops.groupby(["Area"]).apply(lambda x: x["POM Org Area"].sum())
    Crop_Area_only = Crop_Area_only.reset_index(level = 'Area')
    Crop_Area_only = Crop_Area_only.rename(columns = {0: "Org"})
    
    Crop_group_only = FAO_all_crops.groupby(["EAT_group"]).apply(lambda x: x["POM Org Area"].sum())
    Crop_group_only = Crop_group_only.reset_index(level = 'EAT_group')
    Crop_group_only = Crop_group_only.rename(columns = {0: "Org"})
    
    Crop_group_only_EAT = FAO_all_crops.groupby(["EAT_group"]).apply(lambda x: x["POM EAT Area"].sum())
    Crop_group_only_EAT = Crop_group_only_EAT.reset_index(level = 'EAT_group')
    Crop_group_only_EAT = Crop_group_only_EAT.rename(columns = {0: "EAT"})
    FAO_all_crops_group = pd.merge(Crop_group_only, Crop_group_only_EAT, on = 'EAT_group')
    
    Crop_Area_only_EAT = FAO_all_crops.groupby(["Area"]).apply(lambda x: x["POM EAT Area"].sum())
    Crop_Area_only_EAT = Crop_Area_only_EAT.reset_index(level = 'Area')
    Crop_Area_only_EAT = Crop_Area_only_EAT.rename(columns = {0: "EAT"})
    FAO_all_crops_area = pd.merge(Crop_Area_only, Crop_Area_only_EAT, on = 'Area')
    FAO_all_crops_area = FAO_all_crops_area.set_index('Area')
    
    FAO_all_crops['feed Area EAT'] = FAO_all_crops['for feed EAT']/FAO_all_crops['Value']
    
    Crops_group_area = FAO_all_crops.groupby(["Area", "EAT_group"]).apply(lambda x: x["POM EAT Area"].sum())
    Crops_group_area = Crops_group_area.reset_index(level = 'Area')
    Crops_group_area = Crops_group_area.rename(columns = {0:'EAT'})
    
    Crops_group_area_feed =  FAO_all_crops.groupby(["Area", "EAT_group"]).apply(lambda x: x["feed Area EAT"].sum())
    Crops_group_area_feed = Crops_group_area_feed.reset_index(level = 'Area')
    Crops_group_area_feed = Crops_group_area_feed.rename(columns = {0:'feed'})
    
    Crops_group_area['% feed'] = Crops_group_area_feed['feed']/Crops_group_area['EAT']*100
    
    national_area = FAO_all_crops.groupby(["Area"]).apply(lambda x: x['POM EAT Area'].sum())
    
    
    Feed_crop_area= FAO_all_crops[FAO_all_crops['feed Area EAT'] > 0]
    
    return FAO_all_crops_area, Crops_group_area, FAO_all_crops, FAO_all_crops_group


def feed_crop_area(FAO_Crops, POM_protein_feed, feed_list, FAO_Livestock, POM_data):
    """*** Now figure out crops for feed to break down Int vs Ext meat ***"""
    FAO_Crops.drop(FAO_Crops[FAO_Crops['for feed EAT'] == 0].index, inplace = True)
    FAO_Crops = FAO_Crops.reset_index(drop = True)
    FAO_Crops = FAO_Crops.drop(columns = ["Domain Code", "Domain", "Area Code",\
                                          "Element Code", "Year", "Year Code", "Flag", "Flag Description",
                                          "Item Code_y"])
    
    FAO_Crops = FAO_Crops.rename(columns = {"Item Code_x" : "Item Code"})
    FAO_Crops["POM Org Area (Ha)"] = FAO_Crops["POM Org (with waste & feed)"] / FAO_Crops["Value Org"]
    FAO_Crops["POM EAT Area (Ha)"] = FAO_Crops["POM EAT (with waste & feed)"] / FAO_Crops["Value"]
    
    
    FAO_Crops['Yield Crops (1000tons/ha)'] = FAO_Crops ['Value']
    FAO_Crops = FAO_Crops.loc[:,~FAO_Crops.columns.duplicated()]
    
    POM_protein_feed ['Maize (Ha)'] = POM_protein_feed ['Maize']
    POM_protein_feed ['Soybeans (Ha)'] = POM_protein_feed ['Soybeans']
    POM_protein_feed ['Wheat (Ha)'] = POM_protein_feed ['Wheat']
    POM_protein_feed ['Rapeseed (Ha)'] = POM_protein_feed ['Rapeseed']
    POM_protein_feed ['Oats (Ha)'] = POM_protein_feed ['Oats']
    POM_protein_feed ['Peas, dry (Ha)'] = POM_protein_feed ['Peas, dry']
    POM_protein_feed ['Barley (Ha)'] = POM_protein_feed ['Barley']
    feed_area_list = ['Maize (Ha)', 'Soybeans (Ha)', 'Wheat (Ha)', 'Rapeseed (Ha)', 'Oats (Ha)', 'Peas, dry (Ha)', 'Barley (Ha)']
    for i,k in zip(feed_list, feed_area_list):
        for j in FAO_Crops.index:
            POM_protein_feed.loc[(POM_protein_feed['Area'] == FAO_Crops['Area'][j]) & (FAO_Crops['Item'][j] == i), [k]] /= FAO_Crops['Value'][j]
    
    POM_direct_protein_int = FAO_Livestock[['Area', 'feed group', 'POM EAT Area (Ha) int', '% Protein', 'Item']]
    POM_direct_protein_int = POM_direct_protein_int.groupby(['Area', 'feed group']).apply(lambda x: x['POM EAT Area (Ha) int'].sum())
    POM_direct_protein_int = POM_direct_protein_int.reset_index(level = ['Area', 'feed group'])
    POM_direct_protein_int = POM_direct_protein_int.rename(columns = {0: 'Ha int'})
    
    POM_direct_1000TP_int = FAO_Livestock[['Area', 'feed group', '1000T P EAT int']]
    POM_direct_1000TP_int = POM_direct_1000TP_int.groupby(['Area', 'feed group']).apply(lambda x: x['1000T P EAT int'].sum())
    POM_direct_1000TP_int = POM_direct_1000TP_int.reset_index(level = ['Area', 'feed group'])
    POM_direct_1000TP_int = POM_direct_1000TP_int.rename(columns = {0: '1000T P EAT int'})
    
    POM_direct_protein_ext = FAO_Livestock[['Area', 'feed group', 'POM EAT Area (Ha) ext', '% Protein',]]
    POM_direct_protein_ext = POM_direct_protein_ext.groupby(['Area', 'feed group']).apply(lambda x: x['POM EAT Area (Ha) ext'].sum())
    POM_direct_protein_ext = POM_direct_protein_ext.reset_index(level = ['Area', 'feed group'])
    POM_direct_protein_ext = POM_direct_protein_ext.rename(columns = {0: 'Ha ext'})
    
    POM_direct_1000TP_ext = FAO_Livestock[['Area', 'feed group', '1000T P EAT ext']]
    POM_direct_1000TP_ext = POM_direct_1000TP_ext.groupby(['Area', 'feed group']).apply(lambda x: x['1000T P EAT ext'].sum())
    POM_direct_1000TP_ext = POM_direct_1000TP_ext.reset_index(level = ['Area', 'feed group'])
    POM_direct_1000TP_ext = POM_direct_1000TP_ext.rename(columns = {0: '1000T P EAT ext'})
    
    POM_direct_protein_int = pd.merge(POM_direct_protein_int, POM_direct_1000TP_int, on = ['Area', 'feed group'])
    POM_direct_protein_ext = pd.merge(POM_direct_protein_ext, POM_direct_1000TP_ext, on = ['Area', 'feed group'])
    
    POM_direct_protein = pd.merge(POM_direct_protein_int, POM_direct_protein_ext, on = ['Area', 'feed group'])
    
    POM_protein_feed = POM_protein_feed.rename(columns = {'group' : 'feed group'})
    POM_protein_feed = pd.merge(POM_protein_feed, POM_direct_protein, on = ["Area", "feed group"], how ='right')
    POM_protein_feed = POM_protein_feed.rename(columns = {0 : 'direct Area'})
    
    POM_protein_feed['Total int Ha'] = 0
    for i in POM_protein_feed:
        if i in feed_area_list or i == 'Ha int':
            POM_protein_feed['Total int Ha'] += POM_protein_feed[i]
            
    POM_protein_feed['Total Ha'] = POM_protein_feed['Total int Ha'] + POM_protein_feed['Ha ext']
    POM_protein_feed['Total 1000T P'] = POM_protein_feed['1000T P EAT int'] + POM_protein_feed['1000T P EAT ext']
    
    POM_protein_feed['Overall kgP/ha'] = (POM_protein_feed['Total 1000T P']*10**6) / POM_protein_feed['Total Ha']
    POM_protein_feed['int kgP/ha'] = (POM_protein_feed['1000T P EAT int']*10**6) / POM_protein_feed['Total int Ha']
    POM_protein_feed['ext kgP/ha'] = (POM_protein_feed['1000T P EAT ext']*10**6) / POM_protein_feed['Ha ext']
    
    
    POM_pop = POM_data[['Area', 'GROUP', 'Population (2016), 1000person']]
    POM_pop = POM_pop.drop_duplicates().reset_index(drop=True)
    
    POM_protein_feed ['GROUP'] = POM_protein_feed ['feed group']
    POM_protein_feed ['Population (2016), 1000person'] = POM_protein_feed ['feed group']
    
    for i in POM_protein_feed.index:
        for j in POM_pop.index:
            if POM_protein_feed['Area'][i] == POM_pop['Area'][j]:
                POM_protein_feed['GROUP'][i] = POM_pop['GROUP'][j]
                POM_protein_feed ['Population (2016), 1000person'][i] = POM_pop['Population (2016), 1000person'][j]
    
    POM_protein_feed = POM_protein_feed.fillna(0)
    
    Weighted_final_area = POM_protein_feed.groupby(['feed group', 'Area']).apply(lambda x: x['Total Ha'].sum())
    Weighted_final_area = Weighted_final_area.reset_index(level = ['feed group', 'Area'])
    Weighted_final_area = Weighted_final_area.rename(columns = {0 : 'Total Ha'})
    
    #Area
    Weighted_final_area_int = POM_protein_feed.groupby(['feed group', 'Area']).apply(lambda x: x['Total int Ha'].sum())
    Weighted_final_area_int = Weighted_final_area_int.reset_index(level = ['feed group', 'Area'])
    Weighted_final_area_int = Weighted_final_area_int.rename(columns = {0 : 'Total int Ha'})
    
    #Area
    Weighted_final_area_ext = POM_protein_feed.groupby(['feed group', 'Area']).apply(lambda x: x['Ha ext'].sum())
    Weighted_final_area_ext = Weighted_final_area_ext.reset_index(level = ['feed group', 'Area'])
    Weighted_final_area_ext = Weighted_final_area_ext.rename(columns = {0 : 'Ha ext'})
    
    #People
    temp_weight_final = POM_protein_feed.groupby(['feed group', 'Area']).apply(lambda x: x['Population (2016), 1000person'].sum())
    temp_weight_final = temp_weight_final.reset_index(level = ['feed group', 'Area'])
    temp_weight_final = temp_weight_final.rename(columns = {0: 'pop (1000p)' })
    
    #Protein
    protein_weight_final = POM_protein_feed.groupby(['feed group', 'Area']).apply(lambda x: x['Total 1000T P'].sum())
    protein_weight_final = protein_weight_final.reset_index(level = ['feed group', 'Area'])
    protein_weight_final = protein_weight_final.rename(columns = {0 : 'Total 1000T P'})
    
    
    #Protein int
    protein_weight_final_int = POM_protein_feed.groupby(['feed group', 'Area']).apply(lambda x: x['1000T P EAT int'].sum())
    protein_weight_final_int = protein_weight_final_int.reset_index(level = ['feed group', 'Area'])
    protein_weight_final_int = protein_weight_final_int.rename(columns = {0 : '1000T P int'})
    
    #Prtoein ext
    protein_weight_final_ext = POM_protein_feed.groupby(['feed group', 'Area']).apply(lambda x: x['1000T P EAT ext'].sum())
    protein_weight_final_ext = protein_weight_final_ext.reset_index(level = ['feed group', 'Area'])
    protein_weight_final_ext = protein_weight_final_ext.rename(columns = {0 : '1000T P ext'})
    
    Weighted_final = pd.merge(Weighted_final_area, temp_weight_final, on = ['feed group', 'Area'])
    Weighted_final = pd.merge(Weighted_final, Weighted_final_area_int, on = ['feed group', 'Area'])
    Weighted_final = pd.merge(Weighted_final, Weighted_final_area_ext, on = ['feed group', 'Area'])
    Weighted_final = pd.merge(Weighted_final, protein_weight_final, on = ['feed group', 'Area'])
    Weighted_final = pd.merge(Weighted_final, protein_weight_final_int, on = ['feed group', 'Area'])
    Weighted_final = pd.merge(Weighted_final, protein_weight_final_ext, on = ['feed group', 'Area'])
    
    Weighted_final = Weighted_final[Weighted_final['Total 1000T P'] > 0]
    
    Weighted_final ['Total kgP/ha'] = Weighted_final['Total 1000T P']*10**6/Weighted_final['Total Ha']
    Weighted_final ['Total kgP/ha/p'] = Weighted_final['Total 1000T P']*10**6/(Weighted_final['pop (1000p)']*10**3)/Weighted_final['Total Ha']
    Weighted_final ['Total int kgP/ha/p'] = Weighted_final['1000T P int']*10**6/(Weighted_final['pop (1000p)']*10**3)/Weighted_final['Total int Ha']
    Weighted_final ['Total ext kgP/ha/p'] = Weighted_final['1000T P ext']*10**6/(Weighted_final['pop (1000p)']*10**3)/Weighted_final['Ha ext']
    
    Weighted_final ['Total kgP/ha'] = Weighted_final['Total 1000T P']*10**6/Weighted_final['Total Ha']
    Weighted_final ['Total int kgP/ha'] = Weighted_final['1000T P int']*10**6/Weighted_final['Total int Ha']
    Weighted_final ['Total ext kgP/ha'] = Weighted_final['1000T P ext']*10**6/Weighted_final['Ha ext']
    Weighted_final ['1000T P/p'] = Weighted_final['Total 1000T P']*10**6/(Weighted_final['pop (1000p)']*10**3)
    Weighted_final = Weighted_final.fillna(0)
    #Weighted_final = Weighted_final[Weighted_final['GROUP'] != 'Other']
    
    Weighted_final = pd.merge(Weighted_final, POM_protein_feed[['Area','GROUP']], on = 'Area', how = 'left')
    Weighted_final = Weighted_final.drop_duplicates()
    
    Weighted_group_int = Weighted_final.groupby(['GROUP']).apply(lambda x: (x['1000T P int'].sum()*10**6)/x['Total int Ha'].sum())#/(x['pop (1000p)'].sum()*1000))
    Weighted_group_int = Weighted_group_int.reset_index(level = 'GROUP')
    Weighted_group_int = Weighted_group_int.rename(columns = {0: 'kg/ha int'})
    
    Weighted_group_ext = Weighted_final.groupby(['GROUP']).apply(lambda x: (x['1000T P ext'].sum()*10**6)/x['Ha ext'].sum())#/(x['pop (1000p)'].sum()*1000))
    Weighted_group_ext = Weighted_group_ext.reset_index(level = 'GROUP')
    Weighted_group_ext = Weighted_group_ext.rename(columns = {0: 'kg/ha ext'})
    
    Weighted_group_tot = Weighted_final.groupby(['GROUP']).apply(lambda x: (x['Total 1000T P'].sum()*10**6)/x['Total Ha'].sum())#/(x['pop (1000p)'].sum()*1000))
    Weighted_group_tot = Weighted_group_tot.reset_index(level = 'GROUP')
    Weighted_group_tot = Weighted_group_tot.rename(columns = {0: 'kg/ha tot'})
    
    Weighted_group_tot = pd.merge(Weighted_group_tot, Weighted_group_int, on = 'GROUP')
    Weighted_group_tot = pd.merge(Weighted_group_tot, Weighted_group_ext, on = 'GROUP')
    
    #Weighted_group['kg/ha ext'] = Weighted_final.groupby(['GROUP']).apply(lambda x: (x['1000T P ext'].sum()*10**6)/x['Ha ext'].sum())
    #Weighted_group['kg/ha tot'] = Weighted_final.groupby(['GROUP']).apply(lambda x: (x['Total 1000T P'].sum()*10**6)/x['Total Ha'].sum())
    
    Weighted_national_int = Weighted_final.groupby(['Area']).apply(lambda x: (x['1000T P int'].sum()*10**6)/x['Total int Ha'].sum())#/(x['pop (1000p)'].sum()*1000))
    Weighted_national_int = Weighted_national_int.reset_index(level = ['Area'])
    Weighted_national_int = Weighted_national_int.rename(columns = {0: 'kg/ha int'})
    
    Weighted_national_ext = Weighted_final.groupby(['Area']).apply(lambda x: (x['1000T P ext'].sum()*10**6)/x['Ha ext'].sum())#/(x['pop (1000p)'].sum()*1000))
    Weighted_national_ext = Weighted_national_ext.reset_index(level = ['Area'])
    Weighted_national_ext = Weighted_national_ext.rename(columns = {0: 'kg/ha ext'})
    
    Weighted_national_tot = Weighted_final.groupby(['Area']).apply(lambda x: (x['Total 1000T P'].sum()*10**6)/x['Total Ha'].sum())#/(x['pop (1000p)'].sum()*1000))
    Weighted_national_tot = Weighted_national_tot.reset_index(level = ['Area'])
    Weighted_national_tot = Weighted_national_tot.rename(columns = {0: 'kg/ha tot'})
    
    Weighted_national_tot = pd.merge(Weighted_national_tot, Weighted_national_int, on = 'Area')
    Weighted_national_tot = pd.merge(Weighted_national_tot, Weighted_national_ext, on = 'Area')
    
    Weighted_item_int = Weighted_final.groupby(["Area"]).apply(lambda x: x["1000T P int"]/x["1000T P int"].sum())
    Weighted_item_int = Weighted_item_int.reset_index(level = ['Area'])
    Weighted_item_int = Weighted_item_int.rename(columns = {'1000T P int': '% of int'})
    
    Weighted_item_ext = Weighted_final.groupby(["Area"]).apply(lambda x: x["1000T P ext"]/x["1000T P ext"].sum())
    Weighted_item_ext = Weighted_item_ext.reset_index(level = ['Area'])
    Weighted_item_ext = Weighted_item_ext.rename(columns = {'1000T P ext': '% of ext'})
    
    Weighted_item_tot = Weighted_final.groupby(["Area"]).apply(lambda x: x["Total 1000T P"]/x["Total 1000T P"].sum())
    Weighted_item_tot = Weighted_item_tot.reset_index(level = ['Area'])
    Weighted_item_tot = Weighted_item_tot.rename(columns = {'Total 1000T P': '% of Total'})
    
    Weighted_item_tot = pd.merge(Weighted_item_tot, Weighted_item_int['% of int'], left_index = True, right_index = True)
    Weighted_item_tot = pd.merge(Weighted_item_tot, Weighted_item_ext['% of ext'], left_index = True, right_index = True)
    Weighted_item_tot = pd.merge(Weighted_item_tot, Weighted_final['feed group'], left_index = True, right_index = True)
    
    Weighted_areaitem_int = Weighted_final.groupby(["Area"]).apply(lambda x: x["Total int Ha"]/x["Total int Ha"].sum())
    Weighted_areaitem_int = Weighted_areaitem_int.reset_index(level = ['Area'])
    Weighted_areaitem_int = Weighted_areaitem_int.rename(columns = {'Total int Ha': '% of int'})
    
    Weighted_areaitem_ext = Weighted_final.groupby(["Area"]).apply(lambda x: x["Ha ext"]/x["Ha ext"].sum())
    Weighted_areaitem_ext = Weighted_areaitem_ext.reset_index(level = ['Area'])
    Weighted_areaitem_ext = Weighted_areaitem_ext.rename(columns = {'Ha ext': '% of ext'})
    
    Weighted_areaitem_tot = Weighted_final.groupby(["Area"]).apply(lambda x: x["Total Ha"]/x["Total Ha"].sum())
    Weighted_areaitem_tot = Weighted_areaitem_tot.reset_index(level = ['Area'])
    Weighted_areaitem_tot = Weighted_areaitem_tot.rename(columns = {'Total Ha': '% of tot'})
    
    Weighted_areaitem_tot = pd.merge(Weighted_areaitem_tot, Weighted_areaitem_int['% of int'], left_index = True, right_index = True)
    Weighted_areaitem_tot = pd.merge(Weighted_areaitem_tot, Weighted_areaitem_ext['% of ext'], left_index = True, right_index = True)
    Weighted_areaitem_tot = pd.merge(Weighted_areaitem_tot, Weighted_final['feed group'], left_index = True, right_index = True)
    
    #Weighted_national['kg/ha ext'] = Weighted_final.groupby(['Area']).apply(lambda x: (x['1000T P ext'].sum()*10**6)/x['Ha ext'].sum())
    #Weighted_national['kg/ha tot'] = Weighted_final.groupby(['Area']).apply(lambda x: (x['Total 1000T P'].sum()*10**6)/x['Total Ha'].sum())
    Feed_crops_area = POM_protein_feed[['Area', 'feed group', 'Ha int', 'Total int Ha']]
    Feed_crops_area['Feed crop Area'] = POM_protein_feed['Total int Ha'] - POM_protein_feed['Ha int']
    Feed_crops_area_sum = Feed_crops_area.groupby(['Area']).apply(lambda x: x['Feed crop Area'].sum())
    Feed_crops_area_sum = Feed_crops_area_sum.reset_index(level = ['Area'])
    Feed_crops_area_sum = Feed_crops_area_sum.rename(columns = { 0: 'Feed crop Area'})
    

    
    return Feed_crops_area_sum, Weighted_final