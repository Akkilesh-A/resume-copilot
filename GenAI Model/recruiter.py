import streamlit as st
import google.generativeai as genai
import os
import docx2txt
import PyPDF2 as pdf
from dotenv import load_dotenv
import re
import webbrowser

# Load environment variables from a .env file
load_dotenv()

# Configure the generative AI model with the Google API key
genai.configure(api_key=os.getenv("AIzaSyCC0ixjF5MwOyG_WTToz-VQR5oWdJoqggY"))


# Set up the model configuration for text generation
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Define safety settings for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]


def generate_response_from_gemini(input_text):
    # Create a GenerativeModel instance with 'gemini-pro' as the model type
    llm = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    # Generate content based on the input text
    output = llm.generate_content(input_text)
    # Return the generated text
    return output.text


def extract_text_from_pdf_file(uploaded_file):
    # Use PdfReader to read the text content from a PDF file
    pdf_reader = pdf.PdfReader(uploaded_file)
    text_content = ""
    for page in pdf_reader.pages:
        text_content += str(page.extract_text())
    return text_content


def extract_text_from_docx_file(uploaded_file):
    # Use docx2txt to extract text from a DOCX file
    return docx2txt.process(uploaded_file)


# Streamlit app
# Initialize Streamlit app
url = 'http://localhost:5173/adminjobsportal'

if st.button('Go Back'):
    webbrowser.open_new_tab(url)

with open('./wave.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title("Intelligent ATS-Enhance Your Resume ATS")
st.markdown('<style>h1{color: black; text-align: center;}</style>', unsafe_allow_html=True)
job_description = st.text_area("Paste the Job Description", height=300)
uploaded_files = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], accept_multiple_files=True, help="Please upload PDF or DOCX files")

submit_button = st.button("Submit")

if submit_button:
    if uploaded_files:
        selected_candidates = []
        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf_file(uploaded_file)
                print("Extracted PDF Text:", resume_text)  # Debugging statement
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = extract_text_from_docx_file(uploaded_file)
                print("Extracted DOCX Text:", resume_text)  # Debugging statement
            
            response_text = generate_response_from_gemini(resume_text)

            # Check if candidate meets minimum score criteria (not implemented)
            match_percentage = 100  # Placeholder for match percentage

            # Extract candidate name from anywhere within the resume text
            candidate_name_match = re.search(r'(\b[A-Z][a-z]*\b\s+\b[A-Z][a-z]*\b)', resume_text)  # Find name pattern
            candidate_name = candidate_name_match.group(0) if candidate_name_match else "Name not found"

            # Extract candidate mobile number from anywhere within the resume text
            candidate_mobile_match = re.search(r'(\b\d{10,12}\b|\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}\b)', resume_text)  # Find phone number pattern
            candidate_mobile = candidate_mobile_match.group(0) if candidate_mobile_match else "Mobile number not found"

            # Append candidate details to the list of selected candidates
            selected_candidates.append((candidate_name, candidate_mobile))

        # Display selected candidates' names and phone numbers
        if selected_candidates:
            st.subheader("Selected Candidates:")
            for i, candidate_info in enumerate(selected_candidates, start=1):
                st.write(f"S.No: {i}, Name: {candidate_info[0]}, Mobile Number: {candidate_info[1]}")
        else:
            st.text("No candidates meet the minimum score criteria (50% or above)")
