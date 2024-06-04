import pandas as pd

# Load the full dataset
full_data = pd.read_csv('full_data.csv')

# Load the subset dataset
subset_data = pd.read_csv('subset_data.csv')

# Merge the datasets based on the specified columns
merged_data = pd.merge(
    full_data,
    subset_data[['Upscaler', 'Starting Folder', 'Folder Name', 'Frame', 'Width', 'Height', 'Area', 'NIQE']],
    on=['Upscaler', 'Starting Folder', 'Folder Name', 'Frame', 'Width', 'Height', 'Area'],
    how='left'
)

# Fill NaN values in the NIQE column with -1
merged_data['NIQE'] = merged_data['NIQE'].fillna(-1)

# Save the merged dataset to a new CSV file
merged_data.to_csv('merged_data.csv', index=False)
