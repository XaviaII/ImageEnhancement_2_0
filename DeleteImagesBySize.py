import os
import csv
from PIL import Image
from tqdm import tqdm

def check_image_sizes(root_folder, min_width, min_height, folder):
    csv_filename = os.path.join('03_Daten_PreProcessing/test', f"{folder}_deleted_images.csv")
    # Open CSV file for writing
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['File Path', 'Width', 'Height'])

        # Traverse folders and subfolders
        total_files = sum(len(files) for _, _, files in os.walk(root_folder))
        progress_bar = tqdm(total=total_files, desc="Checking Image Sizes", unit="image")
        for root, dirs, files in os.walk(root_folder):
            for file in files:
                if file.endswith(".png"):
                    file_path = os.path.join(root, file)
                    try:
                        with Image.open(file_path) as img:
                            width, height = img.size
                            if width < min_width or height < min_height:
                                csv_writer.writerow([file_path, width, height])
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
                    progress_bar.update(1)
        progress_bar.close()
    return csv_filename

def delete_images_from_csv(csv_filename):
    deleted_count = 0
    with open(csv_filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip header row
        total_files = sum(1 for _ in csv_reader)
        progress_bar = tqdm(total=total_files, desc="Deleting Images", unit="image")
        csvfile.seek(0)  # Reset file pointer to start
        next(csv_reader)  # Skip header row again
        for row in csv_reader:
            file_path = row[0]
            try:
                os.remove(file_path)
                deleted_count += 1
                progress_bar.update(1)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        progress_bar.close()
    return deleted_count

if __name__ == "__main__":
    folders = [
        "02_HighRes_Subset_Images"
        # "00_NearestNeighbor",
        # "01_Photoshop",
        # "02_ESRGAN",
        # "03_RealESRGAN",
        # "04_BSRGAN",
        # "05_SwinIR",
        # "06_SwinIR-L",
        # "07_HAT",
        # "08_HAT-L"
    ]

    min_width = 193
    min_height = 193

    for folder in folders:
        print(f"start: {folder}")
        folder_path = f'03_Daten_PreProcessing/test/{folder}'
        csv_filename = check_image_sizes(folder_path, min_width, min_height, folder)
        print(f"Image sizes checked and saved to {csv_filename} successfully.")



    for folder in folders:
        csv_filename = f"03_Daten_PreProcessing/test/{folder}_deleted_images.csv"
        print(f"start: {folder}")
        deleted_count = delete_images_from_csv(csv_filename)
        print(f"Total files deleted: {deleted_count}")