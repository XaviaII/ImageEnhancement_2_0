import pandas as pd


if __name__ == "__main__":

    folders = [
        "achau-02_left", "achau-02_right",
        "altenfelden-04_left", "altenfelden-04_right",
        "grossebersdorf-03_left", "grossebersdorf-03_right",
        "grossweikersdorf-15_left", "grossweikersdorf-15_right",
        "hellas-kagran-01_left", "hellas-kagran-01_right"
    ]
    # path = "04_AI_Upscale/LR_upscaling/08_HAT-L"
    path = "04_AI_Upscale/HR_upscaling_subset/08_HAT-L"

    for folder in folders:
        # Read in the first CSV file
        df1 = pd.read_csv(f'{path}/{folder}/{folder}.csv')

        # Read in the second CSV file
        # df2 = pd.read_csv(f'{path}/{folder}/{folder}_LPIPS.csv')
        df2 = pd.read_csv(f'{path}/{folder}/{folder}_NIQE.csv')

        # Merge the two DataFrames
        merged_df = pd.concat([df1, df2['NIQE']], axis=1)

        # Save the merged DataFrame to a new CSV file
        merged_df.to_csv(f'{path}/{folder}/{folder}_combined.csv', index=False)
