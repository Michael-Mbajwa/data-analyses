import re
from datetime import datetime
import numpy as np
import pandas as pd
import csv
import json
from numpy import nan as NA
from dateutil.parser import parse
import collections
import seaborn as sns
import matplotlib.pyplot as plt

"""
The US Department of Agriculture makes available a database of food nutrient information. 
"""
path = '/Users/mac/Desktop/pydata-book-2nd-edition/datasets/usda_food/database.json'

with open(path) as usa_food:
    db = json.load(usa_food)

sample = db[0]['nutrients']
df = pd.DataFrame(sample)
info_keys = ['description', 'group', 'id', 'manufacturer']
info = pd.DataFrame(db, columns=info_keys)

'''nutrients = pd.DataFrame(db[0]['nutrients'])  # 6636
nutrients['id'] = db[0]['id']
for i in range(1, 6636):
    temp_nutrients = pd.DataFrame(db[i]['nutrients'])
    temp_nutrients['id'] = db[i]['id']
    nutrients = pd.concat([nutrients, temp_nutrients], ignore_index=True)'''

# The above code is too slow. I would need to make it more efficient.
list_nutrients = []
for i in range(6636):
    temp_nutrients = pd.DataFrame(db[i]['nutrients'])
    temp_nutrients['id'] = db[i]['id']
    list_nutrients.append(temp_nutrients)

nutrients = pd.concat(list_nutrients, ignore_index=True)

# We can inspect the number of duplicated data
nutrients.duplicated().sum()
nutrients = nutrients.drop_duplicates()

ndata = pd.merge(nutrients, info, how='outer', on='id')
