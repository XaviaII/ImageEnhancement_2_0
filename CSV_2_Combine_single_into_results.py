import os
import pandas as pd

def combine_csv_files(folder_path, folder):
    # Initialize an empty list to store all DataFrames
    all_dfs = []

    # Iterate through each file in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.csv'):
                # Read the CSV file into a DataFrame
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                print(file_path)
                all_dfs.append(df)

    # Concatenate all DataFrames into one
    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Save the combined DataFrame to a new CSV file named 'results.csv' in the folder location
    combined_file_path = os.path.join(folder_path, f'{folder}_results.csv')
    combined_df.to_csv(combined_file_path, index=False)


if __name__ == "__main__":

    folders = [
        "00_NearestNeighbor",
        "01_Photoshop",
        "02_ESRGAN",
        "03_RealESRGAN",
        "04_BSRGAN",
        "05_SwinIR",
        #"06_SwinIR-L",
        "07_HAT",
        "08_HAT-L"
    ]

    for folder in folders:
        # Path to the folder containing CSV files
        #folder_path = f'04_AI_Upscale/LR_upscaling/{folder}'
        folder_path = f'04_AI_Upscale/HR_upscaling_subset_csv_only/{folder}'

        # Combine all CSV files in the folder and save the result
        combine_csv_files(folder_path, folder)

