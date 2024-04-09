import React from 'react'

const ResumeScore = () => {
  return (
    <div className='mx-8 mt-16'>
        <div className='text-[2.5em] font-bold '>
            Your Resume Score is 90%
        </div>
        <div className='flex flex-col'>
            <h1 className='font-semibold'>Your GitHub Summary!</h1>
            <div className='flex'>
                <img className="mx-4" src="https://github-readme-stats.vercel.app/api/top-langs?username=Akkilesh-A&show_icons=true&locale=en&layout=compact&theme=chartreuse-light" alt="ovi" />
                <img src="https://myreadme.vercel.app/api/embed/Akkilesh-A?panels=userstatistics,toprepositories,toplanguages,commitgraph" alt="reimaginedreadme" />
            </div>
        </div>
        
    </div>
  )
}

export default ResumeScore