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

'----------------------------------------------------------------------------------------------------------------------'

round_to = 2 # rounds value to 2 decimals

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

def calculate_psnr(img_original, img_generated):
    psnr_value = cv2.PSNR(img_original, img_generated)
    return round(psnr_value, round_to)

def calculate_ssim(img_original, img_generated):
    # Images_Gray
    img_original_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    img_generated_gray = cv2.cvtColor(img_generated, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    (score, diff) = structural_similarity(img_original_gray, img_generated_gray, full=True)

    # diff is in range [0, 1]. Convert it in range [0, 255]
    diff = (diff * 255).astype("uint8")
    #cv2.imshow("Difference", diff)

    # Apply threshold
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Find contours
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    # Loop over each contour
    smalest_details = 5

    for contour in contours:
        if cv2.contourArea(contour) > smalest_details:
            # Calculate bounding box
            x, y, w, h = cv2.boundingRect(contour)
            # Draw rectangle bounding box
            cv2.rectangle(img_original, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(img_generated, (x, y), (x + w, y + h), (0, 0, 255), 2)

            cv2.putText(img_generated, "Similarity: " + str(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    x = np.zeros(img_original.shape, dtype='uint8')
    result = np.hstack((img_original, x, img_generated))
    # cv2.imshow("Differences", result)
    # cv2.waitKey(0)

    # * 100 for % if needed
    return round(score, round_to)

def calculate_lpips(original_image_path, generated_image_path):
    img_original = convert_normalize(original_image_path)
    img_generated = convert_normalize(generated_image_path)

    lpips = LearnedPerceptualImagePatchSimilarity(net_type='vgg')
    score = lpips(img_original, img_generated)

    return round(float(score), round_to)

def convert_normalize(image_path):
    image = Image.open(image_path).convert('RGB')

    # Definiere die Transformationen
    transform = transforms.Compose([
        transforms.Resize((64, 64)),  # Ändere die Bildgröße auf 64x64 Pixel
        transforms.ToTensor(),  # Konvertiere das Bild in einen Tensor
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        # Normalisiere den Tensor auf den Bereich [-1, 1]
    ])

    # Wende die Transformationen auf das Bild an
    normalized_image = transform(image)

    # Füge eine zusätzliche Dimension hinzu, um die Batch-Dimension (1) zu simulieren
    normalized_image = normalized_image.unsqueeze(0)
    return normalized_image

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

def process_folder(folder_path, reference_path, starting_folder_name):
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
                #frame = extract_frame_from_filename(file)

                # Check if the corresponding original image exists in the reference folder
                original_image_path = os.path.join(reference_path, folder_name, file)
                if os.path.exists(original_image_path):
                    # Extract image dimensions
                    #width, height = get_image_dimensions(generated_image_path)
                    #area = width * height
                    # Calculate sharpness
                    #sharpness = calculate_sharpness(original_image_path, generated_image_path)

                    # Images
                    #img_original = cv2.imread(original_image_path)
                    #img_generated = cv2.imread(generated_image_path)

                    # Calculate PSNR
                    #psnr_value = calculate_psnr(img_original, img_generated)

                    # Calculate SSIM
                    #ssim_value = calculate_ssim(img_original, img_generated)

                    # Calculate LPIPS
                    lpips_value = calculate_lpips(original_image_path, generated_image_path)

                    #print(original_image_path)
                    #print(generated_image_path)

                    # Append data to list
                    data.append({
                        #'Upscaler': "Photoshop",
                        #'Starting Folder': starting_folder_name,
                        #'Folder Name': folder_name,
                        #'Frame': frame,
                        #'Width': width,
                        #'Height': height,
                        #'Area': area,
                        #'Sharpness': sharpness,
                        #'PSNR': psnr_value,
                        #'SSIM': ssim_value
                        #'LPIPS': lpips_value
                    })
                else:
                    print(f"Original image not found for {generated_image_path}")

            completed_files += 1
            percent_completed = (completed_files / total_files) * 100
            print(f'Progress: {percent_completed:.2f}%')

    return pd.DataFrame(data)

def main(root_folder, reference_folder):
    starting_folder_name = os.path.basename(root_folder)
    df = process_folder(root_folder, reference_folder, starting_folder_name)

    # print(df)

    # Save DataFrame to CSV within the starting folder
    csv_filename = os.path.join(root_folder, starting_folder_name + "_LPIPS" + ".csv")
    df.to_csv(csv_filename, index=False)


if __name__ == "__main__":

    folders = [
        #"achau-02_left", "achau-02_right",
        #"altenfelden-04_left", "altenfelden-04_right",
        #"grossebersdorf-03_left",
        "grossebersdorf-03_right",
        #"grossweikersdorf-15_left", "grossweikersdorf-15_right",
        #"hellas-kagran-01_left",
        #"hellas-kagran-01_right"
    ]

    for folder in folders:
        folder_path = f"04_AI_Upscale/LR_upscaling/06_SwinIR-L/{folder}"
        reference_path = f"03_Daten_PreProcessing/00_HighRes_Images/0_combined/{folder}"
        main(folder_path, reference_path)
