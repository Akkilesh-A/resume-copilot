from flask import request,jsonify,render_template
from config import app,db
from models import Jobs,AdminLogin,JobSeekerResumeScore,BestResumes,NonTechnicalBestResumes
import csv
import google.generativeai as genai
import os
import docx2txt
import PyPDF2 as pdf
import re
import webbrowser
import spacy
from spacy.matcher import Matcher
from PyPDF2 import PdfFileReader
import phonenumbers
import fitz  # PyMuPDF


@app.route('/jobs',methods=['GET'])
def get_jobs():
    jobs=Jobs.query.all()
    json_jobs=list(map(lambda job:job.to_json(),jobs))
    return jsonify(json_jobs)


@app.route('/create_job',methods=['POST'])
def create_job():
    job_title=request.json.get("jobTitle")
    tech_stack=request.json.get("techStack")

    if not job_title or not tech_stack:
        return jsonify({"error":"Please provide job title and tech stack"}),400
    
    new_job=Jobs(job_title=job_title,tech_stack=tech_stack)

    try:
        db.session.add(new_job)
        db.session.commit()
    except Exception as e:
        return ({"message":str(e)},400)
    
    return jsonify({"message":"Job Post created successfully"}),201

@app.route('/delete_job/<int:user_id>',methods=['DELETE'])
def delete_job(user_id):
    job=Jobs.query.filter_by(id=user_id).first()

    if not job:
        return jsonify({"message":"Job not found"}),404
    
    db.session.delete(job)
    db.session.commit()

    return jsonify({"message":"Job deleted successfully"}),200


@app.route('/admin_login',methods=['POST'])
def admin_login():
    user_id=request.json.get("userId")
    password=request.json.get("password")
    user_id_from_db=AdminLogin.query.filter_by(user_id=user_id).first()
    password_from_db=AdminLogin.query.filter_by(password=password).first()
    if(user_id_from_db and password_from_db):
        return jsonify({"message":"Login successful"}),200
    else:
        return jsonify({"message":"Login failed"}),401
    
