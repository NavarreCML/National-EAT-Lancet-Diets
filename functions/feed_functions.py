# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 16:15:46 2020

@author: navarrenhn
"""

import pandas as pd

def feed_demand(groups, Lancet_diet):
    Region_demands = {}

    for name, group in groups:
        d = Lancet_diet.copy()
        d["GROUP"] = name
        #print(d)
        ##create animal product demands:
        d.loc[["beef and lamb"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Meat", "Total"].min())             
        d.loc[["pork"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Meat", "Total"].min())             
        d.loc[["chicken and other poultry"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Meat", "Total"].min())             
        d.loc[["fish"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Fishandseafood", "Total"].min())  
        #d = d.drop(["fish"])
        #d.loc[["whole milk or derivative equivalents"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Milk", "Total"].min())   
        #d.loc[["eggs"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Milk", "Total"].min())                       
        
        ##create feed demands:
        
        ##need to determine oil production from soymeal production for feed
        ##feed required for 1 dairy cow per day 
        ##similar feed is assumed for beef cattle being reared on mixed system (pasture/crop-fed)
        ##all concentrates except corn and soy assumed to be by-products
        ##soymeal in concentrate equals 0.8 times fresh soybeans in weight (soymeal.org)
        ##corn equals sum of fresh and corn in concentrate
        ##corn (maize grain) in concentrate equals 0.86 times fresh yield? Based on dry mass?
        cow_dict = {"type": ["grass", "corn", "soybean meal"], ##"citrus pulp concentrate", "palm kernel meal concentrate", "rapeseed meal concentrate", "beet pulp concentrate", "wheat concentrate", "rest products"],
               "gram": [41250, 13750 + (1250*0.86), 750*0.8 ]}##, 500, 500, 500, 250, 250, 1000]}
        cow_Lancet_diet_per_day = pd.DataFrame(cow_dict)
        cow_Lancet_diet_per_day = cow_Lancet_diet_per_day.set_index(["type"])
        cow_feed_per_g_milk = cow_Lancet_diet_per_day["gram"]/25000
        
        ##beef production from dairy cows and dairy calf rearing
        calf_per_g_milk = (1.5/(25000*365*6)) ##3 calves per cow divided by two as only males are used(?)
        
        ##Type A calf of Nguyen 2010 using 8438 kg of feed per 1000 kg carcass weight (= per 660kg edible meat)
        ##(significantly more soymeal --> look into, maybe change Lancet_diet) 
        g_calf_per_g_milk = calf_per_g_milk * 214880
        cow_feed_per_g_calf = ((cow_Lancet_diet_per_day["gram"]/55000)*8438000)/660000
        
        ##One 680 kg Holstein dairy cow delivers 224.52 kg of meat (excluding offal and bones) ##what to do with offal? 
        g_dairycow_beef_per_g_milk = 224520.0 / 36500000.0 #36500000 g milk in her milk giving time of 4 years
        g_beef_per_g_milk = g_calf_per_g_milk + g_dairycow_beef_per_g_milk 
        
        ##feed demand from classic suckler-cow rearing systems is 20863 kg of feed per 1000kg carcass weight (= per 660kg edible meat) (Nguyen 2010)
        cow_feed_per_g_suckler_beef = ((cow_Lancet_diet_per_day["gram"]/55000)*20863000)/660000 
        
        ##required extra beef production besides dairy cows and their calves to reach demand
        required_extra_beef_production = max(d.loc[["beef and lamb"], ["BMI" , "EAT", "Org"]].values[0][0] - (d.loc[["whole milk or derivative equivalents"], ["BMI" , "EAT", "Org"]].values[0][0] * g_beef_per_g_milk), 0)
        
        ##this needs a lamb factor
        total_feed_cows_for_Lancet_diet_per_day = (d.loc[["whole milk or derivative equivalents"], ["BMI" , "EAT", "Org"]].values[0][0] * g_calf_per_g_milk * cow_feed_per_g_calf) + (d.loc[["whole milk or derivative equivalents"], ["BMI" , "EAT", "Org"]].values[0][0] * cow_feed_per_g_milk) + (required_extra_beef_production * cow_feed_per_g_suckler_beef)
        
        ##one dutch cow delivers on average 25 liter milk per day and eats 55kg of feed a day
        ##assuming 3 calves per dairy cow of which half is male so used for slaughter
        ##one dutch dairy cow is culled after 6 years on average 
        ##if not, how much feed does a meat cow need?
        ##how much manure do the cows produce? (for effect on N input ratio)
        
        ##soybean meal assumed to equal 0.8 times fresh soybean weight as in cow Lancet_diet
        ##whole grains assumed here
        ##one dutch egg-laying chicken lays 0.85232877 egg per day amounting to 19400/311.1 = 62.35937 gram egg per day
        ##one dutch chicken eats 121.3 gram feed per day (both broiler and egg) 
        ##chicken feed based on Rezaei et al (high protein organic Lancet_diet) and ratios based on 1/3 of feeds used in first and 2/3 of last stages of life, byproducts and supplements (under 3%) placed in "other"
        ##one dutch broiler chicken lives 6 weeks, averages 2446g and delivers 166+547+243+520 = 1476 gram of meat
        ##is chicken manure used as fertilizer? How much manure does a chicken produce?
        chicken_dict = {"type": ["wheat", "soybean meal", "rapeseed", "oats", "peas"], ##"other"],
               "gram": [45.95, 21.62*0.8, 4.04, 23.15, 9.7]} ##, 16.84]}
        chicken_Lancet_diet_per_day = pd.DataFrame(chicken_dict)
        chicken_Lancet_diet_per_day = chicken_Lancet_diet_per_day.set_index(["type"]) 
        chicken_feed_per_g_meat = (chicken_Lancet_diet_per_day["gram"]*42)/1476
        chicken_feed_per_g_egg = chicken_Lancet_diet_per_day["gram"]/62.35937
        
        total_feed_meat_chickens_for_Lancet_diet_per_day = chicken_feed_per_g_meat * d.loc[["chicken and other poultry"], ["BMI" , "EAT", "Org"]].values[0][0]
        total_feed_egg_chickens_for_Lancet_diet_per_day = chicken_feed_per_g_egg * d.loc[["eggs"], ["BMI" , "EAT", "Org"]].values[0][0]
        
        ##feed required for 1 lamb per day
        ##all concentrates except corn and soy assumed to be by-products
        ##soymeal in concentrate equals 0.8 times fresh soybeans in weight (soymeal.org)
        ##corn (maize grain) in concentrate equals 0.86 times fresh yield? Based on dry mass?
        ##one lamb gives 35.24% of its original weight as meat. One slaughtered lamb weighs 40kg so 40* 0.3524 = 14.096 kg meat per lamb
        ##feed composition assumed to be similar to milk cow (both pasture raised and ruminants).Feed requirement about 1kg a day (Bello et al, 2016)
        ##manure production 
        lamb_dict = {"type": ["grass", "corn", "soybean meal"], ##"citrus pulp concentrate", "palm kernel meal concentrate", "rapeseed meal concentrate", "beet pulp concentrate", "wheat concentrate", "rest products"],
               "gram": [687.5, 312.5 + (20.8*0.86), 12.5*0.8]} ##, 8.33, 8.33, 8.33, 4.15, 4.15, 16.66]}
        lamb_Lancet_diet_per_day = pd.DataFrame(lamb_dict)
        lamb_Lancet_diet_per_day = lamb_Lancet_diet_per_day.set_index(["type"])
        lamb_feed_per_g_meat = (lamb_Lancet_diet_per_day["gram"]*365)/14096
        
        total_feed_lamb_for_Lancet_diet_per_day = lamb_feed_per_g_meat * d.loc[["beef and lamb"], ["BMI" , "EAT", "Org"]].values[0][0]
        ##need to add beef/lamb ratio
        
        ##one slaughtered pig gives on average 57% of its live weight as meat, slaughtered weight is 95.2kg so 95.2*0.57 = 54.264kg meat per fattening pig
        ##one pig lives 88 days (based on BINternet growth per day) and uses 185,064kg of feed in its life (based on BINternet feed conversion) so eats 2,103kg of feed a day
        ##feed requirement based on byproducts scenario of Lassaletta et al 2016
        ##manure production
        ##swill and molasses assumed to be by-products 
        ##are brans a by-product? Do they require extra production? Assumed to be about 10% of original crop (Feedipedia)
        pig_dict = {"type": ["corn", "barley", "brans", "wheat"], ##"swill", "molasses"],
                    "gram": [378.54, 147.21, 525.75, 630.9]} ##, 210.3, 210.3]}
        pig_Lancet_diet_per_day = pd.DataFrame(pig_dict)
        pig_Lancet_diet_per_day = pig_Lancet_diet_per_day.set_index(["type"])
        pig_feed_per_g_meat = (pig_Lancet_diet_per_day["gram"]*88)/54264
        total_feed_pig_for_Lancet_diet_per_day = pig_feed_per_g_meat * d.loc[["pork"], ["BMI" , "EAT", "Org"]].values[0][0]
        
        ##create crop demands including demand for feed crops:
        ##assuming no waste in feedcrops
        d.loc[["rice wheat corn and other"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Cereals", "Total"].min())
        d.loc[["rice wheat corn and other"], ["BMI" , "EAT", "Org"]] += total_feed_cows_for_Lancet_diet_per_day.loc["corn"] + total_feed_meat_chickens_for_Lancet_diet_per_day.loc["wheat"] + total_feed_meat_chickens_for_Lancet_diet_per_day.loc["oats"] + total_feed_egg_chickens_for_Lancet_diet_per_day.loc["wheat"] + total_feed_egg_chickens_for_Lancet_diet_per_day.loc["oats"] +  total_feed_lamb_for_Lancet_diet_per_day.loc["corn"] + total_feed_pig_for_Lancet_diet_per_day.loc["corn"] + total_feed_pig_for_Lancet_diet_per_day.loc["barley"] + total_feed_pig_for_Lancet_diet_per_day.loc["wheat"]
        d.loc[["potatoes and cassava"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Rootsandtubers", "Total"].min())
        d.loc[["dry beans lentils and peas"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Oilseedsandpulses", "Total"].min())         
        d.loc[["dry beans lentils and peas"], ["BMI" , "EAT", "Org"]] += total_feed_meat_chickens_for_Lancet_diet_per_day.loc["peas"] + total_feed_egg_chickens_for_Lancet_diet_per_day.loc["peas"] 
        d.loc[["soy foods"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Oilseedsandpulses", "Total"].min())
        d.loc[["soy foods"], ["BMI" , "EAT", "Org"]] += total_feed_cows_for_Lancet_diet_per_day.loc["soybean meal"] + total_feed_lamb_for_Lancet_diet_per_day.loc["soybean meal"] + total_feed_meat_chickens_for_Lancet_diet_per_day.loc["soybean meal"] + total_feed_egg_chickens_for_Lancet_diet_per_day.loc["soybean meal"]
        d.loc[["peanuts"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Oilseedsandpulses", "Total"].min())         
        d.loc[["tree nuts"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Oilseedsandpulses", "Total"].min())
        #d.loc[["palm oil"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Oilseedsandpulses", "Total"].min())
        d.loc[["unsaturated oils"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Oilseedsandpulses", "Total"].min())     
        d.loc[["unsaturated oils"], ["BMI" , "EAT", "Org"]] += total_feed_meat_chickens_for_Lancet_diet_per_day.loc["rapeseed"] + total_feed_egg_chickens_for_Lancet_diet_per_day.loc["rapeseed"]
        d.loc[["all fruit"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Fruitsandvegetables", "Total"].min())            
        #d.loc[["all vegetables"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Fruitsandvegetables", "Total"].min())             
        d.loc[["dark green vegetables"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Fruitsandvegetables", "Total"].min())             
        d.loc[["red and orange vegetables"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Fruitsandvegetables", "Total"].min())             
        
        Region_demands[name] = d.loc[(Lancet_diet["GROUP"] == name)]
    return Region_demands

def feed_remove(groups, Lancet_diet):
    Region_demands = {}
    
    for name, group in groups:
        d = Lancet_diet.copy()
        d["GROUP"] = name
        #print(d)
        ##create animal product demands:
        d.loc[["beef and lamb"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Meat", "Total"].min())             
        d.loc[["pork"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Meat", "Total"].min())             
        d.loc[["chicken and other poultry"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Meat", "Total"].min())             
        d.loc[["fish"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Fishandseafood", "Total"].min())  
        #d = d.drop(["fish"])
        #d.loc[["whole milk or derivative equivalents"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Milk", "Total"].min())   
        #d.loc[["eggs"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Milk", "Total"].min())                       
        
        ##create feed demands:
        
        ##need to determine oil production from soymeal production for feed
        ##feed required for 1 dairy cow per day 
        ##similar feed is assumed for beef cattle being reared on mixed system (pasture/crop-fed)
        ##all concentrates except corn and soy assumed to be by-products
        ##soymeal in concentrate equals 0.8 times fresh soybeans in weight (soymeal.org)
        ##corn equals sum of fresh and corn in concentrate
        ##corn (maize grain) in concentrate equals 0.86 times fresh yield? Based on dry mass?
        cow_dict = {"type": ["grass", "corn", "soybean meal"], ##"citrus pulp concentrate", "palm kernel meal concentrate", "rapeseed meal concentrate", "beet pulp concentrate", "wheat concentrate", "rest products"],
               "gram": [41250, 13750 + (1250/0.86), 750/0.8 ]}##, 500, 500, 500, 250, 250, 1000]}
        cow_Lancet_diet_per_day = pd.DataFrame(cow_dict)
        cow_Lancet_diet_per_day = cow_Lancet_diet_per_day.set_index(["type"])
        cow_feed_per_g_milk = cow_Lancet_diet_per_day["gram"]/25000
        
        ##beef production from dairy cows and dairy calf rearing
        calf_per_g_milk = (1.5/(25000*365*6)) ##3 calves per cow divided by two as only males are used(?)
        
        ##Type A calf of Nguyen 2010 using 8438 kg of feed per 1000 kg carcass weight (= per 660kg edible meat)
        ##(significantly more soymeal --> look into, maybe change Lancet_diet) 
        g_calf_per_g_milk = calf_per_g_milk * 214880
        cow_feed_per_g_calf = ((cow_Lancet_diet_per_day["gram"]/55000)*8438000)/660000
        
        ##One 680 kg Holstein dairy cow delivers 224.52 kg of meat (excluding offal and bones) ##what to do with offal? 
        g_dairycow_beef_per_g_milk = 224520.0 / 36500000.0 #36500000 g milk in her milk giving time of 4 years
        g_beef_per_g_milk = g_calf_per_g_milk + g_dairycow_beef_per_g_milk 
        
        ##feed demand from classic suckler-cow rearing systems is 20863 kg of feed per 1000kg carcass weight (= per 660kg edible meat) (Nguyen 2010)
        cow_feed_per_g_suckler_beef = ((cow_Lancet_diet_per_day["gram"]/55000)*20863000)/660000 
        
        ##required extra beef production besides dairy cows and their calves to reach demand
        required_extra_beef_production = max(d.loc[["beef and lamb"], ["Org_nf"]].values[0][0] - (d.loc[["whole milk or derivative equivalents"], ["Org_nf"]].values[0][0] * g_beef_per_g_milk), 0)
        
        ##this needs a lamb factor
        total_feed_cows_for_Lancet_diet_per_day = (d.loc[["whole milk or derivative equivalents"], ["Org_nf"]].values[0][0] * g_calf_per_g_milk * cow_feed_per_g_calf) + (d.loc[["whole milk or derivative equivalents"], ["Org_nf"]].values[0][0] * cow_feed_per_g_milk) + (required_extra_beef_production * cow_feed_per_g_suckler_beef)
        
        ##one dutch cow delivers on average 25 liter milk per day and eats 55kg of feed a day
        ##assuming 3 calves per dairy cow of which half is male so used for slaughter
        ##one dutch dairy cow is culled after 6 years on average 
        ##if not, how much feed does a meat cow need?
        ##how much manure do the cows produce? (for effect on N input ratio)
        
        ##soybean meal assumed to equal 0.8 times fresh soybean weight as in cow Lancet_diet
        ##whole grains assumed here
        ##one dutch egg-laying chicken lays 0.85232877 egg per day amounting to 19400/311.1 = 62.35937 gram egg per day
        ##one dutch chicken eats 121.3 gram feed per day (both broiler and egg) 
        ##chicken feed based on Rezaei et al (high protein organic Lancet_diet) and ratios based on 1/3 of feeds used in first and 2/3 of last stages of life, byproducts and supplements (under 3%) placed in "other"
        ##one dutch broiler chicken lives 6 weeks, averages 2446g and delivers 166+547+243+520 = 1476 gram of meat
        ##is chicken manure used as fertilizer? How much manure does a chicken produce?
        chicken_dict = {"type": ["wheat", "soybean meal", "rapeseed", "oats", "peas"], ##"other"],
               "gram": [45.95, 21.62/0.8, 4.04, 23.15, 9.7]} ##, 16.84]}
        chicken_Lancet_diet_per_day = pd.DataFrame(chicken_dict)
        chicken_Lancet_diet_per_day = chicken_Lancet_diet_per_day.set_index(["type"]) 
        chicken_feed_per_g_meat = (chicken_Lancet_diet_per_day["gram"]*42)/1476
        chicken_feed_per_g_egg = chicken_Lancet_diet_per_day["gram"]/62.35937
        
        total_feed_meat_chickens_for_Lancet_diet_per_day = chicken_feed_per_g_meat * d.loc[["chicken and other poultry"], ["Org_nf"]].values[0][0]
        total_feed_egg_chickens_for_Lancet_diet_per_day = chicken_feed_per_g_egg * d.loc[["eggs"], ["Org_nf"]].values[0][0]
        
        ##feed required for 1 lamb per day
        ##all concentrates except corn and soy assumed to be by-products
        ##soymeal in concentrate equals 0.8 times fresh soybeans in weight (soymeal.org)
        ##corn (maize grain) in concentrate equals 0.86 times fresh yield? Based on dry mass?
        ##one lamb gives 35.24% of its original weight as meat. One slaughtered lamb weighs 40kg so 40* 0.3524 = 14.096 kg meat per lamb
        ##feed composition assumed to be similar to milk cow (both pasture raised and ruminants).Feed requirement about 1kg a day (Bello et al, 2016)
        ##manure production 
        lamb_dict = {"type": ["grass", "corn", "soybean meal"], ##"citrus pulp concentrate", "palm kernel meal concentrate", "rapeseed meal concentrate", "beet pulp concentrate", "wheat concentrate", "rest products"],
               "gram": [687.5, 312.5 + (20.8/0.86), 12.5/0.8]} ##, 8.33, 8.33, 8.33, 4.15, 4.15, 16.66]}
        lamb_Lancet_diet_per_day = pd.DataFrame(lamb_dict)
        lamb_Lancet_diet_per_day = lamb_Lancet_diet_per_day.set_index(["type"])
        lamb_feed_per_g_meat = (lamb_Lancet_diet_per_day["gram"]*365)/14096
        
        total_feed_lamb_for_Lancet_diet_per_day = lamb_feed_per_g_meat * d.loc[["beef and lamb"], ["Org_nf"]].values[0][0]
        ##need to add beef/lamb ratio
        
        ##one slaughtered pig gives on average 57% of its live weight as meat, slaughtered weight is 95.2kg so 95.2*0.57 = 54.264kg meat per fattening pig
        ##one pig lives 88 days (based on BINternet growth per day) and uses 185,064kg of feed in its life (based on BINternet feed conversion) so eats 2,103kg of feed a day
        ##feed requirement based on byproducts scenario of Lassaletta et al 2016
        ##manure production
        ##swill and molasses assumed to be by-products 
        ##are brans a by-product? Do they require extra production? Assumed to be about 10% of original crop (Feedipedia)
        pig_dict = {"type": ["corn", "barley", "brans", "wheat"], ##"swill", "molasses"],
                    "gram": [378.54, 147.21, 525.75, 630.9]} ##, 210.3, 210.3]}
        pig_Lancet_diet_per_day = pd.DataFrame(pig_dict)
        pig_Lancet_diet_per_day = pig_Lancet_diet_per_day.set_index(["type"])
        pig_feed_per_g_meat = (pig_Lancet_diet_per_day["gram"]*88)/54264
        total_feed_pig_for_Lancet_diet_per_day = pig_feed_per_g_meat * d.loc[["pork"], ["Org_nf"]].values[0][0]
        
        ##create crop demands including demand for feed crops:
        ##assuming no waste in feedcrops
        d.loc[["rice wheat corn and other"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Cereals", "Total"].min())
        d.loc[["rice wheat corn and other"], ["Org_nf"]] -= total_feed_cows_for_Lancet_diet_per_day.loc["corn"] + total_feed_meat_chickens_for_Lancet_diet_per_day.loc["wheat"] + total_feed_meat_chickens_for_Lancet_diet_per_day.loc["oats"] + total_feed_egg_chickens_for_Lancet_diet_per_day.loc["wheat"] + total_feed_egg_chickens_for_Lancet_diet_per_day.loc["oats"] +  total_feed_lamb_for_Lancet_diet_per_day.loc["corn"] + total_feed_pig_for_Lancet_diet_per_day.loc["corn"] + total_feed_pig_for_Lancet_diet_per_day.loc["barley"] + total_feed_pig_for_Lancet_diet_per_day.loc["wheat"]
        d.loc[["potatoes and cassava"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Rootsandtubers", "Total"].min())
        d.loc[["dry beans lentils and peas"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Oilseedsandpulses", "Total"].min())         
        d.loc[["dry beans lentils and peas"], ["Org_nf"]] -= total_feed_meat_chickens_for_Lancet_diet_per_day.loc["peas"] + total_feed_egg_chickens_for_Lancet_diet_per_day.loc["peas"] 
        d.loc[["soy foods"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Oilseedsandpulses", "Total"].min())
        d.loc[["soy foods"], ["Org_nf"]] -= total_feed_cows_for_Lancet_diet_per_day.loc["soybean meal"] + total_feed_lamb_for_Lancet_diet_per_day.loc["soybean meal"] + total_feed_meat_chickens_for_Lancet_diet_per_day.loc["soybean meal"] + total_feed_egg_chickens_for_Lancet_diet_per_day.loc["soybean meal"]
        d.loc[["peanuts"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Oilseedsandpulses", "Total"].min())         
        d.loc[["tree nuts"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Oilseedsandpulses", "Total"].min())
        #d.loc[["palm oil"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Oilseedsandpulses", "Total"].min())
        d.loc[["unsaturated oils"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Oilseedsandpulses", "Total"].min())     
        d.loc[["unsaturated oils"], ["Org_nf"]] -= total_feed_meat_chickens_for_Lancet_diet_per_day.loc["rapeseed"] + total_feed_egg_chickens_for_Lancet_diet_per_day.loc["rapeseed"]
        d.loc[["all fruit"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Fruitsandvegetables", "Total"].min())            
        #d.loc[["all vegetables"], ["BMI" , "EAT", "Org"]] *= (1 + group.loc[group["Foodtype"] == "Fruitsandvegetables", "Total"].min())             
        d.loc[["dark green vegetables"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Fruitsandvegetables", "Total"].min())             
        d.loc[["red and orange vegetables"], ["Org_nf"]] *= (1 - group.loc[group["Foodtype"] == "Fruitsandvegetables", "Total"].min())             
    
        Region_demands[name] = d.loc[(Lancet_diet["GROUP"] == name)]
    return Region_demands