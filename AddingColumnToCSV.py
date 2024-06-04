import pandas as pd

# Define the input variable for the Type value
input_type_value = 1  # You can change this value as needed

# Load the CSV file into a DataFrame
df = pd.read_csv('05_Auswertung/AllInOne_HR_Upscaling_results_with_type.csv')

# Apply the input type value to rows matching the conditions
condition = (df['Starting Folder'] == 'rum-09_right') & (df['Folder Name'] == 'bbox_25')
df.loc[condition, 'Type'] = input_type_value

# Save the updated DataFrame back to a CSV file
df.to_csv('05_Auswertung/AllInOne_HR_Upscaling_results_with_type.csv', index=False)

print("The 'Type' column has been updated based on the specified conditions.")
