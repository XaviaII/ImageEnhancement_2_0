import pandas as pd
import cv2 as cv

# Read the CSV file
df = pd.read_csv("05_Auswertung/AllInOne_LR_Upscaling_results.csv")

# Define the metric you want to use
metric = 'LPIPS'

# Define the minimum width and minimum height thresholds
min_width = 0
min_height = 0

# Filter rows based on the minimum width and minimum height thresholds
# df_filtered = df[(df['Width'] >= min_width) & (df['Height'] >= min_height)]
df_filtered = df[
    (df['Starting Folder'] == 'achau-02_right')
    & (df['Folder Name'] == 'bbox_23')
    & (df['Frame'] == 4)
    & (df['Upscaler'] == 'HAT-L')
]

print(len(df_filtered))

if df_filtered.empty:
    print("No images found matching the defined minimum width and height thresholds.")
else:
    # Find the row with the highest value for the chosen metric
    max_metric_row = df_filtered.loc[df_filtered[metric].idxmin()]

    # Extract necessary columns
    upscaler = max_metric_row['Upscaler']
    width = max_metric_row['Width']
    height = max_metric_row['Height']
    starting_folder = max_metric_row['Starting Folder']
    folder_name = max_metric_row['Folder Name']
    frame = max_metric_row['Frame']
    metric_value = max_metric_row[metric]

    best_frame = max_metric_row['Frame']
    best_sharpness = max_metric_row['Sharpness']
    best_psnr = max_metric_row['PSNR']
    best_ssim = max_metric_row['SSIM']
    best_lpips = max_metric_row['LPIPS']

    # Print the path and metric value
    path = f"{upscaler}/{starting_folder}/{folder_name}/{frame}"
    print(f"Path with the highest {metric} value: {path}: {metric}: {metric_value}")

    print(
        f"Upscaler: {upscaler},\n"
        f"Resolution: {width} x {height}, \n"
        f"Game: {'Game 01 - Right'},\n"
        f"Sharpness: {best_sharpness},\n"
        f"PSNR: {best_psnr},\n"
        f"SSIM: {best_ssim},\n"
        f"LPIPS: {best_lpips}"
    )

number = folder_name.split('_')[1]


img = cv.imread(f'04_AI_Upscale/HR_upscaling_all/08_{upscaler}/{starting_folder}/{folder_name}/{starting_folder}_{number}_{frame}.png')
#img2 = cv.imread("04_AI_Upscale/HR_upscaling_all/08_HAT-L/achau-02_right/bbox_23/achau-02_right_23_4.png")

#print(img)

cv.namedWindow("Output", cv.WINDOW_NORMAL)
cv.imshow("Output", img)
k = cv.waitKey(0)