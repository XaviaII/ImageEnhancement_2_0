import matplotlib
matplotlib.use('Qt5Agg')  # Specify a different backend
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress, zscore
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Load combined CSV file into DataFrame
df = pd.read_csv('05_Auswertung/AllInOne_HR_Upscaling_results_with_type.csv')

# Define minimum width and height thresholds
min_width_threshold = 0
min_height_threshold = 0

# Filter data based on minimum width and height thresholds
df_filtered = df[(df['Width'] >= min_width_threshold) & (df['Height'] >= min_height_threshold)
                 & (df['NIQE'] >= 0)
                 ]

# Group by 'Upscaler' first
grouped_by_upscaler = df_filtered.groupby('Upscaler')

print(len(df_filtered))




# Function to apply min-max normalization
def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())


# Apply min-max normalization to BRISQUE, PIQUE, and NIQE columns for all entries
df_filtered.loc[:, 'BRISQUE'] = min_max_normalize(df_filtered['BRISQUE'])
df_filtered.loc[:, 'PIQUE'] = min_max_normalize(df_filtered['PIQUE'])
df_filtered.loc[:, 'NIQE'] = min_max_normalize(df_filtered['NIQE'])

# Calculate the average of the combined BRISQUE, PIQUE, and NIQE
df_filtered['Average'] = df_filtered[['BRISQUE', 'PIQUE', 'NIQE']].mean(axis=1)

# Display the first few rows of the normalized dataframe with the average column
print(df_filtered.head())

# Create a new DataFrame with the Average column as the last column
df_final = df_filtered.copy()

# Ensure 'Average' is the last column
cols = df_final.columns.tolist()
cols.append(cols.pop(cols.index('Average')))
f_final = df_final[cols]





#df_one = df_final[
#    (df['Starting Folder'] == 'achau-02_right')
#    & (df['Folder Name'] == 'bbox_23')
#    & (df['Frame'] == 4)
#    & (df['Upscaler'] == 'NearestNeighbor')
#]
#
## Output average values as a table
#selected_image = df_one.groupby(['Upscaler']).agg({
#    'BRISQUE': 'mean',
#    'PIQUE': 'mean',
#    'NIQE': 'mean',
#    'Average': 'mean'
#}).reset_index()
#
#print("Selected Image:")
#print(round(selected_image, 2))



# Group by 'Upscaler'
grouped_by_upscaler = df_final.groupby('Upscaler')


# Initialize an empty list to store average values for each Upscaler
avg_values_list = []

# Iterate over each group (Upscaler)
for upscaler, group_data in grouped_by_upscaler:
    # Group by 'Starting Folder' and calculate average values
    avg_values = group_data.groupby('Starting Folder').agg({
        'Width': 'mean',
        'Height': 'mean',
        'Area': 'mean',
        'BRISQUE': 'mean',
        'PIQUE': 'mean',
        'NIQE': 'mean',
        'Average': 'mean'
    }).reset_index()

    # Add Upscaler column to the DataFrame
    avg_values['Upscaler'] = upscaler

    # Append to the list
    avg_values_list.append(avg_values)

# Concatenate all DataFrames in the list into a single DataFrame
avg_values_combined = pd.concat(avg_values_list)

# Sort DataFrame by 'Starting Folder'
avg_values_sorted = avg_values_combined.sort_values(by='Starting Folder')

# Define custom x-axis tick labels
custom_labels = [
    'Game 01 - Left', 'Game 01 - Right',
    'Game 02 - Left', 'Game 02 - Right',
    'Game 03 - Left', 'Game 03 - Right',
    # 'Game 04 - Left', 'Game 04 - Right',
    # 'Game 05 - Left', 'Game 05 - Right'
]

# Create plots for Width, Height, and Area as bar plots, and for the other metrics as line plots
for metric in ['Width', 'Height', 'Area']:
    plt.figure(figsize=(8, 6))
    for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
        plt.bar(group_data['Starting Folder'], group_data[metric], label=upscaler, color='orange')

    plt.title(f'LR Dataset - Average {metric} per Game')
    plt.ylabel(f'Average {metric} [$pixels^2$]')
    plt.xticks(range(0, len(custom_labels)), custom_labels, rotation=45)  # Set custom x-axis tick labels and rotate them
    plt.gca().margins(x=0.01)  # Add margin to adjust the left space
    plt.grid(True)
    plt.tight_layout(rect=[0, 0, 0.75, 1])  # Adjust layout to leave space for the legend
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

