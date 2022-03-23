#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:42:36 2021

@author: nicolasnavarre
"""
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


figures = 'figures/'

def production_by_group(POM_data):
    POM_global = pd.DataFrame() 
    POM_global ["Org"] = POM_data.groupby(["Area"]).apply(lambda x: x["Org per Capita (with waste & feed)"].sum())
    POM_global ["EAT"] = POM_data.groupby(["Area"]).apply(lambda x: x["EAT per Capita (with waste & feed)"].sum())
    


    import numpy as np
    for j in POM_data['GROUP'].unique().tolist():  
        
        food_list_eat = []
        food_list_org = []
        group_list = []
        
        diet_df = pd.DataFrame()
        width = 0.35
        
        fig, ax = plt.subplots()
        
        temp_count = 0
        temp_counteat = 0
        food_data = POM_data.groupby(["EAT_group"]).apply(lambda x: (x["POM"].sum()/(x["Population (2016), 1000person"].sum()*1000)))
        if j == 'Other':
            continue
        for i in food_data.index:
        
            df_temp = POM_data.loc[(POM_data['EAT_group'] == i) & (POM_data['GROUP'] == j)]
            
            df_pop = df_temp[['Area', 'Population (2016), 1000person']]
            df_pop = df_pop.drop_duplicates()
            
            Org_avg = df_temp.groupby(["Area"]).apply(lambda x: (x["POM Org (with waste & feed)"].sum()))
            EAT_avg = df_temp.groupby(["Area"]).apply(lambda x: (x["POM EAT (with waste & feed)"].sum()))
            
            Org_avg = pd.DataFrame(Org_avg)
            Org_avg = Org_avg.reset_index()
            Org_avg = pd.merge(Org_avg, df_pop, on = 'Area', how = 'left')
            
            Org_avg = Org_avg.rename(columns = {0 : 'food'})
            Org_food = ((Org_avg['food'] * 1000 * 1000 * 1000) / 365 ).sum() / (Org_avg["Population (2016), 1000person"] * 1000).sum()
            
            EAT_avg = pd.DataFrame(EAT_avg)
            EAT_avg = EAT_avg.reset_index()
            EAT_avg = pd.merge(EAT_avg, df_pop, on = 'Area', how = 'left')
        
            EAT_avg = EAT_avg.rename(columns = {0 : 'food'})
            EAT_food = ((EAT_avg['food'] * 1000 * 1000 * 1000) / 365 ).sum() / (EAT_avg["Population (2016), 1000person"] * 1000).sum()
            
            
            temp_count += Org_food
            temp_counteat += EAT_food
            
            food_list_eat.append(EAT_food)
            food_list_org.append(Org_food)
            group_list.append(i)
         
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
        legend_elements = [Line2D([0], [0], lw = 0, marker='s', color='r', label='Current Diet\nTotal = '+str(int(temp_count))+' g/d',\
                                  markerfacecolor='r'),
                            Line2D([0], [0], lw = 0, marker='s', color='g', label='EAT Lancet Diet\nTotal = '+str(int(temp_counteat))+' g/d',\
                                  markerfacecolor='g')]
        lg = ax.legend(handles=legend_elements)
        fig.savefig(figures+j+" EAT_Group Production.png", bbox_extra_artists=(lg,), bbox_inches='tight', dpi = 400)

        
        
        plt.close()
    
    plt.close()
        
        
    temp_count = 0
    temp_counteat = 0
    food_data = POM_data.groupby(["EAT_group"]).apply(lambda x: (x["POM"].sum()/(x["Population (2016), 1000person"].sum()*1000)))
    x_labels = []
    eat_bar = []
    org_bar = []
    group_list = []
    food_list_eat = []
    food_list_org = []
    cal_list_eat = []
    cal_list_org = []
    diet_df = pd.DataFrame()
    extra_nations = ['Puerto Rico', 'Palestine', 'Greenland', 'Falkland Islands (Malvinas)'\
                     'New Caledonia', 'China', 'China, Taiwan Province of' ]
    POM_data['OrgCal perD']= ((POM_data['POM (no waste)']*10**9)/365 * POM_data['calories per g'])/(POM_data["Population (2016), 1000person"]*1000)
    for i in food_data.index:

        df_temp = POM_data.loc[(POM_data['EAT_group'] == i)]
        
        df_pop = df_temp[['Area', 'Population (2016), 1000person']]
        df_pop = df_pop.drop_duplicates()
        
        Org_avg = df_temp.groupby(["Area"]).apply(lambda x: (x["POM Org (with waste & feed)"].sum()))
        EAT_avg = df_temp.groupby(["Area"]).apply(lambda x: (x["POM EAT (with waste & feed)"].sum()))
        Org_cal = df_temp.groupby(["Area"]).apply(lambda x: (x["OrgCal perD"].sum()))
        EAT_cal = df_temp.groupby(["Area"]).apply(lambda x: (x["Cal Needed"].sum()))
        
        Org_avg = pd.DataFrame(Org_avg)
        Org_avg = Org_avg.reset_index()
        Org_avg = pd.merge(Org_avg, df_pop, on = 'Area', how = 'left')
    
        Org_avg = Org_avg.rename(columns = {0 : 'food'})
        Org_avg = Org_avg[Org_avg['Population (2016), 1000person'] != 0]
        Org_avg = Org_avg[~Org_avg['Area'].isin(extra_nations)]
        
        Org_food = ((Org_avg['food'] * 1000 * 1000 * 1000) / 365 ).sum() / (Org_avg["Population (2016), 1000person"] * 1000).sum()
        
        EAT_avg = pd.DataFrame(EAT_avg)
        EAT_avg = EAT_avg.reset_index()
        
        EAT_avg = pd.merge(EAT_avg, df_pop, on = 'Area', how = 'left')
   
        EAT_avg = EAT_avg.rename(columns = {0 : 'food'})
        EAT_avg = EAT_avg[EAT_avg['Population (2016), 1000person'] != 0]
        EAT_avg = EAT_avg[~EAT_avg['Area'].isin(extra_nations)]
        EAT_food = ((EAT_avg['food'] * 1000 * 1000 * 1000) / 365 ).sum() / (EAT_avg["Population (2016), 1000person"] * 1000).sum()
        
        Org_cal = pd.DataFrame(Org_cal)
        Org_cal = Org_cal.reset_index()
        Org_cal = pd.merge(Org_cal, df_pop, on = 'Area', how = 'left')
        
        Org_cal = Org_cal.rename(columns = {0 : 'cal'})
        Org_cal = Org_cal[Org_cal['Population (2016), 1000person'] != 0]
        Org_cal = Org_cal[~Org_cal['Area'].isin(extra_nations)]
        Org_cal_food = Org_cal['cal'].sum()/ len(Org_cal['cal'])
        
        EAT_cal = pd.DataFrame(EAT_cal)
        EAT_cal = EAT_cal.reset_index()
        EAT_cal = pd.merge(EAT_cal, df_pop, on = 'Area', how = 'left')
        
        EAT_cal = EAT_cal.rename(columns = {0 : 'cal'})
        EAT_cal = EAT_cal[EAT_cal['Population (2016), 1000person'] != 0]
        EAT_cal = EAT_cal[~EAT_cal['Area'].isin(extra_nations)]
        EAT_cal_food = EAT_cal['cal'].sum()/ len(EAT_cal['cal'])

        group_list.append(i)
        food_list_eat.append(EAT_food)
        food_list_org.append(Org_food)
        cal_list_eat.append(EAT_cal_food)
        cal_list_org.append(Org_cal_food)
        
        x_labels.append(i)
        eat_bar.append(EAT_food/1000)
        org_bar.append(Org_food/1000)
        
        temp_count += Org_food
        temp_counteat += EAT_food
    
    diet_df['group'] = group_list
    diet_df['gF EAT'] = food_list_eat
    diet_df['gF Org'] = food_list_org
    diet_df['Cal EAT'] = cal_list_eat
    diet_df['Cal Org'] = cal_list_org
    
    df_plot = diet_df
    df_plot['dif'] = df_plot["gF Org"] - df_plot["gF EAT"] 
    df_plot = df_plot.sort_values(by=['dif'], ascending=False)
    
    df_plot = diet_df
    df_plot['dif'] = df_plot["gF Org"] - df_plot["gF EAT"] 
    df_plot = df_plot.sort_values(by=['dif'], ascending=False)
    
    
    x = np.arange(len(x_labels))
    width = 0.35
    #fig, ax = plt.subplots()
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw = {"height_ratios":[1,10]})
    fig.subplots_adjust(hspace=0.10)
    
    ax1.bar(x + width/2, df_plot['gF EAT'], width, label='EAT Diet', color = 'g')
    ax1.bar(x - width/2, df_plot['gF Org'], width, label='BAU Diet', color = 'r')
    ax2.bar(x + width/2, df_plot['gF EAT'], width, label='EAT Diet', color = 'g')
    ax2.bar(x - width/2, df_plot['gF Org'], width, label='BAU Diet', color = 'r')
    
    ax1.set_ylim(3000, 3150)  # outliers only
    ax2.set_ylim(0, 2350)  # most of the data
    
    ax1.spines['bottom'].set_visible(False)
    ax1.xaxis.tick_top()
    ax1.tick_params(axis='x', length = 0)  # don't put tick labels at the top
    
    ax2.spines['top'].set_visible(False)
    ax2.xaxis.tick_bottom()
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_plot['group'])
    plt.xticks(rotation = 90)
    plt.ylabel('Prod/capita (g/person-day)')
    
    ax1.axvspan(-0.5, 8.5, facecolor='0.2', alpha=0.25, zorder=-100)
    ax2.axvspan(-0.5, 8.5, facecolor='0.2', alpha=0.25, zorder=-100)
    
    legend_elements = [Line2D([0], [0], lw = 0, marker='s', color='r', label='Current Diet\nTotal = '+str(int(temp_count))+' g/d',\
                              markerfacecolor='r'),
                       Line2D([0], [0], lw = 0, marker='s', color='g', label='EAT Lancet Diet\nTotal = '+str(int(temp_counteat))+' g/d',\
                              markerfacecolor='g'),
                       Line2D([0], [0], lw = 0, marker='s', color='0.2', alpha=0.25, label='Reduction in production',\
                              markerfacecolor='0.2')]
    lg = ax2.legend(handles=legend_elements, loc='upper right')
    fig.savefig(figures+"Bar-graph.png", bbox_extra_artists=(lg,), bbox_inches='tight', dpi = 400)
    plt.close()

    
    return POM_global, Org_food, EAT_food, diet_df