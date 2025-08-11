import streamlit as st
from modules.personalize import personalize_page

def save_bot_purpose(user, selected_purpose):
    """Saves the bot purpose selection to a text file."""
    with open("bot_purpose.txt", "a") as file:
        file.write(f"User: {user}\nPurpose of the bot: {selected_purpose}\n\n")

def bot_purpose():
    st.title("Onboarding Bot")
    st.markdown("""
        <style>
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                width: 100%;
                padding: 10px;
                border-radius: 5px;
            }
            .stSelectbox label {
                font-size: 16px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("### First Time Onboarding")
        st.markdown("## Purpose of the chatbot")
        st.write("Select what you want this chatbot to do.")
        
        # Dropdown for selecting the purpose
        purpose_options = [
            "Product Search & Recommendation (General Sales)",
            "Troubleshooting (Technical Support)",
            "Information Retrieval",
            "Personal Assistance",
            "E-commerce and Order Management",
            "Education and Training",
            "Healthcare Assistance",
            "Entertainment and Engagement",
            "Feedback and Surveys",
            "Internal Business Operations",
            "Social Media Engagement",
            "Language Translation and Learning",
            "Financial Assistance",
            "Crisis Support"
        ]
        selected_purpose = st.selectbox("Select a purpose", purpose_options)
        
        # Display purpose and examples based on selection
        if selected_purpose == "Product Search & Recommendation (General Sales)":
            st.markdown("**Purpose**: Assist users in finding and recommending products.")
            st.markdown("**Examples**:")
            st.write("- Helping users find products based on preferences.")
            st.write("- Recommending complementary products.")
            st.write("- Providing product details and reviews.")
        
        elif selected_purpose == "Troubleshooting (Technical Support)":
            st.markdown("**Purpose**: Provide technical support and resolve user issues.")
            st.markdown("**Examples**:")
            st.write("- Guiding users through troubleshooting steps.")
            st.write("- Answering FAQs about technical problems.")
            st.write("- Escalating issues to human agents if needed.")
        
        elif selected_purpose == "Information Retrieval":
            st.markdown("**Purpose**: Provide quick access to information from a knowledge base or database.")
            st.markdown("**Examples**:")
            st.write("- Answering questions about company policies, procedures, or services.")
            st.write("- Retrieving real-time data like weather updates, stock prices, or news.")
            st.write("- Providing details about events, schedules, or locations.")
        
        elif selected_purpose == "Personal Assistance":
            st.markdown("**Purpose**: Help users manage tasks, schedules, and daily activities.")
            st.markdown("**Examples**:")
            st.write("- Setting reminders, alarms, or calendar events.")
            st.write("- Booking appointments, reservations, or tickets.")
            st.write("- Providing personalized recommendations (e.g., movies, restaurants, travel).")
        
        elif selected_purpose == "E-commerce and Order Management":
            st.markdown("**Purpose**: Assist users in browsing, purchasing, and managing orders.")
            st.markdown("**Examples**:")
            st.write("- Helping users find products based on preferences.")
            st.write("- Processing orders and payments.")
            st.write("- Providing order status updates and tracking information.")
        
        elif selected_purpose == "Education and Training":
            st.markdown("**Purpose**: Deliver educational content, quizzes, and training materials.")
            st.markdown("**Examples**:")
            st.write("- Providing interactive lessons or tutorials.")
            st.write("- Answering student questions about course material.")
            st.write("- Conducting assessments and providing feedback.")
        
        elif selected_purpose == "Healthcare Assistance":
            st.markdown("**Purpose**: Provide medical information, schedule appointments, and offer basic health advice.")
            st.markdown("**Examples**:")
            st.write("- Answering questions about symptoms and treatments.")
            st.write("- Booking doctor appointments or lab tests.")
            st.write("- Sending medication reminders and health tips.")
        
        elif selected_purpose == "Entertainment and Engagement":
            st.markdown("**Purpose**: Engage users with fun and interactive content.")
            st.markdown("**Examples**:")
            st.write("- Playing games or quizzes.")
            st.write("- Telling jokes, stories, or trivia.")
            st.write("- Recommending movies, books, or music.")
        
        elif selected_purpose == "Feedback and Surveys":
            st.markdown("**Purpose**: Collect user feedback and conduct surveys.")
            st.markdown("**Examples**:")
            st.write("- Asking customers for reviews or ratings.")
            st.write("- Conducting market research or customer satisfaction surveys.")
            st.write("- Gathering insights to improve products or services.")
        
        elif selected_purpose == "Internal Business Operations":
            st.markdown("**Purpose**: Streamline internal processes and improve employee productivity.")
            st.markdown("**Examples**:")
            st.write("- Assisting employees with HR-related queries (e.g., leave policies, payroll).")
            st.write("- Providing IT support for technical issues.")
            st.write("- Automating repetitive tasks like data entry or report generation.")
        
        elif selected_purpose == "Social Media Engagement":
            st.markdown("**Purpose**: Interact with users on social media platforms to enhance engagement.")
            st.markdown("**Examples**:")
            st.write("- Responding to comments and messages on social media.")
            st.write("- Running promotional campaigns or contests.")
            st.write("- Providing updates about new posts or events.")
        
        elif selected_purpose == "Language Translation and Learning":
            st.markdown("**Purpose**: Assist users with language translation or learning.")
            st.markdown("**Examples**:")
            st.write("- Translating text or conversations in real-time.")
            st.write("- Teaching new languages through interactive lessons.")
            st.write("- Providing grammar or vocabulary assistance.")
        
        elif selected_purpose == "Financial Assistance":
            st.markdown("**Purpose**: Help users manage finances and make informed decisions.")
            st.markdown("**Examples**:")
            st.write("- Providing account balance and transaction details.")
            st.write("- Offering budgeting tips and financial advice.")
            st.write("- Assisting with loan applications or investment options.")
        
        elif selected_purpose == "Crisis Support":
            st.markdown("**Purpose**: Provide immediate assistance during emergencies or crises.")
            st.markdown("**Examples**:")
            st.write("- Offering mental health support and resources.")
            st.write("- Providing emergency contact information.")
            st.write("- Guiding users through crisis management steps.")
        
        if st.button("Continue"):
            if "current_user" in st.session_state:
                save_bot_purpose(st.session_state.current_user, selected_purpose)
            st.session_state.page = "Personalize Your Bot"  # Redirect to Personalize Your Bot
            st.rerun()
    
    with col2:
        # st.image("/Users/shaal/605- DS Practicum 1/Algo8/Code shared by Akshay/StreamlitChatbot/modules/download (4).jpeg", use_column_width=True)
        st.image("./modules/download (4).jpeg", use_column_width=True)

if "authenticated" in st.session_state and st.session_state.authenticated:
    personalize_page()