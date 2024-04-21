import streamlit as st
import google.generativeai as genai
import os
import docx2txt
import PyPDF2 as pdf
from dotenv import load_dotenv
import re
import webbrowser
import spacy
from spacy.matcher import Matcher
from PyPDF2 import PdfFileReader
import phonenumbers
import fitz  # PyMuPDF

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

# Load English tokenizer, tagger, parser, NER, and word vectors for SpaCy
nlp = spacy.load("en_core_web_sm")

# Define a new matcher to find patterns of one or two proper nouns (potential names)
matcher = Matcher(nlp.vocab)
pattern = [{"POS": "PROPN"}, {"POS": "PROPN", "OP": "?"}]
matcher.add("NAME", [pattern])

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

def extract_candidate_name(resume_text):
    # Extract names from resume text using SpaCy
    doc = nlp(resume_text)
    names = []
    matches = matcher(doc)
    for match_id, start, end in matches:
        names.append(doc[start:end].text)
    # If no names found, return "Candidate Name"
    return names[0] if names else "Candidate Name"

def extract_candidate_phone_number(resume_text, default_country_code):
    # Find all occurrences of phone numbers in the text
    candidate_phones = phonenumbers.PhoneNumberMatcher(resume_text, default_country_code)

    # Initialize a list to store formatted phone numbers
    formatted_phones = []

    # Iterate over the phone number matches
    for match in candidate_phones:
        # Get the phone number object
        phone_number = match.number

        # Format the phone number as a string
        formatted_phone = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        # Add the formatted phone number to the list
        formatted_phones.append(formatted_phone)

    # If phone numbers are found
    if formatted_phones:
        return formatted_phones
    else:
        return "Phone number not found"

def extract_github_links_from_pdf(uploaded_file):
    # Get the file path of the uploaded PDF file
    file_path = f"/tmp/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Initialize a list to store extracted links
    links = []

    # Open the PDF file
    pdf_document = fitz.open(file_path)

    # Iterate through each page of the PDF
    for page_num in range(len(pdf_document)):
        # Get the page object
        page = pdf_document[page_num]
        
        # Extract links from the page
        page_links = page.get_links()
        
        # Iterate through each link on the page
        for link in page_links:
            # Get the URL of the link
            url = link.get("uri")
            # Check if the URL is a GitHub link
            if "github.com" in url:
                links.append(url)

    # Close the PDF document
    pdf_document.close()

    # Delete the temporary file
    os.remove(file_path)

    return links

def calculate_match_percentage(resume_text, job_description, minimum_passing_score):
    # Implement this function to calculate the match percentage
    # Placeholder implementation for now
    return 0

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

minimum_passing_score = st.number_input("Enter the minimum passing score (%)", min_value=0, max_value=100, value=0)
submit_button = st.button("Submit")

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

                # Extract candidate name
                candidate_name = extract_candidate_name(resume_text)

                # Extract GitHub links
                github_links = extract_github_links_from_pdf(uploaded_file)

                # Calculate job description match percentage
                match_percentage = calculate_match_percentage(resume_text, job_description, minimum_passing_score)

                # Check if candidate meets minimum score criteria
                if match_percentage is not None and match_percentage >= minimum_passing_score:
                    # Extract candidate phone number
                    candidate_phone = extract_candidate_phone_number(resume_text, "ZZ")  # Assuming ZZ as the default country code

                    # Append candidate details to the list of selected candidates
                    selected_candidates.append((candidate_name, candidate_phone, github_links))
                    no_candidates_meet_criteria = False

            # Display selected candidates' names, phone numbers, and GitHub links in columns with improved style
            if selected_candidates:
                st.subheader("🌟 Selected Candidates 🌟")
                for i, (name, phone, github_links) in enumerate(selected_candidates, start=1):
                    st.markdown(f"""
                        <div style="background-color: #fff; border: 2px solid #333; padding: 10px; margin-bottom: 10px;">
                            <p style="font-family: 'Poppins', sans-serif; font-weight: 600; font-size: 1.2rem;">Candidate {i}</p>
                            <p style="font-family: 'Poppins', sans-serif; font-size: 1rem;">Name: {name}</p>
                            <p style="font-family: 'Poppins', sans-serif; font-size: 1rem;">Phone: {phone}</p>
                            <p style="font-family: 'Poppins', sans-serif; font-size: 1rem;">GitHub Links: {', '.join(github_links) if github_links else 'None'}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.error(f"🛑 No candidates meet the minimum score criteria ({minimum_passing_score}% or above).")
