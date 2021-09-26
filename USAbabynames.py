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

'''
The United States Social Security Administration (SSA) has made available data on the frequency of baby names from 1880 
through the present.
'''

names = pd.read_csv('/Users/mac/Desktop/pydata-book-2nd-edition/datasets/babynames/names/yob1880.txt',
                    names=['name', 'sex', 'births'])
names['year'] = 1880

"""
Since the dataset is split into files by year, one of the first things to do is to assemble all of the data into a single 
DataFrame and further to add a year field. """

years = range(1880, 2021)

for year in years:
    path = '/Users/mac/Desktop/pydata-book-2nd-edition/datasets/babynames/names/yob{0}.txt'.format(year)
    new_names = pd.read_csv(path, names=['name', 'sex', 'births'])
    new_names['year'] = year
    names = pd.concat([names, new_names], ignore_index=True)

# Let's look at total births from each year
total_births = names.pivot_table('births', index='year', columns='sex', aggfunc='sum')

total_births.plot(title='Total births by sex and year')


# Next, let’s insert a column prop with the fraction of babies given each name relative to the total number of births.
def add_prop(group):
    group['prop'] = group.births / group.births.sum()
    return group


names = names.groupby(['year', 'sex']).apply(add_prop)

# To conduct a sanity check on the operation carried out on line 47
names.groupby(['year', 'sex']).prop.sum()


# Let's get the top 1000 names for each year/sex combination. We'll use the derived dataset for subsequent analysis.
def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]


top1000 = names.groupby(['year', 'sex']).apply(get_top1000)
top1000.reset_index(inplace=True, drop=True)

# Let's split the Top 1,000 names into the boy and girl portions
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

# Let’s form a pivot table of the total number of births by year and name
total_births = top1000.pivot_table('births', index='year', columns='name', aggfunc='sum')
subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
subset = subset.fillna(0)  # To handle missing data

# Let's plot the number of births of those selected names over the years
subset.plot(title='Number of births per year', subplots=True, figsize=(12, 10))

# Let's measure increase in name diversity
table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc='sum')
table.plot(title='Sum of table1000.prop by year and sex',
           yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2030, 10))

# Let's consider the boys names in 2010
df = boys[boys.year == 2010]
prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
prop_cumsum.values.searchsorted(0.5)


def get_quantile_count(group, q=0.5):
    group = group.sort_values(by='prop', ascending=False)
    return group.prop.cumsum().values.searchsorted(q) + 1


diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
diversity.plot(title='Number of popular names in top 50 percent')

# The last letter revolution
"""
In 2007, baby name researcher Laura Wattenberg pointed out on her website that the distribution of boy names by final 
letter has changed significantly over the last 100 years. To see this, we first aggregate all of the births in the full 
dataset by year, sex, and final letter:
"""
get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
names['last_letter'] = last_letters
tables = names.pivot_table('births', index='last_letter', columns=['sex', 'year'], aggfunc='sum')

# Let's select three representative years spanning the history
subtable = tables.reindex(columns=[1910, 1960, 2010], level='year')
# Next we check the proportion of the yearly number of births of each letter as compared to the total births
letter_prop = subtable / subtable.sum()
fig, axes = plt.subplots(2, 1, figsize=(10, 8))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female', legend=False)

letters_prop = tables / tables.sum()
# Let's select a subset of letters for the boy name
dns_ts = letters_prop.loc[['d', 'n', 'y'], 'M'].transpose()
dns_ts.plot()
plt.show()