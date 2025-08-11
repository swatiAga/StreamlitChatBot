import json
import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from pathlib import Path
from langchain.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredFileLoader
)
import streamlit as st
from dotenv import load_dotenv
# Load from .env file into environment variables
load_dotenv()

def vector():


    # Load JSON file
    json_file_path = "./website_data.json"

    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Extract relevant text fields
    documents = []
    for item in data:
        text_parts = []
        if "Title" in item and item["Title"]:
            text_parts.append(item["Title"])
        if "Meta Description" in item and item["Meta Description"] != "No description":
            text_parts.append(item["Meta Description"])
        if "Headings" in item:
            for key, values in item["Headings"].items():
                text_parts.extend(values)
        if "Paragraphs" in item:
            text_parts.extend(item["Paragraphs"])
        
        # Combine extracted text into a single document
        combined_text = " ".join(text_parts).strip()
        if combined_text:
            documents.append(combined_text)

    # Ensure documents are not empty
    if not documents:
        raise ValueError("No relevant text extracted from JSON. Check the JSON structure.")

    # OpenAI API Key
    
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
    # Text splitting
    text_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )

    for doc in documents:
        text_chunks.extend(text_splitter.split_text(doc))

    # Ensure text_chunks are not empty
    if not text_chunks:
        raise ValueError("No text chunks were created. Check if the extracted text is valid.")

    # Generate embeddings
    embeddings = OpenAIEmbeddings()

    # Test the embedding model
    try:
        test_embedding = embeddings.embed_query("test")
    except Exception as e:
        raise RuntimeError(f"Embedding model error: {e}")

    # Convert to FAISS vector database
    faiss_index_vectors = FAISS.from_texts(text_chunks, embeddings)

    # Save FAISS index locally
    faiss_index_vectors.save_local("faiss_index_vectors")

    print("FAISS vector store saved successfully!")


def load_and_chunk(file_path: str, category: str):
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext in [".doc", ".docx"]:
        loader = UnstructuredWordDocumentLoader(file_path)
    elif ext in [".png", ".jpg", ".jpeg", ".bmp"]:
        loader = UnstructuredFileLoader(file_path)  # OCR on images
    else:
        loader = UnstructuredFileLoader(file_path)

    docs = loader.load()
    
    # OpenAI API Key

    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", "!", "?", ",", " "]
    )

    chunks = splitter.split_documents(docs)
    for chunk in chunks:
        chunk.metadata["category"] = category
        chunk.metadata["source_file"] = Path(file_path).name
    return chunks


def process_and_vectorize_files(
        saved_file_paths_by_category: dict,
        vectorstore_path: str = "faiss_index_vectors"):
    """
    Processes saved files by category, chunks them, and stores
    embeddings in FAISS using OpenAI.
    
    Parameters:
        saved_file_paths_by_category (dict): {category:
        [file1_path, file2_path, ...]}
        vectorstore_path (str): folder to save FAISS index
    """
    all_chunks = []

    for category, file_paths in saved_file_paths_by_category.items():
        for file_path in file_paths:
            try:
                chunks = load_and_chunk(file_path, category)
                all_chunks.extend(chunks)
            except Exception as e:
                st.error(f"Failed to process {file_path}: {e}")

    if not all_chunks:
        st.warning("No documents to vectorize.")
        return
    
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    db = FAISS.from_documents(all_chunks, embeddings)
    db.save_local(vectorstore_path)
    st.success(f"FAISS vectorstore saved to '{vectorstore_path}'")