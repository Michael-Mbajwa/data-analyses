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

"""In 2011, URL shortening service Bitly partnered with the US government website USA.gov to provide a feed of 
anonymous data gathered from users who shorten links ending with .gov or .mil. """

path = '/Users/mac/Desktop/pydata-book-2nd-edition/datasets/bitly_usagov/example.txt'

with open(path) as f:
    x = f.readlines()
# Since each line of the data is in JSON format, we will use the json package to read it
records = [json.loads(line) for line in x]
len(records)  # we have 3560 lines

# Looking at the data, we will find there is a tz section for timezones. Now let's look at the most reoccurring
# timezones.
time_zones = [rec['tz'] for rec in records if 'tz' in rec]
counts_tz = collections.Counter(time_zones)  # 'America/New_York' is the most reoccurring timezone.

# Migrating the data to pandas
frame = pd.DataFrame(records)
# frame.info() allows to get a feel of the different columns

# We can simply count the occurrence of different timezones this way
count_time_zone = frame['tz'].value_counts()

# Let's handle missing and na values
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
clean_tz_counts = clean_tz.value_counts()

subset = clean_tz_counts[:10]
# sns.barplot(y=subset.index, x=subset.values)

# Let's study the browsers, devices and applications used
# Let's look at browser capability
results = pd.Series([x.split()[0] for x in frame.a.dropna()])
results_counts = results.value_counts()


'''Now, suppose we wanted to decompose the top time zones into Windows and non- Windows users. As a simplification, 
let’s say that a user is on Windows if the string 'Windows' is in the agent string. Since some of the agents are 
missing, we’ll exclude these from the data:
'''
cframe = frame[frame['a'].notnull()]
cframe['os'] = np.where(cframe.a.str.contains('Windows'), 'Windows', 'Not Windows')

# Let's now group the new cframe by the time zone and os
by_tz_os = cframe.groupby(['tz', 'os']).size()
agg_counts = by_tz_os.unstack().fillna(0)

# Let's take the largest and plot
top_ten = agg_counts.nlargest(10, columns=['Not Windows', 'Windows'])
subset = top_ten.stack()
subset.name = 'total'
subset = subset.reset_index()
subset.iloc[2, 0] = 'Null'
subset.iloc[3, 0] = 'Null'

# sns.barplot(x=subset.total, y=subset.tz, hue=subset.os)


# Let's plot group totals
def norm_total(group):
    group['normed_total'] = group.total / group.total.sum()
    return group


grouped_total = subset.groupby('tz').apply(norm_total)
sns.barplot(x=grouped_total.normed_total, y=grouped_total.tz, hue=grouped_total.os)
plt.show()