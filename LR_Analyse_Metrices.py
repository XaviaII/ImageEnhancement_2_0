import pandas as pd
import numpy as np

# Read data from CSV
df = pd.read_csv('04_AI_Upscale/LR_upscaling/AllInOne_LR_Upscaling_results.csv')

# Define thresholds for minimum width and minimum height
min_width = 100
min_height = 100

# Filter rows based on minimum width and minimum height
df_filtered = df[(df['Width'] > min_width) & (df['Height'] > min_height)].copy()

if df_filtered.empty:
    print("No images found bigger than the defined width and height thresholds.")
else:
    # Normalize the data excluding non-numeric columns
    df_normalized = df_filtered.copy()
    numeric_columns = ['PSNR', 'SSIM', 'LPIPS']
    df_normalized[numeric_columns] = (df_filtered[numeric_columns] - df_filtered[numeric_columns].min()) / (df_filtered[numeric_columns].max() - df_filtered[numeric_columns].min())

    # Assign weights
    weights = {
        'Sharpness': 1,
        'PSNR': 1,
        'SSIM': 1,
        'LPIPS': 0
    }

    # Calculate overall score
    overall_score = (df_normalized[numeric_columns] * np.array([weights[col] for col in numeric_columns])).sum(axis=1)

    # Add overall score to dataframe
    df_filtered['Overall Score'] = overall_score

    # Find the row corresponding to the best image
    best_image_row = df_filtered.loc[df_filtered['Overall Score'].idxmax()]

    # Extract relevant information
    best_upscaler = best_image_row['Upscaler']
    best_starting_folder = best_image_row['Starting Folder']
    best_folder_name = best_image_row['Folder Name']
    best_frame = best_image_row['Frame']
    best_sharpness = best_image_row['Sharpness']
    best_psnr = best_image_row['PSNR']
    best_ssim = best_image_row['SSIM']
    best_lpips = best_image_row['LPIPS']

    # Print the information
    path = f"{best_upscaler}/{best_starting_folder}/{best_folder_name}/{best_frame}"
    print("Best Image:")
    print(
        f"Path: {path},\n"
        f"Sharpness: {best_sharpness},\n"
        f"PSNR: {best_psnr},\n"
        f"SSIM: {best_ssim},\n"
        f"LPIPS: {best_lpips}"
    )
