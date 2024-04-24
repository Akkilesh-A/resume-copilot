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
    <div className='mt-24 mx-8'>
        <h1 className='text-[3rem] font-bold text-center' > Your Resume Score!</h1>
        <div className='flex justify-center '>
        {
            score.length > 0 && (
                <div className='mx-4 w-[40vw]'>
                    <div className='my-4 h-[5vh] flex flex-col items-center'>
                        <div className='flex-col bg-gray-300 hover:fill-white hover:scale-110 duration-300 hover:duration-300 border-4 border-black p-4 rounded-xl flex justify-center items-center'>
                            <h1 className='mx-4 text-[1em] font-semibold '>
                                <span className='font-bold'>Job Position:</span> {score[score.length - 1].jobPosition}
                            </h1>
                            <p>
                                <span className='font-bold'>Tech Stack Required:</span> {score[score.length - 1].techStack}
                            </p>
                            <div className='flex flex-col justify-center items-center'>
                                <p><span className='font-bold'>Score: </span> {score[score.length - 1].name}</p>
                                <p><span className='font-bold'>Result: </span> {score[score.length - 1].phoneNumber}</p>
                            </div>
                        </div>
                    </div>
                </div>
            )
        }
        </div>
    </div>
  )
}

export default ResumeScore