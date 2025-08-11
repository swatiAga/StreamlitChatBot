import streamlit as st
from modules.website_crawler import crawl_website
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import pandas as pd
from flask import jsonify
import json
import openai
from .chatbot.vector import vector


def generate_tags_from_gpt(json_data):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    prompt = f"""
Given the website data in JSON format, extract and categorize the relevant information into the following structured tags, donot include (```json) in your response:

1️⃣ Products: Identify and list all products mentioned on the website.  
2️⃣ Industries: Extract and list all industries relevant to the website content.  
3️⃣ Applications: Identify and list all applications mentioned.  
4️⃣ FAQs: Extract all FAQ questions and their corresponding answers. If any FAQs are missing but are logically important based on the data, generate relevant FAQs.

### Output Format:
- Products:
  - List of products (one per line)
  
- Industries:
  - List of industries (one per line)

- Applications:
  - List of applications (one per line)

- FAQs:
  - Ensure that **every FAQ contains both a question and a corresponding answer**.  
  - If an answer is missing in the data, **predict a reasonable answer** based on the context.

---

### example Output Format:
Products:

Product 1
Product 2
Product 3
Industries:

Industry 1
Industry 2
Industry 3
Applications:

Application 1
Application 2
FAQs: [
    
    -Q1: What is the product used for? 
    A1: This product is used to enhance workflow automation.
    
    

    
    -Q2: How does the application work?
      A2: The application integrates with existing tools to streamline operations and improve productivity.
      

    
    -Q3: What industries benefit from this product? 
    A3: This product is ideal for manufacturing, healthcare, and logistics industries.
    
    ]

yaml
Copy
Edit
---

### Important Instructions:
- The FAQs section must always contain complete questions and answers (never leave them null or empty).
- The output must be structured and formatted clearly as shown in the example above.
- Extract only the most relevant information from the provided JSON.

---

JSON Data: {json.dumps(json_data[:10], indent=2)}
"""




    response = llm.predict(prompt)
    return response
# def scraper_page():
#     st.title("🌐 Website Scraper & GPT Tag Generator")
#     # [Original Scraper page implementation]
#     # ... [Copy full implementation from original code]
#     website_url = st.text_input("🔗 Enter Website URL")

#     if st.button("Scrape Website"):
#         if website_url:
#             with st.spinner("Scraping website..."):
#                 df = crawl_website(website_url)
#             st.success("✅ Website scraping completed!")

#             json_data = df.to_dict(orient="records")
#             with open("website_data.json", "w") as f:
#                 json.dump(json_data, f, indent=4)

#             st.write("### Extracted Data Preview:")
#             st.dataframe(df.head())

#             with open("website_scrape.xlsx", "rb") as f:
#                 st.download_button("📥 Download Extracted Data", f, "website_scrape.xlsx")

#     if st.button("Generate Tags"):
#         with st.spinner("Generating tags "):
#             df=pd.read_excel('website_scrape.xlsx')
#             json_data = df.to_dict(orient="records")
#             with open("website_data.json", "w") as f:
#                 json.dump(json_data, f, indent=4)
#             st.session_state.tags = generate_tags_from_gpt(json_data)
#         st.session_state.page = "Generated Tags"
#         st.rerun()


def scraper_page():
    st.title("🌐 Website Scraper & GPT Tag Generator")
    website_url = st.text_input("🔗 Enter Website URL")

    if st.button("Scrape Website"):
        if website_url:
            with st.spinner("Scraping website..."):
                # Initialize an empty list to store all scraped data
                all_data = []

                # Create a placeholder for the table
                table_placeholder = st.empty()

                # Iterate through the generator function
                for link_data in crawl_website(website_url):
                    # Append the data to the list
                    all_data.append(link_data)

                    # Convert the list of dictionaries to a DataFrame
                    df = pd.DataFrame(all_data)

                    # Display the updated table in the placeholder
                    table_placeholder.write("### Scraped Links:")
                    table_placeholder.dataframe(df[["URL", "Title", "Meta Description"]])  # Show only key columns

            st.success("✅ Website scraping completed!")

            # Save the data to a JSON file
            json_data = df.to_dict(orient="records")
            with open("website_data.json", "w") as f:
                json.dump(json_data, f, indent=4)

            # st.write("### Full Extracted Data Preview:")
            # st.dataframe(df)  # Show the full DataFrame with all columns

            # Save the data to an Excel file and provide a download button
            df.to_excel("website_scrape.xlsx", index=False)
            with open("website_scrape.xlsx", "rb") as f:
                st.download_button("📥 Download Extracted Data", f, "website_scrape.xlsx")
        
            
    if st.button("Generate Tags"):
          
          with st.spinner("Generating tags and creating vector Database "):
            vector()
            st.write("Vector Db created")
            df=pd.read_excel('website_scrape.xlsx')
            json_data = df.to_dict(orient="records")
            with open("website_data.json", "w") as f:
                json.dump(json_data, f, indent=4)
            st.session_state.tags = generate_tags_from_gpt(json_data)
          st.session_state.page = "Generated Tags"
          st.rerun()

