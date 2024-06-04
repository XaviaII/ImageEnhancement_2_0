import matplotlib
matplotlib.use('Qt5Agg')  # Specify a different backend
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress, zscore
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


# Load combined CSV file into DataFrame
df = pd.read_csv('05_Auswertung/AllInOne_LR_Upscaling_results.csv')


# Determine the threshold for the top 20% largest areas
area_threshold = df['Area'].quantile(0.80)

# Filter the data to include only entries with an area greater than or equal to the threshold
df_top_20_percent_area = df[df['Area'] >= area_threshold]

print(len(df))
print(len(df_top_20_percent_area))



cv.namedWindow("Output", cv.WINDOW_NORMAL)
cv.imshow("Output", img)