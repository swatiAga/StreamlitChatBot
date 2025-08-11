from modules.auth import login_signup
from modules.bot_purpose import bot_purpose
from modules.personalize import personalize_page
import debugpy
# Check if debugpy is already listening
if not debugpy.is_client_connected():
    # Allow VS Code to attach to the Streamlit process
    debugpy.listen(("localhost", 5678))
    print("Waiting for debugger to attach...")
    # Pause execution until the debugger is attached
    debugpy.wait_for_client()
import streamlit as st
from modules.scraper import scraper_page
from modules.tags import tags_page
from modules.Knowledgebase import onboarding_page
from modules.Training import main_dashboard
from modules.chatbot.vector import vector
from modules.chatbot.chat import chatting
# from modules.training import training_page
# from modules.chat import chat_page

# Streamlit UI
if "page_config_set" not in st.session_state:
    st.set_page_config(page_title="Website Scraper & AI-Generated Tags", layout="wide")
    st.session_state.page_config_set = True

# Page Navigation
pages = {
    "Login/Signup": login_signup,
    "Bot Purpose": bot_purpose,
    "Personalize Your Bot" : personalize_page,
    "Scraper": scraper_page,
    "Generated Tags": tags_page,
    "Knowledgebase": onboarding_page,
    "Training" : main_dashboard,
    "Deploy the bot" : chatting
    # "Upload & Train Bot": training_page,
    # "Chat with Bot": chat_page,
}


# Session State Variables
if "page" not in st.session_state:
    st.session_state.page = "Login/Signup"

# Sidebar Navigation
selected_page = st.sidebar.radio("📌 Navigation", list(pages.keys()), index=list(pages.keys()).index(st.session_state.page))

# Render the selected page
if selected_page == "Login/Signup":
    login_signup()
    if "authenticated" in st.session_state and st.session_state.authenticated:
        st.session_state.page = "Bot Purpose"
        st.rerun()
elif selected_page == "Bot Purpose":
    bot_purpose()

elif selected_page == "Personalize Your Bot":
    personalize_page()

elif selected_page == "Scraper":
    scraper_page()

elif selected_page == "Generated Tags":
    
    tags_page()
    # vector()

elif selected_page == "Knowledgebase" :
    onboarding_page()

elif selected_page == "Training" :
    main_dashboard()

elif selected_page == "Deploy the bot":
    chatting()


