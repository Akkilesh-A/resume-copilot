import React,{useState} from 'react'
import {Link} from 'react-router-dom'

function AdminJobsList({jobs,updateCallback, onUpdate}){
    const [jobClicked,setJobClicked]=useState("")

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

    async function handleSubmit(){
        e.preventDefault();
        const data={
            jobTitle:jobClicked,
        }
        alert("submit done")
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
                    <Link to={"/resumescanned/"+job.jobTitle+"&"+job.techStack} >
                        <div className='mx-4'>
                            <form onSubmit={handleSubmit}>
                                <div className=' my-4 h-[5vh]'>
                                    <div className='flex-col bg-gray-300  hover:fill-white hover:scale-110 duration-300 hover:duration-300 border-4 border-black p-4 rounded-xl flex justify-center items-center'>
                                        <h1 className='mx-4 text-[1em] font-bold '>
                                            {job.jobTitle}
                                        </h1>
                                        <p>
                                            {job.techStack}
                                        </p>
                                        <div>
                                            <button onClick={()=> onDelete(job.id)} className='border-2 text-black text-xs rounded px-2 mt-2 mx-2 bg-white hover:bg-gray-200'>
                                                Delete
                                            </button>
                                            <button onClick={()=> onUpdate(job.id)} className='border-2 text-black text-xs rounded px-2 mt-2 bg-white hover:bg-gray-200'>
                                                Update
                                            </button>
                                        </div>
                                        <button className='border-2 text-black text-xs rounded px-2 mt-2 mx-2 bg-white hover:bg-gray-200' type="submit">Resumes</button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </Link>
                    )
                }
            )
        }   
    </div>
  )
}

export default AdminJobsList