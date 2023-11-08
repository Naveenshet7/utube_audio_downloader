import pytube
import streamlit as st
import requests
import os
import base64


# Function to sanitize a string for use as a filename
def sanitize_filename(filename):
    # Replace invalid characters with underscores
    invalid_characters = '\\/:*?"<>|'
    for char in invalid_characters:
        filename = filename.replace(char, '_')
    return filename

def get_file_size(video_url):
    try:
        yt = pytube.YouTube(video_url)
        video = yt.streams.filter(only_audio=True).first()
        file_size = video.filesize
        return file_size
    except Exception as e:
        return None

def download_audio(video_url, confirm, audio_format):
    try:
        if not confirm:
            st.warning("Please confirm that you want to download the audio.")
            return

        # Create a YouTube object from the URL
        yt = pytube.YouTube(video_url)

        # Get the best video stream with audio
        audio = yt.streams.filter(only_audio=True).first()

        # Get the video title and sanitize it for use as the filename
        video_title = sanitize_filename(yt.title)
        st.info(f"Downloading: {video_title}")

        # Define the output file path based on the selected audio format
        if audio_format == "MP3":
            output_file_path = video_title + ".mp3"
        elif audio_format == "OGG":
            output_file_path = video_title + ".ogg"

        # Download the video as an audio file
        response = requests.get(audio.url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))

        with open(output_file_path, "wb") as f:
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                downloaded_size = len(data)

        st.success(f"Audio downloaded successfully as '{video_title}.{audio_format.lower()}'")

        return output_file_path, video_title

    except pytube.exceptions.RegexMatchError:
        st.error("Invalid YouTube URL. Please enter a valid YouTube video URL.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

st.title("YouTube Audio Downloader")

# Input field for YouTube video URL
video_url = st.text_input("Enter YouTube Video URL:")

# Button to submit the YouTube URL
if st.button("Enter"):
    # Calculate and display audio file size
    file_size = get_file_size(video_url)
    if file_size:
        st.info(f"Estimated Audio File Size is: {file_size / (1024 * 1024):.2f} MB")
    else:
        st.warning("File size information is not available for this video.")

# Checkbox for confirmation
confirmation = st.checkbox("Confirm to download this Audio")

# Select audio format
audio_format = st.selectbox("Select Audio Format", ["MP3", "OGG"])

# Button to trigger the download process
if st.button("Download Audio"):
    # Call the download function with confirmation status and selected audio format
    output_file_path, video_title = download_audio(video_url, confirmation, audio_format)

# Function to create a download link
def create_download_link(file_path, audio_format, video_title):
    with open(file_path, "rb") as file:
        file_contents = file.read()
    b64 = base64.b64encode(file_contents).decode()
    return f'<a href="data:file/{audio_format};base64,{b64}" download="{video_title}.{audio_format.lower()}">Click here to download</a>'

# Display a download link if the audio file exists
if 'output_file_path' in locals():
    st.write("Download your audio:")
    st.markdown(create_download_link(output_file_path, audio_format, video_title), unsafe_allow_html=True)
    st.balloons() 
    
# Developer information
st.sidebar.title("Dev")
st.sidebar.markdown(
    """
    **Developer:** NK21
    https://t.me/technicalsagar7
    """
)
