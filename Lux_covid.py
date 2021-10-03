import pandas as pd
import numpy as np
import pprint
from skimpy import skim
from deep_translator import GoogleTranslator as gtr
from matplotlib import pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta

"""
This dataset comes from a certified public service.

Data from the Ministry of Health on the COVID19 crisis in Luxembourg, this dataset contains: the number of people 
hospitalized in normal and intensive care, the number of deaths, the number of people who left the hospital, 
number of people tested for COVID and number of people tested COVID +
"""

# We first load the dataset from the link below
url = 'https://data.public.lu/en/datasets/r/32f94473-9a6d-4640-9b92-a5b019d38111'
covid_data = pd.read_excel(url)

# Getting an overview of the data
# info = covid_data.info()
desc = covid_data.describe()
data_types = covid_data.dtypes
# data_skim = skim(covid_data)


# Since the data was downloaded in french language, I will Translate Column Names from French to English and print
col_names_en = {x: gtr('fr', 'en').translate(x) for x in covid_data.columns}

# Looking at the translated names, there are two names we would have to manually edit
col_names_en['[1.NbMorts]'] = 'Cumulative Number of deaths'
col_names_en['Nb de positifs'] = 'Number of positives'
col_names_en['Date'] = 'Date'
# pprint.pprint(col_names_en)
covid_data = covid_data.rename(columns=col_names_en)
# print(covid_data.columns)
# print(covid_data)

# Covert column(s) containing date as string to `DateTime` object and other numeric columns to number
for col in covid_data.columns:
    if col == 'Date':
        covid_data[col] = pd.to_datetime(covid_data[col], format='%d/%m/%Y')
    else:
        covid_data[col] = pd.to_numeric(covid_data[col], errors='coerce')

# Calculate Positivity rate for each day
covid_data['positivity_rate'] = (covid_data['Number of positives']/covid_data['Number of tests performed']) * 100

# Calculate daily number of deaths
covid_data['Daily number of deaths'] = covid_data['Cumulative Number of deaths'].diff()
# print(covid_data[['Cumulative Number of deaths', 'Daily number of deaths']][100:120])

# Calculate month-wise average intensive care, daily death, daily positive cases, and positivity rate
covid_data['Month'] = covid_data['Date'].dt.to_period('M')
mw_average = covid_data.groupby(['Month']).mean()[['Intensive care', 'Daily number of deaths', 'Number of positives',
                                                   'positivity_rate']]

# Calculate correlation of Hospitalization, Intensive care, and Death with the Positive cases
'''cols = ['Normal care', 'Intensive care', 'Daily number of deaths']
for col in cols:
    print('Correlation of', col, 'with the Positive cases is', covid_data[col].corr(covid_data['Number of positives']))

# Recalculate this correlation before and after the starting of general vaccination campaign (April 2021)
b4_vac_camp = covid_data[covid_data['Month'] <= '2021-04']
for col in cols:
    print('Correlation of', col, 'with the Positive cases is', b4_vac_camp[col].corr(b4_vac_camp['Number of positives']))

aft_vac_camp = covid_data[covid_data['Month'] > '2021-04']
for col in cols:
    print('Correlation of', col, 'with the Positive cases is', aft_vac_camp[col].corr(aft_vac_camp['Number of positives']))'''


vacc_url = 'https://data.public.lu/en/datasets/r/a3c13d63-6e1d-4bd6-9ba4-2dba5cf9ad5b'
vacc_data = pd.read_excel(vacc_url)

# Inspection of the vaccination data
# vacc_data.info()
dtyp_vacc = vacc_data.dtypes  # The datatypes are appropraite
vacc_descrp = vacc_data.describe()

# Translate column names from french to english
column_names_en = {y: gtr('fr', 'en').translate(y) for y in vacc_data.columns}
# Manually edit some names I am not comfortable with
column_names_en['Date'] = 'Date'
vacc_data = vacc_data.rename(columns=column_names_en)
covid_data.name = 'Covid-19 Data'
vacc_data.name = 'Vaccination Data'


# Find the effectiveness of vaccination in controlling the infection (with adjustment of 1 month later from the second
# vaccine dose)

# I join the COVID-19 infection and vaccination datasets
new_data = pd.merge(covid_data, vacc_data, on='Date', how='left')


# I want to segregate the data
# I first identify the first day of dose2 and locate the Date
dt = new_data['Number of doses 2']
dt.fillna(0, inplace=True)
dose2_start_index = np.nonzero(np.array(dt))[0][0]

dose2_date = new_data.iloc[329, ]['Date']

# Effective starts one month later second dose so I add one month to the dose 2 start date to calculate when
# effectiveness begins
efficacy_start = dose2_date + relativedelta(months=+1)

data_b4_immunity = new_data[new_data['Date'] < efficacy_start]
data_aft_immunity = new_data[new_data['Date'] >= efficacy_start]
print('Mean positivity rate before second dose is', data_b4_immunity['positivity_rate'].mean())
print('Mean positivity rate after second dose is', data_aft_immunity['positivity_rate'].mean())
# The result shows that the mean positivity rate before and after the second dose of vaccination is significant.
# Although it's tempting to say this is the result of the vaccination, it will be good to recall other methods such as
# social distancing, wearing masks etc may have contributed to this reduction.

# Let's now look at correlation
# Correlation between total number of doses and positivity rate/number of positives
# Before Immunity kicks in
var = ['positivity_rate', 'Number of positives']
for v in var:
    print('Correlation of', v, 'with total number of doses', data_b4_immunity[v].corr(data_b4_immunity['Total number of doses']))

# After Immunity kicks in
for v in var:
    print('Correlation of', v, 'with total number of doses', data_aft_immunity[v].corr(data_aft_immunity['Total number of doses']))

# Although both periods have negative correlations which goes to show steps taken to curb the spread of the virus
# were proving effective, you would notice the negative correlation of number of doses to positivity rate became
# significantly higher when immunity began.
