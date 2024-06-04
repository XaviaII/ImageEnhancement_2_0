import matplotlib
matplotlib.use('Qt5Agg')  # Specify a different backend
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Load combined CSV file into DataFrame
df = pd.read_csv('05_Auswertung/AllInOne_LR_Upscaling_results_with_type.csv')

# Define minimum width and height thresholds
min_width_threshold = 0
min_height_threshold = 0

# Filter data based on minimum width and height thresholds
df_filtered = df[(df['Width'] >= min_width_threshold) & (df['Height'] >= min_height_threshold) & (
    df['Starting Folder'].isin(['achau-02_left', 'achau-02_right']))]

# Split the data into three different sets based on 'Type' column
df_type_1 = df_filtered[df_filtered['Type'] == 1]
df_type_2 = df_filtered[df_filtered['Type'] == 2]

# Define the sets and their labels
sets = [(df_type_1, 'Type 1'), (df_type_2, 'Type 2')]
set_labels = ['Type 1', 'Type 2']

# Metrics to be plotted
metrics = ['Sharpness', 'PSNR', 'SSIM', 'LPIPS']

# Create a bar plot for each metric
for metric in metrics:
    plt.figure(figsize=(10, 8))

    # Initialize a list to store average values for each type
    avg_values_per_type = []

    for df_set, label in sets:
        grouped_by_upscaler = df_set.groupby('Upscaler')

        # Calculate average values for the current metric for each Upscaler
        avg_values = grouped_by_upscaler[metric].mean()

        # Calculate the overall average for the current metric
        overall_avg = avg_values.mean()
        avg_values_per_type.append(overall_avg)

    # Create bar plot
    plt.bar(set_labels, avg_values_per_type, color=['blue', 'green'])

    plt.title(f'Average {metric} per Type')
    plt.xlabel('Type')
    plt.ylabel(f'Average {metric}')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Calculate and print the mean values of Width, Height, and Area for each type
width_means = [df_set['Width'].mean() for df_set, label in sets]
height_means = [df_set['Height'].mean() for df_set, label in sets]
area_means = [df_set['Area'].mean() for df_set, label in sets]

print("Mean Values for Width, Height, and Area:")
for label, width_mean, height_mean, area_mean in zip(set_labels, width_means, height_means, area_means):
    print(f"{label} - Width: {width_mean:.2f}, Height: {height_mean:.2f}, Area: {area_mean:.2f}")

# Calculate and print the average values of metrics for Type 1 and Type 2
avg_metrics_type_1 = df_type_1[metrics].mean()
avg_metrics_type_2 = df_type_2[metrics].mean()

print("\nAverage Metric Values for Type 1 and Type 2:")
for metric in metrics:
    print(f"{metric} - Type 1: {avg_metrics_type_1[metric]:.2f}, Type 2: {avg_metrics_type_2[metric]:.2f}")

# Calculate and print the percentage difference between Type 1 and Type 2
print("\nPercentage Difference between Type 1 and Type 2:")
for metric in metrics:
    percentage_difference = ((avg_metrics_type_2[metric] - avg_metrics_type_1[metric]) / avg_metrics_type_1[metric]) * 100
    print(f"{metric} - % Difference: {percentage_difference:.2f}%")

# Calculate and print the mean width and height of the entire dataframe
overall_width_mean = df_filtered['Width'].mean()
overall_height_mean = df_filtered['Height'].mean()

print(f"\nOverall Mean Values for the entire DataFrame:")
print(f"Width: {overall_width_mean:.2f}, Height: {overall_height_mean:.2f}")
