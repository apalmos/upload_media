import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add scripts to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from main import add_filepath_column, main

class TestBrixtonRadio(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.show_time = datetime.now()
        
        # DataFrame mimicking the Google Sheet
        self.metadata = pd.DataFrame({
            'Start time of your show': [self.show_time],
            '30m before': [self.show_time - timedelta(minutes=30)],
            '30m after': [self.show_time + timedelta(minutes=30)],
            'Show Name': ['Test Show']
        })

        # DataFrame mimicking the Local/Dropbox files
        self.files = pd.DataFrame({
            'Name': ['test_show.mp4', 'other_show.mp4'],
            'Client_Mod': [self.show_time, self.show_time - timedelta(hours=2)]
        })

    def test_add_filepath_column(self):
        """Test matching logic (timestamp based)"""
        result_df = add_filepath_column(self.metadata.copy(), self.files)
        
        # Check if matched
        matched_path = result_df.iloc[0]['filepath']
        self.assertEqual(matched_path, "test/input/test_show.mp4")

    @patch('main.get_google_sheet')
    @patch('main.get_local_files')
    @patch('main.convert_directory')
    @patch('main.upload_to_mixcloud')
    def test_main_local_mode(self, mock_upload, mock_convert, mock_get_files, mock_get_sheet):
        """Integration test for main function in local mode"""
        
        # Setup mocks
        mock_get_sheet.return_value = self.metadata
        mock_get_files.return_value = self.files
        
        # Run main with today's date formatted
        today_str = self.show_time.strftime('%d/%m/%Y')
        
        main(todays_date=today_str, use_local_files=True)
        
        # Verify calls
        mock_convert.assert_called_once()
        mock_get_files.assert_called_with("test/input")
        mock_upload.assert_called() # Should be called for the matched row

    def test_no_match(self):
        """Test when no files match the time window"""
        # Files completely outside the window
        files_no_match = pd.DataFrame({
            'Name': ['old_show.mp4'],
            'Client_Mod': [self.show_time - timedelta(hours=5)]
        })
        
        result_df = add_filepath_column(self.metadata.copy(), files_no_match)
        self.assertIsNone(result_df.iloc[0]['filepath'])

if __name__ == '__main__':
    unittest.main()
