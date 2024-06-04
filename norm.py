import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.preprocessing import StandardScaler
from scipy import stats

# Define the metric column name
metric = 'PIQUE'  # Change this to the desired metric column name

# Load combined CSV file into DataFrame
df = pd.read_csv('05_Auswertung/AllInOne_HR_Upscaling_results_with_type.csv')

# Filter data based on the specified folders
df_filtered = df[df['Starting Folder'].isin(['achau-02_left', 'achau-02_right']) & df['Upscaler'].isin(['HAT'])]

# Check if the filtered DataFrame is not empty
if df_filtered.empty:
    raise ValueError("Filtered DataFrame is empty. Check the filtering criteria.")

# Ensure 'Type', 'Area', and the metric columns are in the filtered DataFrame
required_columns = ['Type', 'Area', metric]
for col in required_columns:
    if col not in df_filtered.columns:
        raise ValueError(f"'{col}' column is missing from the DataFrame.")

# Convert 'Type' column to categorical data
df_filtered.loc[:, 'Type'] = df_filtered['Type'].astype('category')

# Detect and remove outliers using Z-score
z_scores = np.abs(stats.zscore(df_filtered[['Area', metric]]))
filtered_entries = (z_scores < 3).all(axis=1)
df_filtered = df_filtered[filtered_entries]


# Combine the metric values and areas into a single DataFrame for ANCOVA
df_ancova = df_filtered[[metric, 'Type', 'Area']]

# Fit the ANCOVA model
model = smf.ols(f'{metric} ~ Type + Area', data=df_ancova).fit()

# Check for normality of residuals
residuals = model.resid
normality_test = stats.shapiro(residuals)
print(f'Normality test (Shapiro-Wilk): Statistic={normality_test.statistic}, p-value={normality_test.pvalue}')

# Check for homogeneity of variances
homogeneity_test = stats.levene(df_ancova[metric], df_ancova['Area'], center='mean')
print(f'Homogeneity of variances (Levene\'s test): Statistic={homogeneity_test.statistic}, p-value={homogeneity_test.pvalue}')

# Get the summary of the model
anova_table = sm.stats.anova_lm(model, typ=2)

print(anova_table)

# Interpretation
alpha = 0.05
print("Interpretation of Results:")

# Checking significance of the 'Type' factor
type_pvalue = anova_table['PR(>F)']['Type']
if type_pvalue < alpha:
    print(f"There is a significant difference in {metric} values between Team 1 and Team 2 when controlling for image size (reject H0)")
    print("H1: The team trikot has an influence on the upscaler resulting in different PSNR values.")
else:
    print(f"There is no significant difference in {metric} values between Team 1 and Team 2 when controlling for image size (fail to reject H0)")
    print("H0: The team trikot does not have an influence on the upscaler resulting in different PSNR values.")

# Checking significance of the 'Area' factor
area_pvalue = anova_table['PR(>F)']['Area']
if area_pvalue < alpha:
    print(f"Image size (Area) has a significant effect on {metric} (reject H0)")
    print("H1: Image size significantly impacts the PSNR values.")
else:
    print(f"Image size (Area) does not have a significant effect on {metric} (fail to reject H0)")
    print("H0: Image size does not significantly impact the PSNR values.")
