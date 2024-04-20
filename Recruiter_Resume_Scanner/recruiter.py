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
    return text_content


def extract_text_from_docx_file(uploaded_file):
    # Use docx2txt to extract text from a DOCX file
    return docx2txt.process(uploaded_file)


# Function to extract candidate name from resume text
def extract_candidate_name(resume_text):
    # Regular expression to find candidate names
    name_pattern = r'\b[A-Z][a-z]*\b\s+\b[A-Z][a-z]*\b'
    
    # Find all occurrences of the name pattern in the resume text
    candidate_names = re.findall(name_pattern, resume_text)
    
    # If names are found, return the first name as the candidate name
    if candidate_names:
        return candidate_names[0]
    else:
        # If no name found, return a generic Indian name
        return "Candidate Name"


# Function to extract candidate phone number from resume text
def extract_candidate_phone_number(resume_text):
    # Regular expression to find phone numbers
    phone_pattern = r'(\b\d{10,12}\b|\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}\b)'
    
    # Find all occurrences of the phone number pattern in the resume text
    candidate_phones = re.findall(phone_pattern, resume_text)
    
    # If phone numbers are found, return the first phone number
    if candidate_phones:
        return candidate_phones[0]
    else:
        # If no phone number found, return a generic Indian phone number
        return "+91 XXXXXXXXXX"


# Function to calculate job description match percentage
def calculate_match_percentage(resume_text, job_description):
    # PROMPT TEMPLATE
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
    {{"Job Description Match":"%", "Missing Keywords":""}}
    """
    
    # Generate response from Gemini model
    response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description))

    # Extract Job Description Match percentage from the response
    match_percentage_str = response_text.split('"Job Description Match":"')[1].split('"')[0]

    # Check if match percentage is "N/A"
    if match_percentage_str == "N/A":
        return None

    # Remove percentage symbol and convert to float
    match_percentage = float(match_percentage_str.rstrip('%'))

    return match_percentage


# Streamlit app
# Initialize Streamlit app
url = 'http://localhost:5173/adminjobsportal'

with open('./recruiter.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title("Upload Resumes 🚀")
st.markdown('<style>h1{color: black; text-align: center;}</style>', unsafe_allow_html=True)
job_description = st.text_area("Paste the Job Description", height=300)
uploaded_files = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], accept_multiple_files=True, help="Please upload PDF or DOCX files")

submit_button = st.button("Submit")

# Set the minimum passing score
minimum_passing_score = 70

if submit_button:
    # Check if job description is provided
    if not job_description:
        st.error("⚠️ Please provide the job description.")
    else:
        if uploaded_files:
            selected_candidates = []
            no_candidates_meet_criteria = True
            for uploaded_file in uploaded_files:
                if uploaded_file.type == "application/pdf":
                    resume_text = extract_text_from_pdf_file(uploaded_file)
                    print("Extracted PDF Text:", resume_text)  # Debugging statement
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    resume_text = extract_text_from_docx_file(uploaded_file)
                    print("Extracted DOCX Text:", resume_text)  # Debugging statement
                
                # Calculate job description match percentage
                match_percentage = calculate_match_percentage(resume_text, job_description)

                # Check if candidate meets minimum score criteria
                if match_percentage is not None and match_percentage >= minimum_passing_score:
                    # Extract candidate name and phone number
                    candidate_name = extract_candidate_name(resume_text)
                    candidate_phone = extract_candidate_phone_number(resume_text)

                    # Append candidate details to the list of selected candidates
                    selected_candidates.append((candidate_name, candidate_phone))
                    no_candidates_meet_criteria = False

            # Display selected candidates' names and phone numbers in columns with improved style
            if selected_candidates:
                st.subheader("🌟 Selected Candidates 🌟")
                for i, (name, phone) in enumerate(selected_candidates, start=1):
                    st.markdown(f"""
                        <div style="background-color: #fff; border: 2px solid #333; padding: 10px; margin-bottom: 10px;">
                            <p style="font-family: 'Poppins', sans-serif; font-weight: 600; font-size: 1.2rem;">Candidate {i}</p>
                            <p style="font-family: 'Poppins', sans-serif; font-size: 1rem;">Name: {name}</p>
                            <p style="font-family: 'Poppins', sans-serif; font-size: 1rem;">Phone: {phone}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("🛑 No candidates meet the minimum score criteria (70% or above).")