import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pandas import DataFrame

# Load the data and view a subset of it
import pandas as pd
df_91_20 = pd.read_csv('https://data.public.lu/fr/datasets/r/850ca2c2-88c5-4518-bf57-3fec2008821d',
                       delimiter=";", encoding = "ISO-8859-1")
df_81_10 = pd.read_csv('https://data.public.lu/fr/datasets/r/4f4c8a32-84bf-4098-95eb-696e7e4ba3ec',
                       delimiter=";", encoding = "ISO-8859-1")
df_91_20.head()
df_81_10.head()

# For both the dataframes, I rename the column "MONTH" to "Parameters" and make it the index to aid with analysis
# Rename column MONTH to Parameters for both dataframes
df_91_20.rename(columns={'MONTH': 'Parameters'}, inplace=True)
df_81_10.rename(columns={'MONTH': 'Parameters'}, inplace=True)

# Make the renamed column the index
df_91_20.set_index('Parameters', inplace=True)
df_81_10.set_index('Parameters', inplace=True)

df_81_10.head()
df_91_20.head()

# I Check the datatypes of each column and change non-numeric columns to numeric
print(df_91_20.dtypes)
print(df_81_10.dtypes)


# Change non numeric columns to numeric Two columns, OCT and NOV in the df_81_10 dataset have two non-numeric
# columns. Studying the columns, I write a function to clean the string data that will hinder me from directly
# converting the columns dtype to a numeric one.
def str2num(num):
    if num[0] == '<':
        return num[1:]
    else:
        return num


for column in df_81_10.columns:
    if df_81_10[column].dtype == object:
        df_81_10[column] = df_81_10[column].map(str2num)

df_81_10 = df_81_10.astype('float64')

# We can now confirm all datasets have numeric columns
print(df_81_10.dtypes)
print(df_91_20.dtypes)


# Line-plot temperatures (in a single chart) and bar-plot humidity parameters
# Line-plot temperatures (in a single chart)
# For 1981-2010
all_temp = df_81_10.loc[['NM_T (°C)', 'NM_XT (°C)', 'NM_NT (°C)'], :]
all_temp.columns.name = 'Month'
all_temp = all_temp.unstack()
all_temp = all_temp.unstack('Parameters')
all_temp.plot(title='Line plot of Temperature parameters from 1981-2010')


# For 1991-2020
all_temp2 = df_91_20.loc[['NM_T (°C)', 'NM_XT (°C)', 'NM_NT (°C)'], :]
all_temp2.columns.name = 'Month'
all_temp2 = all_temp2.unstack()
all_temp2 = all_temp2.unstack('Parameters')
all_temp2.plot(title='Line plot of Temperature parameters from 1991-2020')

# Bar-plot of humidity parameters
# For 1981-2010
all_hum = df_81_10.loc[['NM_U (%)', 'NM_RR06_06 (mm)'], :]
all_hum.columns.name = 'Month'
all_hum = all_hum.unstack()
all_hum = all_hum.unstack('Parameters')
all_hum.plot.bar(title='Bar-plot of humidity parameters from 1981-2010')

# For 1991-2020
all_hum2 = df_91_20.loc[['NM_U (%)', 'NM_RR06_06 (mm)'], :]
all_hum2.columns.name = 'Month'
all_hum2 = all_hum2.unstack()
all_hum2 = all_hum2.unstack('Parameters')
all_hum2.plot.bar(title='Bar-plot of humidity parameters from 1991-2020')
plt.show()

# Find quarterly (3 month wise) differences of the parameters between 81-10 vs 91-20
# Create a dictionary to map months to quarters
quarters = {'JAN': 'Q1', 'FEB': 'Q1', 'MAR': 'Q1',
            'APR': 'Q2', 'MAY': 'Q2', 'JUN': 'Q2',
            'JUL': 'Q3', 'AUG': 'Q3', 'SEP': 'Q3',
            'OCT': 'Q4', 'NOV': 'Q4', 'DEC': 'Q4'}

# Reshape each data set so I can best work with it
df_81_10_2 = df_81_10.unstack()
df_81_10_2 = df_81_10_2.unstack('Parameters')

df_91_20_2 = df_91_20.unstack()
df_91_20_2 = df_91_20_2.unstack('Parameters')

# Create a column for quarter for each dataset to help with grouping
df_81_10_2['Quarter'] = df_81_10_2.index.map(quarters)
df_91_20_2['Quarter'] = df_91_20_2.index.map(quarters)

# Group each dataset by quarter and aggregate with sum
grped_df_81_10 = df_81_10_2.groupby('Quarter').sum()
grped_df_91_20 = df_91_20_2.groupby('Quarter').sum()

# I simply subtract the two datasets to find the quarterly differences of their
# different parameters.
quarter_diff = grped_df_81_10 - grped_df_91_20
print(quarter_diff)

# I would like to write code to check for the following
# Quarterly mean temperature is not affected by climate change
# Quarterly mean temperature is not affected by climate change
qrt_meantemp_81 = df_81_10_2.groupby('Quarter')['NM_T (°C)'].mean()
qrt_meantemp_91 = df_91_20_2.groupby('Quarter')['NM_T (°C)'].mean()
print(qrt_meantemp_91)
print(qrt_meantemp_81)
qrt_meantemp_81.name = 'Mean_Temp_81_10'
qrt_meantemp_91.name = 'Mean_Temp_91_20'
comb = pd.merge(qrt_meantemp_81, qrt_meantemp_91, right_index=True, left_index=True)
comb.plot.bar()

