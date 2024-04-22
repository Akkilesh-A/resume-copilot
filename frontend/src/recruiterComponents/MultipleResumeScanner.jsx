import React, { useState } from 'react';

function MultipleResumeScanner() {
    const [images, setImages] = useState([]);
    const [jobTitle,setJobTitle]=useState("")
    const [techStack,setTechStack]=useState("")
    const [match,setMatch]=useState(0)

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
        formData.append('match',match)

        const url = "http://localhost:5000/recruiter_resume_scan"; // Ensure this matches your Flask route
        const options = {
            method: 'POST',
            body: formData
        };

        try {
            const response = await fetch(url, options);
            const data = await response.json();

            if (response.ok) {
                // alert(data.message);
                // alert(data.stringGotten);
                window.location.href="/bestresumes"
                
            } else {
                alert(data.error || 'Failed to process files');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Unable to connect with backend server');
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
                        <th className='p-4'>All Resumes!</th>
                        <td><input type='file' multiple name='file'className='border-2 border-black p-2 rounded w-[20vw]' onChange={handleImage} /></td>
                    </tr>
                    {/* <tr>
                        <th>Match Percentage Criteria</th>
                        <td className='flex items-center justify-center'>
                            <input className='border-2 border-black p-2 rounded w-[15vw]' min={0} max={100} step={1} type="range" name="match" id='match' value={match} onChange={(e) => setMatch(e.target.value)} />
                            <p className='ml-1'>{match}%</p>
                        </td>
                    </tr> */}
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
