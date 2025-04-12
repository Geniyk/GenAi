from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to handle PDF input and convert first page to image
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read(),
                poppler_path=r"C:\Program Files (x86)\poppler-24.08.0\Library\bin")

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    
##Streamlit app

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description:",key="input")
uploaded_file=st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1=st.button("Tell Me About the Resume")

#submit2=st.button("How can I Improvise my skills")

submit3=st.button("Percentage match")

input_prompt1="""
You are an experienced Technical Human Resource Manager in the field of any one job role from Data Science,Full Stack,Web Development,ML Engineer,
Big Data Engineering,Data Analyst,DEVOPS, your task is to reveiw the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with role.
Highlight the strengths and weaknesses of applicant in relation to the specified job requirements.

"""

# input_prompt2="""

#You are an experienced Technical Human Resource Manager with expertise in the field of Data Science,Full Stack,Web Development,ML Engineer,
#Big Data Engineering,Data Analyst,DEVOPS, your role is to srcutinize the provided resume in light of the job description provided.
#share your insight on the candidate's on suitability for the role from and HR perspective.
#Additionally, offer advice on enhancing the candidate's skills and identify areas .

#"""

input_prompt3="""
You are an skilled ATS(Applicant Tracking System) scanner with deep understanding of any one job role Data Science, Full Stack, Web Development, ML Engineer,
Big Data Engineering, Data Analyst, DEVOPS and deep ATS Functionality. 
Your task is to evaluate the resume against the provided joib description, give me percentage match if resume matches
job description. First the output should come as percentage and then keywords missing and last final thoughts.

"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume") 

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume") 

