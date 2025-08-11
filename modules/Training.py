import streamlit as st
import os
from modules.file_upload import process_files
from modules.scraper import product
from modules.scraper import sku
from modules.scraper import file
from modules.scraper import Faq_generation
from modules.scraper import guidenace_generation
from modules.scraper import handoff_generation
from modules.scraper import video
import pandas as pd
import json
from .chatbot.chat import chatting


df = pd.read_excel('website_scrape.xlsx')
json_data = df.to_dict(orient="records")
with open("website_data.json", "w") as f:
    json.dump(json_data, f, indent=4)

# Specify the folder where files are uploaded
upload_folder = './uploads'

# Process the files and generate the JSON
json_files_data = process_files(upload_folder)

def show_products():
    st.header("Products")
    df = pd.read_excel('website_scrape.xlsx')
    json_data = df.to_dict(orient="records")
    with open("website_data.json", "w") as f:
        json.dump(json_data, f, indent=4)
    response_pro=product(json_data)
    # response_pro_j = json.loads(response_pro)
    # products_df = pd.DataFrame({"Products": response_pro.get("products", [])})
    products_df = pd.DataFrame(response_pro.get("Products", []))

    styled_df = products_df.style.set_properties(**{
    'font-weight': 'bold',  # Make column headers bold
    'text-align': 'left'    # Align text to the left
    }) # Hide the index column

# Display the styled DataFrame
    st.table(styled_df)
    # st.table(products_df)
 
    # st.write("List of products will appear here.")

# Function to display SKUs
def show_skus():
    st.header("SKUs")
    df = pd.read_excel('website_scrape.xlsx')
    json_data = df.to_dict(orient="records")
    with open("website_data.json", "w") as f:
        json.dump(json_data, f, indent=4)
    response_pro=sku(json_data)
    sku_df = pd.DataFrame(response_pro.get("SKUS", []))
    styled_df = sku_df.style.set_properties(**{
    'font-weight': 'bold',  # Make column headers bold
    'text-align': 'left'    # Align text to the left
    }) # Hide the index column

# Display the styled DataFrame
    st.table(styled_df)
    st.write("List of SKUs will appear here.")

# Function to display File Uploads
def show_file_uploads():
    st.header("File Uploads")
    response_file=file(json_files_data)
    # st.write(response_file)
    file_df = pd.DataFrame(response_file.get("files", []))
    styled_df = file_df.style.set_properties(**{
    'font-weight': 'bold',  # Make column headers bold
    'text-align': 'left'    # Align text to the left
    }) # Hide the index column

# Display the styled DataFrame
    st.table(styled_df)
    




# Function to display FAQs
def show_faqs():
    st.header("FAQs")
    with open("./faqs.json", "r") as file:
        faq_dict = json.load(file)
    
    response_faq=Faq_generation(json_files_data)
    faq_dict_2 = response_faq.get("faqs", [])
    print(faq_dict_2)
    if 'faq_states' not in st.session_state:
        st.session_state.faq_states = {}

# Function to save the FAQ states to a file
    def save_faq_states_to_file():
        with open("FAQ.txt", "w") as file:
            for key, value in st.session_state.faq_states.items():
                file.write(f"{key}: {value}\n")
    for faq in faq_dict_2:
                for key, value in faq.items():  # Iterate over key-value pairs in each dictionary
                    if key.startswith("Q"):  # If the key starts with "Q", it's a question
                        question = value  # The value of the "Qx" key is the question
                        # Find the corresponding answer (assuming the answer key is always "A" + number)
                        answer_key = key.replace("Q", "A")
                        answer = faq.get(answer_key, "No answer available.")  # Get the corresponding answer

                        # Display the question and answer
                        if question and answer:
                            with st.expander(question):  # Display each question as an expandable element
                                st.write(answer)  # S # Show the corresponding answer
                                radio_key = f"radio_{key}"  # Unique key for the radio button
                                radio_state = st.radio(
                                    "Toggle On/Off",
                                    options=["Off", "On"],
                                    key=radio_key,
                                    index=0 if st.session_state.faq_states.get(radio_key, "Off") == "Off" else 1
                                )
                                
                                # Update the session state with the current radio button state
                                st.session_state.faq_states[radio_key] = radio_state

    for faq in faq_dict:
                for key, value in faq.items():  # Iterate over key-value pairs in each dictionary
                    if key.startswith("Q"):  # If the key starts with "Q", it's a question
                        question = value  # The value of the "Qx" key is the question
                        # Find the corresponding answer (assuming the answer key is always "A" + number)
                        answer_key = key.replace("Q", "A")
                        answer = faq.get(answer_key, "No answer available.")  # Get the corresponding answer

                        # Display the question and answer
                        if question and answer:
                            with st.expander(question):  # Display each question as an expandable element
                                st.write(answer)
    # st.write(response_faq)


