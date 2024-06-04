import matplotlib
matplotlib.use('TkAgg')  # Set the matplotlib backend to TkAgg before importing pyplot
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
from scipy.stats import spearmanr

mectic_name = 'NIQE'

# Load combined CSV file into DataFrame
df = pd.read_csv('05_Auswertung/AllInOne_HR_Upscaling_results_with_type.csv')

# Define minimum width and height thresholds
min_width_threshold = 50 * 4
min_height_threshold = 50 * 4

# Filter data based on minimum width and height thresholds
df_filtered = df[(df['Width'] >= min_width_threshold) & (df['Height'] >= min_height_threshold)
                 #& (df['NIQE'] >= 0)
                 #& (df['Upscaler'] == 'SwinIR')
                 # & (df['Starting Folder'].isin(['rum-09_right']))
                 ]

# Define the area and metric columns
area = df_filtered['Area']
metric = df_filtered[mectic_name]

# Add a constant to the independent variable (area)
X = sm.add_constant(area)
y = metric

# Fit the linear regression model
model = sm.OLS(y, X).fit()

print(model.summary())

# Get the regression results
intercept, slope = model.params
p_value = model.pvalues[1]


# Set the y-axis range
y_range = (0, 40)

# Plot the data points and the regression line with smaller points
plt.figure(figsize=(10, 6))
plt.scatter(area, metric, color='blue', label='Data points', s=1)  # Set the size of points to 5
plt.plot(area, intercept + slope * area, color='red', label='Regression line')
plt.xlabel('Area [$pixels^2$]')
plt.ylabel(f'{mectic_name}')
plt.title(f'Linear Regression of SwinIR for {mectic_name} vs Image Area')
plt.legend()
plt.grid(True)

# Set the y-axis range
plt.ylim(y_range)

# Annotate p-value on the plot
#plt.text(0.1, 0.9, f'p-value: {p_value:.5f}', ha='center', va='center', transform=plt.gca().transAxes, fontsize=12, color='red')

#plt.show()

# Check if the p-value is less than alpha
alpha = 0.05
significant = p_value < alpha

print(f"Intercept: {intercept}")
print(f"Slope: {slope}")
print(f"P-value: {p_value}")
print(f"Is the relationship significant? {'Yes' if significant else 'No'}")
