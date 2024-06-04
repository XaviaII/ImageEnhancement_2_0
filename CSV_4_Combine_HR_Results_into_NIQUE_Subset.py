import pandas as pd

# Read the full dataset and the subset
full_df = pd.read_csv("04_AI_Upscale/HR_upscaling_csv_only/AllInOne_HR_Upscaling_results.csv")
subset_df = pd.read_csv("04_AI_Upscale/HR_upscaling_subset_csv_only/AllInOne_HR_Upscaling_NIQE_results.csv")

# Merge the full dataset with the subset on common columns
merged_df = pd.merge(subset_df, full_df[['Upscaler', 'Starting Folder', 'Folder Name', 'Frame', 'BRISQUE', 'PIQUE']],
                     on=['Upscaler', 'Starting Folder', 'Folder Name', 'Frame'],
                     how='left')

# Save the merged dataset with the new columns
merged_df.to_csv("04_AI_Upscale/HR_upscaling_subset_csv_only/AllInOne_HR_Upscaling_results.csv", index=False)
