import React, { useEffect,useState } from 'react'
import JobsList from './JobsList'
import { Link } from 'react-router-dom'

const JobsPortal = () => {
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
        <div className='flex m-auto justify-center items-center '>
            <h1 className='text-[2.5em] font-bold text-center'>Job Openings</h1>
            <div className='w-[50vw] text-center flex justify-end '>
                <a target="_self" href="https://get-your-resume-score.streamlit.app/">
                    <button className='hover:bg-black hover:fill-white  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold'>
                    <h1 className='text-xl'>Get Your Resume Score 🚀</h1> 
                    </button> 
                </a>
            </div>
        </div>
        <div className='h-[50vh]'>
            <JobsList jobs={jobs} updateCallback={refreshJobsPortal}/>
        </div>       
    </div>

  )
}

export default JobsPortal
