import React,{useState,useEffect} from 'react'

const ResumeScore = () => {

    const [score,setScore]=useState([])

    useEffect(()=>{
        fetchScore()
    },[])

    
    const fetchScore=async()=>{
        const url="http://localhost:5000/resumescore"
        const response=await fetch(url)
        const data=await response.json()
        setScore(data)
    }

  return (
    <div>
        <h1 className='mt-24 mx-8'>Resume Score!</h1>
        {score.map((job) => {
                    return (
                        <div className='mx-4'>
                            <div className='my-4 h-[5vh] flex flex-col items-center'>
                                <div className='flex-col bg-gray-300  hover:fill-white hover:scale-110 duration-300 hover:duration-300 border-4 border-black p-4 rounded-xl flex justify-center items-center'>
                                    <h1 className='mx-4 text-[1em] font-semibold '>
                                        <span className='font-bold'>Job Position:</span> {job.jobPosition}
                                    </h1>
                                    <p>
                                        <span className='font-bold'>Tech Stack Required:</span> {job.techStack}
                                    </p>
                                    <p>
                                        <span className='font-bold'>Name:</span> {job.name}
                                        <span className='font-bold'>Phone Number:</span> {job.phoneNumber}
                                    </p>
                                </div>
                            </div>
                        </div>
                    )
                }
            )
        }  
    </div>
  )
}

export default ResumeScore