from flask import request,jsonify,render_template
from config import app,db
from models import Jobs,AdminLogin,JobSeekerResumeScore
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

# @app.route("/resume_scan_with_ai", methods=['POST'])
# def resume_scanner():
#     if 'image' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     uploaded_file_from_form = request.files['image']
#     if uploaded_file_from_form.filename == '':
#         return jsonify({"error": "No file selected"}), 400

#     # Save the file to the upload folder
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file_from_form.filename)
#     uploaded_file_from_form.save(file_path)

#     job_title = request.form.get('jobTitle')
#     tech_stack = request.form.get('techStack')

#     # Process the uploaded file here if needed
#     genai.configure(api_key="AIzaSyCC0ixjF5MwOyG_WTToz-VQR5oWdJoqggY")


#     # Set up the model configuration for text generation
#     generation_config = {
#         "temperature": 0.4,
#         "top_p": 1,
#         "top_k": 32,
#         "max_output_tokens": 4096,
#     }

#     # Define safety settings for content generation
#     safety_settings = [
#         {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
#         for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
#     ]


#     def generate_response_from_gemini(input_text):
#         # Create a GenerativeModel instance with 'gemini-pro' as the model type
#         llm = genai.GenerativeModel(
#             model_name="gemini-pro",
#             generation_config=generation_config,
#             safety_settings=safety_settings,
#         )
#         # Generate content based on the input text
#         output = llm.generate_content(input_text)
#         # Return the generated text
#         return output.text


#     def extract_text_from_pdf_file(uploaded_file):
#         # Use PdfReader to read the text content from a PDF file
#         pdf_reader = pdf.PdfReader(uploaded_file)
#         text_content = ""
#         for page in pdf_reader.pages:
#             text_content += str(page.extract_text())
#         return text_content


#     def extract_text_from_docx_file(uploaded_file):
#         # Use docx2txt to extract text from a DOCX file
#         return docx2txt.process(uploaded_file)

#     string_to_be_sent=" "

#     selected_candidates = []  

#     if uploaded_file_from_form.mimetype == "application/pdf":
#         with open(file_path, "rb") as pdf_file:
#             resume_text = extract_text_from_pdf_file(pdf_file)
#             print("Extracted PDF Text:", resume_text)  # Debugging statement
#     elif uploaded_file_from_form.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#         with open(file_path, "rb") as docx_file:
#             resume_text = extract_text_from_docx_file(docx_file)
#             print("Extracted DOCX Text:", resume_text)  # Debugging statement
    
#     response_text = generate_response_from_gemini(resume_text)

#     # Check if candidate meets minimum score criteria (not implemented)
#     match_percentage = 100  # Placeholder for match percentage

#     # Extract candidate name from anywhere within the resume text
#     candidate_name_match = re.search(r'(\b[A-Z][a-z]*\b\s+\b[A-Z][a-z]*\b)', resume_text)  # Find name pattern
#     candidate_name = candidate_name_match.group(0) if candidate_name_match else "Name not found"

#     # Extract candidate mobile number from anywhere within the resume text
#     candidate_mobile_match = re.search(r'(\b\d{10,12}\b|\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}\b)', resume_text)  # Find phone number pattern
#     candidate_mobile = candidate_mobile_match.group(0) if candidate_mobile_match else "Mobile number not found"

#     # Append candidate details to the list of selected candidates
#     selected_candidates.append((candidate_name, candidate_mobile))
#     for i, candidate_info in enumerate(selected_candidates, start=1):
#         string_to_be_sent+=f"S.No: {i}, Name: {candidate_info[0]}, Mobile Number: {candidate_info[1]}"+"]["  
#     # string_to_be_sent+=job_title+tech_stack 

    
#     new_job=JobSeekerResumeScore(job_position="lol",tech_stack="lol",name=candidate_name,phone_number=candidate_mobile)

#     try:
#         db.session.add(new_job)
#         db.session.commit()
#     except Exception as e:
#         return ({"message":str(e)},400)
    
#     return jsonify({"message": "File processed and saved successfully & Resume Score stored successfully","stringGotten":string_to_be_sent+job_title+tech_stack}), 200


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

    if uploaded_file_from_form:
        if not tech_stack.strip():
            return jsonify({"message":"Please provide the Job Description ⚠"})
        else:
            uploaded_file = uploaded_file_from_form
            if uploaded_file_from_form.mimetype == "application/pdf":
                with open(file_path, "rb") as pdf_file:
                    resume_text = extract_text_from_pdf_file(pdf_file)
                    print("Extracted PDF Text:", resume_text)  # Debugging statement
            elif uploaded_file_from_form.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                with open(file_path, "rb") as docx_file:
                    resume_text = extract_text_from_docx_file(docx_file)
                    print("Extracted DOCX Text:", resume_text)  # Debugging statement
            response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=tech_stack))

            # Extract Job Description Match percentage from the response
            match_percentage_str = response_text.split('"Job Description Match":"')[1].split('"')[0]

            if match_percentage_str == 'N/A':
                score=match_percentage_str+" Sorry yours Skills do not match with the requirements 😣"
                missing_keywords = response_text.split('"Missing Keywords":"')[1].split('"')[0]
                result=missing_keywords
            
            else:
            # Remove percentage symbol and convert to float
                match_percentage = float(match_percentage_str.rstrip('%'))
                score=match_percentage

                if match_percentage >= 70:
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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
