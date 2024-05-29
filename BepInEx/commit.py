import os
import zipfile
import requests
from tqdm import tqdm

# Config
folders = ['config', 'plugins']
zip_file_path = 'sync/bepinex.zip'
server_url = 'http://YOUR-SERVER-IP:5000/upload'

def compress_folders_to_zip(zip_filename, folders_to_compress):
    total_files = sum(len(files) for folder in folders_to_compress for _, _, files in os.walk(folder))
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        with tqdm(total=total_files, desc='Compressing', unit='file') as pbar:
            for folder in folders_to_compress:
                for root, _, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, os.path.join(os.getcwd(), folder))
                        zipf.write(file_path, arcname=os.path.join(folder, relative_path))
                        pbar.update(1)

def upload_zip_to_server(zip_filename, server_url):
    with open(zip_filename, 'rb') as file:
        files = {'file': file}
        with tqdm(desc='Uploading', unit='B', unit_scale=True) as pbar:
            response = requests.post(server_url, files=files, stream=True)
            content = b''  # Variable to store response content
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    pbar.update(len(chunk))
                    content += chunk  # Append response content

    if response.status_code == 200:
        print("File uploaded successfully.")
    else:
        print(f"Error uploading file: {content.decode('utf-8')}")
        if response.status_code == 403:
            print("Your IP is not whitelisted.")


if __name__ == "__main__":
    # Compress the folders to the zip file
    compress_folders_to_zip(zip_file_path, folders)
    # Upload the zip file to the server
    upload_zip_to_server(zip_file_path, server_url)