import pandas as pd

# Load combined CSV file into DataFrame
df = pd.read_csv('05_Auswertung/AllInOne_LR_Upscaling_results.csv')

# Filter data based on the 'Upscaler' being 'HAT-L'
df_filtered = df[df['Upscaler'] == 'HAT-L']

# Define threshold values for each metric
thresholds = {
    'Sharpness': 0,
    'PSNR': 30,
    'SSIM': 0.7,
    'LPIPS': 0.2
}

# Initialize a dictionary to store counts
counts = {}
percentages = {}

# Count values above or below each threshold and compute percentages
for metric, threshold in thresholds.items():
    if metric == 'LPIPS':
        below_threshold_count = len(df_filtered[df_filtered[metric] <= threshold])
        total_count = len(df_filtered)
        counts[metric] = below_threshold_count
        percentages[metric] = (below_threshold_count / total_count) * 100 if total_count != 0 else 0
    else:
        above_threshold_count = len(df_filtered[df_filtered[metric] >= threshold])
        total_count = len(df_filtered)
        counts[metric] = above_threshold_count
        percentages[metric] = (above_threshold_count / total_count) * 100 if total_count != 0 else 0

# Print the counts and percentages
for metric, count in counts.items():
    print(f"{metric} - {thresholds[metric]}: {count} ({percentages[metric]:.2f}%)")
