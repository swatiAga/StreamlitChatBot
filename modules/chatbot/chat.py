import os
import json
import logging
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import RetrievalQA, create_history_aware_retriever
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.messages import HumanMessage
from .mongo import history_retreval  # Assuming custom MongoDB retrieval method
from dotenv import load_dotenv
# Load from .env file into environment variables
load_dotenv()

def chatting():
    # Setup Logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='app.log',
                        filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    # Load environment variables (your OpenAI API key here)
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")  # Replace with your actual API key
    logging.info('Environment variables loaded.')

    # Load the FAISS index
    embeddings = OpenAIEmbeddings()
    faiss_index_path = './faiss_index_vectors' #"faiss_index_vectors_manuals"  # Path to your FAISS index
    faiss_index = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
    logging.info('FAISS index loaded.')

    # Load JSON data
    file_path = './modules/chatbot/output.json'
    file_path_1 = './modules/chatbot/All_model_no_structure (1).json'
    faq='faqs.json'
    website_data='website_data.json'

    # file_path_2 = 'utube.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    with open(file_path_1, 'r') as file:
        data1 = json.load(file)

    with open(faq, 'r') as file:
        faq_file= json.load(file)
    
    with open(website_data, 'r') as file:
        website_file= json.load(file)

    # with open(file_path_2, 'r') as file:
    #     data2 = json.load(file)

    # Prepare the combined JSON for retrieval context
    json_str = json.dumps(faq_file)
    json_str_1 = json.dumps(website_file)
    # json_str_2 = json.dumps(data2)

    combined_json = {
        "first_json": json_str,
        "second_json": json_str_1,
        # "third_json": json_str_2
    }

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Load prompt from hub
    prompt = hub.pull("rlm/rag-prompt")
    retriever = faiss_index.as_retriever()

    # Create retrieval chain with history awareness
    contextualize_q_system_prompt = """Given a chat history and the latest user question, \
    which might reference context in the chat history, reformulate it as a standalone question. \
    Do NOT answer the question, just reformulate it if needed."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # with open("bot_purpose.txt", "r", encoding="utf-8") as file:
    #     purpose_txt_content = file.read()
    with open("bot_purpose.txt", "r", encoding="utf-8", errors="ignore") as file:
        purpose_txt_content = file.read()
    
    context = """
  "You are an AI-powered chatbot designed to assist users based on the given purpose and personalization details. 
  Below is the chatbot's purpose and its customization parameters:\n\n  ## Chatbot Purpose\n  {purpose_txt_content}\n\n  ## 
  Personalization Details\n  - **Chatbot Name**: ,**Tone & Style**: **Languages**:,**Company Name**
    **Company Description**:,\n  - **Customer Care Email**:\n  - **Industry**:\n  
    Based on this information, your task is to engage with users in a professional and helpful manner, ensuring recommendations align with the specified purpose.
    \n\n  Ensure your responses are relevant, insightful, and aligned with the industry context, while maintaining a tone. Always prioritize user needs 
    and offer the best recommendations based on the provided details.\n\n  ---\n\n  **Input Structures:**\n\n 
      **1. Purpose Input (purpose.txt):**\n  The chatbot's purpose will be loaded from a plain text file named `purpose.txt`.\n\n  
      

take the input from following json  {combined_json} to answer the queries more precisely
{context}
"""

    # Create a retrieval QA chain
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", context),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    def get_bot_name():
        try:
            with open("bot_purpose.txt", "r") as file:
                # Assuming the bot's name is on the first line of the file
                for line in file:
                    # Check if the line contains the variable "Name Your chatbot"
                    if "Name Your chatbot:" in line:
                        # Extract the bot's name from the line
                        bot_name = line.split("Name Your chatbot:")[1].strip()
                        return bot_name
        except FileNotFoundError:
            return "Simple Chatbot with Retrieval System"  # Default title if file is not found

    # Set the title dynamically from purpose.txt
    bot_name = get_bot_name()
    st.title(f"{bot_name}")
    # Streamlit App
    # st.title("Simple Chatbot with Retrieval System")

    # Chat history storage (to be replaced with session storage or a DB)
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        st.write(message["role"] + ": " + message["content"])

    # User input for question
    user_question = st.text_input("Ask a question:")

    # If a question is entered, process it
    if user_question:
        con_id = "some_session_id"  # Replace with actual session identifier

        # Retrieve chat history
        chat_history = history_retreval(con_id)  # Replace with a real method for retrieving history
        joined_history = ' '.join(chat_history)
        
        # Invoke the model chain with the user input
        result = rag_chain.invoke({
            "input": user_question,
            "chat_history": joined_history.split(' '),  # Split history for model input
            "combined_json": json_str,
            "purpose_txt_content" : purpose_txt_content
        })
        
        # Save the user question and response in chat history
        st.session_state.messages.append({"role": "user", "content": user_question})
        st.session_state.messages.append({"role": "bot", "content": result["answer"]})

        # Display the response from the chatbot
        st.write(result["answer"])

    else:
        st.write("Please ask a question to get started.")