# Function to display Web Pages
def show_web_pages():
    st.header("Web Pages")
    # web_pages = []

    df=pd.read_excel('website_scrape.xlsx')
    df=df[['URL']]
    # products_df = pd.DataFrame(response_pro.get("Products", []))

    styled_df = df.style.set_properties(**{
    'font-weight': 'bold',  # Make column headers bold
    'text-align': 'left'    # Align text to the left
    }) # Hide the i
    st.table(styled_df)
    

# Function to display Videos
def show_videos():
    st.header("Videos")
    video_urls = []
    with open('./bot_purpose.txt', 'r') as file:
        video_content = file.read()
        response_video = video(video_content)
        # video_df = pd.DataFrame(response_video.get("videos", []))
        # styled_df = video_df.style.set_properties(**{
        # 'font-weight': 'bold',  # Make column headers bold
        # 'text-align': 'left'    # Align text to the left
        # }) # Hide th

        st.write(response_video)

    

    


def guideance_bot():
    st.header("Guidance Bot")
    
    # Read the initial content from bot_purpose.txt
    with open('./bot_purpose.txt', 'r') as file:
        file_content = file.read()
    
    # Generate the initial response guidance
    # response_guideance = guidenace_generation(file_content)

    

    # Assume `response_guidance` is the output from `guidenace_generation(file_content)`
    response_guidance = guidenace_generation(file_content)

    # Split the response into individual guidance points
    guidance_points = response_guidance.split("\n\n")  # Assuming each point is separated by double newlines

    # Display each guidance point in its own section
    for i, point in enumerate(guidance_points):
        # Extract the section title (first line) and content (remaining lines)
        lines = point.split("\n")
        section_title = lines[0]  # First line is the title
        section_content = "\n".join(lines[1:])  # Remaining lines are the content

        # Display the section title and content
        st.markdown(f"### {section_title}")
        st.write(section_content)

        # Add a text area for user input under each section
        user_guidance = st.text_area(f"Add your manual guidance for '{section_title}' here:", key=f"user_guidance_{i}")

        # If the user provides input, append it to the guidance
        if user_guidance:
            updated_guidance = point + "\n" + user_guidance  # Combine the original point with user input
            st.write("### Updated Guidance for This Section:")
            st.write(updated_guidance)

            # Append the new guidance to the guidance.txt file
            with open('./guidance.txt', 'a') as guidance_file:
                guidance_file.write("\n" + updated_guidance)

            # Optionally, save the full updated guidance back to guidance.txt
            with open('./guidance.txt', 'w') as guidance_file:
                guidance_file.write(updated_guidance)

    #*********************#
    
    # # Display the initial guidance
    # st.write(response_guideance)
    
    # # Add a text input for the user to enter manual guidance
    # user_guidance = st.text_area("Add your manual guidance here:")
    
    # if user_guidance:
    #     # Combine the old file content with new guidance provided by the user
    #     updated_guidance = file_content + "\n" + user_guidance
        
    #     # Append the new guidance to guidance.txt
    #     with open('./guidance.txt', 'a') as guidance_file:
    #         guidance_file.write("\n" + user_guidance)
        
    #     # Show the updated guidance on the Streamlit page
    #     st.write(updated_guidance)
        
    #     # Optionally, save the full updated guidance back to guidance.txt
    #     with open('./guidance.txt', 'w') as guidance_file:
    #         guidance_file.write(updated_guidance)
    

