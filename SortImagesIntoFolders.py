import os
import shutil


# Function to create subfolders and move images
def sort_images_into_subfolders(directory):
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        # Check if the file is a PNG image
        if filename.endswith(".png"):
            # Extract the id from the filename (assuming format: name_id_frame.png)
            name, type, id, _ = filename.split("_")

            # Create a subfolder with the id if it doesn't exist
            subfolder_path = os.path.join(directory, "bbox_" + id)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)

            # Move the image file into the subfolder
            src_path = os.path.join(directory, filename)
            dest_path = os.path.join(subfolder_path, filename)
            shutil.move(src_path, dest_path)
            print(f"Moved {filename} to {subfolder_path}")


# Directory containing the images
directory = "04_AI_Upscale/HR_upscaling_all/01_Photoshop/rum-09_left"

# Call the function to sort images into subfolders
sort_images_into_subfolders(directory)
