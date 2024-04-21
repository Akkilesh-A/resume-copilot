from flask import request,jsonify,render_template
from config import app,db
from models import Jobs,AdminLogin,JobSeekerResumeScore,RecruiterResumeUploads
import csv
import google.generativeai as genai
import os
import docx2txt
import PyPDF2 as pdf
import re


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
#Scanning multiple resumes
@app.route("/recruiter_resume_scan", methods=['POST'])
def multiple_resume_scanner():
    job_title = request.form.get('jobTitle')
    tech_stack = request.form.get('techStack')
    no_of_resumes=int(request.form.get('noOfResumes'))

    if 'image_0' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    uploaded_file_from_form = request.files
    if uploaded_file_from_form['image_0'].filename == '':
        return jsonify({"error": "No file selected"}), 400

    for i in range(0,no_of_resumes):
        # Save the file to the upload folder
        file_path = os.path.join(app.config['MULTIPLE_RESUMES_UPLOAD_FOLDER'], uploaded_file_from_form['image_'+str(i)].filename)
        uploaded_file_from_form['image_'+str(i)].save(file_path)

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


    # Function to extract candidate name from resume text
    def extract_candidate_name(resume_text):
        # Regular expression to find candidate names
        name_pattern = r'\b[A-Z][a-z]\b\s+\b[A-Z][a-z]\b'
        
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

    selection_criteria_percentage=30
    string_to_be_sent=" "

    # Function to calculate job description match percentage
    def calculate_match_percentage(resume_text, job_description, minimum_passing_score):
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


    for i in range(0, no_of_resumes):
        if not tech_stack:
            return jsonify({"message": "⚠ Please provide the job description."}), 400
        else:
            if uploaded_file_from_form:
                selected_candidates = []
                no_candidates_meet_criteria = True
                file_path_here = os.path.join(app.config['MULTIPLE_RESUMES_UPLOAD_FOLDER'],
                                              uploaded_file_from_form['image_' + str(i)].filename)
                for uploaded_file in uploaded_file_from_form:
                    if uploaded_file_from_form.get('image_' + str(i)).content_type == "application/pdf":
                        with open(file_path_here, "rb") as pdf_file:
                            resume_text = extract_text_from_pdf_file(pdf_file)
                            print("Extracted PDF Text:", resume_text)  # Debugging statement
                    elif uploaded_file_from_form.get('image_' + str(i)).content_type == \
                            "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        with open(file_path_here, "rb") as docx_file:
                            resume_text = extract_text_from_docx_file(docx_file)
                            print("Extracted DOCX Text:", resume_text)  # Debugging statement

                    # Calculate job description match percentage with the selected minimum passing score
                    match_percentage = calculate_match_percentage(resume_text, tech_stack,
                                                                  selection_criteria_percentage)

                # Check if candidate meets minimum score criteria
                if match_percentage is not None and match_percentage >= selection_criteria_percentage:
                    # Extract candidate name and phone number
                    candidate_name = extract_candidate_name(resume_text)
                    candidate_phone = extract_candidate_phone_number(resume_text)

                    # Append candidate details to the list of selected candidates
                    selected_candidates.append((candidate_name, candidate_phone))
                    no_candidates_meet_criteria = False

        # Display selected candidates' names and phone numbers in columns with improved style
        if selected_candidates:
            for i, (name, phone) in enumerate(selected_candidates, start=1):
                string_to_be_sent+=name+" "+phone+" "
                new_job=RecruiterResumeUploads(job_position=job_title,tech_stack=tech_stack,name=name,phone_number=phone)
                try:
                    db.session.add(new_job)
                    db.session.commit()
                except Exception as e:
                    return ({"message":str(e)},400)
            return jsonify({"message": "Resume Processed successfully","stringGotten":string_to_be_sent+job_title+tech_stack}), 200
                
        else:
            return jsonify({"message":f"🛑 No candidates meet the minimum score criteria ({selection_criteria_percentage}% or above).","stringGotten":string_to_be_sent+job_title+tech_stack})
    
    return jsonify({"message": "Error Processing Resumes","stringGotten":string_to_be_sent+job_title+tech_stack}), 200




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
