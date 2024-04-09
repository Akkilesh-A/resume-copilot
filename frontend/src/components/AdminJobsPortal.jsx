import React, { useEffect,useState } from 'react'
import AdminJobsList from './AdminJobsList'

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
    <div className='mt-24 mx-8'>
        <h1 className='text-[2.5em] font-bold text-center'>Manage Job Openings</h1>
        <AdminJobsList jobs={jobs} updateCallback={refreshJobsPortal}/>
    </div>
  )
}

export default AdminJobsPortal
