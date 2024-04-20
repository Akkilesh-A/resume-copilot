import streamlit as st
import google.generativeai as genai
import os
import docx2txt
import PyPDF2 as pdf
from dotenv import load_dotenv
import re

# Load environment variables from a .env file
load_dotenv()

# Configure the generative AI model with the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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
    return text_content.lower()  # Convert text to lowercase

def extract_text_from_docx_file(uploaded_file):
    # Use docx2txt to extract text from a DOCX file
    return docx2txt.process(uploaded_file).lower()  # Convert text to lowercase

def tokenize_text(text):
    """Tokenizes text into words and removes punctuation."""
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    words = text.split()  # Tokenize text into words
    return words

def get_missing_keywords(job_description, resume_text):
    """Get missing keywords from job description that are absent in resume."""
    # Tokenize job description and resume text
    job_words = set(tokenize_text(job_description))
    resume_words = set(tokenize_text(resume_text))
    
    # Calculate missing keywords
    missing_keywords = job_words - resume_words  # Difference between job and resume words
    
    # Return sorted list of missing keywords for readability
    return sorted(list(missing_keywords))

# Prompt template
input_prompt_template = """
As an experienced Applicant Tracking System (ATS) analyst,
with profound knowledge in technology, software engineering, data science, 
and big data engineering, your role involves evaluating resumes against job descriptions.
Recognizing the competitive job market, provide top-notch assistance for resume improvement.
Your goal is to analyze the resume against the given job description, 
assign a percentage match based on key criteria, and pinpoint missing keywords accurately.
resume:{text}
description:{job_description}
I want the response in one single string having the structure
"Job Description Match":"%", "Missing Keywords":""
"""

# Streamlit app
# Initialize Streamlit app
with open('./style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title("Get Your Resume Score 🚀")
st.markdown('<style>h1{color: black; text-align: center;}</style>', unsafe_allow_html=True)

# Text area with auto lowercase conversion for job description
job_description = st.text_area("Paste the Job Description", height=300).lower()

# File uploader for resumes, allowing one file at a time
uploaded_files = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], accept_multiple_files=True, help="Please upload a single PDF or DOCX file")

# Submit button
submit_button = st.button("Submit")

# Initialize `resume_text` variable
resume_text = ""

# If there are uploaded files and submit button is pressed
if uploaded_files and submit_button:
    # Ensure that only one file is uploaded
    if len(uploaded_files) > 1:
        st.error("Please upload only one file at a time.")
    elif not job_description.strip():
        st.error("Please provide the Job Description ⚠️")
    else:
        # Get the first uploaded file
        uploaded_file = uploaded_files[0]
        
        # Extract text from the uploaded file
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf_file(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx_file(uploaded_file)
        
        # Generate response from generative AI
        response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description))
        
        # Initialize missing_keywords variable
        missing_keywords = ""
        
        # Extract Job Description Match percentage from the response
        match_percentage_str = response_text.split('"Job Description Match":"')[1].split('"')[0]
        
        # Determine the match percentage and missing keywords
        if match_percentage_str == 'N/A':
            st.error("Sorry, your skills do not match the requirements 😣")
            
            # Get missing keywords from the job description and resume
            missing_keywords = get_missing_keywords(job_description, resume_text)
            
            # Display missing keywords as a list
            st.subheader("Missing Keywords:")
            st.write(", ".join(missing_keywords))
            
            # Provide suggestions for improving the resume
            st.subheader("How to Improve Your Resume:")
            st.write("1. Incorporate the missing keywords from the job description into your resume.")
            st.write("2. Tailor your resume to highlight relevant skills, experience, and accomplishments.")
            st.write("3. Ensure your resume is clear, concise, and well-organized.")
            st.write("4. Review and proofread your resume to eliminate any errors.")
        else:
            # Remove percentage symbol and convert to float
            match_percentage = float(match_percentage_str.rstrip('%'))

            # Display ATS Evaluation Result
            st.subheader("ATS Evaluation Result:")
            st.write("```json")
            st.write(response_text)
            st.write("```")
            
            # Create a progress bar to represent the match percentage
            st.write(f"Your Resume Match: {match_percentage_str}")
            st.progress(match_percentage / 100)
            
            # Determine whether the resume match is good or poor
            if match_percentage >= 70:
                st.success(f"😊 - This resume matches the job description!")
            else:
                st.error(f"😭 - This resume does not match the job description.")
                
                # Get missing keywords from the job description and resume
                missing_keywords = get_missing_keywords(job_description, resume_text)
                
                # Display missing keywords as a list
                st.subheader("Missing Keywords:")
                st.write(", ".join(missing_keywords))
                
                # Provide suggestions for improving the resume
                st.subheader("How to Improve Your Resume:")
                st.write("1. Incorporate the missing keywords from the job description into your resume.")
                st.write("2. Tailor your resume to better highlight your skills and experience relevant to the job.")
