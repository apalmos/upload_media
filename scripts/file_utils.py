import os
import pandas as pd
from datetime import datetime
import dropbox

def get_local_files(directory):
    """
    List files in a local directory and return as a pandas DataFrame.
    """
    files_data = []
    
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return pd.DataFrame(columns=["Name", "Client_Mod"])

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            # Get last modified time
            mod_time = os.path.getmtime(filepath)
            dt_mod_time = datetime.fromtimestamp(mod_time)
            
            files_data.append({
                "Name": filename,
                "Client_Mod": dt_mod_time
            })
            
    return pd.DataFrame(files_data)

def list_files_in_dropbox_folder(folder_path, dbx):
    """
    List files in a Dropbox folder and return as a pandas DataFrame.
    """
    files_data = []

    try:
        # If folder_path is root, pass an empty string
        if folder_path == "/":
            folder_path = ""

        # List all files in the given Dropbox folder
        result = dbx.files_list_folder(folder_path)

        files_data.extend(
            {
                "Name": entry.name,
                "Client_Mod": entry.client_modified,
                "Server_Mod": entry.server_modified,
            }
            for entry in result.entries
            if isinstance(entry, dropbox.files.FileMetadata)
        )
    except dropbox.exceptions.ApiError as err:
        print(f"Failed to list folder contents: {err}")

    return pd.DataFrame(files_data)
