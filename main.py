import os
import time
import warnings
import pandas as pd
import numpy as np
from pandas.core.common import SettingWithCopyWarning

from functions import POM_build
from functions import Livestock_build
from functions import Livestock_area
from functions import Figures_build
from functions import Save_build
from functions import Crop_area
from functions import Extra_analysis
from functions import feed_eff_conv
from functions import land_use as LUfig
from functions import map_figures as Map

startTime = time.time()


warnings.filterwarnings('ignore')
warnings.simplefilter(action="ignore")
print('Code running...')

data = 'data/'
figures = 'figures/'
df_save = 'df/'

if not os.path.exists(figures):
    os.mkdir(figures)

if not os.path.exists(df_save):
    os.mkdir(df_save)

"""*** Scenario Builds ***"""

#INTERVENTION 1...Dietary changes
diet_change = False
if diet_change == False:
    #baseline EAT Lancet see: https://eatforum.org/eat-lancet-commission/eat-lancet-commission-summary-report/
    diet_main = [811, 39, 78, 126, 153, 30, 62, 19, 40, 284, 291, 450, 120]

else:
    # Half meat diet for second intervention
    # diet_main = [811, 39, 78, 126, 153, 15, 31, 9.5, 40, 311.4, 319.1, 450, 120]

    # Vegetarian diet for final intervention
    diet_main = [811, 39, 78, 126, 183, 0, 0, 9.5, 40, 320.4, 326.1, 450, 120]


#INTERVENTION 2&3...Yield changes
change_livestock_yields = False
change_feed_yields = False
change_crop_yields = False

#If false global average will be used. If true, a regional standard is selected.
regional_change_feed = False
regional_change_crop = False

feed_standard = 'Sub-SaharanAfrica'#'South&CentralAmerica'
livestock_standard = 'Sub-SaharanAfrica'#'South&CentralAmerica'
crop_standard = 'Sub-SaharanAfrica' #'Sub-SaharanAfrica'

#Regions which improve yields (Interventions 2 and 3) 
feed_regions = ['Sub-SaharanAfrica', 'SouthandSoutheastAsia', 'Sub-SaharanAfrica','SouthandSoutheastAsia', 'Europe', 'WestandCentralAsia', 'NorthAfrica', 'South&CentralAmerica', 'Other', 'IndustrializedAsia', 'Oceania'] #regions which improve feed yield.
livestock_regions = feed_regions #regions which improve livestock yield.
cr_y_regions = ['Sub-SaharanAfrica', 'SouthandSoutheastAsia', 'Sub-SaharanAfrica','SouthandSoutheastAsia', 'Europe', 'WestandCentralAsia', 'NorthAfrica', 'South&CentralAmerica', 'Other', 'IndustrializedAsia', 'Oceania'] #regions which improve crop yield.

#INTERVENTION 4...Minimum waste per item and supply chain stage
min_waste = False 

#INTERVENTION 5...Interventions 1-4 set to True. 
#INTERVENTION 6...Change nations diet to match a neighbors and expand int 2&3 to specific nations.
intervention_6 = False
crop_proxie = False
ls_proxie = False

feed_countries = ['Slovakia' , 'Haiti', 'Solomon Islands', 'Lebanon', 'Iraq', "Democratic People's Republic of Korea"]
livestock_countries = feed_countries
cr_y_countries = ['Slovakia', 'Haiti', 'Solomon Islands', 'Lebanon', 'Iraq']

if intervention_6 == False:
    feed_countries = []
    cr_y_countries = []
    livestock_countries = []

#Set nations which will use crop proxies and their source (lists much be aligned correctly)
diet_div_crop = ['Equatorial Guinea', 'Libya', 'South Sudan', 'Guyana', 'Eritrea']#,'Papua New Guinea']
diet_source_crop = ['Gabon', 'Egypt', 'Central African Republic', 'Suriname', 'Sudan']#, 'Indonesia']

#Set nations which will use livestock proxies
diet_div_ls = ['Equatorial Guinea', 'Libya', 'South Sudan', 'Guyana', 'Eritrea']
diet_source_ls = ['Gabon', 'Egypt', 'Central African Republic', 'Suriname', 'Sudan']

#Determine nations that only change livestock.
diet_ls_only = list(set(diet_div_crop) - set(diet_div_ls))
diet_ls_only_source = list(set(diet_source_crop) - set(diet_source_ls))

#Value of feed efficiency conversion for cow and lamb dairy
#Standard cow range = 1.82 - 1.03
#Standard lamb ange = 1.44 - 0.77
feed_conv_adj_cow = []
feed_conv_nat_cow = []

