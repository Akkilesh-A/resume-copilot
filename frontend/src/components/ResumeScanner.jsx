import React, { useState } from 'react'

const ResumeScanner = () => {

    const [jobTitle,setJobTitle]=useState("")
    const [techStack,setTechStack]=useState("")
    const [files,setFiles]=useState([])


    async function handleSubmit(e){
        e.preventDefault();
        const data={
            jobTitle:jobTitle,
            techStack:techStack,
            file:files
        }
        const url="http://localhost:5000/resume_scanner_with_ai"
        const options={
            method:'POST',
            headers:{'Content-Type': 'multipart/form-data'},
            body:files
        }
        const response=await fetch(url,options)
        if(response.status!==201 && response.status!==200){
            const data=await response.json()
            alert(data.message)
        }
        else{
            alert('Files Processed Successfully')
            const data=await response.json()
            alert(data.message)
            alert(data.message2)
            setJobTitle('')
            setTechStack('')
            setFiles([])
        }
    }

  return (
    <div className='mt-24 mx-8'>
      <div className='flex justify-center items-center mb-12'>
        <h1 className='text-[2.5em] font-extrabold'>🧑🏻‍🏫 Scan Resumes 👩🏻‍🏫</h1>
      </div>
      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <div className='flex justify-around items-center mb-12'> 
            <table className='text-left'>
                <tr>
                  <th className='p-4'>Job Position</th>
                  <td><input className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="jobTitle" id='jobTitle' value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} /></td>
                </tr>
                <tr>
                  <th className='p-4'>Tech Stacks</th>
                  <td><textarea rows="5" className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="techStack" id='techStack' value={techStack} onChange={(e) => setTechStack(e.target.value)} placeholder='Enter Tech Stacks each seperated by a comma' /></td>
                </tr>
                <tr>
                    <th className='p-4'>Tech Stacks</th>
                    <td><input type="file" className=' border-2 border-black p-2 rounded w-[20vw]' name="file" id='files' onChange={(e) => {const [file] = e.target.files; setFiles((files) => [...files, file]);}} />
                      </td>
                </tr>
            </table>        
        </div>
        <div className='text-center flex justify-center '>
            <button type="submit" className='hover:bg-black hover:fill-white  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold'>
              <h1 className='text-xl'>Upload ⬆️ & Process 🤖</h1> 
            </button> 
        </div>
      </form>       
    </div>
  )
}

export default ResumeScanner