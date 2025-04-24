#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import csv

# 부모 디렉토리 추가하여 JalLib 모듈 import 가능하게 설정
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    
import JalLib
from JalLib.reloadModules import reload_jallib_modules
reload_jallib_modules()

from JalLib.namingConfig import NamingConfig
from JalLib.naming import Naming

def get_name_fron_csv(csv_file_path):
    genNames = []

    # Read the CSV file and extract values, descriptions, and Korean descriptions
    with open(csv_file_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            genName = row[0].strip() # Get the first column value
            if genName: # Skip empty values
                genNames.append(genName)

    return genNames

jalModellerNaming = Naming(configPath=os.path.normpath(r"D:\Dropbox\Programing\Python\PyJalTools\JalLib\ConfigFiles\CharModelerNamingConfig.json"))
jalAnimatorNaming = Naming(configPath=os.path.normpath(r"D:\Dropbox\Programing\Python\PyJalTools\JalLib\ConfigFiles\CharAnimNamingConfig.json"))

mehsCSV = os.path.normpath(r"C:\Users\Admin\Downloads\CharacterMeshName.csv")
animCSV = os.path.normpath(r"C:\Users\Admin\Downloads\AnimName.csv")

# Define output file paths
meshOutputCSV = os.path.normpath(r"C:\Users\Admin\Downloads\CharacterMeshName_KorDesc.csv")
animOutputCSV = os.path.normpath(r"C:\Users\Admin\Downloads\AnimName_KorDesc.csv")


meshNames = get_name_fron_csv(mehsCSV)
animNames = get_name_fron_csv(animCSV)

# Process Mesh Names and store results
meshResults = []
print("Processing Mesh Names...")
for meshName in meshNames:
    nameDic = jalModellerNaming.convert_to_dictionary(meshName)
    korDescNameDic = {} # Initialize dictionary for Korean descriptions

    if nameDic:
        for token_type, token_value in nameDic.items():
            namePart = jalModellerNaming.get_name_part(token_type)
            koreanDesc = namePart.get_korean_description_by_value(token_value) # Get Korean description from the name part

            if koreanDesc == "" and token_value != "":
                koreanDesc = token_value

            korDescNameDic[token_type] = koreanDesc # Store in dictionary for later use

        korDesName = jalModellerNaming.combine(korDescNameDic, "_")
        meshResults.append([meshName, korDesName]) # Store the pair

# Write Mesh results to CSV
print(f"Writing mesh results to {meshOutputCSV}")
with open(meshOutputCSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    # Optionally write a header row
    # writer.writerow(["OriginalName", "KoreanDescriptionName"])
    writer.writerows(meshResults)


# Process Anim Names and store results
animResults = []
print("\nProcessing Anim Names...")
for animName in animNames:
    nameDic = jalAnimatorNaming.convert_to_dictionary(animName)
    korDescNameDic = {} # Initialize dictionary for Korean descriptions

    if nameDic:
        for token_type, token_value in nameDic.items():
            namePart = jalAnimatorNaming.get_name_part(token_type)
            koreanDesc = namePart.get_korean_description_by_value(token_value) # Get Korean description from the name part

            if koreanDesc == "" and token_value != "":
                koreanDesc = token_value

            korDescNameDic[token_type] = koreanDesc # Store in dictionary for later use

        korDesName = jalAnimatorNaming.combine(korDescNameDic, "_")
        animResults.append([animName, korDesName]) # Store the pair

# Write Anim results to CSV
print(f"Writing anim results to {animOutputCSV}")
with open(animOutputCSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    # Optionally write a header row
    # writer.writerow(["OriginalName", "KoreanDescriptionName"])
    writer.writerows(animResults)

print("\nProcessing complete.")
