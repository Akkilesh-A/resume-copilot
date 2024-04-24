import React,{useState,useEffect} from 'react'

const BestResumes = () => {

    const [score,setScore]=useState([])

    useEffect(()=>{
        fetchScore()
    },[])

    
    async function fetchScore(){
        const url="http://localhost:5000/multipleresumescore"
        const response=await fetch(url)
        const data=await response.json()
        setScore(data)
    }

  return (
    <div className='mt-24 mx-8'>
        <div className='flex flex-col justify-center items-center'>
            <h1 className='mx-8 text-[3rem] font-extrabold'>Best Tehnical Resumes!</h1>
            {/* <div className='mb-4 flex '>
                <h1 className='mx-4 text-[2em]'>
                    <span className='font-bold'>Job Position:</span> {score[0].jobPosition}
                </h1>
                <p className='text-[2em]'>
                    <span className='font-bold '>Tech Stack Required:</span> {score[0].techStack}
                </p>
            </div> */}
        </div>
        <div className='flex flex-wrap items-center'>
        {score.map((job) => {
                    return (
                        <div className='flex-col mx-4 my-4 bg-gray-300  hover:fill-white hover:scale-110 duration-300 hover:duration-300 border-4 border-black p-4 rounded-xl flex justify-center items-center'>
                            <p>
                                <span className='font-bold'>Name:</span> {job.name}
                            </p>
                            <p>
                                <span className='font-bold'>Phone Number:</span> {job.phoneNumber=="P"? "Phone Number Not Found":job.phoneNumber}
                            </p>
                            <p>
                                <span className='font-bold'>GitHub Username:</span> {job.githubUsername}
                            </p>
                            <div className='text-center my-4' >
                                GitHub top languages
                                <img className="mx-4" src={"https://github-readme-stats.vercel.app/api/top-langs?username="+job.githubUsername+"&show_icons=true&locale=en&layout=compact&theme=chartreuse-light"} alt="ovi" />
                            </div>
                            <div className='text-center my-4' >
                                Longest streak stats
                                <img src={"https://github-readme-streak-stats.herokuapp.com/?user="+job.githubUsername+"&theme=tokyonight"} alt="mystreak"/>
                            </div>
                        </div>
                    )
                }
            )
        } 
        </div>
    </div>
  )
}

export default BestResumes