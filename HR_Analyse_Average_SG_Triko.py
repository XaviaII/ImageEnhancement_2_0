import pandas as pd
from scipy.stats import ranksums
import numpy as np

# Load combined CSV file into DataFrame
df = pd.read_csv('05_Auswertung/AllInOne_HR_Upscaling_results_with_type.csv')

metrics = ['BRISQUE', 'PIQUE', 'NIQE']

# Define minimum width and height thresholds
min_width_threshold = 0 * 4
min_height_threshold = 0 * 4

# Filter data based on minimum width and height thresholds
df_filtered = df[(df['Width'] >= min_width_threshold) &
                 (df['Height'] >= min_height_threshold) &
                 (df['NIQE'] >= 0) &
                 (df['Starting Folder'].isin(['rum-09_left', 'rum-09_right']))]

# Split the data into two different sets based on 'Type' column
df_type_1 = df_filtered[df_filtered['Type'] == 1]
df_type_2 = df_filtered[df_filtered['Type'] == 2]

# Create subsets for Type 1 and Type 2
type_1_subsets = [group.reset_index(drop=True) for _, group in df_type_1.groupby('Area')]
type_2_subsets = [group.reset_index(drop=True) for _, group in df_type_2.groupby('Area')]

# Make the subsets for Type 1 and Type 2 the same length by cropping to the lower length
#min_length = min(len(type_1_subsets), len(type_2_subsets))
#type_1_subsets = type_1_subsets[:min_length]
#type_2_subsets = type_2_subsets[:min_length]

# Concatenate the data from the subsets
concatenated_type_1 = pd.concat(type_1_subsets, ignore_index=True)
concatenated_type_2 = pd.concat(type_2_subsets, ignore_index=True)

for metric in metrics:
    # Perform Wilcoxon rank-sum test
    statistic, p_value = ranksums(concatenated_type_1[metric], concatenated_type_2[metric])

    # Print results
    print("Wilcoxon Rank-Sum Test:")
    print("Statistic:", statistic)
    print("p-value:", p_value)

    # Interpret the p-value
    alpha = 0.05
    if p_value < alpha:
        print("Reject the null hypothesis: There is a significant difference between the two groups.")
    else:
        print("Fail to reject the null hypothesis: There is no significant difference between the two groups.")
