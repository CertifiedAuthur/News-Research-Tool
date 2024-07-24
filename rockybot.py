import os
import streamlit as st
import time
import requests
import faiss
import numpy as np
from bs4 import BeautifulSoup
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()  # Load environment variables from .env (especially OpenAI API key)

# Initialize OpenAI embeddings and language model
def initialize_openai(api_key: str):
    embeddings = OpenAIEmbeddings(api_key=api_key)
    llm = OpenAI(api_key=api_key)
    return embeddings, llm

def fetch_content_from_urls(urls):
    """Fetch and scrape content from the given URLs."""
    documents = []
    for url in urls:
        if url:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.get_text()
            
            # Create a document with content and metadata
            doc = Document(
                page_content=content,
                metadata={"source": url}
            )
            documents.append(doc)
    return documents

def create_vector_db(urls: list, api_key: str) -> FAISS:
    """Create a vector database from the content fetched from URLs."""
    documents = fetch_content_from_urls(urls)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    
    embeddings, _ = initialize_openai(api_key)
    db = FAISS.from_documents(docs, embeddings)
    return db

def get_response_from_query(db: FAISS, query: str, api_key: str, k: int = 4) -> dict:
    """Generate a response to the query based on the vector database."""
    try:
        docs = db.similarity_search(query, k=k)
        docs_page_content = " ".join([d.page_content for d in docs])
        
        _, llm = initialize_openai(api_key)
        chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=db.as_retriever())
        result = chain({"question": query}, return_only_outputs=True)
        
        response = result.get("answer", "No answer found.")
        sources = result.get("sources", [])
        
        # Ensure the response ends with a full stop.
        if not response.endswith('.'):
            response += '.'

        return {"response": response, "sources": sources}
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return {"response": "An error occurred while generating the response.", "sources": []}

# --- Streamlit App ---
st.title("RockyBot: News Research Tool 📈")

with st.sidebar:
    st.markdown("### News Article URLs")
    urls = [st.text_input(f"URL {i+1}", key=f"url_{i}") for i in range(3)]
    st.markdown("###")
    api_key = st.text_area(label="Input your OpenAI API Key", max_chars=56)
    st.markdown("###")
    process_url_clicked = st.button("Process URLs")

if process_url_clicked and api_key:
    with st.spinner("Processing URLs..."):
        db = create_vector_db(urls, api_key)
        st.session_state.db = db  # Save the database in the session state
        st.session_state.processed = True

if 'processed' in st.session_state and st.session_state.processed:
    st.markdown("###")
    st.header("Ask a Question")
    query = st.text_input("What would you like to know about the content from the URLs?")
    submit_question_clicked = st.button("Submit Question")
    
    if submit_question_clicked and query:
        with st.spinner("Generating response..."):
            result = get_response_from_query(st.session_state.db, query, api_key)
            st.header("Answer")
            st.write(result["response"])
            
            # Display sources, if available
            sources = result.get("sources", [])
            if sources:
                st.subheader("Sources:")
                sources_combined = " ".join(sources)
                sources_combined = sources_combined.replace(" ", "")  # Remove spaces between characters
                st.write(sources_combined)
