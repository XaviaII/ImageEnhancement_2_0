import pandas as pd

# Load combined CSV file into DataFrame
df = pd.read_csv('05_Auswertung/AllInOne_HR_Upscaling_results_with_type.csv')

# Filter data based on the 'Upscaler' being 'HAT-L'
df_filtered_count = df[df['Upscaler'] == 'SwinIR']

df_filtered = df_filtered_count
#df_filtered = df_filtered_count[df_filtered_count['NIQE'] >= 0]


# Function to apply min-max normalization
def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())


# Apply min-max normalization to BRISQUE, PIQUE, and NIQE columns for all entries
df_filtered.loc[:, 'BRISQUE'] = min_max_normalize(df_filtered['BRISQUE'])
df_filtered.loc[:, 'PIQUE'] = min_max_normalize(df_filtered['PIQUE'])
df_filtered.loc[:, 'NIQE'] = min_max_normalize(df_filtered['NIQE'])

# Calculate the average of the combined BRISQUE, PIQUE, and NIQE
df_filtered['Average'] = df_filtered[['BRISQUE', 'PIQUE', 'NIQE']].mean(axis=1)


# Create a new DataFrame with the Average column as the last column
df_final = df_filtered.copy()

# Ensure 'Average' is the last column
cols = df_final.columns.tolist()
cols.append(cols.pop(cols.index('Average')))

df_final = df_final[cols]


# Define threshold values for each metric
thresholds = {
    'Average': 0.44, #52
}

# Initialize a dictionary to store counts
counts = {}
percentages = {}

# Count values above or below each threshold and compute percentages
for metric, threshold in thresholds.items():
    below_threshold_count = len(df_final[df_final[metric] <= threshold])
    total_count = len(df_filtered_count)
    counts[metric] = below_threshold_count
    percentages[metric] = (below_threshold_count / total_count) * 100 if total_count != 0 else 0

# Print the counts and percentages
for metric, count in counts.items():
    print(f"{metric}: {count} ({percentages[metric]:.2f}%)")
