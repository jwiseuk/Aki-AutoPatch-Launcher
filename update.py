import os
import shutil
import zipfile
import hashlib
import asyncio
import subprocess
import requests
from tqdm import tqdm

# Configuration
URL = 'http://YOURSERVERIP:5000/download/bepinex.zip'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_FILENAME = os.path.join('Bepinex', 'bepinex.zip')
DIRECTORIES_TO_DELETE = ['config', 'plugins']

# Function to calculate MD5 checksum
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to delete directories
def delete_directories():
    for directory in DIRECTORIES_TO_DELETE:
        full_path = os.path.join(BASE_DIR, 'Bepinex', directory)
        if os.path.exists(full_path):
            shutil.rmtree(full_path)
            print(f"Deleted directory: {full_path}")
        else:
            print(f"Directory not found: {full_path}")

# Function to download a file with a progress bar
def download_file(url, local_filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192  # 8 Kibibytes

    with open(local_filename, 'wb') as file:
        with tqdm(total=total_size, unit='iB', unit_scale=True) as progress_bar:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
                    progress_bar.update(len(chunk))
    return local_filename

# Function to extract bepinex.zip
def extract_bepinex_zip():
    print("Extracting bepinex.zip")
    zip_file_path = os.path.join(BASE_DIR, 'Bepinex', 'bepinex.zip')
    output_dir = os.path.join(BASE_DIR, 'Bepinex')
    if os.path.exists(zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
    else:
        print("bepinex.zip not found.")

# Function to check if the BepInEx file needs updating
def needs_update():
    print("Checking for Updates...")
    md5_url = f"{URL}.md5"
    try:
        response = requests.get(md5_url)
        response.raise_for_status()
        drive_md5 = response.text.strip().split()[0]
    except requests.RequestException as e:
        print(f"Error fetching file metadata: {e}")
        return False

    local_bepinex_path = os.path.join(BASE_DIR, 'Bepinex', 'bepinex.zip')
    if os.path.exists(local_bepinex_path):
        local_md5 = calculate_md5(local_bepinex_path)
        return drive_md5 != local_md5
    return True

# If hashes do not match, delete directories, download new zip and extract
async def updater():
    if needs_update():
        delete_directories()
        download_file(URL, LOCAL_FILENAME)
        extract_bepinex_zip()
        print("Bepinex Updated to Latest Plugins & Configs.")
    else:
        print("Hashes Match - No Update Required.")
    return True

# Open AKI Launcher
async def open_launcher():
    exe_path = os.path.join(BASE_DIR, "Aki.Launcher.exe")
    try:
        subprocess.Popen([exe_path])
    except Exception as e:
        print(f"Error: {e}")

# Await updater logic to complete then start AKI Launcher and exit script
async def main():
    await updater()
    await open_launcher()

if __name__ == "__main__":
    asyncio.run(main())