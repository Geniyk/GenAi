from dotenv import load_dotenv
load_dotenv()  ## loading all the environment variables


import streamlit as st 
import os
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get responses
## Text--> gemini pro  model & Vision-->gemini pro vision model
model= genai.GenerativeModel("gemini-1.5-pro")
def get_gemini_response(question):
    response=model.generate_content(question)
    return response.text

## initialize our streamlit app

st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

input=st.text_input("Input: ", key="input")
submit=st.button("Ask the question")

##when submit is clicked

if submit:
    response=get_gemini_response(input)
    st.subheader("The Response is")
    st.write(response)


