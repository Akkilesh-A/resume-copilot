import React,{useState} from 'react'
import {Link} from 'react-router-dom'
import {CopyToClipboard} from 'react-copy-to-clipboard';

function AdminJobsList({jobs,updateCallback, onUpdate}){
    const [jobClicked,setJobClicked]=useState("")
    const [copied,setCopied]=useState(false)

    function handleClick(){
        setCopied(true)
        alert("Text Copied!")    
    }

    const onDelete=async(id)=>{
        try{
            const options={
                method:'DELETE',
            }
            const response = await fetch('http://localhost:5000/delete_job/'+id,options)
            if(response.status ===200){
                updateCallback()
            }else{
                console.error("Failed to delete Job Posting")
            }
        }
        catch(error){
            alert(error)
        }
    }

    function handleJobClicked(value){
        setJobClicked(value)
    }

    async function handleSubmit(e){
        e.preventDefault();
        const data={
            jobTitle:jobClicked,
        }
        const url="http://localhost:5000/resume_scanned"
        const options={
            method:"POST",
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify(data)
        }
        const response=await fetch(url,options)
        if(response.status!==201 && response.status!==200){
            const data=await response.json()
            alert(data.message)
        }
        else{
            alert(data.message)
            window.location.href='/resumescanned'
        }
    }

  return (
    <div className='flex'>
        {jobs.map((job) => {
                    return (
                    
                        <div className='mx-4'>
                            <form onSubmit={handleSubmit}>
                                <div className=' my-4 h-[5vh] flex flex-col items-center'>
                                    <div className='flex-col bg-gray-300  hover:fill-white hover:scale-110 duration-300 hover:duration-300 border-4 border-black p-4 rounded-xl flex justify-center items-center'>
                                        <h1 className='mx-4 text-[1em] font-bold '>
                                            {job.jobTitle}
                                        </h1>
                                        <p>
                                            {job.techStack}
                                        </p>
                                        <div className='flex flex-wrap mt-4'>
                                            <button onClick={()=> onDelete(job.id)} className='hover:bg-black hover:fill-white hover:text-white flex justify-center items-center mr-2 rounded px-2 p-1 border-2 border-black font-semibold text-xs'>
                                                Delete
                                            </button>
                                            <button className='hover:bg-black hover:fill-white hover:text-white flex justify-center items-center mr-2 rounded px-2 p-1 border-2 border-black font-semibold text-xs'>
                                                Update
                                            </button>
                                            <Link to={"/resumescanned/"+job.jobTitle+"&"+job.techStack} >
                                                <button className='hover:bg-black hover:fill-white hover:text-white flex justify-center items-center rounded px-2 p-1 border-2 border-black font-semibold text-xs' type="submit">Resumes</button>
                                            </Link>
                                        </div>
                                        
                                    </div>
                                    <CopyToClipboard className="mt-4 w-[60%] border-4 border-black p-2 rounded-xl text-xs hover:bg-black hover:text-white" text={job.techStack} onCopy={handleClick}><button className=' '>Copy Tech Stack</button></CopyToClipboard>
                                </div>
                            </form>
                        </div>
                    
                    )
                }
            )
        }   
    </div>
  )
}

export default AdminJobsList