import zipfile
import os
import shutil

def clear_directory(folder_path):
    """
    Clears all files and subdirectories in the given folder.
    
    Parameters:
    - folder_path: path to the folder to clear
    """
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def save_tempfile_to_permanent_location(temp_file, destination_path="./zip_cache/zip_cache.zip"):
    with open(destination_path, 'wb') as out_file:
        # Reset the file pointer of the temp file to the beginning
        temp_file.seek(0)
        
        # Copy the contents of the temp file to the destination file
        shutil.copyfileobj(temp_file, out_file)



def unzip_file(input_, input_type="file", dest_folder="./zip_cache"):
    """
    Unzips a zip file to a specified destination folder.

    Parameters:
    - zip_filepath: path to the zip file
    - dest_folder: path to the destination folder where files will be extracted
    """

    clear_directory("./zip_cache")

    if input_type == "path":
        with zipfile.ZipFile(input_, 'r') as zip_ref:
            zip_ref.extractall(dest_folder)
    if input_type == "file":
        save_tempfile_to_permanent_location(input_)
        with zipfile.ZipFile("./zip_cache/zip_cache.zip", 'r') as zip_ref:
            zip_ref.extractall(dest_folder)
        

if __name__=="__main__":
    unzip_file("/Users/lishande/Downloads/封存.zip", input_type="path")



