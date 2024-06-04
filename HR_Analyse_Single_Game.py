import os
import re
import cv2
import os
import math
import imutils
import numpy as np
import pandas as pd
import torchvision.transforms as transforms

from dom import DOM
from PIL import Image
from skimage.metrics import structural_similarity
from torchmetrics.image.lpip import LearnedPerceptualImagePatchSimilarity

#from brisque import BRISQUE
#from skimage import io, img_as_float
#import imquality.brisque as brisque

import BlindMetricModule.brisque.brisque as brisque
import BlindMetricModule.niqe.niqe as niqe
import BlindMetricModule.piqe.piqe as piqe
import BlindMetricModule.MetaIQA.model as MetaIQA
import BlindMetricModule.RankIQA.model as RankIQA


'----------------------------------------------------------------------------------------------------------------------'

round_to = 2 # rounds value to 2 decimals

'----------------------------------------------------------------------------------------------------------------------'

def calculate_BRISQUE(img_generated):
    score = brisque.brisque(img_generated)
    return round(score, round_to)

def calculate_NIQE(img_generated):
    score = niqe.niqe(img_generated)
    return round(score, round_to)

def calculate_PIQUE(img_generated):
    score = piqe.piqe(img_generated)
    return round(score, round_to)

'----------------------------------------------------------------------------------------------------------------------'

def calculate_sharpness(original_image_path, generated_image_path):
    img_original = cv2.imread(original_image_path)
    img_generated = cv2.imread(generated_image_path)
    iqa = DOM()

    # Calculate sharpness
    score_original = iqa.get_sharpness(img_original)
    score_generated = iqa.get_sharpness(img_generated)

    # Return the difference in sharpness
    return round((score_generated - score_original) * 100, 2)  # Round to 2 decimal places

'----------------------------------------------------------------------------------------------------------------------'

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height

def extract_frame_from_filename(filename):
    # Extracts the number at the end of the filename
    match = re.search(r'(\d+)\.png$', filename)
    if match:
        return int(match.group(1))
    else:
        return None

def process_folder(folder_path, starting_folder_name):
    total_files = 0
    completed_files = 0

    for root, dirs, files in os.walk(folder_path):
        total_files += len(files)

    data = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.png'):
                # Create image paths
                generated_image_path = os.path.join(root, file)
                folder_name = os.path.basename(root)
                frame = extract_frame_from_filename(file)

                # Extract image dimensions
                width, height = get_image_dimensions(generated_image_path)
                area = width * height

                img_generated = cv2.imread(generated_image_path)
                # gray_image = cv2.cvtColor(img_generated, cv2.COLOR_BGR2GRAY)

                # BRISQUE
                brisque_score = calculate_BRISQUE(img_generated)

                # PIQUE
                pique_score = calculate_PIQUE(img_generated)

                # NIQE
                #niqe_score = calculate_NIQE(img_generated)

                #print(original_image_path)
                #print(generated_image_path)

                # Append data to list
                data.append({
                    'Upscaler': "Photoshop",
                    'Starting Folder': starting_folder_name,
                    'Folder Name': folder_name,
                    'Frame': frame,
                    'Width': width,
                    'Height': height,
                    'Area': area,
                    'BRISQUE': brisque_score,
                    'PIQUE': pique_score,
                    #'NIQE': niqe_score,
                })


            completed_files += 1
            percent_completed = (completed_files / total_files) * 100
            print(f'Progress: {percent_completed:.2f}%')

    return pd.DataFrame(data)

def main(root_folder):
    starting_folder_name = os.path.basename(root_folder)
    df = process_folder(root_folder, starting_folder_name)

    # print(df)

    # Save DataFrame to CSV within the starting folder
    csv_filename = os.path.join(root_folder, starting_folder_name + "_sharpness.csv")
    df.to_csv(csv_filename, index=False)


if __name__ == "__main__":

    folders = [
        #"achau-02_left", "achau-02_right",
        #"altenfelden-04_left", "altenfelden-04_right",
        #"grossebersdorf-03_left", "grossebersdorf-03_right",
        #"grossweikersdorf-15_left", "grossweikersdorf-15_right",
        #"hellas-kagran-01_left", "hellas-kagran-01_right",
        "rum-09_left",
        "rum-09_right"
    ]

    for folder in folders:
        folder_path = f"04_AI_Upscale/HR_upscaling_all/01_Photoshop/{folder}"
        main(folder_path)
