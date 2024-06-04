import os
import pandas as pd

def combine_csv_files(folder_path):
    # Initialize an empty list to store all DataFrames
    all_dfs = []

    # Iterate through each file in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('_results.csv'):
                # Read the CSV file into a DataFrame
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                print(file_path)
                all_dfs.append(df)

    # Concatenate all DataFrames into one
    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Save the combined DataFrame to a new CSV file named 'results.csv' in the folder location
    combined_file_path = os.path.join(folder_path, f'AllInOne_HR_Upscaling_results.csv')
    combined_df.to_csv(combined_file_path, index=False)


if __name__ == "__main__":

    # Path to the folder containing CSV files
    folder_path = f'04_AI_Upscale/HR_upscaling_subset_csv_only'

    # Combine all CSV files in the folder and save the result
    combine_csv_files(folder_path)

