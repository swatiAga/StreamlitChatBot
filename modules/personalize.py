import streamlit as st
from modules.scraper import scraper_page

def save_personalization(user, bot_config):
    """Saves bot personalization details to the same text file."""
    with open("bot_purpose.txt", "a") as file:
        file.write(f"User: {user}\nPersonalization Details:\n")
        for key, value in bot_config.items():
            file.write(f"{key}: {value}\n")
        file.write("\n")

def personalize_page():
    st.title("🎨 Personalize Your Bot")
    
    if "bot_config" not in st.session_state:
        st.session_state.bot_config = {}

    Name_Your_chatbot = st.text_input("Name Your chatbot", st.session_state.bot_config.get("bot_name", ""))
    tone = st.selectbox("Tone & Style", ["Professional", "Casual", "Inspirational", "Authoritative", "Friendly", "Energetic", "Persuasive", "Other"], key="tone_select_unique")
    if tone == "Other":
        tone = st.text_input("Specify Tone", "", key="tone_other_unique")
    
    languages = st.selectbox("Languages", ["Arabic", "English", "French", "Spanish", "German", "Chinese", "Russian", "Japanese", "Hindi", "Portuguese", "Italian", "Dutch", "Swedish", "Polish", "Korean", "Turkish", "Greek", "Hebrew", "Czech", "Thai"], key="language_select_unique")
    company_name = st.text_input("Company Name", "", key="company_name_input_unique")
    company_description = st.text_area("Company Description", "", key="company_desc_input_unique")
    customer_care_email = st.text_input("Customer Care Email Address", "", key="customer_email_input_unique")
    industry = st.selectbox("Industry", ["Ecommerce", "Healthcare", "Manufacturing", "Education", "Travel & Hospitality", "Others"], key="industry_select_unique")
    if industry == "Others":
        industry = st.text_input("Specify Industry", "", key="industry_other_unique")
    
    if st.button("Save Personalization", key="save_personalization_btn_unique"):
        st.session_state.bot_config.update({
            "Name Your chatbot": Name_Your_chatbot,
            "Tone & Style": tone,
            "Languages": languages,
            "Company Name": company_name,
            "Company Description": company_description,
            "Customer Care Email": customer_care_email,
            "Industry": industry
        })
        save_personalization(st.session_state.current_user, st.session_state.bot_config)
        st.session_state.page = "Scraper"
        st.success("✅ Personalization Saved! Redirecting...")
        st.rerun()




    if st.session_state.page == "Scraper":
        scraper_page()
