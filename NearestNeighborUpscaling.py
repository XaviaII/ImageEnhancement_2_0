import os
import time
from PIL import Image

def upscale_images(input_folder, output_folder, scale_factor):
    start_time = time.time()  # Start time measurement
    # Iterate through all files and folders in the input folder
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            # Check if the file is an image
            if file.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                # Create the corresponding output folder structure
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)

                # Upscale the image and save it to the output folder
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_subfolder, file)
                upscale_image(input_path, output_path, scale_factor)

    end_time = time.time()  # End time measurement
    total_time = end_time - start_time
    print(f"Total time taken: {total_time:.2f} seconds")

def upscale_image(input_path, output_path, scale_factor):
    # Open the image
    image = Image.open(input_path)

    # Upscale the image by nearest neighbor interpolation
    width, height = image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    upscaled_image = image.resize((new_width, new_height), Image.NEAREST)

    # Save the upscaled image
    upscaled_image.save(output_path)
    # print(f"Upscaled {input_path} and saved to {output_path}")
    Image.Image.close

# Example usage
folders = [
    #"achau-02_left", "achau-02_right",
    #"altenfelden-04_left", "altenfelden-04_right",
    #"grossebersdorf-03_left", "grossebersdorf-03_right",
    #"grossweikersdorf-15_left", "grossweikersdorf-15_right",
    #"hellas-kagran-01_left", "hellas-kagran-01_right",
    "rum-09_left", "rum-09_right",
    #"seekirchen-00_left", "seekirchen-00_right",
    #"stadlau-04_left", "stadlau-04_right",
    #"tulln-06_left", "tulln-06_right",
    #"twl-00_left", "twl-00_right",
    #"wsc-pl-02_left", "wsc-pl-02_right"
    ]

for folder in folders:
    print(folder)
    input_folder = f"03_Daten_PreProcessing/00_HighRes_Images/0_combined/0_new/{folder}"
    output_folder = f"04_AI_Upscale/HR_upscaling_all/00_NearestNeighbor/{folder}"
    scale_factor = 4

    upscale_images(input_folder, output_folder, scale_factor)
