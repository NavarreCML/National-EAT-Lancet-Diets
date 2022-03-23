import pandas as pd
import numpy as np
from functions import fao_regions as regions

data = 'data/'

def data_build(crop_proxie, diet_div_crop, diet_source_crop, diet_ls_only, diet_ls_only_source, min_waste):

    """*** Import of country data to build national diets ***"""
    WPR_height = pd.read_csv(r"data/worldpopulationreview_height_data.csv")
    WPR_height.loc[WPR_height.Area == "North Korea", "Area"] = "Democratic People's Republic of Korea"
    Countrycodes = pd.read_csv(r"data/countrycodes.csv", sep = ";")
    #FAO_pop = pd.read_excel(data+"/FAOSTAT_Population_v3.xlsx")
    FAO_pop = pd.read_excel(data+"/FAOSTAT_2018_population.xlsx")
    FAO_pop.loc[FAO_pop.Area == "Cote d'Ivoire", "Area"] = "Côte d'Ivoire"
    FAO_pop.loc[FAO_pop.Area == "French Guyana", "Area"] = "French Guiana"
    FAO_pop.loc[FAO_pop.Area == "RÃ©union", "Area"] = "Réunion"
    
    """*** Import and sorting of data ***"""
    FAO_crops = pd.read_csv(data+"/FAOSTAT_crop Production.csv")
    FAO_crops["group"] = FAO_crops.apply(lambda x: regions.group(x["Item Code"]), axis=1)
    FAO_crops = FAO_crops.rename(columns={"Value" : "Production"})
    FAO_crops["Production"] = FAO_crops["Production"] / 1000
    FAO_crops["Unit"] = "1000 tonnes"
    
    FAO_animals = pd.read_csv(data+"/FAO_animal_prod_2016.csv")
    FAO_animals["group"] = FAO_animals.apply(lambda x: regions.group(x["Item Code"]), axis=1)
    FAO_animals.loc[FAO_animals.Area == "United Kingdom of Great Britain and Northern Ireland", "Area"] = "United Kingdom"
    FAO_animals = FAO_animals.rename(columns={"Value" : "Production"})
    FAO_animals.drop(FAO_animals[FAO_animals.Unit != 'tonnes'].index, inplace = True)
    FAO_animals["Production"] = FAO_animals["Production"] / 1000
    FAO_animals["Unit"] = "1000 tonnes"
    
    FAO_animals_5 = pd.read_csv(data+"/FAOSTAT_animal_prod_5.csv")
    FAO_animals_5["group"] = FAO_animals_5.apply(lambda x: regions.group(x["Item Code (FAO)"]), axis=1)
    FAO_animals_5.loc[FAO_animals_5.Area == "United Kingdom of Great Britain and Northern Ireland", "Area"] = "United Kingdom"
    FAO_animals_5 = FAO_animals_5.rename(columns={"Value" : "Production"})
    FAO_animals_5.drop(FAO_animals_5[FAO_animals_5.Unit != 'tonnes'].index, inplace = True)
    FAO_animals_5["Production"] = FAO_animals_5["Production"] / 1000
    FAO_animals_5["Unit"] = "1000 tonnes"
    FAO_animals_5 = FAO_animals_5.groupby(['Area', 'Item']).mean().reset_index()
    
    FAO_animals = pd.merge(FAO_animals, FAO_animals_5[['Area', 'Item', 'Production']], on = ["Area", "Item"], how = 'left')
    FAO_animals["Production"] = FAO_animals["Production_y"]
    FAO_animals = FAO_animals.drop(columns = ["Production_x", "Production_y"])

    
    FAO_fish = pd.read_csv(data+"FAOSTAT_Fish.csv")
    FAO_fish = FAO_fish.rename(columns={"Value" : "Production"})
    FAO_fish["group"] = FAO_fish.apply(lambda x: regions.group(x["Item Code"]), axis=1)
    
    meat_products = ["eggs", "beef and lamb", "chicken and other poultry",\
                     "pork", "whole milk or derivative equivalents"]
    
    fish_products = ["Freshwater Fish", "Demersal Fish", "Pelagic Fish",\
                     "Marine Fish, Other", "Crustaceans", "Cephalopods",\
                     "Molluscs, Other", "Meat, Aquatic Mammals", "Aquatic Animals, Others",
                     "Aquatic Plants", "Fish, Body Oil", "Fish, Liver Oil"]
    
    other_items = ["Honey, natural", "Beeswax", "Silk-worm cocoons, reelable"]
    other_items = ["Beeswax", "Silk-worm cocoons, reelable"]

    """*** Import of protein data ***"""
    FAO_Protein = pd.read_csv(data+"protein.csv")
    FAO_Protein["group"] = FAO_Protein["group"].str.replace("dairy", "whole milk or derivative equivalents")
    FAO_Protein = FAO_Protein.rename(columns = {"Country": "Area"})
    
    """*** Build main dataframe ***"""
    POM_data = pd.concat([FAO_crops])
    FAO_pop_temp = FAO_pop.set_index("Area")
    if crop_proxie == True:
        for i,j in zip(diet_ls_only, diet_ls_only_source):
            fao_fix = POM_data.loc[POM_data.Area == j]
            fao_fix['Area'] = i
            
            factor = FAO_pop_temp['Value'][i] / FAO_pop_temp['Value'][j]
            fao_fix['Production'] *= factor
            
            POM_data = POM_data[POM_data.Area != i]
            POM_data = pd.concat([POM_data,fao_fix])

    
    POM_data = pd.concat([POM_data, FAO_animals, FAO_fish])
    
    if crop_proxie == True:
        for i,j in zip (diet_div_crop, diet_source_crop): 
            fao_fix = POM_data.loc[POM_data.Area == j]
            fao_fix['Area'] = i
            
            factor = FAO_pop_temp['Value'][i] / FAO_pop_temp['Value'][j]
           
            fao_fix['Production'] *= factor
            
            POM_data = POM_data[POM_data.Area != i]
            POM_data = pd.concat([POM_data,fao_fix])

    
 
    POM_data = POM_data.reset_index()
    """*** Food source scenarios ***"""
    
    POM_data = POM_data.reset_index(drop = True)
    POM_data = POM_data[~POM_data.Item.isin(other_items)]
    POM_data = POM_data.rename(columns={"group" : "group_nf"})
    POM_data["Production"].clip(lower = 0, inplace = True)
    
    POM_data = pd.merge(POM_data, WPR_height, on = ["Area"], how = 'left')
    POM_data = pd.merge(POM_data, Countrycodes, left_on = "Area", right_on = "COUNTRY", how = 'left')
    POM_data = pd.merge(POM_data, FAO_pop[["Area", "Value"]], on = ["Area"], how = 'left')
    POM_data = POM_data.rename(columns={"Value" : "Population (2016), 1000person"})
    
        
    """*** Fix China data from China to China, mainland to seperate out Taiwan ***"""
    POM_data.loc[POM_data.Area == 'China, mainland', 'REGION'] = 'CHN'
    POM_data.loc[POM_data.Area == 'China, mainland', 'CODE'] = '156'
    temp_height = POM_data['avg height'][1761]
    temp_weight = POM_data['avg weight'][1761]
    POM_data.loc[POM_data.Area == 'China, mainland', 'avg height'] = temp_height
    POM_data.loc[POM_data.Area == 'China, mainland', 'avg weight'] = temp_weight
    POM_data.drop(POM_data[POM_data.Area == 'China'].index)
    POM_data = POM_data.reset_index(drop = True)
    
    """ Remove microstates """
    FAO_land = pd.read_csv(data+"FAOSTAT_Ag Land.csv")
    FAO_land = FAO_land.rename(columns={"Value" : "1000 Ha"})
    POM_data = pd.merge(POM_data, FAO_land[["Area", "1000 Ha"]], on = ["Area"], how = 'left')
    
    France_ot = ['French Guiana', 'Guadeloupe', 'Martinique', 'Réunion']
    for overseas in France_ot: 
        x = POM_data.loc[POM_data.Area == overseas, 'Population (2016), 1000person'].unique()[0]
        POM_data.loc[POM_data.Area == 'France', 'Population (2016), 1000person'] += x
        
        y = POM_data.loc[POM_data.Area == overseas, '1000 Ha'].unique()[0]
        POM_data.loc[POM_data.Area == 'France', '1000 Ha'] += y
    
    
    POM_micro = POM_data.loc[(POM_data["1000 Ha"] <= 100)]
    POM_micro = POM_micro[~POM_micro["Area"].isin(France_ot)]
    POM_micro = POM_micro[['Area', '1000 Ha', 'Population (2016), 1000person']]
    POM_micro = POM_micro.drop_duplicates()

    POM_data = POM_data.loc[(POM_data["1000 Ha"] > 0)]
    POM_data = POM_data[~POM_data["Area"].isin(France_ot)]

    
    POM_data["GROUP"] = POM_data.apply(lambda row: regions.region(row), axis = 1)
    POM_data["IMAGEGROUP"] = POM_data.apply(lambda row: regions.imageregion(row), axis = 1)
    
    """*** Calculate remaining body weights based on GROUP average ***"""
    POM_Group_Data = POM_data.groupby(["GROUP"]).apply(lambda x: x["avg height"].mean())
    
    for i in POM_data["avg height"].index:
        if np.isnan(POM_data["avg height"][i]) == True:
            POM_data["avg height"][i] = POM_Group_Data[POM_data["GROUP"][i]]
            POM_data["avg weight"][i] = POM_data["avg height"][i]**2*22
    
    POM_data = POM_data.drop(["cca2", "maleMetricHeight", "femaleMetricHeight", "Unnamed: 7", "Year",\
              "COUNTRY","Area Code", "pop2019", "Domain", "Domain Code", "Element", "Flag", "Flag Description", "Year Code", "REGION", "CODE"], axis = 1 )
    
    POM_data = POM_data.rename(columns={"Production" : "POM"})
    
    """*** Add in protein data ***"""
    POM_data = pd.merge(POM_data, FAO_Protein[["Area", "g protein per g product", "Item", "Item Code"]], on = ["Area", "Item", "Item Code"], how = 'left')
    POM_data = POM_data.rename(columns = {"g protein per g product": "% Protein" })
    POM_data = POM_data.drop_duplicates()
    POM_data = POM_data.drop(["Element Code"],axis =1)
    POM_data ["% Protein"] = POM_data ["% Protein"]*100
    
    """*** Determine the % of groups production of each item based on POM ***"""
    POM_data["group"] = POM_data.apply(lambda x: regions.group(x["Item Code"]), axis=1)
    
    """*** Remove the waste fraction to get a snapshot of what people eat ***"""
    wastefractions = pd.read_csv(data+"waste_fractions.csv", sep = ";")
    for i in wastefractions.index:
        if wastefractions['Region'][i] == 'LatinAmerica':
            wastefractions['Region'][i] = 'South&CentralAmerica'
    
    groups = wastefractions.groupby(["Region"])
    POM_data["POM no waste"] = POM_data["POM"]
    for n, gr in POM_data.groupby("GROUP"):
        if n == 'Other':
            continue
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"] == "potatoes and cassava"), "POM no waste"] *= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Rootsandtubers"), "Total"].values)
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"].isin(["dry beans lentils and peas", "soy foods", "peanuts", "tree nuts", "palm oil", "unsaturated oils", "all sweeteners"])), "POM no waste"] *= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Oilseedsandpulses"), "Total"].values)
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"] == "rice wheat corn and other"), "POM no waste"] *= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Cereals"), "Total"].values)
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"].isin(["all fruit", "all vegetables", "dark green vegetables", "red and orange vegetables"])), "POM no waste"] *= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Fruitsandvegetables"), "Total"].values)
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"].isin(["eggs", "beef and lamb", "chicken and other poultry", "pork"])), "POM no waste"] *= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Meat"), "Total"].values)
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"].isin(["whole milk or derivative equivalents"])), "POM no waste"] *= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Milk"), "Total"].values)
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"].isin(["fish"])), "POM no waste"] *= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Fishandseafood"), "Total"].values)

    extra_nations = ['Puerto Rico', 'Palestine', 'Greenland', 'Falkland Islands (Malvinas)'\
                     'New Caledonia', 'China', 'China, Taiwan Province of' ]
    POM_data = POM_data[~POM_data['Area'].isin(extra_nations)]
    

    """*** Adjust waste fraction based on scenario ***"""
    if min_waste == True:
        for i in wastefractions:
            if i in ['Foodtype', 'Region']:
                continue
            for j in wastefractions.Foodtype:
                wastefractions.loc[wastefractions.Foodtype == j, i] = wastefractions[i].loc[wastefractions.Foodtype == j].min()

    wastefractions['Total'] = wastefractions['Agricultural_production'] + wastefractions['Postharvest_handling_and_storage']\
        + wastefractions['Processing_and_packaging'] + wastefractions["Distribution"] + wastefractions["Consumption"]



    return POM_data, meat_products, fish_products, FAO_animals, wastefractions, FAO_pop, POM_micro


