import os
# # from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


# from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

embed_tool = OpenAIEmbeddings()
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)