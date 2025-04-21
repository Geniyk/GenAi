import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS  # Vector store DB
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # Vector embedding techniques
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Load API keys
groq_api_key = os.getenv("GROQ_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = google_api_key

st.title("Gemma Model Document Q&A")

# Check if GROQ API key is available
if not groq_api_key:
    st.error("GROQ API Key is missing. Please check your .env file.")
    st.stop()

# Initialize the LLM model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

# Define the prompt template
prompt = ChatPromptTemplate.from_template(
    """ 
    Answer the question based on the provided context only.
    Please provide the most accurate response based on the question.
    <context>
    {context}
    <context>
    Question: {input}
    """
)

def vector_embedding():
    """Function to create and store vector embeddings in session state."""
    if "vectors" not in st.session_state or st.session_state.vectors is None:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        st.session_state.loader = PyPDFDirectoryLoader("./PDFS")  # Data Ingestion
        st.session_state.docs = st.session_state.loader.load()  # Document Loading
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

        st.success("Vector Store DB is Ready")

# Input box for user query
prompt1 = st.text_input("What do you want to ask from the documents?")

# Button to create the vector store
if st.button("Create Vector Store"):
    vector_embedding()

# Ensure vector store exists before querying
if prompt1:
    if "vectors" not in st.session_state or st.session_state.vectors is None:
        st.error("Please create the Vector Store first by clicking the button.")
        st.stop()

    # Create the retrieval chain
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Query the model and measure execution time
   
    start = time.time()  # Start time measurement
    try:
        response = retrieval_chain.invoke({'input': prompt1})
        end = time.time()  # End time measurement
        elapsed_time = end - start  # Calculate elapsed time
        st.write(f"**Response Time:** {elapsed_time:.2f} seconds")  # Display response time
        st.write(f"**Answer:** {response['answer']}")
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        st.stop()
   
    

    # Display relevant document chunks
    with st.expander("Document Similarity Search"):
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")
