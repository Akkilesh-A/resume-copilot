import streamlit as st
import google.generativeai as genai
import os
import docx2txt
import PyPDF2 as pdf
from dotenv import load_dotenv

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

#PROMPT TEMPLATE
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

job_description = st.text_area("Paste the Job Description", height=300).lower()  # Convert to lowercase
uploaded_files = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], accept_multiple_files=True, help="Please upload a single PDF or DOCX file")
submit_button = st.button("Submit")

if uploaded_files and len(uploaded_files) > 1:
    st.error("Please upload only one file at a time.")
elif submit_button and uploaded_files:
    if not job_description.strip():
        st.error("Please provide the Job Description ⚠️")
    else:
        uploaded_file = uploaded_files[0]
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf_file(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx_file(uploaded_file)
        
        # Convert resume text and job description to lowercase
        response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description))

        # Extract Job Description Match percentage from the response
        match_percentage_str = response_text.split('"Job Description Match":"')[1].split('"')[0]

        if match_percentage_str == 'N/A':
            st.error("Sorry, your skills do not match the requirements 😣")
            
            # Extract missing keywords from the response
            missing_keywords = response_text.split('"Missing Keywords":"')[1].split('"')[0].lower()  # Convert to lowercase
            st.subheader("Missing Keywords:")
            st.write(missing_keywords)
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
            # Show progress bar with a numerical value
            st.write(f"Your Resume Match: {match_percentage_str}")
            st.progress(match_percentage / 100)
            # Highlight the Job Description Match percentage and display message
            if match_percentage >= 70:
                st.success(f" Your Resume Match is {match_percentage_str}😊 - This resume matches the job description!")  # Highlight in green for a good match
            else:
                st.error(f" Match {match_percentage_str}😭 - This resume does not match the job description.")  # Highlight in red for a poor match
                
                # Extract missing keywords from the response
                missing_keywords = response_text.split('"Missing Keywords":"')[1].split('"')[0].lower()  # Convert to lowercase
                # Provide suggestions for improving the resume
                st.subheader("How to Improve Your Resume:")
                st.write("1. Incorporate the missing keywords from the job description into your resume.")
                st.write("2. Tailor your resume to better highlight your skills and experience relevant to the job.")
                # Recommend incorporating missing skills
                st.write("3. **Add these skills to improve your resume:**")
                st.write(missing_keywords)
