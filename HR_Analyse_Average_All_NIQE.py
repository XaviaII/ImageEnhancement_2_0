import matplotlib
matplotlib.use('Qt5Agg')  # Specify a different backend
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress, zscore
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Load combined CSV file into DataFrame
# df = pd.read_csv('05_Auswertung/AllInOne_HR_Upscaling_results.csv')
df = pd.read_csv('05_Auswertung/AllInOne_HR_Upscaling_NIQE_results.csv')

# Define minimum width and height thresholds
min_width_threshold = 50 * 4
min_height_threshold = 50 * 4

# Filter data based on minimum width and height thresholds
df_filtered = df[(df['Width'] >= min_width_threshold) & (df['Height'] >= min_height_threshold)]

# Group by 'Upscaler' first
grouped_by_upscaler = df_filtered.groupby('Upscaler')

# Initialize an empty list to store average values for each Upscaler
avg_values_list = []

# Iterate over each group (Upscaler)
for upscaler, group_data in grouped_by_upscaler:
    # Group by 'Starting Folder' and calculate average values
    avg_values = group_data.groupby('Starting Folder').agg({
        'Width': 'mean',
        'Height': 'mean',
        'Area': 'mean',
        #'BRISQUE': 'mean',
        #'PIQUE': 'mean',
        'NIQE': 'mean'
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
    'Game 03 - Left', 'Game 03 - Right'
    #'Game 04 - Left', 'Game 04 - Right',
    #'Game 05 - Left', 'Game 05 - Right'
]

# Create plots for Width, Height, and Area as bar plots, and for the other metrics as line plots
for metric in ['Width', 'Height', 'Area']:
    plt.figure(figsize=(8, 6))
    for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
        plt.bar(group_data['Starting Folder'], group_data[metric], label=upscaler, color = 'orange')

    # Place legend outside to the right
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title(f'Average {metric} per Game')
    plt.ylabel(f'Average {metric}')
    plt.xticks(range(0, len(custom_labels)), custom_labels, rotation=45)  # Set custom x-axis tick labels and rotate them
    plt.gca().margins(x=0.01)  # add margin to adjust the left space
    plt.grid(True)
    plt.tight_layout()

    # Show the plot
    plt.show()

# Create line plots for Sharpness, PSNR, SSIM, and LPIPS
for metric in ['NIQE']: #['BRISQUE', 'PIQUE']:
    plt.figure(figsize=(8, 6))
    for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
        plt.plot(group_data['Starting Folder'], group_data[metric], label=upscaler, marker='o')

    # Place legend outside to the right
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title(f'Average {metric} per Game')
    plt.ylabel(f'Average {metric}')
    plt.xticks(range(0, len(custom_labels)), custom_labels, rotation=45)  # Set custom x-axis tick labels and rotate them
    plt.grid(True)
    plt.tight_layout()

    # Show the plot
    plt.show()

# Create a scatter plot for each upscaler with Area on the x-axis and all metrics in one plot
metrics = ['NIQE']
colors = ['blue']

for upscaler, group_data in grouped_by_upscaler:
    plt.figure(figsize=(10, 8))

    for metric, color in zip(metrics, colors):
        # Calculate Z-scores and identify outliers
        z_scores = zscore(group_data[metric])
        outliers = np.abs(z_scores) > 300

        # Mark outliers in red and the rest in blue
        plt.scatter(group_data['Area'][~outliers], group_data[metric][~outliers], label=metric, color='blue', s=10)
        plt.scatter(group_data['Area'][outliers], group_data[metric][outliers], color='red', s=10, label='Outliers')

        # Perform linear regression on the non-outlier data
        slope, intercept, r_value, p_value, std_err = linregress(group_data['Area'][~outliers], group_data[metric][~outliers])
        regression_line = slope * group_data['Area'] + intercept
        plt.plot(group_data['Area'][~outliers], regression_line[~outliers], color=color, linestyle='--', linewidth=2)

    plt.title(f'Metrics vs. Area for {upscaler}')
    plt.xlabel('Area')
    plt.ylabel('Metric Value')
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()

# Output average values as a table
#avg_table = avg_values_sorted.pivot_table(index='Starting Folder', columns='Upscaler', values=['PIQUE'])
#print(avg_table)

# avg_values = avg_values_sorted.groupby(['Upscaler']).agg({'PIQUE': 'mean', 'BRISQUE': 'mean', 'Width': 'mean', 'Height': 'mean'}).reset_index()
avg_values = avg_values_sorted.groupby(['Upscaler']).agg({'NIQE': 'mean', 'Width': 'mean', 'Height': 'mean'}).reset_index()


print("\nAverage values as a table:")
print(round(avg_values,2))