@app.route('/admin_register',methods=['POST'])
def admin_register():
    user_id=request.json.get("userId")
    password=request.json.get("password")
    if not user_id or not password:
        return jsonify({"error":"Please provide user id and password"}),400
    
    new_user=AdminLogin(user_id=user_id,password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return ({"message":str(e)},400)
    
    return jsonify({"message":"Admin registered successfully"}),201


@app.route("/resume_scanned", methods=['GET'])
def resume_scan():
    job_position_clicked=request.args.get('jobtitle')
    tech_stack_required=request.args.get('techstack')
    with open('uploaded_files/resume.csv', mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        job_position = []
        name=[]
        email=[]
        tech_stack=[]
        for lines in csvFile:
            if(lines[0]==job_position_clicked):
                job_position += "["+lines[0] + "]"
                name += "["+lines[1] + "]"
                email += "["+lines[2] + "]"
                tech_stack += "["+lines[3] + "]"
        if len(job_position)<1:
            job_position+="No Resume Found"

    return jsonify({"techStackRequired":tech_stack_required,"jobPositionClicked": job_position_clicked,"jobPosition": job_position,"name": name,"email": email,"techStack": tech_stack}), 200

UPLOAD_FOLDER = 'uploaded_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#generating score for JOB SEEKERS!
@app.route("/resume_scan_with_ai", methods=['POST'])
def resume_scanner():
    if 'image' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    uploaded_file_from_form = request.files['image']
    if uploaded_file_from_form.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the file to the upload folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file_from_form.filename)
    uploaded_file_from_form.save(file_path)

    job_title = request.form.get('jobTitle')
    tech_stack = request.form.get('techStack')

    # Process the uploaded file here if needed
    genai.configure(api_key="AIzaSyCC0ixjF5MwOyG_WTToz-VQR5oWdJoqggY")


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

    string_to_be_sent=" "

    selected_candidates = []  

    if uploaded_file_from_form.mimetype == "application/pdf":
        with open(file_path, "rb") as pdf_file:
            resume_text = extract_text_from_pdf_file(pdf_file)
            print("Extracted PDF Text:", resume_text)  # Debugging statement
    elif uploaded_file_from_form.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        with open(file_path, "rb") as docx_file:
            resume_text = extract_text_from_docx_file(docx_file)
            print("Extracted DOCX Text:", resume_text)  # Debugging statement

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


    if uploaded_file_from_form:
        if not tech_stack.strip():
            return jsonify({"message":"Please provide the Job Description ⚠"})
        else:
            if uploaded_file_from_form.mimetype == "application/pdf":
                with open(file_path, "rb") as pdf_file:
                    resume_text = extract_text_from_pdf_file(pdf_file)
                    print("Extracted PDF Text:", resume_text)  # Debugging statement
            elif uploaded_file_from_form.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                with open(file_path, "rb") as docx_file:
                    resume_text = extract_text_from_docx_file(docx_file)
                    print("Extracted DOCX Text:", resume_text)  # Debugging statement
            response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=tech_stack))

            # Initialize missing_keywords variable
            missing_keywords = ""

            # Extract Job Description Match percentage from the response
            match_percentage_str = response_text.split('"Job Description Match":"')[1].split('"')[0]

            if match_percentage_str == 'N/A':
                score=match_percentage_str+" Sorry yours Skills do not match with the requirements 😣"
                # Get missing keywords from the job description and resume
                missing_keywords = get_missing_keywords(tech_stack, resume_text)
                result=missing_keywords
            
            else:
            # Remove percentage symbol and convert to float
                match_percentage = float(match_percentage_str.rstrip('%'))
                score=match_percentage

                if match_percentage >= 20:
                    result=f" Your Resume Match is {match_percentage_str}😊 - This resume matches the job description!"  # Highlight in green for a good match
                else:
                    result=f" Match {match_percentage_str}😭 - This resume does not match the job description."  # Highlight in red for a poor match
    
    new_job=JobSeekerResumeScore(job_position=job_title,tech_stack=tech_stack,name=score,phone_number=result)

    try:
        db.session.add(new_job)
        db.session.commit()
    except Exception as e:
        return ({"message":str(e)},400)
    
    return jsonify({"message": "File processed and saved successfully & Resume Score stored successfully","stringGotten":string_to_be_sent+job_title+tech_stack}), 200
              
@app.route('/resumescore',methods=['GET'])
def get_resume_score():
    jobs=JobSeekerResumeScore.query.all()
    json_jobs=list(map(lambda job:job.to_json(),jobs))
    return jsonify(json_jobs)

MULTIPLE_RESUMES_UPLOAD_FOLDER='multiple_resume_uploads'
app.config['MULTIPLE_RESUMES_UPLOAD_FOLDER'] = MULTIPLE_RESUMES_UPLOAD_FOLDER