# FALSE. Mean Temperature is affected by Climate change. There has been an increase in temperature.


# Fog is decreasing in the winter months (Dec-Mar) between decades
def wint_month(mnth):
    if mnth in ['DEC', 'JAN', 'FEB', 'MAR']:
        return 'Winter_Month'
    else:
        return 'No_Winter'


df_81_10_2['Winter_Month'] = df_81_10_2.index.map(wint_month)
df_91_20_2['Winter_Month'] = df_91_20_2.index.map(wint_month)

fog_days_81_10 = df_81_10_2.groupby('Winter_Month')['NM_OFOG (days)'].mean()
fog_days_91_20 = df_91_20_2.groupby('Winter_Month')['NM_OFOG (days)'].mean()

print(fog_days_81_10)
print(fog_days_91_20)

fog_days_81_10.name = 'Days with Fog 81_10'
fog_days_91_20.name = 'Days with Fog 91_20'
comb2 = pd.merge(fog_days_81_10, fog_days_91_20, left_index=True, right_index=True)
comb2.plot.bar(rot=0)
plt.show()

# TRUE. Comparing the two datasets mainly with the aid of the visualization,
# you will notice that FOG is decreasing in the winter months.


# Precipitation (rain) pattern is changing between decades
rain_81_10 = df_81_10_2['NM_RR06_06 (mm)']
rain_91_20 = df_91_20_2['NM_RR06_06 (mm)']
rain_81_10.name = 'Rain patt 81_10'
rain_91_20.name = 'Rain patt 91_20'
comb_precp = pd.merge(rain_81_10, rain_91_20, right_index=True, left_index=True)
comb_precp['diff'] = comb_precp['Rain patt 81_10'] - comb_precp['Rain patt 91_20']
print(comb_precp)

# TRUE. Since the difference between the amount of percipitation in both datasets isn't 0, I can conclude the pattern of
# rain has changed, in fact it is reducing.


# Find out the three most changed parameters and three least changed
# parameters in the quarterly (3 month wise) differences

# Because negative and positive change are all considered change, I first find the absolute of each
# difference and find the total sum for each parameter.
total_para_change = quarter_diff.abs().sum(axis=0)
print('3 most changed parameters are:', pd.Series.nlargest(total_para_change, 3))
print('3 least changed parameters are:', pd.Series.nsmallest(total_para_change, 3))

# Is there any correlation between the most changes parameters
most_changed = ['NM_INS (hours)', 'NM_RR06_06 (mm)', 'NM_U (%)']
# Correlation between SUNSHINE DURATION-NM_INS (hours) and AMOUNT OF PRECIPITATION-NM_RR06_06 (mm)
print('For the 81_10 dataset, the correlation between sunshine duration and amount of precipitation is',
      df_81_10_2[most_changed[0]].corr(df_81_10_2[most_changed[1]]))
print('For the 91_20 dataset, the correlation between sunshine duration and amount of precipitation is',
      df_91_20_2[most_changed[0]].corr(df_91_20_2[most_changed[1]]))
# Conclusion: Based on the results, there is a very weak negative correlation between sunshine duration and amount of precipitation.

# Correlation between SUNSHINE DURATION-NM_INS (hours) and MEAN RELATIVE HUMIDITY-NM_U (%)
print('\nFor the 81_10 dataset, the correlation between sunshine duration and mean relative humidity is',
      df_81_10_2[most_changed[0]].corr(df_81_10_2[most_changed[2]]))
print('For the 91_20 dataset, the correlation between sunshine duration and mean relative humidity is',
      df_91_20_2[most_changed[0]].corr(df_91_20_2[most_changed[2]]))
# Conclusion: There is a strong negative correlation between sunshine duration and mean relative humidity.

# Correlation between AMOUNT OF PRECIPITATION-NM_RR06_06 (mm) and MEAN RELATIVE HUMIDITY-NM_U (%)
print('\nFor the 81_10 dataset, the correlation between amount of precipitation and mean relative humidity is',
      df_81_10_2[most_changed[1]].corr(df_81_10_2[most_changed[2]]))
print('For the 91_20 dataset, the correlation between amount of precipitation  and mean relative humidity is',
      df_91_20_2[most_changed[1]].corr(df_91_20_2[most_changed[2]]))

# Conclusion: There is a weak correlation between amount of precipitation and mean relative humidity.

# Final conclusion: There exists a correlation (negative) between sunshine duration and mean relative humidity only.

# Create a common dataframe (df_temp_81_20) with only month-wise mean temperature and precipitation taken from both
# 81-10 vs 91-20 dataframes, now the month will be the row-index.
part_1 = df_81_10_2[['NM_T (°C)', 'NM_RR06_06 (mm)']] # Temperature and mean from 81_10
part_2 = df_91_20_2[['NM_T (°C)', 'NM_RR06_06 (mm)']] # Temperature and mean from 91_20
part_1.name = '81_10'
part_2.name = '91_20'
def_temp_81_20 = pd.merge(part_1, part_2, left_index=True, right_index=True, suffixes=('_81_10', '_91_20'))
print(def_temp_81_20)

# Create a visualisation where the monthly mean temperature can be compared between 81-10 and 91-20
def_temp_81_20[['NM_T (°C)_81_10', 'NM_T (°C)_91_20']].plot.bar(title='Monthly Mean Temp between 81_10 & 91_20', rot=45)
plt.show()