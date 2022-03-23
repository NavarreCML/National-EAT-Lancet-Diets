 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 11:41:47 2020

@author: nicolasnavarre
"""

import numpy as np 
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pickle
import math
import cartopy.crs as ccrs
mol = ccrs.Mollweide()


def MapWorld(diet_div_crop, diet_div_ls):

    
    data = "data/"
    figures = 'figures/'
    df_save = "df/"

    
    final_df = pickle.load(open(df_save+"final_df", "rb" ))

    df_world = gpd.read_file(data+'CNTR_RG_10M_2016_3857.shp/CNTR_RG_10M_2016_3857.shp')
    df_world = df_world.to_crs(mol.proj4_init)
    
    df_world_org = df_world
    
    df_world['NAME_ENGL'][14] = "Côte D’Ivoire"

    for i in final_df.index:
        if final_df["Countries"][i] == "United States of America":
            final_df["Countries"][i] = "United States"
        if final_df["Countries"][i] == "Viet Nam":
            final_df["Countries"][i] = "Vietnam"
        if final_df["Countries"][i] == "Venezuela (Bolivarian Republic of)":
            final_df["Countries"][i] = "Venezuela"
        if final_df["Countries"][i] == "Republic of Korea":
            final_df["Countries"][i] = "South Korea"
        if final_df["Countries"][i] == "Republic of Moldova":
            final_df["Countries"][i] = "Moldova"
        if final_df["Countries"][i] == "Myanmar":
            final_df["Countries"][i] = "Myanmar/Burma"
        if final_df["Countries"][i] == "Iran (Islamic Republic of)":
            final_df["Countries"][i] = "Iran"
        if final_df["Countries"][i] == "Democratic Republic of the Congo":
            final_df["Countries"][i] = "Democratic Republic of The Congo"
        if final_df["Countries"][i] == "Cabo Verde":
            final_df["Countries"][i] = "Cape Verde"
        if final_df["Countries"][i] == "Bolivia (Plurinational State of)":
            final_df["Countries"][i] = "Bolivia"
        if final_df["Countries"][i] == "Democratic People's Republic of Korea":
            final_df["Countries"][i] = "North Korea"
        if final_df["Countries"][i] == "Republic of Korea":
            final_df["Countries"][i] = "South Korea"
        if final_df["Countries"][i] == "Côte d'Ivoire":
            final_df["Countries"][i] = "Côte D’Ivoire"
        if final_df["Countries"][i] == "Lao People's Democratic Republic":
            final_df["Countries"][i] = "Laos"
        if final_df["Countries"][i] == "China, mainland":
            final_df["Countries"][i] = "China"
        if final_df["Countries"][i] == "Syrian Arab Republic":
            final_df["Countries"][i] = "Syria"
        if final_df["Countries"][i] == "Saint Vincent and the Grenadines":
            final_df["Countries"][i] = "Saint Vincent and The Grenadines"
        if final_df["Countries"][i] == "Sao Tome and Principe":
            final_df["Countries"][i] = "São Tomé and Príncipe"

            
    
    countries = list(final_df["Countries"])
    
    #Drop countries where there is no FAO data from the dataset
    for i in df_world.index:
        if df_world["NAME_ENGL"][i] not in countries:
            df_world = df_world.drop([i])
    
    
    countries = list(df_world["NAME_ENGL"])
    for i in final_df.index:
        if final_df["Countries"][i] not in countries:
            final_df = final_df.drop([i])
        
    
    #for i in final_df.index:
    #    if final_df['Countries'][i] in diet_div_crop or final_df['Countries'][i] in diet_div_ls:
    #        continue
        
        
        # if final_df['Org area'][i] > final_df['Value'][i]:
        #     final_df['Value'][i] = final_df['Org area'][i]
        #     factor = final_df['Value'][i]/final_df['Org area'][i]
        #     final_df['Org area'][i] = final_df['Org area'][i] * factor 
        #     final_df['Ha'][i] = final_df['Ha'][i] * factor 
            
    #final_df.loc[final_df['Countries'] == 'United Arab Emirates', 'Ha'] = 0.651597971469832*10**6

    
    
    final_df['ratio'] = final_df["Ha"] / final_df["Value"] * 100
    
    
    #final_df = pd.read_excel('all_four.xlsx')
    
    df_gradient = pd.merge(df_world, final_df, left_on = "NAME_ENGL", right_on = "Countries")
    #for i in df_gradient.index:
    #    if df_gradient['Value'][i] < 100000:
    #        df_gradient = df_gradient.drop([i])
    #    elif df_gradient['NAME_ENGL'][i] == 'Cyprus':
    #        df_gradient = df_gradient.drop([i])

    
    #max_range = int(math.ceil(max(df_gradient["ratio"])))
    max_range = 500
    
    fig = plt.figure(figsize = (10,10))
    #ax.set_title('Land Use Requirements Needed to Satisfy EAT Lancet Diet')
    #ax.set_ylim(-0.8*10**7, 1.9*10**7)
    ax = fig.add_subplot(1, 1, 1, projection=mol)
    #ax = fig.add_subplot(1, 1, 1)
    ax.set_facecolor('lightblue')
    
    df_world_org.plot(ax = ax, color = 'lightgrey', edgecolor = 'black', linewidth=0.5)
    
    colors_undersea = plt.cm.Greens_r(np.linspace(0.3, 0.85, 256))
    colors_mid = plt.cm.spring_r(np.linspace(0, 0.4, 100))
    colors_land = plt.cm.hot_r(np.linspace(0.45, 0.85, 200))
    all_colors = np.vstack((colors_undersea, colors_mid, colors_land))
    terrain_map = colors.LinearSegmentedColormap.from_list('RdYlGn_r', all_colors)
    
    df_gradient.plot(ax = ax, column = 'ratio', cmap=terrain_map,
                    legend = True, edgecolor = 'black', linewidth = 0.5,
                    scheme='user_defined', classification_kwds={'bins':[50, 75, 100, 125, 150,200,100000]},
                    legend_kwds={'loc':'lower left',
                              'title': 'Percent of Agricultural\nLand Needed (%)',
                              'bbox_to_anchor':(1, 0.3)},
                    )
    
    legend_labels = ['< 50 %', 
                    '50 - 75', 
                    '75 - 100', 
                    '100 - 125',
                    '125 - 150', 
                    '150 - 200', 
                    '> 200 %']
    
    leg = ax.get_legend()
    for text, label in zip(leg.get_texts(), legend_labels):
        text.set_text(label)
        
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    
    fig.savefig(figures+'EAT Land Use Requirements.jpg', dpi = 400, bbox_inches = 'tight')

    final_df['ppl/ag land'] = (final_df['Population']*1000)/final_df['Value']
    final_df['land used share'] = final_df['ratio']/100
    
    for i in final_df.index: 
        if final_df['Countries'][i] == 'New Caledonia':
            final_df = final_df.drop([i])
    final_df['Ha'] *= 1/10**6 
    final_df['Org area'] *= 1/10**6 
    final_df['Value'] *= 1/10**6
    final_df = final_df.drop_duplicates(subset = ['Countries'], keep='first')
    #plt.close()
        
    return final_df

def PopDensity():

    data = 'data/'
    figures = 'figures/'
    df_save = 'df/'
    
    
    final_df = pickle.load(open(df_save+"final_df", "rb" ))
    
    df_world = gpd.read_file(data+'CNTR_RG_10M_2016_3857.shp/CNTR_RG_10M_2016_3857.shp')
    df_world = df_world.to_crs(mol.proj4_init)
    
    df_world['NAME_ENGL'][14] = "Côte D’Ivoire"

    df_world_org = df_world
    
 
    
    for i in final_df.index:
        if final_df["Countries"][i] == "United States of America":
            final_df["Countries"][i] = "United States"
        if final_df["Countries"][i] == "Viet Nam":
            final_df["Countries"][i] = "Vietnam"
        if final_df["Countries"][i] == "Venezuela (Bolivarian Republic of)":
            final_df["Countries"][i] = "Venezuela"
        if final_df["Countries"][i] == "Republic of Korea":
            final_df["Countries"][i] = "South Korea"
        if final_df["Countries"][i] == "Republic of Moldova":
            final_df["Countries"][i] = "Moldova"
        if final_df["Countries"][i] == "Myanmar":
            final_df["Countries"][i] = "Myanmar/Burma"
        if final_df["Countries"][i] == "Iran (Islamic Republic of)":
            final_df["Countries"][i] = "Iran"
        if final_df["Countries"][i] == "Democratic Republic of the Congo":
            final_df["Countries"][i] = "Democratic Republic of The Congo"
        if final_df["Countries"][i] == "Cabo Verde":
            final_df["Countries"][i] = "Cape Verde"
        if final_df["Countries"][i] == "Bolivia (Plurinational State of)":
            final_df["Countries"][i] = "Bolivia"
        if final_df["Countries"][i] == "Democratic People's Republic of Korea":
            final_df["Countries"][i] = "North Korea"
        if final_df["Countries"][i] == "Republic of Korea":
            final_df["Countries"][i] = "South Korea"
        if final_df["Countries"][i] == "Côte d'Ivoire":
            final_df["Countries"][i] = "Côte D’Ivoire"
        if final_df["Countries"][i] == "Lao People's Democratic Republic":
            final_df["Countries"][i] = "Laos"
        if final_df["Countries"][i] == "China, mainland":
            final_df["Countries"][i] = "China"
        if final_df["Countries"][i] == "Syrian Arab Republic":
            final_df["Countries"][i] = "Syria"
    
    
    countries = list(final_df["Countries"])
    
    #Drop countries where there is no CircuMAT data from the dataset
    for i in df_world.index:
        if df_world["NAME_ENGL"][i] not in countries:
            df_world = df_world.drop([i])
    
    
    countries = list(df_world["NAME_ENGL"])
    for i in final_df.index:
        if final_df["Countries"][i] not in countries:
            final_df = final_df.drop([i])
    
    final_df['ratio'] = final_df["Ha"] / final_df["Value"] * 100
    df_gradient = pd.merge(df_world, final_df, left_on = "NAME_ENGL", right_on = "Countries")
    
    for i in df_gradient.index:
        if df_gradient['Value'][i] < 100000:
            df_gradient = df_gradient.drop([i])
        elif df_gradient['NAME_ENGL'][i] == 'Cyprus':
            df_gradient = df_gradient.drop([i])
    
    df_gradient['Population'] = pd.to_numeric(df_gradient['Population'], downcast="float")
    df_gradient['ratio'] = (df_gradient['Population'] * 1000) / df_gradient['Value']
    
    max_range = int(math.ceil(max(df_gradient["ratio"])))
    max_range = 30

    #crs1 = ccrs.Mollweide()
    #fig, ax = plt.subplots(figsize = (10,10))#, subplot_kw={'projection': 'mollweide'})
    
    #fig = plt.figure(figsize = (10,10))
    #ax.set_title('Land Use Requirements Needed to Satisfy EAT Lancet Diet')
    #ax.set_ylim(-0.8*10**7, 1.9*10**7)
    #ax = fig.add_subplot(1, 1, 1, projection=mol)
    #ax = fig.add_subplot(1, 1, 1)
    #ax.set_facecolor('lightblue')
    
    #ax.add_geometries(df_world['geometry'], crs=crs1, linewidth=0.5)
    # this adds the ocean coloring
    #ax.add_feature(cartopy.feature.OCEAN, facecolor='lightblue', edgecolor='none')
    #ax = plt.subplot(111, projection="mollweide")
    #ax.set_title('Population Density of People per Ha of Agricultural Land')
    #ax.set_ylim(-0.8*10**7, 1.9*10**7)
    #ax.set_facecolor('lightblue')
    
    
    fig = plt.figure(figsize = (10,10))
    #ax.set_title('Land Use Requirements Needed to Satisfy EAT Lancet Diet')
    #ax.set_ylim(-0.8*10**7, 1.9*10**7)
    ax = fig.add_subplot(1, 1, 1, projection=mol)
    #ax = fig.add_subplot(1, 1, 1)
    ax.set_facecolor('lightblue')
    
    
    df_world_org.plot(ax = ax, color = 'lightgrey', edgecolor = 'black', linewidth=0.5)
    
    colors_undersea = plt.cm.Greens_r(np.linspace(0.3, 0.85, 256))
    colors_mid = plt.cm.spring_r(np.linspace(0, 0.4, 100))
    #colors_mid2 = plt.cm.cool(np.linspace(0, 0.4, 100))
    colors_land = plt.cm.hot_r(np.linspace(0.45, 0.85, 200))
    #colors_land = plt.cm.jet(np.linspace(0.6, 1, 256))
    #colors_undersea = plt.cm.winter(np.linspace(0.5, 1, 256))
    #colors_land = plt.cm.rainbow(np.linspace(0.7, 0.9, 256))
    all_colors = np.vstack((colors_undersea, colors_mid, colors_land))
    terrain_map = colors.LinearSegmentedColormap.from_list('RdYlGn_r', all_colors)
    
    #colors_undersea = plt.cm.Spectral_r(np.linspace(0.2, 0.4, 256))
    #colors_land = plt.cm.Spectral_r(np.linspace(0.7, 0.9, 256))
    #all_colors = np.vstack((colors_undersea, colors_land))
    #terrain_map = colors.LinearSegmentedColormap.from_list('RdYlGn_r', all_colors)
    
    
    temp_list = list(final_df['ratio'])
    
    df_gradient.plot(ax = ax, column = 'ratio', cmap=terrain_map,
                    legend = True, edgecolor = 'black', linewidth = 0.5,
                    scheme='User_Defined', classification_kwds={'bins':[1, 2, 3, 4, 5, 10, 30]},
                    legend_kwds={'loc':'lower left',
                              'title': 'People / Ha (Agr. Land)',
                              'bbox_to_anchor':(1, 0.3)},
                    )
    
    
    legend_labels = ['< 1', 
                    '1 - 2', 
                    '2 - 3', 
                    '3 - 4',
                    '4 - 5', 
                    '5 - 10', 
                    '> 10']
    
    leg = ax.get_legend()
    for text, label in zip(leg.get_texts(), legend_labels):
        text.set_text(label)
        
    #fig, ax = plt.subplots(figsize = (10,10), subplot_kw={'projection': 'mollweide'})
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    
    fig.savefig(figures+'Population Density.jpg', dpi = 400, bbox_inches = 'tight')
    plt.close()