import React, { useState } from 'react';

function MultipleResumeScanner() {
    const [images, setImages] = useState([]);
    const [jobTitle,setJobTitle]=useState("")
    const [techStack,setTechStack]=useState("")

    function handleImage(e) {
        const files = Array.from(e.target.files); // Convert FileList to array
        console.log(files)
        setImages(files);
    }

    async function handleApi() {
        const formData = new FormData();
        images.forEach((file, index) => {
            formData.append(`image_${index}`, file); // Append each file with a unique key
        });
        formData.append('jobTitle', jobTitle);
        formData.append('techStack', techStack);
        formData.append('noOfResumes',images.length)

        const url = "http://localhost:5000/recruiter_resume_scan"; // Ensure this matches your Flask route
        const options = {
            method: 'POST',
            body: formData
        };

        try {
            const response = await fetch(url, options);
            const data = await response.json();

            if (response.ok) {
                alert('Files processed successfully');
                alert(data.message);
                alert(data.stringGotten)
            } else {
                alert(data.error || 'Failed to process files');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing the files');
        }
    }

    return (
        <div className='mt-24 mx-8'>
            <div className='flex justify-center items-center mb-12'>
                <h1 className='text-[2.5em] font-extrabold'>🧑🏻‍🏫 Get the Best Candidates here! 👩🏻‍🏫</h1>
            </div>
            <div className='flex flex-col justify-around items-center mb-12'> 
                <table className='text-center'>
                    <tr>
                    <th className='p-4'>Job Position</th>
                    <td><input className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="jobTitle" id='jobTitle' value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} /></td>
                    </tr>
                    <tr>
                    <th className='p-4'>Tech Stacks</th>
                    <td><textarea rows="5" className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="techStack" id='techStack' value={techStack} onChange={(e) => setTechStack(e.target.value)} placeholder='Enter Tech Stacks each seperated by a comma' /></td>
                    </tr>
                    <tr>
                        <th className='p-4'>Resume</th>
                        <td><input type='file' multiple name='file'className='border-2 border-black p-2 rounded w-[20vw]' onChange={handleImage} /></td>
                    </tr>
                </table> 
                <div className='flex justify-center' colSpan={2}>
                    <button onClick={handleApi} className='mt-4 hover:bg-black hover:fill-white  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold' >
                        Upload ⬆️ & Process 🤖
                    </button>
                </div>       
            </div>   
        </div>        
    );
}

export default MultipleResumeScanner;