def bau_diet_ratios(POM_data):
    POM_data["POM with waste"] = POM_data["POM"]
    POM_percent = POM_data.groupby(["group", "Area"]).apply(lambda x: x["POM no waste"]/x["POM no waste"].sum()*100)
    POM_percent = POM_percent.reset_index(level = ["group", "Area"])
    POM_percent = POM_percent.fillna(value = 0)
    POM_percent = POM_percent.rename(columns = {"POM no waste": "POM (no waste) group %"})
    
    POM_data = POM_data.merge(POM_percent["POM (no waste) group %"].to_frame(), left_index=True, right_index=True)
    
    POM_percent = POM_data.groupby(["Area"]).apply(lambda x: (x["POM no waste"]/x["POM no waste"].sum())*100)
    POM_percent = POM_percent.reset_index(level = ["Area"])
    POM_percent = POM_percent.fillna(value = 0)
    
    POM_data = POM_data.merge(POM_percent["POM no waste"].to_frame(), left_index=True, right_index=True)
    POM_data = POM_data.rename(columns = {"POM no waste_x": "POM (no waste)", "POM no waste_y":"POM (no waste) total %"})
    
    return POM_data
    

def nutrition(POM_data):
    Nutrition_values = pd.read_csv(r"data/nutritionvalues.csv", sep = ";")
    Nutrition_values = Nutrition_values.rename(columns = {"type": "group"})
    
    N_to_P_conversion = pd.read_csv(data+"FAOnitrogen_protein_conversion_factors.csv", sep = ";")
    Nutrition_values["nitrogen(%)"] = np.where(Nutrition_values["item number"].eq(N_to_P_conversion["item number"]),\
                    Nutrition_values["protein(%)"]/N_to_P_conversion["conversion factor"], 0)
    
    Protein_percent = Nutrition_values.groupby(["group"]).apply(lambda x: x["protein(%)"].mean())
    Nutrient_percent = Protein_percent.reset_index(level = ["group"])
    Nutrient_percent = Nutrient_percent.fillna(value = 0)
    Nutrient_percent = Nutrient_percent.rename(columns = {0: "%protein"})
    
    Calorie_percent = Nutrition_values.groupby(["group"]).apply(lambda x: x["calories (100g)"].mean()/100)
    Calorie_percent = Calorie_percent.reset_index(level = ["group"])
    Calorie_percent = Calorie_percent.fillna(value = 0)
    Calorie_percent = Calorie_percent.rename(columns = {0: "calories per g"})
    
    Fat_percent = Nutrition_values.groupby(["group"]).apply(lambda x: x["fat(%)"].mean())
    Fat_percent = Fat_percent.reset_index(level = ["group"])
    Fat_percent = Fat_percent.fillna(value = 0)
    Fat_percent = Fat_percent.rename(columns = {0: "%fat"})
    
    
    Nutrient_percent["calories per g"] = Calorie_percent["calories per g"]
    Nutrient_percent["%fat"] = Fat_percent['%fat']
    
    POM_data = pd.merge(POM_data, Nutrient_percent, on = ["group"])
    POM_data["% Protein"].fillna(POM_data["%protein"], inplace = True)
    POM_data = POM_data.drop(["%protein"], axis = 1)
    POM_data = POM_data.dropna(subset = ['POM'])
    
    """*** Calculate protein and calorie demand of each nation ***"""
    POM_data["Protein Needed (g)"] =  POM_data["avg weight"] * 1.6
    POM_data["Calories Needed (cal)"] = POM_data["avg weight"] * 15 + 587.5
    
    
    """*** Determine the ratio of what people eat based on EAT Lancet Categories *** """
    POM_data["EAT_group"] = POM_data.apply(lambda x: regions.EAT_Lancet_Group(x["group"]), axis =1)
    POM_data["POM CAL (no waste)"] = POM_data['POM (no waste)']*POM_data['calories per g']
    POM_data["POM fat (no waste)"] = POM_data['POM (no waste)']*POM_data['%fat']/100
    
    #POM_data["POM EAT Group %"] = POM_data["EAT_group"]
    POM_eat_group = POM_data.groupby(["Area", "EAT_group"]).apply(lambda x: (x["POM CAL (no waste)"])/(x["POM CAL (no waste)"]).sum()) #fix the last definition of POM group %
    POM_eat_group = POM_eat_group.to_frame() #set_index("Index", inplace = True)
    POM_eat_group = POM_eat_group.reset_index(level = ["Area", "EAT_group"])
    POM_eat_group = POM_eat_group.rename(columns={0 : "POM CAL (no waste)"})
        #POM_eat_group.set_index("Index", inplace = True)
    POM_data = POM_data.merge(POM_eat_group["POM CAL (no waste)"], left_index=True, right_index = True)
    POM_data = POM_data.rename(columns={"POM CAL (no waste)_x" : "POM CAL (no waste)",\
                                        "POM CAL (no waste)_y" : "POM EAT Group cal %"})
    
    POM_eat_group = POM_data.groupby(["Area", "EAT_group"]).apply(lambda x: x["POM (no waste)"]/x["POM (no waste)"].sum()) #fix the last definition of POM group %
    POM_eat_group = POM_eat_group.to_frame() #set_index("Index", inplace = True)
    POM_eat_group = POM_eat_group.reset_index(level = ["Area", "EAT_group"])
    
    POM_data = POM_data.merge(POM_eat_group["POM (no waste)"], left_index=True, right_index = True)
    POM_data = POM_data.rename(columns={"POM (no waste)_x" : "POM (no waste)",\
                                        "POM (no waste)_y" : "POM EAT Group g %"})
    
    POM_data["POM EAT Group cal %"] = POM_data["POM EAT Group cal %"] * 100 
    POM_data["POM EAT Group g %"] = POM_data["POM EAT Group g %"] * 100 
    
    return POM_data


