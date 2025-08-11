import pandas as pd
import numpy as np
import pymongo


def history_retreval(con_id):
    con_id=con_id
    client = pymongo.MongoClient("mongodb://dev:N47309HxFWE2Ehc@34.121.45.29:27017/ptchatbotdb?authSource=admin")
    db = client["ptchatbotdb"]
    collection_info = db['messages']
    # print(collection_info)
    document_copy = collection_info.find({"conversationId": con_id})
    documents = list(document_copy)

    try:
        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(documents)
        L1=list(df['content'])
        messages = [entry['message'] for entry in L1]
    except :
        pass


    # print(L1)

    # Display or use the DataFrame as needed
    try :

        msg=messages
    except :
        msg=[]
    # print(messages)

    return msg


def feedback_query():#ques
    # con_id=con_id
    client = pymongo.MongoClient("mongodb://dev:N47309HxFWE2Ehc@34.121.45.29:27017/ptchatbotdb?authSource=admin")
    db = client["ptchatbotdb"]
    collection_info = db['messageanalytics']

    data = collection_info.find()

    data_list = list(data)
    # print(collection_info)
    # document_copy = collection_info.find({"userQuestion": ques})
     
    # documents = list(document_copy)

    return data_list
    # Ensure documents is not empty
    # if documents:

    #     user_response = documents[0].get('userReason', '').strip()  # Get 'userReason', default to empty string

    #     # Check if the user response is None or empty string
    #     if not user_response:  # This will catch both None and empty strings
    #         return "no_answer"
    #     else:
    #         return user_response
    # else:
    #     return "no_answer"


   
