import pandas as pd

"""
For this data cleaning exercise, I am working on an xlsx file. This xlsx file read data from the Morningstar API. The 
main sheet - sheet1 contains series of dataframes on it (with different ranges of columns). Each dataframe contains a 
unique FundID. The task is to read the entire sheet, identify the different pandas dataframes (based on unique FundID) 
and merge all the dataframes into one. Save the final result as an excel file.
"""
# dates = pd.date_range(start="2002", end=str(datetime.date.today().year), freq='Q')
file = pd.read_excel("/Users/mac/Downloads/example 2.xlsx")

file.iloc[0, 0] = file.columns[0]

file.dropna(how='all', axis=0, inplace=True)  # remove rows with all NA values
file.reset_index(inplace=True)  # reset the index unsetted by dropna
file.drop("index", axis=1, inplace=True)  # Drop the duplicated index column
file.iloc[:, 0].fillna(method="ffill", inplace=True)  # forward fill the fund company ids in the first column
file.rename(columns={file.columns[0]: "FundID"}, inplace=True)  # change the column name

fund_ids = file['FundID'].unique()  # Identify the unique company ids in the date frame
start = True
final = None

for fund_id in fund_ids:
    if start:  # Only at the first stage
        final = file.loc[file['FundID'] == fund_id]  # Filter file based on the fund_id
        start = False
        final.columns._data[1] = "CompanyID"  # Change the column name of the second column
        final = final.filter(regex='^(?!Unnamed).*', axis=1)  # remove columns that start with Unnamed
    else:
        temp = file.loc[file['FundID'] == fund_id]  # Filter file based on the fund_id

        # Once we encounter a new fund_id, we create a new dataframe from it
        new_header = temp.iloc[0]
        temp = temp[1:]
        temp.columns = new_header
        temp.rename(columns={fund_id: "FundID"}, inplace=True)

        temp.columns._data[1] = "CompanyID"  # Change the column name of the second column
        temp.columns = temp.columns.fillna('drop')  # Change all na column names to drop
        try:  # If the dataframe has a column name drop, remove it
            temp.drop('drop', inplace=True, axis=1)
        except:
            pass  # Else pass.
        # Concatenate final and the temp dataframe calculated
        final = pd.concat([final, temp], axis=0, ignore_index=True)

# Split the data into two parts
part_1 = final.iloc[:, 0:3]
part_2 = final.iloc[:, 3:]

# Sorting the datetime columns of part_2
cols = part_2.columns.tolist()
cols.sort()
part_2 = part_2[cols]

# Concatenate the two parts and return output as an excel file
final = pd.concat([part_1, part_2], axis=1)
# final.to_excel("/Users/mac/Downloads/output.xlsx")
