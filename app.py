import streamlit as st 
import google.generativeai as genai 
import os

import PyPDF2 as pdf 

from dotenv import load_dotenv

load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##gemini response
def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text 

##pdf--> text
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text    


input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text} 
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

##streamlit
st.title("Smart ATS")
st.text("Improve your chances of getting selected")
jd=st.text_area("Paste the job description")
uploaded_file=st.file_uploader("Upload your resume",type="pdf",help="Please upload yhe pdf")

submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
##the text is not uised to get the response rather the prompt is used,
## since inside of the prompt, we placehold text, so it automatically refers to that,
        st.subheader(response)