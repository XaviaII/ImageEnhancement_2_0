import os
import shutil
from tqdm import tqdm


def copytree(src, dst):
    try:
        # Get the total number of files and directories to copy
        total_files = sum(len(files) for _, _, files in os.walk(src))

        # Initialize tqdm with the total number of files
        progress_bar = tqdm(total=total_files, desc="Copying")

        # Copy files
        for root, dirs, files in os.walk(src):
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst, os.path.relpath(src_file, src))
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)
                progress_bar.update(1)  # Update progress bar
        progress_bar.close()

        print(f"Directory '{src}' successfully copied to '{dst}'")
    except OSError as e:
        print(f"Error: {e}")


# Example usage:
source_directory = "03_Daten_PreProcessing/00_HighRes_Images/0_combined"
destination_directory = "//L-203/Users/Default/4_Semester/daten/03_Daten_PreProcessing/00_HighRes_Images/0_combined"

copytree(source_directory, destination_directory)
