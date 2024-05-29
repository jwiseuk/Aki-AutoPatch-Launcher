import os
import zipfile
import requests
from tqdm import tqdm
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

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
    file_size = os.path.getsize(zip_filename)
    
    with open(zip_filename, 'rb') as file:
        encoder = MultipartEncoder(fields={'file': ('filename', file, 'application/zip')})
        
        with tqdm(total=file_size, unit='B', unit_scale=True, desc='Uploading') as pbar:
            def monitor_callback(monitor):
                pbar.update(monitor.bytes_read - pbar.n)
            
            monitor = MultipartEncoderMonitor(encoder, monitor_callback)
            headers = {'Content-Type': monitor.content_type}

            response = requests.post(server_url, data=monitor, headers=headers)
            content = response.content

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
