import os
import shutil

def move_pdf_to_folder(pdf_path, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    new_filepath = os.path.join(folder_path, os.path.basename(pdf_path))
    shutil.move(pdf_path, new_filepath)
    print(f"Moved file to: {new_filepath}")
