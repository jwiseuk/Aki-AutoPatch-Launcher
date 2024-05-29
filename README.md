## Overview

This Python script automates the process of updating BepInEx plugins and configurations for Single Player Tarkov. It performs several tasks including deleting specified directories, downloading and extracting the latest BepInEx zip file from Google Drive, deleting the cache (if necessary), and optionally installing vanilla HUD FOV configurations. The script also checks if an update is needed by comparing the MD5 checksum of the local and remote BepInEx zip files.

## Prerequisites

- Python 3.x
- Required Python packages: `gdown`
- Google Drive API key
- Google Drive file IDs for BepInEx zip and configuration folders containing vanilla HUD fovs (recommend using google drive to sync these from hosts PC.)

## Setup

1. **Install Required Packages:**
   ```bash
   pip install requests gdown
2. Use commit.py to compress your 'plugins' and 'config' folders to '/BepInEx/Sync/BepInEx.Zip'. 
3. Set up Google Drive to share the Sync Folder and make the file public, add the file ID to the script.
4. Optionally, create vanilla HUD FOV configs for Fontaines FOV Fix mod and store them in another shared folder 'sync/configs'. Add the folder ID of /configs to the script.
5. Set Up API Key and IDs:
Replace the placeholder values for API_KEY, file_ids['bepinex'], and folder_ids['config'] with your actual Google Drive API key and file IDs.

## Script Details

**Workflow**
- Check for Updates: The script checks if the local BepInEx zip file needs to be updated by comparing MD5 checksums with the remote file on Google Drive.
- Delete Directories: If an update is needed, specified directories are deleted.
- Download BepInEx Zip: The latest BepInEx zip file is downloaded from Google Drive.
- Extract Zip File: The downloaded zip file is extracted.
- Delete Cache: The user is prompted to delete the cache directory if necessary.
- Install Configurations: The user is prompted to install vanilla HUD FOV configurations.
- Update Completion: If an update was performed, a message is displayed confirming the update.
- Launch Game: The game launcher is opened.
  
## Usage
- Place in your SPT directory
- Run 'Aki-AutoPatch-Launcher.bat in place of 'Aki-Launcher.exe'
