import React, { useEffect,useState } from 'react'
import AdminJobsList from './AdminJobsList'
import { Link } from 'react-router-dom'

const AdminJobsPortal = () => {
    const [jobs,setJobs]=useState([])

    useEffect(()=>{
        fetchJobs()
    },[])

    const refreshJobsPortal=()=>{
        fetchJobs()
    }
    
    const fetchJobs=async()=>{
        const url="http://localhost:5000/jobs"
        const response=await fetch(url)
        const data=await response.json()
        setJobs(data)
    }

  return (
    <div className='mt-24 mx-8 flex flex-col'>
        <h1 className='text-[2.5em] font-bold text-center'>Manage Job Openings</h1>
        <div className='h-[50vh]'>
           <AdminJobsList jobs={jobs} updateCallback={refreshJobsPortal}/> 
        </div>
        
        <div className='flex justify-center'>
            <div className='text-center flex justify-center '>
                <Link to="/postajob">
                    <button className='hover:bg-black hover:fill-white mx-4 hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold'>
                        <h1 className='text-xl'>Post a New Job ➕</h1> 
                    </button> 
                </Link>
            </div>
            <div className='text-center flex justify-center '>
                {/* <a href="https://recruiter-resume-scanner.streamlit.app/"> */}
                <Link to="/multipleresumescanner">
                    <button className='hover:bg-black hover:fill-white mx-4  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold'>
                    <h1 className='text-xl'>Check Resumes ✅</h1> 
                    </button> 
                </Link>
            </div>
        </div>
    </div>
  )
}

export default AdminJobsPortal
