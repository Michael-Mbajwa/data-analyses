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
The US Federal Election Commission publishes data on contributions to political campaigns. This includes contributor 
names, occupation and employer, address, and contribution amount. An interesting dataset is from the 2012 
US presidential election. 
"""
path = '/Files/fec/P00000001-ALL.csv'
fec = pd.read_csv(path, low_memory=False)
print(fec)
# Let's view a sample data
rand_sample = fec.iloc[np.random.randint(1000, 1000001)]

# We realize that on this data, there are no political party affiliations. To solve that, we can extract the names of
# the candidates and map them with their political parties.
unique_cands = fec.cand_nm.unique()
parties = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican', 'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}

# Now, using this mapping and the map method, we can compute an array of political parties from the candidate names:
fec['party'] = fec['cand_nm'].map(parties)
party_counts = fec['party'].value_counts()

# This data includes both contributions and refunds (negative contribution amount).
neg_contr = fec[fec['contb_receipt_amt'] < 0]  # There are 9647 negative contributions

# To simplify the analysis, I’ll restrict the dataset to positive contributions
fec = fec[fec['contb_receipt_amt'] > 0]

# Since Barack Obama and Mitt Romney were the main two candidates, I’ll also prepare a subset
# that just has contributions to their campaigns
fec_mrbo = fec[fec.cand_nm.isin(['Obama, Barack', 'Romney, Mitt'])]

# Donations statistics by Occupation and Employer
# Let' first inspect the number of people who donated from each occupation
don_by_occup = fec.contbr_occupation.value_counts()

# From looking at the occupations, we would notice there are several variants of the same job. We will try to make the
# occupations more compact.
occ_mapping = {'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED', 'INFORMATION REQUESTED': 'NOT PROVIDED',
               'INFORMATION REQUESTED (BEST EFFORTS)': 'NOT PROVIDED', 'C.E.O.': 'CEO'}

fec.contbr_occupation = fec.contbr_occupation.map(lambda x: occ_mapping.get(x, x))

# Let's do the same thing for employers
emp_mapping = {'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED', 'INFORMATION REQUESTED': 'NOT PROVIDED',
               'SELF': 'SELF-EMPLOYED', 'SELF EMPLOYED': 'SELF-EMPLOYED'}
fec.contbr_employer = fec.contbr_employer.map(lambda x: emp_mapping.get(x, x))
test = fec.contbr_employer[1000:1050]

# Let's use pivot table to aggregate the data by party and occupation
by_occupation = fec.pivot_table('contb_receipt_amt', index='contbr_occupation', columns='party', aggfunc='sum')
# Let's filter down to the subset that donated at least $2 million overall
over_2mm = by_occupation[by_occupation.sum(1) > 2000000]
'''over_2mm.plot.barh()
plt.show()'''
# Let's inspect the top donor occupations or top companies that donated to Obama and Romney


def get_top_amount(group, key, n=5):
    totals = group.groupby(key).sum()['contb_receipt_amt']
    return totals.nlargest(n)


mrbo_grouped = fec_mrbo.groupby('cand_nm').apply(get_top_amount, 'contbr_occupation', 7)
mrbo_grouped2 = fec_mrbo.groupby('cand_nm').apply(get_top_amount, 'contbr_employer', 7)

# Donation statistics by state
grouped = fec_mrbo.groupby(['cand_nm', 'contbr_st'])
totals = grouped.sum()['contb_receipt_amt'].unstack('cand_nm').fillna(0)
print(totals)