"""Key Changes:
Display Data Incrementally:

The crawl_website function yields each link's data as a DataFrame.

Inside the loop, st.write and st.datafr"""

def sku(json_data):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    prompt = f""" 
Given the website data in JSON format from the shared website content, extract all the SKU that it serves. 
For each SKU, write a concise description based from the available content also mention from which product it is  Use relevant tags (e.g., where it is used, key features, or categories) to describe the SKU.

The response should be structured in JSON format as follows:

{{
  "SKUS": {{ "Sku_Name" : "SKU name"
    "Sku_description": "A brief description of the product based on the available content.",
    "tags": ["tag1", "tag2", "tag3"]  
    "Product": Product_name 
  }}
}}



Note : donot include '`', "```json in your json response

Ensure the description is clear and the tags are relevant to the product's usage, features, or categories. If no specific details are available, infer logically from the context.
    JSON Data: {json.dumps(json_data[:5], indent=2)}"""



    response = llm.predict(prompt)
    response=json.loads(response)
    return response


def product(json_data):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    prompt = f""" 
Given the website data in JSON format from the shared website content, extract all the products that it serves. 
For each product, write a concise description based on the available content. Use relevant tags (e.g., where it is used, key features, or categories) to describe the product.

The response should be structured in JSON format as follows:

{{
  "Products": {{ "Product_Name" : "product name"
    "product_description": "A brief description of the product based on the available content.",
    "tags": ["tag1", "tag2", "tag3"]  
  }}
}}

for example :
{{
  'Products': [
    {{
      'Product Name': 'Electric Immersion Heaters',
      'product_description': 'Designed to heat a variety of non-flammable aqueous process chemistries.',
      'tags': ['heating', 'industrial', 'UL listed']
    }},
    {{
      'Product Name': 'Inline Heaters',
      'product_description': 'Efficient heating solutions for consistent temperature control.',
      'tags': ['inline heating', 'energy efficiency']
    }}
  ]
}}

Note : donot include '`', "```json in your json response

Ensure the description is clear and the tags are relevant to the product's usage, features, or categories. If no specific details are available, infer logically from the context.
    JSON Data: {json.dumps(json_data[:5], indent=2)}"""



    response = llm.predict(prompt)
    response=json.loads(response)
    return response

def video(video_content):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    prompt = f""" Given a YouTube channel link take it from the {video_content}, extract the following information for each video available on the channel:

Video Title: Retrieve the title of each video.
Video Link: Extract the direct URL to each video.
Video Description: Provide a concise description of each video, limited to no more than 50 words.
Format the extracted information into a structured JSON do not include any paragraph in starting or ending of the json:
{{
  "videos": [
    {{
      "title": "Title of the Video",
      "link": "Direct URL to the Video",
      "description": "Concise description of the video, limited to 50 words."
    }},
    {{
      "title": "Title of Another Video",
      "link": "Direct URL to Another Video",
      "description": "Concise description of another video, limited to 50 words."
    }}
    // More videos can be added in similar format
  ]
}}
Ensure that the descriptions succinctly capture the essence of each video while adhering strictly to the word limit of 50 words.
Double-check that all links are directly accessible and lead to the specific videos mentioned.
If possible, also include information on the publication date and number of views, but prioritize title, link, and description.
Return the formatted JSON object containing all the necessary details about the videos from the provided YouTube channel link."""




    response = llm.predict(prompt)
    print(response)
    # response=json.loads(response)
    return response
      

def file(json_data_file):
    


    # print(json_data_file)
    # Initialize Langchain's ChatOpenAI model
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Define the prompt template
    template = """
   I have a JSON file containing metadata about multiple documents. The JSON structure is as follows:

    {json_data_file}

Please process this JSON and return the following information in JSON format:

1. **File name**: The exact name of the file.
2. **File description**: Provide a concise summary of the document, limited to no more than 30 words. The summary should capture the core topic or purpose of the document.
3. **Tags**: Identify the products mentioned in the document and list them as tags.
4. **Keywords**: Extract key applications and features mentioned throughout the document. List these as keywords.

The output should be in the following JSON format donot include any test in starting or ending of the json:

{{
    "files": [
        {{
            "file_name": "document1.pdf",
            "file_description": "A concise summary of the content of the document in no more than 30 words.",
            "tags": ["product1", "product2"],
            "keywords": ["application1", "feature1", "feature2"]
        }},
        {{
            "file_name": "report.docx",
            "file_description": "Summary of the document content in under 30 words.",
            "tags": ["product3", "product4"],
            "keywords": ["application3", "feature3", "feature4"]
        }}
    ]
}}

 
    """

    # Create a PromptTemplate with the placeholder for JSON data
    prompt = PromptTemplate(input_variables=["json_data_file"], template=template)

    # Create a chain using the LLM and the prompt template
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # print(json_data_file)

    # Get the result by passing the JSON data to the chain
    result = llm_chain.run({"json_data_file": json_data_file})

    # # Print the result
    # print("888888888888888888")
    # print(result)

    response=json.loads(result)
    return response