feed_conv_adj_lamb = [] 
feed_conv_nat_lamb = []

"""*** End scenario building ***"""



"""*** Build initial POM data according to FAO data ***"""
POM_data, meat_products, fish_products, FAO_animals, wastefractions, FAO_pop, POM_micro =\
    POM_build.data_build(crop_proxie, diet_div_crop, diet_source_crop, diet_ls_only, diet_ls_only_source, min_waste)


"""*** Determine food ratios based on waste-free diet ***"""
POM_data = POM_build.bau_diet_ratios(POM_data)


"""*** Calculate nutritional and nitrogen value of food being produced ***"""
POM_data = POM_build.nutrition(POM_data)


"""*** Build national eat lancet diets based on desired caloric ratios *** """
POM_data = POM_build.eat_diet_build(POM_data, wastefractions, diet_main)


#remove nations that can't provide all food groups.
#include nations that can provide protein sources even if it's not all of them.
unique_nations = POM_data.Area.unique().tolist()
food_groups = POM_data.EAT_group.unique().tolist()
protein_source = ["dairy foods", "beef, lamb and pork", "chicken and other poultry",\
              "eggs", "fish", "legumes", "nuts"]
#groups which the diet allows for NO consusmption
zero_groups = ['added sugars', 'potatoes and cassava']
missing_groups = protein_source + zero_groups
mand_groups = list(set(food_groups) - set(missing_groups))

global_pop = sum(POM_data['Population (2016), 1000person'].unique().tolist())
    
missing_items = {}
missing_some_items = {}

list_mi = []

# for nation in unique_nations:
    
#     POM_nation = POM_data.loc[POM_data.Area == nation]
#     nation_food_groups = POM_nation.EAT_group.unique().tolist()
#     if set(nation_food_groups) != set(food_groups):
#         if len(set(food_groups) - set(nation_food_groups)) > 2:
#             missing_items[nation] = set(food_groups) - set(nation_food_groups)
#             list_mi.append([nation, POM_nation.GROUP.unique().tolist()[0]])
#         else:
            
#             missing = set(food_groups) - set(nation_food_groups)

#             if any(elem in missing for elem in missing_groups) and len(missing) == 1:
#                 pass
#             elif all(elem in protein_source for elem in missing):
#                 pass
#             elif any(elem in missing for elem in missing_groups) == False and len(missing) > 1:
#                 missing_items[nation] = set(food_groups) - set(nation_food_groups)
#             else:
#                 missing_some_items[nation] = set(food_groups) - set(nation_food_groups)

for nation in unique_nations:
    POM_nation = POM_data.loc[POM_data.Area == nation]
    nation_food_groups = POM_nation.EAT_group.unique().tolist()
    if set(nation_food_groups) != set(food_groups):
        missing = set(food_groups) - set(nation_food_groups)
        if any(elem in missing for elem in mand_groups):
            missing_items[nation] = set(food_groups) - set(nation_food_groups)
            
        if any(elem in missing for elem in missing_groups):
            if len(set(food_groups) - set(nation_food_groups)) > 3:
                missing_items[nation] = set(food_groups) - set(nation_food_groups)
            else:
                missing_some_items[nation] = set(food_groups) - set(nation_food_groups)

d2 = {}
check_mis = set(missing_some_items) - set(missing_items)
for key in check_mis:
    if key in missing_some_items:
        d2[key] = missing_some_items[key]


POM_whole = POM_data
POM_whole_pop = POM_data.drop_duplicates('Area')
whole_pop = POM_whole_pop['Population (2016), 1000person'].sum()
print('Whole pop is:', whole_pop)
POM_data = POM_data[~POM_data["Area"].isin(missing_items.keys())]
#POM_data = POM_data[~POM_data["Area"].isin(missing_some_items.keys())]

POM_cant = POM_whole[~POM_whole['Area'].isin(POM_data['Area'].unique().tolist())]
POM_cant = POM_cant.drop_duplicates('Area')
cant_pop = POM_cant['Population (2016), 1000person'].sum()

POM_can = POM_whole[POM_whole['Area'].isin(POM_data['Area'].unique().tolist())]
POM_can = POM_can.drop_duplicates('Area')
can_pop = POM_can['Population (2016), 1000person'].sum()

POM_temp = POM_data.drop_duplicates('Area')
glob_pop = POM_temp['Population (2016), 1000person'].sum()
print('Sub pop is: ', glob_pop)
POM_temp = POM_temp[['Area', 'avg height', 'avg weight', 'Cal Provided', 'Protein Needed (g)','Fat Provided']]


