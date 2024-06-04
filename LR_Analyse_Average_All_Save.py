import matplotlib

matplotlib.use('Qt5Agg')  # Specify a different backend
import pandas as pd
import matplotlib.pyplot as plt

# Load combined CSV file into DataFrame
df = pd.read_csv('04_AI_Upscale/LR_upscaling/AllInOne_LR_Upscaling_results.csv')

# Group by 'Upscaler' first
grouped_by_upscaler = df.groupby('Upscaler')

# Initialize an empty list to store average values for each Upscaler
avg_values_list = []

# Iterate over each group (Upscaler)
for upscaler, group_data in grouped_by_upscaler:
    # Group by 'Starting Folder' and calculate average values
    avg_values = group_data.groupby('Starting Folder').agg({
        'Width': 'mean',
        'Height': 'mean',
        'Area': 'mean',
        'Sharpness': 'mean',
        'PSNR': 'mean',
        'SSIM': 'mean',
        'LPIPS': 'mean'
    }).reset_index()

    # Add Upscaler column to the DataFrame
    avg_values['Upscaler'] = upscaler

    # Append to the list
    avg_values_list.append(avg_values)

# Concatenate all DataFrames in the list into a single DataFrame
avg_values_combined = pd.concat(avg_values_list)

# Sort DataFrame by 'Starting Folder'
avg_values_sorted = avg_values_combined.sort_values(by='Starting Folder')

# Create subplots for each metric
fig, axs = plt.subplots(2, 4, figsize=(18, 10))

# Plot for Width
# Bar Plot:
for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
    axs[0, 0].bar(group_data['Starting Folder'], group_data['Width'], label=upscaler)
axs[0, 0].set_title('Average Width')
axs[0, 0].set_xlabel('Starting Folder')
axs[0, 0].set_ylabel('Average Width')

# Line Plot:
#for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
#    axs[0, 0].plot(group_data['Starting Folder'], group_data['Width'], label=upscaler, marker='o')
#axs[0, 0].set_title('Average Width')
#axs[0, 0].set_xlabel('Starting Folder')
#axs[0, 0].set_ylabel('Average Width')

# Plot for Height
# Bar Plot:
for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
    axs[0, 1].bar(group_data['Starting Folder'], group_data['Height'], label=upscaler)
axs[0, 1].set_title('Average Height')
axs[0, 1].set_xlabel('Starting Folder')
axs[0, 1].set_ylabel('Average Height')

# Line Plot:
#for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
#    axs[0, 1].plot(group_data['Starting Folder'], group_data['Height'], label=upscaler, marker='o')
#axs[0, 1].set_title('Average Height')
#axs[0, 1].set_xlabel('Starting Folder')
#axs[0, 1].set_ylabel('Average Height')

# Plot for Area
# Bar Plot:
for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
    axs[0, 2].bar(group_data['Starting Folder'], group_data['Area'], label=upscaler)
axs[0, 2].set_title('Average Area')
axs[0, 2].set_xlabel('Starting Folder')
axs[0, 2].set_ylabel('Average Area')

# Line Plot:
#for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
#    axs[0, 2].plot(group_data['Starting Folder'], group_data['Area'], label=upscaler, marker='o')
#axs[0, 2].set_title('Average Area')
#axs[0, 2].set_xlabel('Starting Folder')
#axs[0, 2].set_ylabel('Average Area')

# Plot for Sharpness
for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
    axs[1, 0].plot(group_data['Starting Folder'], group_data['Sharpness'], label=upscaler, marker='o')
axs[1, 0].set_title('Average Sharpness')
axs[1, 0].set_xlabel('Starting Folder')
axs[1, 0].set_ylabel('Average Sharpness')
axs[1, 0].legend()

# Plot for PSNR
for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
    axs[1, 1].plot(group_data['Starting Folder'], group_data['PSNR'], label=upscaler, marker='o')
axs[1, 1].set_title('Average PSNR')
axs[1, 1].set_xlabel('Starting Folder')
axs[1, 1].set_ylabel('Average PSNR')
axs[1, 1].legend()

# Plot for SSIM
for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
    axs[1, 2].plot(group_data['Starting Folder'], group_data['SSIM'], label=upscaler, marker='o')
axs[1, 2].set_title('Average SSIM')
axs[1, 2].set_xlabel('Starting Folder')
axs[1, 2].set_ylabel('Average SSIM')
axs[1, 2].legend()

# Plot for SSIM
for upscaler, group_data in avg_values_sorted.groupby('Upscaler'):
    axs[1, 3].plot(group_data['Starting Folder'], group_data['LPIPS'], label=upscaler, marker='o')
axs[1, 3].set_title('Average LPIPS')
axs[1, 3].set_xlabel('Starting Folder')
axs[1, 3].set_ylabel('Average LPIPS')
axs[1, 3].legend()

# Adjust layout
plt.tight_layout()
plt.show()
