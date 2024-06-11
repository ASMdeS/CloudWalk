# Importing pandas
import pandas as pd

# Loading the CSV file into a DataFrame
transaction_data = pd.read_csv('transactions_1.csv')

# Creating a pivot table with the columns set as status, values as the number of transactions and rows as time
pivot_table = pd.pivot_table(transaction_data, values='f0_', index=['time'], columns='status', aggfunc='sum')

# Adding a column on our pivot table with the sum of all transactions on the given time
pivot_table['Row_Sum'] = pivot_table.sum(axis=1)

# Filling all the NaN values with 0
pivot_table = pivot_table.fillna(0)

# Creating a table with the ratio of transactions by type compared to the number of total transactions
ratio_table = pivot_table.div(pivot_table['Row_Sum'], axis=0)

# Drop the 'Row_Sum' column from the ratio table as it's always 1
ratio_table = ratio_table.drop(columns=['Row_Sum'])

whisker = {}

for column in ratio_table.columns:
    Quartile_1 = ratio_table[column].quantile(0.25)
    Quartile_3 = ratio_table[column].quantile(0.75)
    InterQuartileRange = Quartile_3 - Quartile_1
    whisker[column] = Quartile_3 + (1.5 * InterQuartileRange)


filtered_whisker = ratio_table[(ratio_table['denied'] > whisker['denied']) | (ratio_table['failed'] > whisker['failed']) | (ratio_table['reversed'] > whisker['reversed'])]

z_score_table = pd.DataFrame(columns=ratio_table.columns)
means = {}
standard_deviations = {}

for column in ratio_table.columns:
    mean = ratio_table[column].mean()
    std_dev = ratio_table[column].std()
    z_score_table[column] = (ratio_table[column] - mean) / std_dev
    means[column] = mean
    standard_deviations[column] = std_dev

filtered_scores = z_score_table[(z_score_table['denied'] > 3) | (z_score_table['failed'] > 3) | (z_score_table['reversed'] > 3)]
