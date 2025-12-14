from moviepy.editor import VideoFileClip
import os

def convert_mp4_to_mp3(mp4_path, mp3_path):
    """
    Convert an MP4 file to an MP3 file.

    Parameters:
    mp4_path (str): The path to the input MP4 file.
    mp3_path (str): The path to the output MP3 file.
    """
    try:
        # Load the video file
        video = VideoFileClip(mp4_path)
        
        # Extract the audio
        audio = video.audio
        
        # Write the audio to an MP3 file
        audio.write_audiofile(mp3_path)
        
        # Close the video and audio clips
        audio.close()
        video.close()
        
        print(f"Successfully converted {mp4_path} to {mp3_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_directory(input_dir, output_dir):
    """
    Convert all mp4 files in input_dir to mp3 in output_dir.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".mp4"):
            mp4_path = os.path.join(input_dir, filename)
            mp3_filename = os.path.splitext(filename)[0] + ".mp3"
            mp3_path = os.path.join(output_dir, mp3_filename)
            
            # Check if already exists to avoid re-conversion (optional optimization)
            if not os.path.exists(mp3_path):
                convert_mp4_to_mp3(mp4_path, mp3_path)
            else:
                print(f"Skipping {filename}, already converted.")
