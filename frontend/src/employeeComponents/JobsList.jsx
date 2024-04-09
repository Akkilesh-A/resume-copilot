import React from 'react'

function AdminJobsList({jobs}){
    return (
    <div className='flex'>
        {jobs.map((job) => {
                    return (
                        <div className='mx-4'>
                            <button className=' my-4 h-[5vh]'>
                                <div className='flex-col bg-gray-300  hover:fill-white hover:scale-110 duration-300 hover:duration-300 border-4 border-black p-4 rounded-xl flex justify-center items-center'>
                                    <h1 className='mx-4 text-[1em] font-bold '>
                                        {job.jobTitle}
                                    </h1>
                                    <p>
                                        {job.techStack}
                                    </p>
                                </div>
                            </button>
                        </div>
                    )
                }
            )
        }   
    </div>
  )
}

export default AdminJobsList