# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 12:18:29 2020

@author: navarrenhn
"""

def region(row): ##group countries to groups used in FAO food waste report based on ISO 3166-1 alpha-3 code
    if row["REGION"] in ["ALB", "ARM", "AUT", "AZE", "BLR", "BEL", "BIH", "BGR", "HRV", 
                  "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "GEO", "DEU", "GRC",
                  "HUN", "ISL", "IRL", "ITA", "LVA", "LTU", "LUX", "MKD", "MDA",
                  "MNE", "NLD", "NOR", "POL", "PRT", "ROU", "RUS", "SRB", "SVK",
                  "SVN", "ESP", "SWE", "CHE", "UKR", "GBR"]:
        return "Europe"
    
    if row["REGION"] in ["CAN", "USA", "PRI"]: 
        return "NorthAmerica"
    
    if row["REGION"] in ["JPN", "CHN", "ROK", 'TWN', "KOR"]:
        return "IndustrializedAsia"
    
    if row["REGION"] in ["AGO", "BEN", "BWA", "BFA", "BDI", "CMR", "CAF", "TCD", "COG",
                    "COD", "CIV", "GNQ", "ERI", "ETH", "GAB", "GMB", "GHA", "GIN",
                    "GNB", "KEN", "LSO", "LBR", "MWI", "MLI", "MRT", "MOZ", "NAM", 
                    "NER", "NGA", "RWA", "SEN", "SLE", "SOM", "ZAF", "SDN", "SWZ",
                    "TZA", "TGO", "UGA", "ZMB", "ZWE", "SSD", "DJI", "MDG", "COM",
                    "STP", "MUS", "CPV"]:
        return "Sub-SaharanAfrica"
    
    if row["REGION"] in ["IRQ", "ISR", "JOR", "KAZ", "KWT", "KGZ", "LBN",
                         "MNG", "OMN", "SAU", "SYR", "TJK", "TUR",
                         "TKM", "ARE", "UZB", "YEM", "PSE"]:
        return "WestandCentralAsia"
    
    if row["REGION"] in ["AFG", "BGD", "BTN", "KHM", "IND", "IDN", "IRN", "LAO", "MYS", 
                    "MMR", "NPL", "PAK", "PHL", "LKA", "THA", "VNM", "PNG", "TLS"]:
        return "SouthandSoutheastAsia"
    
    if row["REGION"] in ["ARG", "BLZ", "BOL", "CHL", "COL", "CRI", "CUB", "DOM", "ECU",
                    "SLV", "GTM", "GUY", "HTI", "HND", "JAM", "MEX", "NIC", "PAN",
                    "PRY", "PER",  "SUR", "URY", "VEN", 'BRA', 'VCT', 'ATG', 'GRD',
                    ]:
        return "South&CentralAmerica"
    
    if row ["REGION"] in ['AUS', 'NZL', 'FJI', 'VUT', 'SLB']:
        return 'Oceania'
    
    if row ["REGION"] in ['MAR', 'ESH', 'DZA', 'EGY', 'TUN', 'LBY']:
        return 'NorthAfrica'
    
    if row ['Area'] in ["Côte d'Ivoire"]:
        return "Sub-SaharanAfrica"
    
    return "Other" ##what to do with Other countries?

def imageregion(row): ##group countries to groups used in FAO food waste report based on ISO 3166-1 alpha-3 code
    if row["CODE"] in [124]:
        return "Canada"
    if row["CODE"] in [666, 840, 581]: 
        return "USA"
    if row["CODE"] in [484]:
        return "Mexico"
    if row["CODE"] in [660, 28, 533, 44, 52, 84, 60, 136, 188, 192, 212, 214, 
                       222, 308, 312, 320, 332, 340, 388, 474, 500, 530, 558, 
                       591, 630, 659, 662, 670, 780, 796, 92, 850]:
        return "Central America"
    if row["CODE"] in [76]:
        return "Brazil"
    if row["CODE"] in [32, 68, 74, 152, 170, 218, 238, 254, 328, 600, 604, 239, 
                       740, 858, 862]:
        return "South America"
    if row["CODE"] in [12, 818, 434, 504, 788, 732]:
        return "North Africa"
    if row["CODE"] in [204, 854, 120, 132, 140, 148, 178, 180, 384, 226, 266, 
                       270, 288, 324, 624, 430, 466, 478, 562, 566, 654, 678, 
                       686, 694, 768]:
        return "West Africa"
    if row["CODE"] in [108, 174, 262, 232, 231, 404, 450, 480, 175, 638, 646, 
                       690, 706, 736, 800, 728, 729]:
        return "East Africa"
    if row["CODE"] in [710]:
        return "South Africa"
    if row["CODE"] in [20, 40, 56, 208, 234, 246, 250, 276, 292, 300, 336, 352,
                       372, 380, 438, 442, 492, 528, 578, 620, 674, 724, 744, 
                       752, 756, 826]:
        return "Western Europe"
    if row["CODE"] in [8, 70, 100, 191, 196, 203, 233, 348, 428, 440, 807, 470,
                       616, 642, 703, 705, 891, 499, 688]:
        return "Eastern Europe"
    if row["CODE"] in [792]:
        return "Turkey"
    if row["CODE"] in [112, 498, 804]:
        return "Ukraine"
    if row["CODE"] in [417, 762, 795, 860, 398]:
        return "Central Asia"
    if row["CODE"] in [51, 31, 268, 643]:
        return "Russia"
    if row["CODE"] in [48, 364, 368, 376, 400, 414, 422, 512, 634, 682, 760,
                       784, 887, 275, 792]:
        return "Middle East"
    if row["CODE"] in [356]:
        return "India"
    if row["CODE"] in [408, 410]:
        return "Korea"
    if row["CODE"] in [156, 344, 466, 496, 158, 351]:
        return "China"
    if row["CODE"] in [96, 116, 418, 458, 104, 608, 702, 764, 704]:
        return "South East Asia"
    if row["CODE"] in [626, 360, 598]:
        return "Indonesia"
    if row["CODE"] in [392]:
        return "Japan"
    if row["CODE"] in [16, 36, 162, 166, 184, 242, 258, 260, 316, 334, 296, 
                       584, 583, 520, 540, 554, 570, 574, 580, 585, 612, 882, 
                       90, 772, 776, 798, 548, 876]:
        return "Oceania"
    if row["CODE"] in [4, 50, 64, 86, 462, 524, 586, 144]:
        return "South Asia"
    if row["CODE"] in [24, 72, 426, 454, 508, 516, 748, 834, 894, 716]:
        return "Southern Africa"
    return "Other" 

def other(row):
    if (row["GROUP"] == "Other") & (row["IMAGEGROUP"] == "USA") | (row["IMAGEGROUP"] == "Oceania"):
        return "NorthAmericaandOceania"
    if ((row["GROUP"] == "Other") & (row["IMAGEGROUP"] == "Central America") | (row["IMAGEGROUP"] == "South America") | (row["IMAGEGROUP"] == "Brazil")):
        return "South&CentralAmerica"
    if ((row["GROUP"] == "Other") & (row["IMAGEGROUP"] == "Western Europe") | (row["IMAGEGROUP"] == "Eastern Europe") | (row["IMAGEGROUP"] == "Ukraine") | (row["IMAGEGROUP"] == "Russia") | (row["CODE"] == 304)): #Greenland is assumed to be Europe
        return "Europe"
    if ((row["GROUP"] == "Other") & (row["IMAGEGROUP"] == "West Africa") | (row["IMAGEGROUP"] == "East Africa") | (row["IMAGEGROUP"] == "Southern Africa") | (row["CODE"] == 728) | (row["CODE"] == 728)):
        return "Sub-SaharanAfrica"
    if ((row["GROUP"] == "Other") & (row["CODE"] == 410) | (row["CODE"] in [702, 344, 158])): ##Singapore, Hong Kong and South Korea are assumed to be in Industrialized Asia
        return "IndustrializedAsia"
    if (row["GROUP"] == "Other") & (row["IMAGEGROUP"] == "Indonesia") | (row["IMAGEGROUP"] == "South East Asia") | (row["IMAGEGROUP"] == "South Asia") | (row["CODE"] == 408):
        return "SouthandSoutheastAsia"
    if (row["CODE"] in [48, 634, 732, 275]):
        return "NorthAfrica,WestandCentralAsia" ##Bahrain & Qatar & Western Sahara are assumed to be Middle East, Middle East placed under west asia
    else:
        return row["GROUP"]
    
def group(item_code):       
    if item_code in [81, 30, 447, 448, 41, 113, 20, 85, 17, 59, 44, 89, 101, 108, 94, 103, 56, 79, 75, 92, 27, 71, 83, 97, 15, 2905, 2520, 2513, 2514, 2517, 2516, 2805, 2515, 2511, 2518]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "rice wheat corn and other"
    elif item_code in [249, 260, 575, 537, 561, 515, 526, 527, 572, 486, 558, 552, 591, 531, 530, 554, 550, 577, 569, 512, 619, 542, 541, 603, 549, 507, 560, 592, 497, 571, 568, 490, 600, 534, 521, 587, 574, 489, 536, 523, 547, 544, 495, 567, 2617, 2615, 2614, 2619, 2919, 2625, 2613, 2620, 2612, 2563, 2611, 2618, 2616]:
        #561 is raisins dried 527 apricots dry 537 prumes dry 575 pineapple canned 250 dessicated coconuts
        return "all fruit"
    elif item_code in [265, 329, 336, 277, 310, 263, 333, 299, 292, 339, 256, 296, 270, 280, 289, 267, 305, 275, 2913, 2586, 2570, 2580, 2562, 2577, 2576, 2578, 2574, 2558, 2581, 2579, 2571, 2573, 2914, 2582, 2572, 2575, 2781, 2782]:
        return "unsaturated oils" ##undecided whether to use all or just 20% each of olive, soybean, rapeseed, sunflower, and peanut oil as in the original report
    elif item_code in [239, 236, 2555]:
        # 239 is soya sauce
        return "soy foods" #soy foods
    elif item_code in [242, 2556]: 
        return "peanuts" ##groundnut
    elif item_code in [254, 257, 2577, 2576]: #include coconut oil here?
        return "palm oil"
    elif item_code in [203, 176, 181, 191, 195, 201, 210, 187, 197, 211, 205, 417, 414, 461, 2546, 2547, 2911, 2549]:
        return "dry beans lentils and peas"
    elif item_code in [118, 125, 116, 149, 122, 136, 137, 135, 2532, 2531, 2534, 2907, 2533, 2535]:
        return "potatoes and cassava"
    elif item_code in [232, 230, 221, 216, 217, 220, 225, 231, 234, 223, 222, 2912, 2551, 2560]:
        #231, 230, 232 are shelled
        return "tree nuts"
    elif item_code in [469, 472, 460, 476, 471, 473, 475, 474, 366, 367, 358, 378, 430, 393, 397, 406, 407, 372, 446, 449, 403, 402, 373, 423, 463, 420, 2602, 2918, 2605]:
        #460, 476, 471, 473, 475, 474, 472 are preserved vegetables 469 is dehydrated
        return "dark green vegetables"
    elif item_code in [391, 392, 426, 401, 399, 394, 388, 689, 2601]: ##includes carrots and turnips, chillies and pepers, eggplants, pumpkins, squash and gourds and tomatoes
        #391 392 are tomatoes paste and peeled
        return "red and orange vegetables"
    elif item_code in [163, 169, 162, 164, 167, 1062, 1091, 2744]: 
        # 169, 162, 164, 167, 163 from trade
        return "eggs" ##includes honey (no land use dedicated to beehives)
    elif item_code in [156, 157, 161, 1182, 1064, 1063, 2949, 2909, 2542, 2537, 2536, 2908, 2541, 2543, 2745]:
        #1064 eggs dried
        return "all sweeteners"
    elif item_code in [1164, 867, 870, 874, 875, 944, 947, 972, 977, 1012, 1017, 1032, 1097, 1111, 1108, 1120, 1122, 1124, 1127, 1137, 1158, 1161, 1163, 1166, 1806, 1807, 1924, 1925, 2071, 2731, 2732, 2735, 2736]:
        return "beef and lamb" #includes buffalo, goat, horse, donkey/mule, game, camel(ids) and other --> also includes rabbits/rodents and snails when food balance is used
    elif item_code in [1058, 1061, 1069, 1084, 1094, 1070, 1073, 1077, 1080, 1087, 1089, 1775, 1926, 2734]:
        return "chicken and other poultry"
    elif item_code in [1035, 1039, 1041, 1042, 1055, 2027, 2733]:
        return "pork"
    elif item_code in [890, 885, 892, 900, 893, 886, 901, 907, 951, 1130, 882, 1020, 982, 2740, 2743, 2848, 2948]:
        #901 907 are cheese 886 is butter 893 buttermilk 892 yoghurt 900 whey 890 whey condensed 885 cream fresh
        return "whole milk or derivative equivalents"
    elif item_code in [2769, 2766, 2765, 2762, 2960, 2761, 2767, 2764, 2763, 2768, 2775]:
        return "fish" #includes aquatic mammals, crustaceans, cephalopods and other molluscs
    elif item_code in [2946, 2941, 2945, 2737]:
        return "animal byproducts"
    elif item_code in [1141]:
        return "rabbit"
    else:
        return "other"

def EAT_Lancet_Group(item_code):       
    if item_code in ["rice wheat corn and other"]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "whole grains"
    elif item_code in ["potatoes and cassava"]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "potatoes and cassava"
    elif item_code in ["dark green vegetables", "red and orange vegetables"]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "vegetables"
    elif item_code in ["all fruit"]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "all fruit"
    elif item_code in ["whole milk or derivative equivalents"]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "dairy foods"
    elif item_code in ["beef and lamb", "pork"]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "beef, lamb and pork"
    elif item_code in ["chicken and other poultry"]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "chicken and other poultry"
    elif item_code in ["eggs"]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "eggs"
    elif item_code in ["fish"]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "fish"
    elif item_code in ["dry beans lentils and peas", "soy foods"]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "legumes"
    elif item_code in ["tree nuts", "peanuts"]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "nuts"
    elif item_code in ["unsaturated oils", "palm oil"]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "added fats"
    elif item_code in ["all sweeteners"]:
        #81, 59, 85, 17 are brans 20 is bread 41, 113 are preparations 448 447 is sweet corn
        return "added sugars"
    else:
        return "other"

