import statsmodels.api as sm
import pandas as pd
from scipy.stats import pearsonr, spearmanr

# Define the dependent and independent variables

area_LR = [7206.57, 8523.86, 4056.6, 4933.71, 3419.74, 3583.18]
area_HR = [115305.18, 136381.71, 64905.54, 78939.29, 54715.91, 57330.94]

# LR Times
time_LR_NearestNeighbor = [0.005245, 0.005208, 0.005024, 0.005100, 0.001174, 0.001711]
time_LR_Photoshop = [0.506419, 0.539792, 0.614193, 0.628302, 0.549524, 0.559132]
time_LR_ESRGAN = [0.085592, 0.083045, 0.091299, 0.097992, 0.057642, 0.097992]
time_LR_Real_ESRGAN = [0.085592, 0.091349, 0.091299, 0.103756, 0.063407, 0.097992]
time_LR_BSRGAN = [0.078459, 0.091349, 0.099599, 0.097992, 0.069171, 0.109521]
time_LR_SwinIR = [0.078459, 0.074740, 0.082999, 0.086464, 0.057642, 0.086464]
time_LR_HAT = [0.135521, 0.132872, 0.124499, 0.126813, 0.086464, 0.155635]
time_LR_HAT_L = [0.271041, 0.249135, 0.215797, 0.230570, 0.155635, 0.270919]

# HR Times
time_HR_NearestNeighbor = [0.010307, 0.011250, 0.008235, 0.009265, 0.003024, 0.008919]
time_HR_Photoshop = [0.592011, 0.431834, 0.688892, 0.634067, 0.374676, 0.611010]
time_HR_ESRGAN = [0.149786, 0.174394, 0.116199, 0.161399, 0.144106, 0.219041]
time_HR_Real_ESRGAN = [0.142653, 0.157785, 0.149398, 0.178692, 0.097992, 0.167163]
time_HR_BSRGAN = [0.135521, 0.166090, 0.190898, 0.207513, 0.097992, 0.167163]
time_HR_SwinIR = [0.271041, 0.307266, 0.232397, 0.253627, 0.149870, 0.242098]
time_HR_HAT = [0.584879, 0.633910, 0.307096, 0.438082, 0.219041, 0.380440]
time_HR_HAT_L = [0.912981, 1.004844, 0.473094, 0.599481, 0.374676, 0.639831]

area = area_HR
time = time_HR_HAT_L

#pearson_corr, pearson_p_value = pearsonr(area, time)

#print("Pearson Correlation Coefficient:", pearson_corr)
#print("Pearson p-value:", pearson_p_value)

# Spearman Correlation
spearman_corr, spearman_p_value = spearmanr(area, time)

print("Spearman Correlation Coefficient:", spearman_corr)
print("Spearman p-value:", spearman_p_value)

# Interpretation of p-values
alpha = 0.05
#if pearson_p_value < alpha:
#    print("Pearson: Reject the null hypothesis - significant correlation.")
#else:
#    print("Pearson: Fail to reject the null hypothesis - no significant correlation.")

if spearman_p_value < alpha:
    print("Spearman: Reject the null hypothesis - significant correlation.")
else:
    print("Spearman: Fail to reject the null hypothesis - no significant correlation.")