def handoff_bot():
    with open('./bot_purpose.txt', 'r') as file:
        file_content = file.read()
    
    # Generate the initial response guidance
    response_handoff = handoff_generation(file_content)
    guidance_points = response_handoff.split("\n\n")  # Assuming each point is separated by double newlines

    # Display each guidance point in its own section
    for i, point in enumerate(guidance_points):
        # Extract the section title (first line) and content (remaining lines)
        lines = point.split("\n")
        section_title = lines[0]  # First line is the title
        section_content = "\n".join(lines[1:])  # Remaining lines are the content

        # Display the section title and content
        st.markdown(f"### {section_title}")
        st.write(section_content)

        # Add a text area for user input under each section
        user_guidance = st.text_area(f"Add your manual guidance for '{section_title}' here:", key=f"user_guidance_{i}")

        # If the user provides input, append it to the guidance
        if user_guidance:
            updated_guidance = point + "\n" + user_guidance  # Combine the original point with user input
            st.write("### Updated Guidance for This Section:")
            st.write(updated_guidance)

            # Append the new guidance to the guidance.txt file
            with open('./guidance.txt', 'a') as guidance_file:
                guidance_file.write("\n" + updated_guidance)

            # Optionally, save the full updated guidance back to guidance.txt
            with open('./guidance.txt', 'w') as guidance_file:
                guidance_file.write(updated_guidance)
    
    # # Display the initial guidance
    # st.write(response_handoff)
    
    # # Add a text input for the user to enter manual guidance
    # user_handoff = st.text_area("Add your handoff suggesstion here:")
    
    # if user_handoff:
    #     # Combine the old file content with new guidance provided by the user
    #     updated_guidance = file_content + "\n" + user_handoff
        
    #     # Append the new guidance to guidance.txt
    #     with open('./handoff.txt', 'a') as handoff_file:
    #         handoff_file.write("\n" + user_handoff)
        
    #     # Show the updated guidance on the Streamlit page
    #     st.write(handoff_file)
        
    #     # Optionally, save the full updated guidance back to guidance.txt
    #     with open('./guidance.txt', 'w') as handoff_file:
    #         handoff_file.write(updated_guidance)
    




def syncbot_section():
    st.header("SyncBot")
    # Sidebar for tabs
    st.sidebar.header("Dashboard")
    tab = st.sidebar.radio("Select a section:", ["Products", "SKUs", "File Uploads", "FAQs", "Web Pages", "Videos"])

    if tab == "Products":
        show_products()
    elif tab == "SKUs":
        show_skus()
    elif tab == "File Uploads":
        show_file_uploads()
    elif tab == "FAQs":
        show_faqs()
    elif tab == "Web Pages":
        show_web_pages()
    elif tab == "Videos":
        show_videos()
    st.write("Here you can manage your SyncBot configuration and functionalities.")
    # You can add the functionality of SyncBot here

# Function to display Training section
def training_section():
    st.header("Training")
    st.write("This section is for managing training data, processes, and models.")
    st.sidebar.header("Dashboard")
    tab = st.sidebar.radio("Select a section:", ["Guideance Bot", "Handoff Bot", "FAQ BOT"])

    if tab == "Guideance Bot":
        guideance_bot()
    # Add training functionality here

    if tab == "Handoff Bot" :
        handoff_bot()

    if tab == "FAQ BOT" :
        show_faqs()


# Function to display Live Chat section
def live_chat_section():
    st.header("Test the bot")
    chatting()
    # st.button("Deploy the bot")

    if st.button("Deploy the bot"):
        st.session_state.page = "Deploy the bot"
        st.rerun()
    
    
    
    # Add live chat functionality here

# Main function to display the page
def main_dashboard():
    # st.title("Sync_Bot")

    st.markdown("""
        <style>
            .stRadio > div {
                display: flex;
                justify-content: space-around;
                flex-wrap: nowrap;
            }
            .stRadio label {
                padding-right: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Top navigation as tabs
    tab = st.sidebar.radio(
        "Select a Section",
        ["SyncBot", "Training", "Test Bot"]
    )

    if tab == "SyncBot":
        syncbot_section()  # Show SyncBot section
    elif tab == "Training":
        training_section()  # Show Training section
    elif tab == "Test Bot":
        live_chat_section()  # Show Live Chat section
   

    
