import os
import zipfile

def compress_folders_to_zip(zip_filename, folders_to_compress):
    # Check if the zip file already exists, if so, remove it
    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    # Create a new zip file
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder in folders_to_compress:
            # Add the entire folder and its contents to the zip file
            for root, _, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, os.path.join(os.getcwd(), folder))
                    zipf.write(file_path, arcname=os.path.join(folder, relative_path))

if __name__ == "__main__":
    # Define the folders to compress
    folders = ['config', 'plugins']
    # Define the path to the zip file
    zip_file_path = 'sync/bepinex.zip'
    
    # Call the function to compress the folders to the zip file
    compress_folders_to_zip(zip_file_path, folders)

    print(f'Folders {folders} compressed to {zip_file_path}')
