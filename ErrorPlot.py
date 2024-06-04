import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Set the matplotlib backend to TkAgg before importing pyplot
import matplotlib.pyplot as plt
import numpy as np


# Load combined CSV file into DataFrame
df = pd.read_csv('05_Auswertung/AllInOne_HR_Upscaling_results_with_type.csv')

# Define minimum width and height thresholds
min_width_threshold = 50 * 4
min_height_threshold = 50 * 4

# Filter data based on minimum width and height thresholds
df_filtered = df[(df['Width'] >= min_width_threshold) & (df['Height'] >= min_height_threshold)
                 & (df['NIQE'] >= 0)
                 ]

# Group by 'Upscaler' first
grouped_by_upscaler = df_filtered.groupby('Upscaler')

# Define the list of upscalers to analyze
selected_upscalers = ['NearestNeighbor', 'Photoshop', 'ESRGAN', 'RealESRGAN', 'BSRGAN', 'SwinIR', 'HAT', 'HAT-L']

# Check for discrepancies or missing data
for upscaler in selected_upscalers:
    if upscaler not in grouped_by_upscaler.groups:
        print(f"Data for upscaler '{upscaler}' is missing in the DataFrame.")
        continue
    group = grouped_by_upscaler.get_group(upscaler)
    print(f"Number of data points for upscaler '{upscaler}': {len(group)}")

# Define the list of metrics
#selected_metrics = ['Sharpness', 'PSNR', 'SSIM', 'LPIPS']
selected_metrics = ['BRISQUE', 'PIQUE', 'NIQE']

# Loop through each metric
for metric in selected_metrics:
    # Create a new figure for each metric
    plt.figure(figsize=(12, 8))

    # Initialize data list for the current metric
    data = []

    # Iterate over selected upscalers
    for upscaler in selected_upscalers:
        # Extract data for the current upscaler and metric
        if upscaler in grouped_by_upscaler.groups:
            group = grouped_by_upscaler.get_group(upscaler)
            if metric in group:
                data.append(group[metric].dropna())
            else:
                # If data for the current metric is not available, append an empty list
                data.append([])
        else:
            # If data for the current upscaler is not available, append an empty list
            data.append([])

    # Create the boxplot
    plt.boxplot(data, patch_artist=True)

    # Add title and labels
    plt.title(f'{metric} scores')
    plt.xlabel('Upscaler')
    plt.ylabel(metric)

    # Add x-axis tick labels
    plt.xticks(range(1, len(selected_upscalers) + 1), selected_upscalers, rotation=45, ha='right')

    # Add grid for better readability
    plt.grid(True)

    # Display the plot for the current metric
    plt.show()
