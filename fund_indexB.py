import pandas as pd


# Load file 1
file_1 = pd.read_excel("/Users/mac/Downloads/output.xlsx")
file_1 = file_1.iloc[:, 1:]  # Duplication of index from excel file so I remove it
file_1 = pd.melt(file_1, ['FundID', 'CompanyID', 'Name'], var_name="QDate")  # Transform the dataframe to a long format
# I will extract year from the QDate column
file_1["Year"] = pd.to_datetime(file_1['QDate']).dt.year


# Load file 2
file_2 = pd.read_excel("/Users/mac/Downloads/example 2 law.xlsx")
file_2 = pd.melt(file_2, ['Law'], var_name="Year")

# Join the two datasets
file = pd.merge(file_1, file_2, left_on=["CompanyID", "Year"], right_on=["Law", "Year"], how="left")
file.rename(columns={"value_x": "quarter_val", "value_y": "yearly_val"}, inplace=True)

# Remove redundant columns
file.drop(["Year", "Law"], inplace=True, axis=1)
file.fillna(0, inplace=True)

# Get the weighted average
grouped_file = file.groupby(['FundID', 'Name', 'QDate'])  # Group_by three columns


def weighted_average(group):
    """
    The special function for calculating the weighted average
    :param group: The grouped data
    :return: calculated value for each group
    """
    group['Weighted'] = (group['quarter_val'] / group['quarter_val'].sum()) * group['yearly_val']
    return group


result = grouped_file.apply(weighted_average)
result.fillna(0, inplace=True)
result.drop(["CompanyID", "quarter_val", "yearly_val"], inplace=True, axis=1)

final_result = result.groupby(['FundID', 'Name', 'QDate']).agg('sum')

final_result.to_excel("/Users/mac/Downloads/output3.xlsx")