def eat_diet_build(POM_data, wastefractions, diet_main):
    Lancet_Targets = {"group": ["whole grains", "tubers or starchy vegetables", "vegetables",\
              "all fruit", "dairy foods", "beef, lamb and pork", "chicken and other poultry",\
              "eggs", "fish", "legumes", "nuts", "added fats", "added sugars"],

              "caloric intake": diet_main}
    Lancet_Targets = pd.DataFrame(Lancet_Targets)

    Lancet_percent = pd.DataFrame()
    Lancet_percent ["group total"] = Lancet_Targets.groupby(["group"]).apply(lambda x: x["caloric intake"].sum())
    Lancet_percent ["% of total"] = (Lancet_percent["group total"]/Lancet_Targets["caloric intake"].sum())*100
    Lancet_percent = Lancet_percent.rename(index={"tubers or starchy vegetables" : "potatoes and cassava"})

    POM_data ["EAT CAL %"] = POM_data ["POM (no waste) total %"]
    for n, gr in POM_data.groupby("EAT_group"):
        POM_data.loc[(POM_data["EAT_group"] == n), "EAT CAL %"] = Lancet_percent.loc[(Lancet_percent.index == n), "% of total"].values[0]


    POM_data['EAT Cons Cal'] = POM_data ["EAT CAL %"] * POM_data['POM EAT Group cal %']/100
    POM_data['gP/cal'] = (POM_data['% Protein']/100)/POM_data['calories per g']
    POM_data['gP'] = POM_data['gP/cal'] * POM_data['EAT Cons Cal']/100
    POM_data['p factor'] = 0
    for i in POM_data.Area.unique().tolist():
        POM_data.loc[POM_data.Area == i, 'p factor'] = float(POM_data.loc[POM_data.Area == i, 'Protein Needed (g)'].unique() / POM_data.loc[POM_data.Area == i, 'gP'].sum())
    #POM_data['gP'] *= POM_data['p factor']
    POM_data['gP Needed'] = POM_data['gP'] * POM_data['p factor']
    POM_data['Cal Needed'] = POM_data['gP Needed']/POM_data['gP/cal']

    for i in POM_data.Area.unique().tolist():
        POM_data.loc[(POM_data.gP == 0)&(POM_data.Area == i), 'Cal Needed' ] = POM_data.loc[(POM_data.Area == i),'Cal Needed'].sum() * POM_data.loc[(POM_data.gP == 0)&(POM_data.Area == i),'EAT Cons Cal']/100
        
    POM_data['gF Needed'] = POM_data['Cal Needed']/POM_data['calories per g']
    POM_data['EAT POM'] = (POM_data["gF Needed"])*POM_data["Population (2016), 1000person"]*1000*365/(10**9)
    POM_data["EAT POM fat (no waste)"] = POM_data['gF Needed']*POM_data['%fat']/100
    
    POM_data['gF per Capita'] = 0
    POM_data['Cal Provided'] = 0
    for i in POM_data.Area.unique().tolist():
        POM_data.loc[POM_data.Area == i, 'Cal Provided'] = float(POM_data.loc[(POM_data.Area == i),'Cal Needed'].sum())
        POM_data.loc[POM_data.Area == i, 'gF per Capita'] = float(POM_data.loc[(POM_data.Area == i),'gF Needed'].sum())
        POM_data.loc[POM_data.Area == i, 'Fat Provided'] = float(POM_data.loc[(POM_data.Area == i),'EAT POM fat (no waste)'].sum())



    """***Determine the WASTE fraction of foods regionally and on the supply chain.***"""
    POM_data["EAT POM (with waste)"] = POM_data["EAT POM"]
    for n, gr in POM_data.groupby("GROUP"):
        if n == 'Other':
            continue
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"] == "potatoes and cassava"), "EAT POM (with waste)"] /= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Rootsandtubers"), "Total"].values)
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"].isin(["dry beans lentils and peas", "soy foods", "peanuts", "tree nuts", "palm oil", "unsaturated oils", "all sweeteners"])), "EAT POM (with waste)"] /= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Oilseedsandpulses"), "Total"].values)
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"] == "rice wheat corn and other"), "EAT POM (with waste)"] /= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Cereals"), "Total"].values)
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"].isin(["all fruit", "all vegetables", "dark green vegetables", "red and orange vegetables"])), "EAT POM (with waste)"] /= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Fruitsandvegetables"), "Total"].values)
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"].isin(["eggs", "beef and lamb", "chicken and other poultry", "pork"])), "EAT POM (with waste)"] /= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Meat"), "Total"].values)
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"].isin(["whole milk or derivative equivalents"])), "EAT POM (with waste)"] /= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Milk"), "Total"].values)
        POM_data.loc[(POM_data["GROUP"] == n) & (POM_data["group"].isin(["fish"])), "EAT POM (with waste)"]/= (1 - wastefractions.loc[(wastefractions["Region"] == n) & (wastefractions["Foodtype"] == "Fishandseafood"), "Total"].values)

    POM_percent = POM_data.groupby(["Area"]).apply(lambda x: (x["EAT POM (with waste)"]/x["EAT POM (with waste)"].sum())*100)
    POM_percent = POM_percent.reset_index(level = ["Area"])
    POM_percent = POM_percent.fillna(value = 0)
    POM_data = POM_data.merge(POM_percent["EAT POM (with waste)"].to_frame(), left_index=True, right_index=True)
    POM_data = POM_data.rename(columns = {"EAT POM (with waste)_x": "EAT POM (with waste)",\
                                        "EAT POM (with waste)_y": "EAT POM Total %"})
    
    return POM_data