import pandas as pd
import numpy as np

# Read data from CSV
df = pd.read_csv('04_AI_Upscale/HR_upscaling_subset/merged_subset_dataset.csv')

# Normalize the data excluding non-numeric columns
df_normalized = df.copy()
numeric_columns = ['BRISQUE', 'PIQUE', 'NIQE']
df_normalized[numeric_columns] = (df[numeric_columns] - df[numeric_columns].min()) / (df[numeric_columns].max() - df[numeric_columns].min())

# Assign weights
weights = {
    'BRISQUE': -1,  # Lower BRISQUE is better
    'PIQUE': -1,    # Lower PIQUE is better
    'NIQE': -1      # Lower NIQE is better
}

# Calculate overall score
overall_score = (df_normalized[numeric_columns] * np.array([weights[col] for col in numeric_columns])).sum(axis=1)

# Add overall score to dataframe
df['Overall Score'] = overall_score

# Find the row corresponding to the best image
best_image_row = df.loc[df['Overall Score'].idxmax()]

# Extract relevant information
best_upscaler = best_image_row['Upscaler']
best_starting_folder = best_image_row['Starting Folder']
best_folder_name = best_image_row['Folder Name']
best_frame = best_image_row['Frame']
best_brisque = best_image_row['BRISQUE']
best_pique = best_image_row['PIQUE']
best_niqe = best_image_row['NIQE']

# Print the information
path = f"{best_upscaler}/{best_starting_folder}/{best_folder_name}/{best_frame}"
print("Best Image:")
print(
    f"Path: {path},\n"
    f"BRISQUE: {best_brisque},\n"
    f"PIQUE: {best_pique},\n"
    f"NIQE: {best_niqe}"
)