print(f"Calories provided: {POM_temp['Cal Provided'].mean()}")
print(f"Fat provided: {POM_temp['Fat Provided'].mean()}")
print(f"Protein Needed/Provided: {POM_temp['Protein Needed (g)'].mean()}")

food_items = []
for nation in POM_data.Area.unique().tolist():
    POM_temp = POM_data.loc[POM_data.Area == nation]
    food_items.append(len(POM_temp))

print(np.mean(food_items))




"""***Determine the feed needed for livestock ***"""
#get baseline livestock data and yields
FAO_Livestock = Livestock_build.livestock_pom(POM_data, FAO_animals, ls_proxie, diet_div_ls, diet_source_ls, FAO_pop)

#build feed demand based on number of animals
POM_data, FAO_LSU_Coeffs, beef_items, beef_milk_items, lamb_items, lamb_milk_items, feed_list, POM_protein_feed,\
    global_beef_milk_in, feed_dict, feed_detail, feed_lamb = Livestock_build.feed_demand(POM_data, FAO_Livestock, change_livestock_yields,\
                                     livestock_standard,livestock_regions, livestock_countries)


"""*** Graph production per capita per eat group ***"""
POM_global, Org_food, EAT_food, diet_df = Figures_build.production_by_group(POM_data)


"""*** Data save ***"""
Save_build.save_data(POM_global, POM_data)


"""*** Determine Land Use of data ***"""
FAO_Livestock, Meat_Area, Meat_Area_group, Meat_group = Livestock_area.livestock_area(FAO_Livestock, FAO_LSU_Coeffs, POM_data,\
                                beef_items, beef_milk_items, lamb_items, lamb_milk_items, ls_proxie, diet_div_ls, diet_source_ls)

POM_data = feed_eff_conv.feed_eff_conv(feed_detail, feed_lamb, POM_data,\
                                       FAO_Livestock, feed_conv_adj_lamb, feed_conv_nat_lamb, feed_conv_adj_cow, feed_conv_nat_cow)
    
"""*** Determine crop Land Use ***"""
FAO_Crops, FAO_Crop_yield, yield_avg_feed, yield_avg_crop, global_avg_feed, global_avg_crop = \
    Crop_area.crop_yield(POM_data, fish_products, meat_products, feed_list,\
                         crop_proxie, diet_div_crop, diet_source_crop)

       
        
"""*** Determine crop are after yield adjustments ***"""                             
FAO_all_crops_area, Crops_group_area, FAO_all_crops, FAO_all_crops_group =\
    Crop_area.crop_area(FAO_Crops, yield_avg_feed, change_feed_yields,regional_change_feed,feed_standard,feed_regions,\
              feed_countries,global_avg_feed,change_crop_yields,regional_change_crop,yield_avg_crop,crop_standard,\
                  cr_y_regions,cr_y_countries,global_avg_crop)


"""*** Determine area of crops for feed to break down Int vs Ext meat ***"""
Feed_crops_area_sum, Weighted_final = Crop_area.feed_crop_area(FAO_Crops, POM_protein_feed, feed_list, FAO_Livestock, POM_data)


"""*** Area mapping ***"""
Total_Area = pd.concat([Meat_Area, FAO_all_crops_area])
Group_Area = pd.concat([Meat_group, FAO_all_crops_group])
Group_Area = Group_Area.set_index('EAT_group')

POM_cal = POM_data[~POM_data["group"].isin(meat_products)]
POM_cal = POM_cal[~POM_cal["group"].isin(fish_products)]
POM_cal = POM_cal[POM_cal["POM (no waste)"] != 0]


"""*** Save area data***"""
Save_build.save_area_data(Meat_Area, FAO_all_crops_area, Feed_crops_area_sum, Weighted_final, FAO_pop, Total_Area, POM_data)

#%%
"""*** Build Maps ***"""
LUfig.Area_data()
Map.PopDensity() 
final_df = Map.MapWorld(diet_div_crop, diet_div_ls)

final_df_cant = final_df.loc[final_df['ratio'] > 100]
final_df_can = final_df.loc[final_df['ratio'] <= 100]

impossible_nations = {**missing_items, **missing_some_items}
imp_nations_df = pd.DataFrame()
imp_nations_df['Area'] = pd.DataFrame(impossible_nations.keys())
imp_nations_df = pd.concat([imp_nations_df, final_df_cant['Countries']])


#%%
"""*** End Run ***"""
print ('Run compelte.')
executionTime = (time.time() - startTime)/60
print('Execution time in minutes: ' + str(round(executionTime,3)))
print('Results added to the figures subfolder.')