# Create line plots for Sharpness, PSNR, SSIM, and LPIPS
for metric in ['BRISQUE', 'PIQUE', 'NIQE']:
    plt.figure(figsize=(8, 6))
    for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
        plt.plot(group_data['Starting Folder'], group_data[metric], label=upscaler, marker='o')

    plt.title(f'Average {metric} per Game')
    plt.ylabel(f'Average {metric}')
    plt.xticks(range(0, len(custom_labels)), custom_labels, rotation=45)  # Set custom x-axis tick labels and rotate them
    plt.grid(True)
    plt.tight_layout(rect=[0, 0, 0.75, 1])  # Adjust layout to leave space for the legend
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

# Create a scatter plot for each upscaler with Area on the x-axis and all metrics in one plot
metrics = ['PIQUE']
colors = ['blue']

# Define sets for the loop (this should be defined earlier in your code or provided by the user)
sets = [(df_filtered, metrics)]

# Determine the number of subplots
n_upscalers = len(df_filtered['Upscaler'].unique())
n_cols = 2  # Set the number of columns for the grid
n_rows = 4  # Set the number of rows for the grid

# Fixed y-range for all subplots
y_range = (0, 1)

# Create a scatter plot for each set with Area on the x-axis and the metrics in one plot
for df_set, label in sets:
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 20), squeeze=False, constrained_layout=True, gridspec_kw={'hspace': 0.35, 'wspace': 0.15, 'top': 0.95})
    axes = axes.flatten()  # Flatten axes array for easy iteration

    for i, (upscaler, group_data) in enumerate(df_set.groupby('Upscaler')):
        ax = axes[i]
        for metric, color in zip(metrics, colors):
            # Calculate Z-scores and identify outliers
            z_scores = zscore(group_data[metric])
            outliers = np.abs(z_scores) > 3

            # Mark outliers in red and the rest in blue
            ax.scatter(group_data['Area'][~outliers], group_data[metric][~outliers], label=f'{upscaler} - {metric}', s=1, color=color)
            ax.scatter(group_data['Area'][outliers], group_data[metric][outliers], label=f'{upscaler} - OUTLIERS', color='red', s=1)

            # Perform linear regression on the non-outlier data
            slope, intercept, r_value, p_value, std_err = linregress(group_data['Area'][~outliers], group_data[metric][~outliers])
            regression_line = slope * group_data['Area'] + intercept
            ax.plot(group_data['Area'][~outliers], regression_line[~outliers], color='gray', linestyle='--', linewidth=2)

        ax.set_ylim(y_range)  # Set the y-range to the fixed values
        ax.set_title(f'{upscaler} - {label}')
        ax.set_xlabel('Area [$pixels^2$]')
        ax.set_ylabel(f'{metric} Value')
        ax.grid(True)
        ax.legend(loc='best')

    # Remove any empty subplots
    for j in range(i + 1, n_rows * n_cols):
        fig.delaxes(axes[j])

    plt.tight_layout(rect=[0, 0, 0.95, 1])  # Adjust layout to leave space for the legend
    plt.show()

# Calculate the average of the combined BRISQUE, PIQUE, and NIQE
#df_normalized['Average'] = avg_values_sorted.groupby[['BRISQUE', 'PIQUE', 'NIQE']].mean(axis=1)

# Output average values as a table
avg_values = avg_values_sorted.groupby(['Upscaler']).agg({
    'BRISQUE': 'mean',
    'PIQUE': 'mean',
    'NIQE': 'mean',
    'Average': 'mean'
}).reset_index()

print("Mean Values:")
print(round(avg_values, 2))

# Output median values as a table
median_values = avg_values_sorted.groupby(['Upscaler']).agg({
    'BRISQUE': 'median',
    'PIQUE': 'median',
    'NIQE': 'median',
    'Average': 'median'
}).reset_index()

#print("Median Values:")
#print(round(median_values, 2))