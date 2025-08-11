import streamlit as st
import os
from modules.chatbot.vector import process_and_vectorize_files
from modules import Knowledgebase_extension
from collections import defaultdict

# Define the main upload folder
UPLOAD_FOLDER = "./uploads"

# Define the file for bot purpose
BOT_PURPOSE_FILE = "./bot_purpose.txt"


# Ensure the main upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to create subfolders if they don't exist
def create_subfolder(folder_name):
    subfolder_path = os.path.join(UPLOAD_FOLDER, folder_name)
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
    return subfolder_path

def onboarding_page():
    # Set the title and description of the page
    st.title("First Time Onboarding")
    st.markdown("## Knowledge Base")
    st.markdown("Add more knowledge from various sources.")

    # Layout for file upload categories
    categories = ["SKU's", "Product Information", "Troubleshooting Guides", "FAQs", "Guidelines", "Government Guidelines"]

    uploaded_files = {category: None for category in categories}
    
    # Create subfolders for each category
    subfolders = {category: create_subfolder(category) for category in categories}
    
    # Upload and input fields for each category
    for category in categories:
        with st.expander(f"Upload {category} Files"):
            uploaded_files[category] = st.file_uploader(f"Choose files for {category}", accept_multiple_files=True)
    
    youtube_url = st.text_input("Enter the YouTube Channel URL")

    # Submit button to save files and YouTube link
    if st.button("Submit"):
        saved_files = []
        saved_file_paths_by_category = defaultdict(list)
        for category, files in uploaded_files.items():
            if files:
                for uploaded_file in files:
                    file_path = os.path.join(subfolders[category], uploaded_file.name)

                    # Save the file
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    saved_files.append(f"{category}: {uploaded_file.name}")
                    saved_file_paths_by_category[category].append(file_path)
        process_and_vectorize_files(saved_file_paths_by_category)
        # Save YouTube link in bot purpose file
        saved_youtube_urls = True
        video_links = []
        if youtube_url:
            if Knowledgebase_extension.is_valid_youtube_channel(youtube_url):
                with open(BOT_PURPOSE_FILE, "w") as f:
                    f.write(f"YouTube Channel: {youtube_url}\n")
                # Fetch video links
                video_links = Knowledgebase_extension.get_video_links(youtube_url)
                if video_links:
                    with open(BOT_PURPOSE_FILE, "a") as f:
                        for link in video_links:
                            f.write(f"\t YouTube Channel Link: {link}\n")
                else:
                    st.warning("No videos found for this channel.")
            else:
                saved_youtube_urls = False


        # Display saved files
        saved_files_to_disk = True
        if saved_files:
            st.write("### Uploaded Files:")
            for file in saved_files:
                st.write(f"✅ {file}")

        if youtube_url and saved_youtube_urls is True:
            if video_links:
                    for link in video_links:
                        st.write(f"- [{link}]({link})")
            st.write(f"✅ YouTube Channel Link Saved: {youtube_url}")
        else:
            st.error("Invalid YouTube Channel URL! Please enter a valid link.")
        if saved_files_to_disk is True and saved_youtube_urls is True:
        # Show success message
            st.success("Data saved successfully!")
        
    # Skip and Back buttons
    st.markdown("---")
    col_back, col_skip = st.columns(2)
    with col_back:
        st.button("Back")
    with col_skip:
        st.button("Skip for now")
    
    if st.button("Continue"):
        # st.session_state.page = "Knowledgebase"
        st.session_state.page = "Training"
        st.rerun()

