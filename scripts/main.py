"""main function"""

from datetime import datetime
import pandas as pd 

from mp4_to_mp3 import convert_directory
from parse_google_doc import get_google_sheet
from get_dropbox_files import get_dropbox_files
from file_utils import get_local_files
from upload import upload_to_mixcloud

def add_filepath_column(filtered_df, files):
    # Ensure Client_Mod is in datetime format
    files['Client_Mod'] = pd.to_datetime(files['Client_Mod'])

    # Create the new filepath column in filtered_df
    filtered_df['filepath'] = None
    
    # Iterate over rows of filtered_df
    for index, row in filtered_df.iterrows():
        # Extract the 30m before and 30m after times for the current row
        time_before = row['30m before']
        time_after = row['30m after']
        
        # Find the matching rows in 'files' where Client_Mod falls between 30m before and 30m after
        matching_row = files[(files['Client_Mod'] >= time_before) & (files['Client_Mod'] <= time_after)]
        
        # If a match is found, add the 'Name' value with prefix to the filepath column
        if not matching_row.empty:
            # Assuming 'Name' column exists in 'files' and taking the first match
            filtered_df.at[index, 'filepath'] = "test/input/" + matching_row['Name'].values[0]

    return filtered_df

def main(todays_date, use_local_files=False):

    convert_directory(input_dir="test/input", 
                       output_dir="test/output")

    metadata = get_google_sheet()

    if not todays_date:
        today = datetime.now()
        formatted_date = today.strftime('%Y-%m-%d')
    else:
        date_object = datetime.strptime(todays_date, '%d/%m/%Y')
        formatted_date = date_object.strftime('%Y-%m-%d')

    filtered_df = metadata[metadata['Start time of your show'].dt.strftime('%Y-%m-%d') == formatted_date]

    if use_local_files:
        files = get_local_files("test/input")
    else:
        files = get_dropbox_files(mp4_path="test/input",
                                acess_token_path="dropbox_access_token", 
                                )
    
    filtered_df = add_filepath_column(filtered_df, files)

    for index, row in filtered_df.iterrows():
        upload_to_mixcloud(row, "access_token")