#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 16:31:56 2021

@author: nicolasnavarre
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

figures = 'figures/'

def extra_analysis(POM_data, Org_food, EAT_food, FAO_Crops, FAO_Crop_yield, POM_protein_feed, meat_products, final_df, Group_Area):
    
    POM_p_balance = POM_data.loc[POM_data.Item.isin(['Milk, whole fresh cow'])]
    
    POM_diet = POM_data

    # temp_list = []
    # for i in final_df["IMAGEGROUP"].unique().tolist():
    #     temp_ha = round(final_df.loc[final_df["IMAGEGROUP"] == i, 'Ha'].sum(),2)
    #     temp_org = round(final_df.loc[final_df["IMAGEGROUP"] == i, 'Org area'].sum(),2)
    #     temp_land = round(final_df.loc[final_df["IMAGEGROUP"] == i, 'Value'].sum(),2)
    #     print(i, temp_ha, temp_org, temp_land)
    #     temp_list.append(temp_ha)
    # print(sum(temp_list))
    
    # print("Micro Data")
    # print(final_df.Population.sum()/(final_df.Population.sum()+POM_micro['Population (2016), 1000person'].sum()))
    # print(final_df.Value.sum()/(final_df.Value.sum()+POM_micro['1000 Ha'].sum()))
    
    # POM_micro['1000 Ha'].sum()
    # final_df.Value.sum()
    # final_df.Value.sum()+POM_micro['1000 Ha'].sum()
    
    #Goes in the main.
    # print((Feed_crops_area_sum['Feed crop Area'].sum() + Meat_Area['EAT'].sum())/Total_Area['EAT'].sum())
    # print(Feed_crops_area_sum['Feed crop Area'].sum() + Meat_Area['EAT'].sum())
    # print(Total_Area['EAT'].sum())
        
    # feed_detail['prod'] = 0
    
    # feed_detail = pd.merge(feed_detail, POM_p_balance[['Area', 'EAT POM (with waste)', 'GROUP']], left_on = 'Area', right_on = 'Area' )
    
    
    # for i in feed_detail.Area.tolist():
    #     feed_detail.loc[feed_detail.Area == i, 'prod'] = float(POM_p_balance.loc[POM_p_balance.Area == i, 'EAT POM (with waste)'])
    
    
    # feed_detail['prod'] *= feed_detail['fraction'] 
    # #feed_detail['prod'] *= 0.141926
    
    # #feed_detail['grass'] *= 0.18
    # #feed_detail['Maize'] *= 0.100455
    # #feed_detail['Soybeans'] *= 0.20333
    
    # feed_detail['ratio'] = feed_detail['prod']/(feed_detail['grass'] + feed_detail['Maize'] + feed_detail['Soybeans'])
    # feed_detail['ratio'] *= 100
    
    # p_in = feed_detail['grass'].sum() + feed_detail['Maize'].sum() + feed_detail['Soybeans'].sum()
    # print(p_in)
    # print(feed_detail['prod'].sum())
    
    # print(feed_detail['prod'].sum()/p_in)
    
    #import Prod_Global_Figures as Gfigs
    #import Prod_Regional_Figures as Rfigs
    #Gfigs.GlobalFig()
    #Rfigs.RegionalFig("Europe")
    temp_list = []
    for i in final_df["IMAGEGROUP"].unique().tolist():
        temp_ha = round(final_df.loc[final_df["IMAGEGROUP"] == i, 'Ha'].sum(),2)
        temp_org = round(final_df.loc[final_df["IMAGEGROUP"] == i, 'Org area'].sum(),2)
        temp_land = round(final_df.loc[final_df["IMAGEGROUP"] == i, 'Value'].sum(),2)
        print(i, temp_ha, temp_org, temp_land)
        temp_list.append(temp_ha)
    print(sum(temp_list))
    POM_waste = POM_data
    
    POM_nations = POM_data
    nation_list = []
    food_times_list = []
    for i in POM_nations.Area.unique().tolist():
        POM_temp = POM_nations.loc[POM_nations.Area == i]
        if i == 'Syrian Arab Republic':
            nation_list.append(i)
        food_times_list.append(len(POM_temp.Area))
    
    #df_temp = pd.DataFrame()
    #df_temp['Area'] = nation_list
    #df_temp['Times'] = food_times_list
    
    gp_nat = POM_waste[['Area', 'Cal Provided']].drop_duplicates(subset=['Area'])

    
    POM_waste['eat waste'] = POM_waste['EAT POM (with waste)']- POM_waste['EAT POM']
    POM_waste['eat feed'] = POM_waste['POM EAT (with waste & feed)'] - POM_waste['EAT POM (with waste)']
    
    POM_waste = pd.merge(POM_waste, FAO_Crop_yield[['Area', 'Item', 'Value']], on=["Area", 'Item'], how = 'left')
    
    check_waste = POM_waste.groupby(["EAT_group"]).apply(lambda x: x["eat waste"].sum())
    zcheck_feed = POM_waste['for feed EAT'].sum()/POM_waste['POM EAT (with waste & feed)'].sum()
    zcheck_waste = POM_waste['eat waste'].sum()/POM_waste['POM EAT (with waste & feed)'].sum()
    zcheck_food = POM_waste['POM (no waste)'].sum()/POM_waste['POM Org (with waste & feed)'].sum()
    zcheck_waste_nofeed = 1 - POM_waste['EAT POM'].sum()/POM_waste['EAT POM (with waste)'].sum()
    zcheck_waste_nofeed = 1 - POM_waste['POM (no waste)'].sum()/POM_waste['POM'].sum()
    
    waste_total = POM_waste['eat waste'].sum()
    waste_veg = POM_waste.loc[POM_waste['EAT_group'] == 'vegetables', 'eat waste'].sum()
    
    print(waste_veg/waste_total)
    print(POM_waste['POM (no waste)'].sum()/POM_waste['POM Org (with waste & feed)'].sum())
    POM_legumes = POM_waste.loc[POM_waste['EAT_group'] == 'dairy foods', 'EAT POM'].sum()
    
    
    feed_by_nation_eat = POM_waste.loc[POM_waste.Item != 'grass'].groupby(["GROUP"]).apply(lambda x: x["for feed EAT"].sum())#/x["POM EAT (with waste & feed)"].sum())
    feed_by_nation_org = POM_waste.loc[POM_waste.Item != 'grass'].groupby(["GROUP"]).apply(lambda x: x["for feed Org"].sum())#/x["POM Org (with waste & feed)"].sum())
    print(POM_waste['for feed Org'].sum())
    feed_global_eat = POM_waste['eat feed'].sum()/POM_waste['POM EAT (with waste & feed)'].sum()
    feed_global_org = POM_waste['for feed Org'].sum()/POM_waste['POM Org (with waste & feed)'].sum()
    
    POM_meat = POM_waste[POM_waste['group_nf'].isin(meat_products)]
    temp = POM_waste['EAT POM (with waste)'].sum() - POM_meat['EAT POM (with waste)'].sum()
    print(temp/POM_waste['POM EAT (with waste & feed)'].sum())
    
    meat_by_group_eat = POM_meat.groupby(["GROUP"]).apply(lambda x: x['POM EAT (with waste & feed)'].sum())
    meat_by_group_org = POM_meat.groupby(["GROUP"]).apply(lambda x: x['POM Org (with waste & feed)'].sum())
    meat_by_group_eat = pd.DataFrame(meat_by_group_eat)
    meat_by_group_org = pd.DataFrame(meat_by_group_org)
    
    food_eat = POM_waste.groupby(["GROUP"]).apply(lambda x: x["POM EAT (with waste & feed)"].sum())
    food_org = POM_waste.groupby(["GROUP"]).apply(lambda x: x["POM Org (with waste & feed)"].sum())
    food_eat = pd.DataFrame(food_eat)
    food_org = pd.DataFrame(food_org)
    
    meat_by_group_eat = pd.merge(meat_by_group_eat, food_eat, left_index=True, right_index=True)
    meat_by_group_eat['share'] = meat_by_group_eat['0_x']/meat_by_group_eat['0_y']
    
    meat_by_group_org = pd.merge(meat_by_group_org, food_org, left_index=True, right_index=True)
    meat_by_group_org['share'] = meat_by_group_org['0_x']/meat_by_group_org['0_y']
    
    temp_count = 0
    temp_counteat = 0
    fig, ax = plt.subplots()
    for i,j in zip(meat_by_group_eat.index, meat_by_group_org.index) :
        
        if i == 'Other':
            continue
    
    
        ax.plot(j, meat_by_group_org['share'][j]*100 , "rd")
        ax.plot(i, meat_by_group_eat['share'][i]*100 ,  "gd")
        
        temp_count += Org_food
        temp_counteat += EAT_food
    
    #ax.title.set_text("Global per Capita Food Group Production (inc. waste & feed)")
    ax.grid(alpha = 0.5)
    ax.tick_params(labelrotation=90)
    plt.yticks(rotation = "horizontal")
    plt.ylabel("Feed Share (%)")
    plt.ylim(-0.2, 100)
    
    legend_elements = [Line2D([0], [0], lw = 0, marker='d', color='r', label='Current Diet\nGlobal = '+str(round((meat_by_group_org['0_x'].sum()/meat_by_group_org['0_y'].sum())*100,1))+' % animal products',\
                              markerfacecolor='r'),
                       Line2D([0], [0], lw = 0, marker='d', color='g', label='EAT Lancet Diet\nGlobal = '+str(round((meat_by_group_eat['0_x'].sum()/meat_by_group_eat['0_y'].sum())*100,1))+' % animal products',\
                              markerfacecolor='g')]
    lg = ax.legend(handles=legend_elements, bbox_to_anchor=(1.0, 0.42), loc="lower left")
    #plt.legend(handles =[one, two])
    fig.savefig(figures+"Global Meat Share.png", bbox_extra_artists=(lg,), bbox_inches='tight', dpi = 400)
    plt.close()

    temp_count = 0
    temp_counteat = 0
    group_list = []
    food_list_eat = []
    food_list_org = []
    fig, ax = plt.subplots()
    for i,j in zip(feed_by_nation_org.index, feed_by_nation_eat.index) :
        
        if i == 'Other':
            continue
    
    
        ax.plot(i, feed_by_nation_org[i]* 1000 , "rd")
        ax.plot(j, feed_by_nation_eat[j]* 1000 , "gd")
        
        temp_count += Org_food
        temp_counteat += EAT_food
        group_list.append(i)
        food_list_eat.append(feed_by_nation_eat[j]* 1000)
        food_list_org.append(feed_by_nation_org[i]* 1000)
        
    
    #ax.title.set_text("Global per Capita Food Group Production (inc. waste & feed)")
    ax.grid(alpha = 0.5)
    ax.tick_params(labelrotation=90)
    plt.yticks(rotation = "horizontal")
    plt.ylabel("Feed Produced (tonnes)")
    #plt.ylim(-0.2, 100)
    
    legend_elements = [Line2D([0], [0], lw = 0, marker='d', color='r', label='Current Diet\nTotal = '+str(round(POM_waste['for feed Org'].sum()*1000/10**9,1))+' 1e9 tonnes',\
                              markerfacecolor='r'),
                       Line2D([0], [0], lw = 0, marker='d', color='g', label='EAT Lancet Diet\nTotal = '+str(round(POM_waste['for feed EAT'].sum()*1000/10**9,1))+' 1e9 tonnes',\
                              markerfacecolor='g')]
    lg = ax.legend(handles=legend_elements, bbox_to_anchor=(1.0, 0.42), loc="lower left")
    #plt.legend(handles =[one, two])
    fig.savefig(figures+"Global Feed Share.png", bbox_extra_artists=(lg,), bbox_inches='tight', dpi = 400)
    
    
    fig, ax = plt.subplots()
    diet_df = pd.DataFrame()
    width = 0.35
    x = np.arange(len(group_list))
    
    diet_df['group'] = group_list
    diet_df['gF EAT'] = food_list_eat
    diet_df['gF Org'] = food_list_org
    diet_df['dif'] = diet_df['gF Org'] - diet_df['gF EAT']
    
    diet_df = diet_df.sort_values(by=['dif'], ascending=False)

    ax.bar(x + width/2, diet_df['gF EAT'], width, label='EAT Diet', color = 'g')
    ax.bar(x - width/2, diet_df['gF Org'], width, label='BAU Diet', color = 'r')
    
    ax.set_ylabel('Prod/capita (g/person-day)')
    ax.set_xticks(x)
    ax.set_xticklabels(diet_df['group'])
    
    pos_values = len(diet_df[diet_df["dif"]>0])
    ax.axvspan(-0.5, pos_values-0.5, facecolor='0.2', alpha=0.25, zorder=-100)
    plt.xticks(rotation = 90)
    POM_leg = POM_waste.loc[POM_waste.Item != 'grass']
    legend_elements = [Line2D([0], [0], lw = 0, marker='s', color='r', label='Current Diet\nTotal = '+str(round(POM_leg['for feed Org'].sum()*1000/10**9,1))+' 1e9 tonnes',\
                              markerfacecolor='r'),
                        Line2D([0], [0], lw = 0, marker='s', color='g', label='EAT Lancet Diet\nTotal = '+str(round(POM_leg['for feed EAT'].sum()*1000/10**9,1))+' 1e9 tonnes',\
                              markerfacecolor='g'),
                        Line2D([0], [0], lw = 0, marker='s', color='0.2', alpha=0.25, label='Reduction in production',\
                              markerfacecolor='0.2')]
    lg = ax.legend(handles=legend_elements, bbox_to_anchor=(1.0, 0.42), loc="lower left")
    fig.savefig(figures+j+" EAT_Group Production.png", bbox_extra_artists=(lg,), bbox_inches='tight', dpi = 400)

    
    plt.close()
    
    FAO_yield_glob = FAO_Crops[['Area', "Item", 'Value', 'GROUP', 'for feed EAT', 'for feed Org']]
    FAO_yield_glob = FAO_yield_glob[FAO_yield_glob.Item != 'grass' ]
    FAO_yield_glob['EAT Feed Area'] = FAO_yield_glob['for feed EAT']/FAO_yield_glob['Value']
    FAO_yield_glob['Org Feed Area'] = FAO_yield_glob['for feed Org']/FAO_yield_glob['Value']
    
    global_yield_feed = FAO_yield_glob.groupby(["GROUP"]).apply(lambda x: x['for feed EAT'].sum()/x['EAT Feed Area'].sum())
    
    
    fig, ax = plt.subplots()
    for i in global_yield_feed.index :
        
        if i == 'Other':
            continue
        
        ax.plot(i, global_yield_feed[i]*1000, 'kd')
        
    
    
    #ax.title.set_text("Global per Capita Food Group Production (inc. waste & feed)")
    ax.grid(alpha = 0.5)
    ax.tick_params(labelrotation=90)
    plt.yticks(rotation = "horizontal")
    plt.ylabel("Feed Crop Yields (tons/ha)")
    plt.ylim(-0.2, 4)


    
    fig, ax = plt.subplots()
    group_list = []
    food_list = []
    for i in global_yield_feed.index :
        
        if i == 'Other':
            continue
 
        ax.plot(i, global_yield_feed[i]*1000, 'kd')
        group_list.append(i)
        food_list.append(global_yield_feed[i]*1000)
    
    
    diet_df = pd.DataFrame()
    width = 0.35
    x = np.arange(len(group_list))
    
    diet_df['group'] = group_list
    diet_df['food'] = food_list_eat
    
    ax.bar(x, diet_df['food'], width, label='EAT Diet', color = 'k')
    #ax.bar(x - width/2, diet_df['gF Org'], width, label='BAU Diet', color = 'r')
    
    ax.set_ylabel('Prod/capita (g/person-day)')
    ax.set_xticks(x)
    ax.set_xticklabels(diet_df['group'])
    
    #pos_values = len(diet_df[diet_df["dif"]>0])
    #ax.axvspan(-0.5, pos_values-0.5, facecolor='0.2', alpha=0.25, zorder=-100)
    plt.xticks(rotation = 90)
    fig.savefig(figures+j+" yield_crop.png", dpi = 400)
    
    
    
    legend_elements = [Line2D([0], [0], lw = 0, marker='s', color='r', label='Current Diet\nTotal = '+str(round(POM_waste['for feed Org'].sum()*1000/10**9,1))+' 1e9 tonnes',\
                              markerfacecolor='r'),
                        Line2D([0], [0], lw = 0, marker='s', color='g', label='EAT Lancet Diet\nTotal = '+str(round(POM_waste['for feed EAT'].sum()*1000/10**9,1))+' 1e9 tonnes',\
                              markerfacecolor='g'),
                        Line2D([0], [0], lw = 0, marker='s', color='0.2', alpha=0.25, label='Reduction in production',\
                              markerfacecolor='0.2')]
    lg = ax.legend(handles=legend_elements, bbox_to_anchor=(1.0, 0.42), loc="lower left")
    fig.savefig(figures+j+" EAT_Group Production.png", bbox_extra_artists=(lg,), bbox_inches='tight', dpi = 400)

    
    #ax.title.set_text("Global per Capita Food Group Production (inc. waste & feed)")
    ax.grid(alpha = 0.5)
    ax.tick_params(labelrotation=90)
    plt.yticks(rotation = "horizontal")
    plt.ylabel("Feed Crop Yields (tons/ha)")
    plt.ylim(-0.2, 5)

    
    
    #lg = ax.legend(handles=legend_elements, bbox_to_anchor=(1.0, 0.42), loc="lower left")
    #plt.legend(handles =[one, two])
    fig.savefig(figures+"Global Feed yield.png", bbox_inches='tight', dpi = 400)
    plt.close()
    
    #print(zcheck_feed+zcheck_waste+zcheck_food)
    #print(zcheck_feed)
    #print(zcheck_waste)
    
    POM_chicken = POM_data.loc[POM_data.Item == 'Eggs, hen, in shell']
    POM_chicken = POM_chicken[['Area', 'POM', 'EAT POM']]
    POM_chicken['Change'] = POM_chicken['EAT POM']/POM_chicken['POM']
    #print(sum(POM_chicken.POM))
    #print(sum(POM_chicken['EAT POM']))
    
    #protein_sources = []
    #POM_protein = POM_data.loc[POM_data.EAT_group.isin(protein_sources)
    POM_protein = POM_data.loc[POM_data.group.isin(['tree nuts', 'dry beans lentils and peas', 'peanuts', 'soy foods'])]
    protein_yield = pd.merge(POM_protein, FAO_Crop_yield[['Area', 'Item', 'Value']], on = ['Area', 'Item'], how = 'left') 
    
    POM_veg_prot = protein_yield[['Area', 'Item', 'GROUP', 'group_nf', '% Protein', 'EAT POM (with waste)', 'Value']]
    POM_veg_prot = POM_veg_prot.drop(POM_veg_prot[POM_veg_prot['EAT POM (with waste)'] == 0].index)
    
    POM_veg_prot = POM_veg_prot.dropna()
    POM_veg_prot['kgP'] = POM_veg_prot['EAT POM (with waste)']*POM_veg_prot['% Protein']/100*10**6
    POM_veg_prot['ha'] = POM_veg_prot['EAT POM (with waste)']/POM_veg_prot['Value']
    
    figure_veg_prot = POM_veg_prot.groupby(['GROUP', 'group_nf']).apply(lambda x: (x['kgP'].sum()))
    figure_veg_prot = figure_veg_prot.reset_index(level = ['GROUP', 'group_nf'])
    
    figure_veg_land = POM_veg_prot.groupby(['GROUP', 'group_nf']).apply(lambda x: x['ha'].sum())
    figure_veg_land = figure_veg_land.reset_index(level = ['GROUP', 'group_nf'])
    
    figure_veg_prot['ha'] = figure_veg_land[0]
    figure_veg_prot['kgP/ha'] = figure_veg_prot[0]/figure_veg_prot['ha']
    
    
    # POM_meat_prot = POM_protein_feed[["Area", 'GROUP', 'feed group', 'Total 1000T P', 'Total Ha']]
    # POM_meat_prot['kgP'] = POM_meat_prot['Total 1000T P'] * 10**6
    
    # figure_meat_prot = POM_meat_prot.groupby(['GROUP', 'feed group']).apply(lambda x: (x['kgP'].sum()))
    # figure_meat_prot = figure_meat_prot.reset_index(level = ['GROUP', 'feed group'])
    # figure_meat_prot = figure_meat_prot.dropna()
    
    # figure_meat_land = POM_meat_prot.groupby(['GROUP', 'feed group']).apply(lambda x: (x['Total Ha'].sum()))
    # figure_meat_land = figure_meat_land.reset_index(level = ['GROUP', 'feed group'])
    
    # figure_meat_prot['ha'] = figure_meat_land[0]
    # figure_meat_prot['kgP/ha'] = figure_meat_prot[0]/figure_meat_prot['ha']
    # figure_meat_prot = figure_meat_prot.dropna()
    # figure_meat_prot = figure_meat_prot.drop(figure_meat_prot[figure_meat_prot.GROUP == 'Other'].index)
    
    # POM_figure = POM_protein_feed[['Area', 'GROUP', 'Overall kgP/ha']]
    
    
    
    bau_area = final_df.groupby(['IMAGEGROUP']).apply(lambda x: ((x["Org area"].sum())/(x["Population"].sum()*1000)))
    eat_area = final_df.groupby(["IMAGEGROUP"]).apply(lambda x: ((x["Ha"].sum())/(x["Population"].sum()*1000)))
    
    bau_avg = (final_df["Org area"].sum())/(final_df["Population"].sum()*1000)
    eat_avg = (final_df["Ha"].sum())/(final_df["Population"].sum()*1000)
    
    fig, ax = plt.subplots()
    for i,j in zip(bau_area.index, eat_area.index) :
        if i == 'Other':
            continue
        
        
        ax.plot(i, bau_area[i] , "rd")
        ax.plot(j, eat_area[j], "gd")
            
    
    #ax.title.set_text("Global per Capita Food Group Production (inc. waste & feed)")
    ax.grid(alpha = 0.5)
    ax.tick_params(labelrotation=90)
    plt.yticks(rotation = "horizontal")
    plt.ylabel("Land Use ha/person")
    plt.ylim(0, 1)
    
    legend_elements = [Line2D([0], [0], lw = 0, marker='d', color='r', label='Current Diet\nTotal = '+str(round(bau_avg,1))+' ha/person',\
                              markerfacecolor='r'),
                       Line2D([0], [0], lw = 0, marker='d', color='g', label='EAT Lancet Diet\nTotal = '+str(round(eat_avg,1))+' ha/person',\
                              markerfacecolor='g')]
    lg = ax.legend(handles=legend_elements, bbox_to_anchor=(1.0, 0.42), loc="lower left")
    #plt.legend(handles =[one, two])
    fig.savefig(figures+"Global land Share.png", bbox_extra_artists=(lg,), bbox_inches='tight', dpi = 400)
    plt.close()
    
    population = POM_data['Population (2016), 1000person'].unique().sum()*1000
    Group_Area
   
    fig, ax = plt.subplots()
    for i in sorted(POM_data.EAT_group.unique().tolist()):
        if i == 'fish':
            continue
        
        ax.plot(i, Group_Area['EAT'][i]/population, "gd")
        ax.plot(i, Group_Area['Org'][i]/population, "rd")
        
            
    #ax.title.set_text("Global per Capita Food Group Production (inc. waste & feed)")
    ax.grid(alpha = 0.5)
    ax.tick_params(labelrotation=90)
    plt.yticks(rotation = "horizontal")
    plt.ylabel("Land Use ha/person")
    #plt.ylim(0, 1)
    
    legend_elements = [Line2D([0], [0], lw = 0, marker='d', color='r', label='Current Diet\nTotal = '+str(round(Group_Area['Org'].sum()/population,1))+' ha/person',\
                              markerfacecolor='r'),
                       Line2D([0], [0], lw = 0, marker='d', color='g', label='EAT Lancet Diet\nTotal = '+str(round(Group_Area['EAT'].sum()/population,1))+' ha/person',\
                              markerfacecolor='g')]
    lg = ax.legend(handles=legend_elements, bbox_to_anchor=(1.0, 0.42), loc="lower left")
    #plt.legend(handles =[one, two])
    fig.savefig(figures+"Group land Share.png", bbox_extra_artists=(lg,), bbox_inches='tight', dpi = 400)
    plt.close()


    
    return