import pandas as pd
import numpy as np
import pprint
from skimpy import skim
from deep_translator import GoogleTranslator as gtr

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
print(covid_data.columns)
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
cols = ['Normal care', 'Intensive care', 'Daily number of deaths']
for col in cols:
    print('Correlation of ', col, 'with the Positive cases is', covid_data[col].corr(covid_data['Number of positives']))

# Recalculate this correlation before and after the starting of general vaccination campaign (April 2021)
b4_vac_camp = covid_data[covid_data['Month'] <= '2021-04']
for col in cols:
    print('Correlation of ', col, 'with the Positive cases is', b4_vac_camp[col].corr(b4_vac_camp['Number of positives']))

aft_vac_camp = covid_data[covid_data['Month'] > '2021-04']
for col in cols:
    print('Correlation of ', col, 'with the Positive cases is', aft_vac_camp[col].corr(aft_vac_camp['Number of positives']))