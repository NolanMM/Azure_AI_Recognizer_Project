import os
import shutil


def delete_folder(folder_path):
    try:
        full_path = os.getcwd()
        desired_path = full_path.split(".venv")[0].rstrip(os.path.sep)
        path = os.path.join(desired_path, folder_path)
        # Delete the folder and its contents
        shutil.rmtree(path)
        print(f"Folder '{path}' and its contents deleted successfully.")
    except OSError as e:
        print(f"Error: {path} : {e.strerror}")
