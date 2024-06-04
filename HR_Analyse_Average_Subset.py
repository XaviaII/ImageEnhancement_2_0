import matplotlib
matplotlib.use('Qt5Agg')  # Specify a different backend
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Load combined CSV file into DataFrame
df = pd.read_csv('04_AI_Upscale/HR_upscaling_subset/AllInOne_LR_Upscaling_results.csv')

# Group by 'Upscaler' first
grouped_by_upscaler = df.groupby('Upscaler')

# Initialize an empty list to store average values for each Upscaler
avg_values_list = []

# Iterate over each group (Upscaler)
for upscaler, group_data in grouped_by_upscaler:
    # Group by 'Starting Folder' and calculate average values
    avg_values = group_data.groupby('Starting Folder').agg({
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
    'Game 01 - Left', 'Game 01 - Right', 'Game 02 - Left', 'Game 02 - Right',
    'Game 03 - Left', 'Game 03 - Right', 'Game 04 - Left', 'Game 04 - Right',
    'Game 05 - Left', 'Game 05 - Right'
]

# Create line plots for Sharpness, PSNR, SSIM, and LPIPS
for metric in ['NIQE']:
    plt.figure(figsize=(8, 6))
    for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
        plt.plot(group_data['Starting Folder'], group_data[metric], label=upscaler, marker='o')

    # Place legend outside to the right
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title(f'Average {metric} per Game')
    plt.ylabel(f'Average {metric}')
    plt.xticks(range(0, 10), custom_labels, rotation=45)  # Set custom x-axis tick labels and rotate them
    plt.grid(True)
    plt.tight_layout()

    # Show the plot
    plt.show()



avg_values = avg_values_sorted.groupby(['Upscaler']).agg({'NIQE': 'mean'}).reset_index()

print("\nAverage values as a table:")
print(round(avg_values,2))