import React,{useState,useEffect} from 'react'

const NonTechnicalBestResumes = () => {

    const [score,setScore]=useState([])

    useEffect(()=>{
        fetchScore()
    },[])

    
    async function fetchScore(){
        const url="http://localhost:5000/nontechnicalmultipleresumescore"
        const response=await fetch(url)
        const data=await response.json()
        setScore(data)
    }

  return (
    <div className='mt-24 mx-8'>
        <div className='flex flex-col justify-center items-center'>
            <h1 className='mx-8 text-[3rem] font-extrabold'>Best Non Technical Resumes!</h1>
        </div>
        <div className='flex flex-wrap items-center justify-center'>
        {score.map((job) => {
                    return (
                        <div className='flex-col mx-4 my-4 bg-gray-300  hover:fill-white hover:scale-110 duration-300 hover:duration-300 border-4 border-black p-4 rounded-xl flex justify-center items-center'>
                            <p>
                                <span className='font-bold'>Name:</span> {job.name}
                            </p>
                            <p>
                                <span className='font-bold'>Phone Number:</span> {job.phoneNumber=="P"? "Phone Number Not Found":job.phoneNumber}
                            </p>
                        </div>
                    )
                }
            )
        } 
        </div>
    </div>
  )
}

export default NonTechnicalBestResumes