# # Scanning Non Technical multiple resumes WORKING new THINGY
@app.route("/non_technical_recruiter_resume_scan", methods=['POST'])
def non_technical_multiple_resume_scanner():
    job_title = request.form.get('jobTitle')
    tech_stack = request.form.get('techStack')
    no_of_resumes=int(request.form.get('noOfResumes'))
    match=int(request.form.get('match'))

    job_description=tech_stack
    minimum_passing_score=match

    if 'image_0' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    uploaded_file_from_form = request.files
    if uploaded_file_from_form['image_0'].filename == '':
        return jsonify({"error": "No file selected"}), 400

    for i in range(0,no_of_resumes):
        # Save the file to the upload folder
        file_path = os.path.join(app.config['MULTIPLE_RESUMES_UPLOAD_FOLDER'], uploaded_file_from_form['image_'+str(i)].filename)
        uploaded_file_from_form['image_'+str(i)].save(file_path)

    genai.configure(api_key="AIzaSyCC0ixjF5MwOyG_WTToz-VQR5oWdJoqggY")

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
        try:
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
                        # Use regex to extract the username after "github.com/"
                        match = re.search(r"github\.com/([^/]+)", url)
                        if match:
                            username = match.group(1)
                            links.append(username)

            # Close the PDF document
            pdf_document.close()

            return links
        except Exception as e:
            # Handle any exceptions (e.g., file operations, PDF parsing)
            print(f"Error: {e}")

        return []

    def calculate_match_percentage(resume_text, job_description, minimum_passing_score):
        # Implement this function to calculate the match percentage
        # Placeholder implementation for now
        return 0

    string_to_be_sent=" "

    if not job_description:
        return jsonify({"message":"⚠️ Please provide the job description.","stringGotten":"Nothing"}),200
    else:
        if uploaded_file_from_form:
            selected_candidates = []
            no_candidates_meet_criteria = True
            for  i in range(0,no_of_resumes):
                file_path_here = os.path.join(app.config['MULTIPLE_RESUMES_UPLOAD_FOLDER'],uploaded_file_from_form['image_' + str(i)].filename)
                if uploaded_file_from_form['image_'+str(i)].content_type == "application/pdf":
                    with open(file_path_here, "rb") as pdf_file:
                        resume_text = extract_text_from_pdf_file(pdf_file)
                        print("Extracted PDF Text:", resume_text)  # Debugging statement
                elif uploaded_file_from_form['image_'+str(i)].content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    with open(file_path_here, "rb") as docx_file:
                        resume_text = extract_text_from_docx_file(docx_file)
                        print("Extracted DOCX Text:", resume_text)  # Debugging statement
                
                # Extract candidate name
                candidate_name = extract_candidate_name(resume_text)

                # Extract GitHub links
                # github_links = extract_github_links_from_pdf(uploaded_file_from_form['image_'+str(i)])

                # Calculate job description match percentage
                match_percentage = calculate_match_percentage(resume_text, job_description, minimum_passing_score)

                # Check if candidate meets minimum score criteria
                if match_percentage is not None and match_percentage >= minimum_passing_score:
                    # Extract candidate phone number
                    candidate_phone = extract_candidate_phone_number(resume_text, "ZZ")  # Assuming ZZ as the default country code

                    # Append candidate details to the list of selected candidates
                    # if not github_links[0]:
                    #     github_links[0]="No GitHub Username Found"
                    # selected_candidates.append((candidate_name, candidate_phone, github_links[0]))
                    selected_candidates.append((candidate_name, candidate_phone))

                    no_candidates_meet_criteria = False

        if selected_candidates!=[]:
            for candidate in selected_candidates: 
                new_job = NonTechnicalBestResumes(
                    job_position=job_title,
                    tech_stack=tech_stack,
                    name=candidate[0],
                    phone_number=candidate[1][0]
                )
                db.session.add(new_job)
                db.session.commit()
        else:
           return jsonify({"message":f"🛑 No candidates meet the minimum score criteria ({minimum_passing_score}% or above).","stringGotten":"Nothing"}),200

    return jsonify({"message": "Files uploaded successfully","stringGotten":selected_candidates}), 200

