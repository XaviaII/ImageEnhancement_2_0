import os
from PIL import Image

def crop_images(input_folder, output_folder):
    # Iterate through all files and folders in the input folder
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            # Check if the file is an image
            if file.endswith('.png'):
                # Create the corresponding output folder structure
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)

                # Crop the image and save it to the output folder
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_subfolder, file)
                crop_image(input_path, output_path)

def crop_image(input_path, output_path):
    # Open the image
    image = Image.open(input_path)

    # Get the dimensions of the image
    width, height = image.size

    # Calculate the new width and height divisible by 4
    new_width = width - (width % 4)
    new_height = height - (height % 4)

    # Crop the image
    cropped_image = image.crop((0, 0, new_width, new_height))

    # Save the cropped image
    cropped_image.save(output_path)

# Example usage
input_folder = "03_Daten_PreProcessing/00_HighRes_Images"
output_folder = "03_Daten_PreProcessing/00_HighRes_Images_new"

crop_images(input_folder, output_folder)
