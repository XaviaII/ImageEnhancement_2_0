import os
import pandas as pd

def calculate_average_csv(folder_path):
    # Initialize an empty list to store the average values
    avg_values_list = []

    # Iterate through each file in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.csv'):
                # Read the CSV file into a DataFrame
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)

                # Calculate the average of each column, excluding the first two columns
                avg_values = df.iloc[:, 2:].mean(axis=0)

                # Get the length of the imported CSV as ID
                id_value = len(df)

                # Create a dictionary with average values and ID
                avg_dict = avg_values.to_dict()
                avg_dict['ID'] = id_value

                # Append the dictionary to the list
                avg_values_list.append(avg_dict)

    # Convert the list of dictionaries to a DataFrame
    avg_df = pd.DataFrame(avg_values_list)

    return avg_df


# Path to the folder containing CSV files
folder_path = '04_AI_Upscale/LR_upscaling/01_Photoshop/test/upscale'


# Calculate the average values
average_dataframe = calculate_average_csv(folder_path)

# Display the resulting DataFrame
print(average_dataframe)
