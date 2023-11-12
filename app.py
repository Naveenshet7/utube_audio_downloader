import streamlit as st
from st_clickable_images import clickable_images
import pandas as pd
from pytube import YouTube
import os
import requests
from time import sleep
import base64  # Import base64 module for encoding the MP3 file

@st.cache_data
def save_audio(url):
    yt = YouTube(url)
    try:
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download()
        
        # Calculate file size
        file_size = os.path.getsize(out_file) / (1024 * 1024)  # Convert to MB

        base, ext = os.path.splitext(out_file)
        file_name = base + '.mp3'
        
        # Check if the destination file already exists
        if os.path.exists(file_name):
            os.remove(file_name)  # Delete the existing file
        
        os.rename(out_file, file_name)
    except:
        return None, None, None, None
    print(yt.title + " has been successfully downloaded.")
    print(file_name)
    return yt.title, file_name, yt.thumbnail_url, file_size

st.title("Utube Audio Downloader")

file = st.file_uploader("Upload a file that includes the links (.txt)")

if file is not None:
    dataframe = pd.read_csv(file, header=None)
    dataframe.columns = ['urls']
    urls_list = dataframe['urls'].tolist()

    titles = []
    locations = []
    thumbnails = []
    file_sizes = []

    for video_url in urls_list:
        # download audio
        video_title, save_location, video_thumbnail, file_size = save_audio(video_url)
        if video_title:
            titles.append(video_title)
            locations.append(save_location)
            thumbnails.append(video_thumbnail)
            file_sizes.append(file_size)

    selected_video = clickable_images(thumbnails,
    titles = titles,
    div_style={"height": "230px", "display": "flex", "justify-content": "center", "flex-wrap": "wrap", "overflow-y":"auto"},
    img_style={"margin": "8px", "height": "200px"}
    )

    st.markdown(f"Thumbnail #{selected_video} clicked" if selected_video > -1 else "No image clicked")

    if selected_video > -1:
        video_url = urls_list[selected_video]
        video_title = titles[selected_video]
        save_location = locations[selected_video]
        size_mb = file_sizes[selected_video]

        st.header(video_title)
        st.write(f"File Size: {size_mb:.2f} MB")  # Display the file size before playing audio
        st.audio(save_location)

        # Button to generate download link
        if st.button("Generate Download Link"):
            with open(save_location, 'rb') as file:
                audio_data = file.read()
                # Encode the MP3 file as a data URI for download
                audio_base64 = base64.b64encode(audio_data).decode()
                st.markdown(f'<a href="data:audio/mp3;base64,{audio_base64}" download="{video_title}.mp3">Download {video_title}.mp3</a>', unsafe_allow_html=True)
        
        # Trigger balloon animation when the image is clicked
        if st.button("NK21❤️"):
            st.balloons()

# Developer information
st.sidebar.title("Dev")
st.sidebar.markdown(
    """
    **Developer:** NK21
    https://t.me/technicalsagar7
    """
)