def Faq_generation(json_data):
    

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Define the prompt template
    template = """
   I have a JSON file containing metadata about multiple documents and scraped website content. The JSON structure is as follows respectively :

     {json_data}

    Using this JSON information, create a maximum of 20 FAQs. The FAQs should be complex and relevant to the information provided. 
    Do not include basic or generic questions. The questions should be specific and detailed based on the given data.
    Structure the output in JSON format as follows and  donot include any text or special character in starting or ending of the json::
    {{
        "faqs": [
            {{
                "Q1": "What is Streamlit?",
                "A1": "Streamlit is an open-source app framework for Machine Learning and Data Science projects."
            }},
            {{
                "Q2": "How do I install Streamlit?",
                "A2": "You can install Streamlit using pip: pip install streamlit."
            }}
        ]
    }}


    """

    # Create a PromptTemplate with the placeholder for JSON data
    prompt = PromptTemplate(input_variables=["json_data_file","json_data"], template=template)

    # Create a chain using the LLM and the prompt template
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # print(json_data_file)

    # Get the result by passing the JSON data to the chain
    result = llm_chain.run({"json_data": json_data })

    # Print the result
    print("888888888888888888")
    # print(result)

    response=json.loads(result)
    return response


def guidenace_generation(file_content):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    prompt = f""" 
 use the {file_content} to get the bot name and the company name
    
    You are tasked with creating a set of guidelines for the chatbot of [Bot Name]. The chatbot will assist users with company-related queries. Please ensure the following:

Guidance Points for [CompanyName] Chatbot:
Relevance to [CompanyName]:
The chatbot should only answer questions related to [CompanyName]'s products, services, policies, and any other company-specific information.
It should never respond to questions that fall outside the scope of [CompanyName] or that are not mentioned in the provided company documentation (Word doc).
Focus on Company-Specific Information:
The chatbot must stay focused on the topics that are directly linked to [CompanyName], ensuring conversations are strictly company-centered.
It should avoid responding to inquiries unrelated to the company, such as general knowledge, competitors, or other irrelevant subjects.

Response should be in pointers"""



    response = llm.predict(prompt)
    # response=json.loads(response)
    return response
      

def handoff_generation(file_content):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    prompt = f""" 
 use the {file_content} to explore the youtube channel link provided also explore the website link provided 
    
    Generate a set of clear and concise guidelines for a chatbot to determine when it should hand off a conversation to a customer care representative. The guidelines should include:

Complex Issues Beyond the Chatbot’s Scope:

When should the chatbot hand off the conversation for personalized support or troubleshooting (e.g., account-specific issues, technical support, billing inquiries)?
Queries Related to Specific Products or Services:

When should the chatbot transfer the conversation to customer care for expert advice or product-related support?
Requests for Escalation:

How should the chatbot respond when the user explicitly asks to speak with a customer care representative (e.g., “I need human assistance” or “Can someone help me with this issue?”)?
Content Not Available on YouTube Channel or Website:

What should the chatbot do if the user's query pertains to information that is not available on the provided YouTube channel or website, suggesting they contact customer care for more detailed help?
Inquiries About the YouTube Channel or Website Content:

How should the chatbot handle inquiries that require more in-depth support or clarification, directing users to customer care when necessary?"""



    response = llm.predict(prompt)
    # response=json.loads(response)
    return response
      
      
# def generate_related_faq():
def generate_related_faq(question, answer):
      
      """
      Use an LLM to generate 5 related FAQs based on the given question and answer.
      Returns a list of dictionaries with "Qx" as questions and "Ax" as answers.
      """
      llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
      prompt = f"""
      The following is a FAQ and its answer:
      
      Q: {question}
      A: {answer}
      
      Generate 5 more related FAQs in JSON format as a list of dictionaries where:
      - Questions are labeled as "Q1", "Q2", ..., "Q5".
      - Answers are labeled as "A1", "A2", ..., "A5".
      
       Structure the output in JSON format as follows and  donot include any text or special character in starting or ending of the json::
    
       ["faqs": 
            {{
                "Q1": "What is Streamlit?",
                "A1": "Streamlit is an open-source app framework for Machine Learning and Data Science projects."
            }},
            {{
                "Q2": "How do I install Streamlit?",
                "A2": "You can install Streamlit using pip: pip install streamlit."
            }}
        ]
    
      """

      result = llm.predict(prompt)
      # print(response)
      response=json.loads(result)


      return response

    
