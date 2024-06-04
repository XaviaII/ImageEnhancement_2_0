import numpy as np


def detect_outliers_zscore(data, threshold=3.5):
    """
    Detect outliers in the given dataset using Z-score method.

    Parameters:
        data (array-like): The input data.
        threshold (float): The threshold for Z-score to identify outliers.
                           Default is 3.5, which is a commonly used value.

    Returns:
        list: A list of indices corresponding to the outliers in the input data.
    """
    outliers = []
    mean = np.mean(data)
    std_dev = np.std(data)

    for i, value in enumerate(data):
        z_score = (value - mean) / std_dev
        if np.abs(z_score) > threshold:
            outliers.append(i)

    return outliers


# Provided dataset
data = [0.01, 0.57, 0.09, 0.09, 0.09, 0.08, 0.12, 0.13, 0.24]

# Detect outliers
outliers = detect_outliers_zscore(data)

if outliers:
    print("Outliers detected at indices:", outliers)
    print("Outlier values:", [data[i] for i in outliers])
else:
    print("No outliers detected.")