# # Scanning multiple Technical resumes WORKING new THINGY
@app.route("/recruiter_resume_scan", methods=['POST'])
def multiple_resume_scanner():
    job_title = request.form.get('jobTitle')
    tech_stack = request.form.get('techStack')
    no_of_resumes=int(request.form.get('noOfResumes'))
    match=int(request.form.get('match'))

    job_description=tech_stack
    minimum_passing_score=match

    if 'image_0' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    uploaded_file_from_form = request.files
    if uploaded_file_from_form['image_0'].filename == '':
        return jsonify({"error": "No file selected"}), 400

    for i in range(0,no_of_resumes):
        # Save the file to the upload folder
        file_path = os.path.join(app.config['MULTIPLE_RESUMES_UPLOAD_FOLDER'], uploaded_file_from_form['image_'+str(i)].filename)
        uploaded_file_from_form['image_'+str(i)].save(file_path)

    genai.configure(api_key="AIzaSyCC0ixjF5MwOyG_WTToz-VQR5oWdJoqggY")

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
        try:
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
                        # Use regex to extract the username after "github.com/"
                        match = re.search(r"github\.com/([^/]+)", url)
                        if match:
                            username = match.group(1)
                            links.append(username)

            # Close the PDF document
            pdf_document.close()

            return links
        except Exception as e:
            # Handle any exceptions (e.g., file operations, PDF parsing)
            print(f"Error: {e}")

        return []

    def calculate_match_percentage(resume_text, job_description, minimum_passing_score):
        # Implement this function to calculate the match percentage
        # Placeholder implementation for now
        return 0

    string_to_be_sent=" "

    if not job_description:
        return jsonify({"message":"⚠️ Please provide the job description.","stringGotten":"Nothing"}),200
    else:
        if uploaded_file_from_form:
            selected_candidates = []
            no_candidates_meet_criteria = True
            for  i in range(0,no_of_resumes):
                file_path_here = os.path.join(app.config['MULTIPLE_RESUMES_UPLOAD_FOLDER'],uploaded_file_from_form['image_' + str(i)].filename)
                if uploaded_file_from_form['image_'+str(i)].content_type == "application/pdf":
                    with open(file_path_here, "rb") as pdf_file:
                        resume_text = extract_text_from_pdf_file(pdf_file)
                        print("Extracted PDF Text:", resume_text)  # Debugging statement
                elif uploaded_file_from_form['image_'+str(i)].content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    with open(file_path_here, "rb") as docx_file:
                        resume_text = extract_text_from_docx_file(docx_file)
                        print("Extracted DOCX Text:", resume_text)  # Debugging statement
                
                # Extract candidate name
                candidate_name = extract_candidate_name(resume_text)

                # Extract GitHub links
                # github_links = extract_github_links_from_pdf(uploaded_file_from_form['image_'+str(i)])

                # Calculate job description match percentage
                match_percentage = calculate_match_percentage(resume_text, job_description, minimum_passing_score)

                # Check if candidate meets minimum score criteria
                if match_percentage is not None and match_percentage >= minimum_passing_score:
                    # Extract candidate phone number
                    candidate_phone = extract_candidate_phone_number(resume_text, "ZZ")  # Assuming ZZ as the default country code

                    # Append candidate details to the list of selected candidates
                    # if not github_links[0]:
                    #     github_links[0]="No GitHub Username Found"
                    # selected_candidates.append((candidate_name, candidate_phone, github_links[0]))
                    selected_candidates.append((candidate_name, candidate_phone))

                    no_candidates_meet_criteria = False

        if selected_candidates!=[]:
            for candidate in selected_candidates: 
                new_job = NonTechnicalBestResumes(
                    job_position=job_title,
                    tech_stack=tech_stack,
                    name=candidate[0],
                    phone_number=candidate[1][0]
                )
                db.session.add(new_job)
                db.session.commit()
        else:
           return jsonify({"message":f"🛑 No candidates meet the minimum score criteria ({minimum_passing_score}% or above).","stringGotten":"Nothing"}),200

    return jsonify({"message": "Files uploaded successfully","stringGotten":selected_candidates}), 200





@app.route('/multipleresumescore',methods=['GET'])
def get_best_resumes():
    jobs=BestResumes.query.all()
    json_jobs=list(map(lambda job:job.to_json(),jobs))
    return jsonify(json_jobs)


@app.route('/nontechnicalmultipleresumescore',methods=['GET'])
def get_best_non_technical_resumes():
    jobs=NonTechnicalBestResumes.query.all()
    json_jobs=list(map(lambda job:job.to_json(),jobs))
    return jsonify(json_jobs)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
