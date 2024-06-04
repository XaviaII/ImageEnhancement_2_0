import pandas as pd

# Read the CSV file
df = pd.read_csv("05_Auswertung/AllInOne_HR_Upscaling_results_with_type.csv")

# Define the metric you want to use
metric = 'Average'

# Define the minimum width and minimum height thresholds
min_width = 0
min_height = 0

# Filter rows based on the minimum width and minimum height thresholds
df_filtered = df[(df['Width'] >= min_width) & (df['Height'] >= min_height)
                & (df['NIQE'] >= 0)
                & (df['Area'] <= 50000)
                & df['Upscaler'].isin(['NearestNeighbor'])
            ]

#df_filtered = df[
#    (df['Starting Folder'] == 'achau-02_right')
#    & (df['Folder Name'] == 'bbox_23')
#    & (df['Frame'] == 4)
#    & (df['Upscaler'] == 'HAT-L')
#]

# Function to apply min-max normalization
def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())


# Apply min-max normalization to BRISQUE, PIQUE, and NIQE columns for all entries
df_filtered.loc[:, 'BRISQUE'] = min_max_normalize(df_filtered['BRISQUE'])
df_filtered.loc[:, 'PIQUE'] = min_max_normalize(df_filtered['PIQUE'])
df_filtered.loc[:, 'NIQE'] = min_max_normalize(df_filtered['NIQE'])

# Calculate the average of the combined BRISQUE, PIQUE, and NIQE
df_filtered['Average'] = df_filtered[['BRISQUE', 'NIQE']].mean(axis=1)


# Create a new DataFrame with the Average column as the last column
df_final = df_filtered.copy()

df_final = df_final[(df_final['BRISQUE'] >= 0.01)]

# Ensure 'Average' is the last column
cols = df_final.columns.tolist()
cols.append(cols.pop(cols.index('Average')))

df_final = df_final[cols]




print(len(df_final))

if df_final.empty:
    print("No images found matching the defined minimum width and height thresholds.")
else:
    # Find the row with the highest value for the chosen metric
    max_metric_row = df_final.loc[df_final[metric].idxmin()]

    # Extract necessary columns
    upscaler = max_metric_row['Upscaler']
    width = max_metric_row['Width']
    height = max_metric_row['Height']
    starting_folder = max_metric_row['Starting Folder']
    folder_name = max_metric_row['Folder Name']
    frame = max_metric_row['Frame']
    metric_value = max_metric_row[metric]

    best_frame = max_metric_row['Frame']
    best_brisque = max_metric_row['BRISQUE']
    best_pique = max_metric_row['PIQUE']
    best_niqe = max_metric_row['NIQE']
    best_average = max_metric_row['Average']

    # Print the path and metric value
    path = f"{upscaler}/{starting_folder}/{folder_name}/{frame}"
    print(f"Path with the highest {metric} value: {path}: {metric}: {metric_value}")

    print(
        f"Upscaler: {upscaler},\n"
        f"Resolution: {width} x {height}, \n"
        f"Game: {'Game 03 - Right'},\n"
        f"BRISQUE: {best_brisque},\n"
        f"PIQUE: {best_pique},\n"
        f"NIQE: {best_niqe},\n"
        f"Average: {best_average}"
    )
