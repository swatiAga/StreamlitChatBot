import streamlit as st
import pandas as pd
import yaml
from modules.scraper import generate_tags_from_gpt
from modules.scraper import generate_related_faq
import json

def tags_page():
    st.title("🏷️ AI-Generated Tags & FAQs")
    tabs = st.tabs(["Tags", "FAQs"])
    
    with tabs[0]:
        st.markdown("Tags help categorize and organize content, improving chatbot response accuracy.")
        df = pd.read_excel('website_scrape.xlsx')
        json_data = df.to_dict(orient="records")
        with open("website_data.json", "w") as f:
            json.dump(json_data, f, indent=4)
        response = generate_tags_from_gpt(json_data)
        print("****************************")
        print(response)
        print("****************************")
        try:
            parsed_response = yaml.safe_load(response)
            if isinstance(parsed_response, list):
                response_dict = {}
                for item in parsed_response:
                    if isinstance(item, dict):
                        for key, value in item.items():
                            if key in response_dict:
                                response_dict[key].extend(value)
                            else:
                                response_dict[key] = value
            elif isinstance(parsed_response, dict):
                response_dict = parsed_response
            else:
                raise ValueError("Unexpected YAML structure!")
        except yaml.YAMLError as e:
            st.error(f"Error parsing YAML: {e}")
            response_dict = {"Products": [], "Industries": [], "Applications": [], "FAQs": {}}
    
        products_df = pd.DataFrame({"Products": response_dict.get("Products", [])})
        industries_df = pd.DataFrame({"Industries": response_dict.get("Industries", [])})
        applications_df = pd.DataFrame({"Applications": response_dict.get("Applications", [])})
    
        col1, col2, col3 = st.columns(3)
    
        with col1:
            st.subheader("📦 Products")
            st.table(products_df)
    
        with col2:
            st.subheader("🏭 Industries")
            st.table(industries_df)
    
        with col3:
            st.subheader("⚙️ Applications")
            st.table(applications_df)
    
    # with tabs[1]:
    #     st.markdown("### FAQs Section")
    #     st.write("Click on a question to reveal the answer.")

    #     # Inspect the response_dict structure
    #     st.write(response_dict)  # This helps to understand the structure and debug if necessary
        
    #     # Attempt to extract the FAQ section safely
    #     faq_dict = response_dict.get("FAQs", None)

    #     # Check if faq_dict is found and has content
    #     if response_dict:
    #         # Directly display the FAQ content as is (assuming it's a string or list of Q&A)
    #         with st.expander("FAQs"):
    #             st.write(faq_dict)
    #     else:
    #         st.write("No FAQs available or 'FAQs' key is missing.")

    #     # Section to add a new FAQ
    #     st.markdown("#### Add a New FAQ")
    #     new_faq = st.text_input("Question")
    #     new_answer = st.text_area("Answer")

    #     if st.button("Save FAQ"):
    #         if new_faq and new_answer:
    #             # Append the new FAQ to the faqs.txt file
    #             with open("faqs.txt", "a") as f:
    #                 f.write(f"Q1: {new_faq}\nA1: {new_answer}\n")
    #             st.success("FAQ Saved!")
    #         else:
    #             st.warning("Please fill out both the question and the answer.")

    # st.markdown("---")
    # if st.button("⬅️ Back to Scraper"):
    #     st.session_state.page = "Scraper"
    #     st.rerun()
    # if st.button("Proceed to Upload & Train Bot"):
    #     st.session_state.page = "Upload & Train Bot"
    #     st.rerun()
    with tabs[1]:
        st.markdown("### FAQs Section")
        st.write("Click on a question to reveal the answer.")

        # Assuming faq_dict is the list of dictionaries as described
        faq_dict = response_dict.get("FAQs", [])
        
        

        if faq_dict:
            with open("faqs.json", "w") as f:
                json.dump(faq_dict, f, indent=4)
            # Iterate over each item in faq_dict (list of dictionaries)
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
                                st.write(answer)  # S # Show the corresponding answer

        else:
            st.write("No FAQs available at the moment.")

        # Section to add a new FAQ
        st.markdown("#### Add a New FAQ")
        new_faq = st.text_input("Question")
        new_answer = st.text_area("Answer")
#***************************************************************
        if st.button("Save FAQ"):
            if new_faq and new_answer:
                with open("faqs.txt", "a") as f:
                    f.write(f"\n{new_faq}\n{new_answer}\n")
                st.success("FAQ Saved!")

                related_faqs=generate_related_faq(new_faq,new_answer)
                print("************************")
                print(related_faqs)
                print("************************")
                

            if related_faqs:
                st.subheader("Related FAQs:")

                # Store checkboxes in session state
                if "selected_faqs" not in st.session_state:
                    st.session_state.selected_faqs = {i: True for i in range(len(related_faqs))}

                for i, faq in enumerate(related_faqs):
                    for key, value in faq.items():  # Iterate over key-value pairs
                        if key.startswith("Q"):  # Identify question keys
                            question = value  
                            answer_key = key.replace("Q", "A")  # Find corresponding answer key
                            answer = faq.get(answer_key, "No answer available.")

                            # Create a checkbox for each FAQ
                            st.session_state.selected_faqs[i] = st.checkbox(question, value=st.session_state.selected_faqs[i], key=f"faq_{i}")

                            # Display the question and answer in an expandable section
                            if question and answer:
                                with st.expander(question):
                                    st.write(answer)

                # Save only selected FAQs
                if st.button("Save Selected FAQs"):
                    with open("faqs.txt", "a") as f:
                        for i, faq in enumerate(related_faqs):
                            if st.session_state.selected_faqs[i]:  # Only save checked FAQs
                                for key, value in faq.items():
                                    f.write(f"{key}: {value}\n")
                    st.success("Selected FAQs Saved!")

            else:
                st.warning("Please fill out both the question and the answer.")

    st.markdown("---")
    if st.button("⬅️ Back to Scraper"):
        st.session_state.page = "Scraper"
        st.rerun()
    if st.button("Continue"):
        st.session_state.page = "Knowledgebase"
        st.rerun()
