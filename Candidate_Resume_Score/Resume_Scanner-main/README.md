https://www.youtube.com/watch?v=7lP7fune0Gw&t=908s


app1.py --- Students code is there 

test--- sujal is working on new features on this file


for running the code first download the requirement (pip install -r requirements.txt) and google api key is required for that (https://aistudio.google.com/app/apikey) then to run the streamlit code you just have to use (streamlit run recruiter.py)

[Working of the Code is explained here in easy words-:]

1. Imports: At the beginning of the code, we import the necessary libraries and modules:
    - `Streamlit`: A Python library used for building interactive web applications.
    - `Google. generativeai`: A library for accessing Google's generative AI   models.
    - `os`: Provides functions for interacting with the operating system.
    - `docx2txt`: A module for extracting text from DOCX files.
    - `PyPDF2`: A library for working with PDF files.
    - `dotenv`: Loads environment variables from a `.env` file.

2. Environment Variables: We load environment variables, such as the Google API key, from a `.env` file.

3. Generative AI Model Configuration: We configure the generative AI model for text generation. This includes setting parameters like temperature, top_p, top_k, and max_output_tokens.

4. Safety Settings: We define safety settings for content generation to ensure that the generated content meets certain safety criteria.

5. Function Definitions:
    - `generate_response_from_gemini`: This function takes an input text and generates content using the generative AI model.
    - `extract_text_from_pdf_file`: This function extracts text from a PDF file.
    - `extract_text_from_docx_file`: This function extracts text from a DOCX file.

6. **Prompt Template**: We define a prompt template for generating text. This template includes placeholders for the resume text and job description.

7. **Streamlit App**:
    - We initialize the Streamlit app.
    - We create input fields for the job description and resume upload.
    - When the user clicks the submit button, we extract text from the uploaded resume file and generate a response using the generative AI model.
    - We extract the job description match percentage from the response and display it to the user.
    - We display the ATS evaluation result along with the match percentage, highlighting it in green for a good match and red for a poor match.

Overall, this code sets up a Streamlit web application that allows users to upload their resumes and a job description. It then evaluates the resume against the job description using a generative AI model and provides feedback on how well the resume matches the job description.


