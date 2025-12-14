# Brixton Radio Automation Pipeline

This project automates the workflow for Brixton Radio, handling the fetching of show metadata, conversion of audio files, and uploading shows to Mixcloud.

## Features

-   **Metadata Synchronization**: Fetches show schedules from a Google Sheet.
-   **Audio Processing**: Converts `.mp4` video recordings to `.mp3` audio format.
-   **Automated Uploads**: Uploads the processed audio to Mixcloud with correct metadata (Title, Description, Tags).
-   **Flexible File Source**: Supports fetching files from Dropbox (Live Mode) or a local directory (Test Mode).

## Prerequisites

-   Python 3.8+
-   `ffmpeg` (required for audio conversion via `moviepy`)
-   A Google Cloud Project with Sheets API enabled.
-   A Dropbox App.
-   A Mixcloud App.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/brixton_radio.git
    cd brixton_radio
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` is missing, install: `pandas`, `moviepy`, `dropbox`, `requests`)*

## Configuration & Tokens

To run this pipeline, you need several access tokens. Save these in the root directory of the project.

### 1. Mixcloud
1.  Go to [Mixcloud Developers](https://www.mixcloud.com/developers/) and create a new app.
2.  Note your `Client ID` and `Client Secret`.
3.  Use the provided `access_token` file mechanism or Authorization Code flow to generate an OAuth token.
    -   **Auth URL**: `https://www.mixcloud.com/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI`
    -   Get the code from the redirect URL.
    -   **Exchange for Token**: `https://www.mixcloud.com/oauth/access_token?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&client_secret=YOUR_CLIENT_SECRET&code=OAUTH_CODE`
4.  Save the token string in a file named `access_token`.

### 2. Dropbox
1.  Go to [Dropbox App Console](https://www.dropbox.com/developers/apps).
2.  Create an app with "Full Dropbox" or "App Folder" access.
3.  Generate an Access Token in the settings.
4.  Save it in a file named `dropbox_access_token`.

### 3. Google Sheets
1.  The script currently reads a public published CSV link or requires a Service Account JSON.
2.  For this version, ensure the Google Sheet is accessible or update `parse_google_doc.py` with your credentials.

## Usage

### Local / Test Mode
Use this mode to test the pipeline with local files without connecting to Dropbox.

1.  Place your testing `.mp4` files in `test/input/`.
2.  Run the script with the local flag:
    ```bash
    python3 scripts/main.py --local
    ```
    *(Note: You may need to modify `main.py` entry point to accept command line args or call the function directly as shown in `test/test_main.py`)*

    **Current Script Usage:**
    Open `scripts/main.py` or run the test suite to see it in action:
    ```bash
    python3 test/test_main.py
    ```

### Live / Dropbox Mode
1.  Ensure files are uploaded to your Dropbox folder.
2.  Run the script:
    ```bash
    python3 scripts/main.py
    ```

## Development

### Running Tests
Unit and integration tests are located in the `test/` directory.
```bash
python3 test/test_main.py
```

### Directory Structure
-   `scripts/`: Core logic (`main.py`, `upload.py`, etc.)
-   `test/`: Unit tests and local test files.
-   `test/input/`: Place `.mp4` files here for local testing.
-   `test/output/`: Converted `.mp3` files will appear here.

