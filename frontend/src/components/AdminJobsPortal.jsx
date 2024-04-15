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
                    {/* <svg xmlns="http://www.w3.org/2000/svg" height="20" width="17.5" viewBox="0 0 448 512"><path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"/></svg>           */}
                    </button> 
                </Link>
            </div>
            <div className='text-center flex justify-center '>
                <Link to="/resumescannerform">
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
