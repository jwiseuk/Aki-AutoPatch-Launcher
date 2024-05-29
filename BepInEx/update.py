import os, shutil, zipfile, hashlib, asyncio, subprocess, requests, gdown

directories_to_delete = [
    "config",
    "plugins"
]

file_ids = {
    "bepinex": "YOUR-FILE-ID-HERE",
}

folder_ids = {
    "config": "YOUR-CONFIG-FOLDER-ID-HERE",
}

API_KEY = "YOUR-API-KEY-HERE"

# Function to delete directories
def delete_directories():
    for directory in directories_to_delete:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"Deleted directory: {directory}")
        else:
            print(f"Directory not found: {directory}")

#Function to delete cacche
def delete_cache():
    response = input("Delete Cache? (Game will need to re-download mod bundles from server. Only delete if required) (Y/N): ").strip().upper()
    if response == "Y":
        BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
        cache_dir = os.path.join(BASE_DIR, 'user', 'cache')
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                print(f"Cache directory '{cache_dir}' deleted successfully.")
            except Exception as e:
                print(f"Error deleting cache directory: {e}")
        else:
            print(f"Cache directory '{cache_dir}' does not exist.")
    elif response == "N":
        print("Cache not deleted.")
    else:
        print("Invalid response. Please enter 'Y' or 'N'.")

# Function to download bepinex zip
def download_directories():
    output_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
    for directory, file_id in file_ids.items():
        output_path = os.path.join(output_dir, f"{directory}.zip")
        gdown.download(f"https://drive.google.com/uc?id={file_id}&export=download", output=output_path)

# Function to extract bepinex.zip
def extract_bepinex_zip():
    print("Extracting bepinex.zip")
    zip_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bepinex.zip")
    output_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            file_count = len(zip_ref.filelist)
            extracted_count = 0
            for file_info in zip_ref.infolist():
                zip_ref.extract(file_info, output_dir)
                extracted_count += 1
                progress = (extracted_count / file_count) * 100
                print(f"Progress: {progress:.2f}%\r", end='')
            print("\nExtracted bepinex.zip")
    else:
        print("bepinex.zip not found.")

# Function to check if the BepInEx file on Google Drive needs updating
def needs_update():
    print("Checking for Updates...")
    file_id = file_ids['bepinex']
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=md5Checksum&key={API_KEY}"
    requests.packages.urllib3.util.connection.HAS_IPV6 = False #Force requests to use IPV4 to correpsond with API key whitelists
    response = requests.get(url)
    if response.status_code == 200:
        drive_md5 = response.json().get('md5Checksum')
        local_bepinex_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bepinex.zip")
        if os.path.exists(local_bepinex_path):
            with open(local_bepinex_path, 'rb') as f:
                local_md5 = hashlib.md5(f.read()).hexdigest()
            return drive_md5 != local_md5
        return True
    else:
        print("Error fetching file metadata:", response.text)
        return False

# Function to download alternate configs
def download_configs():
    for directory, folder_id in folder_ids.items():
        url = f"https://drive.google.com/drive/folders/{folder_id}"
        print(url)
        gdown.download_folder(url)

#Function to prompt if user wants to Install Vanilla HUD FOV Configs
def prompt_install_configs():
    response = input("Install Vanilla HUD FOV Configs? (Y/N): ").strip().upper()
    if response == "Y":
        download_configs()
    elif response == "N":
        print("Skipping Vanilla HUD FOV configs installation.")
    else:
        print("Invalid response. Please enter 'Y' or 'N'.")
        prompt_install_configs()

#If hashes do not match, delete directories, download new zip and extract
async def updater():
    if needs_update():
        delete_directories()
        download_directories()
        extract_bepinex_zip()
        delete_cache()
        prompt_install_configs() #comment this out if not required
        print("Bepinex Updated to Latest Plugins & Configs.")
    else:
        print("Hashes Match - No Update Required.")
    return True

#Open AKI Launcher 
async def open_launcher():
    BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
    exe_path = os.path.join(BASE_DIR, "Aki.Launcher.exe")
    try:
        os.chdir(BASE_DIR)
        subprocess.Popen(exe_path)
    except Exception as e:
        print(f"Error: {e}")

#Await udpater logic to complete then start AKI Launcher and exit script
async def main():
    check_task = asyncio.create_task(updater())
    await check_task
    await open_launcher()

if __name__ == "__main__":
    asyncio.run(main())