import React from 'react'
import { Link } from 'react-router-dom'

const Jobs = () => {
  return (
    <div className='mt-24 mx-8'>
        <h1 className='text-[2.5em] font-bold text-center'>Jobs</h1>
        <div className='flex items-center flex-wrap'>
            <div className='my-4 mx-4'>
              <Link to="/resumescoreform">
                <button className='w-[20vw] h-[5vh]'>
                    <div className='hover:bg-white hover:fill-black hover:text-black text-white border-4 border-black bg-black p-4 rounded-xl flex justify-center items-center'> 
                        <h1 className='mx-4 text-[1em] font-bold'>
                            Software Engineer
                        </h1>
                    </div>  
                </button>
                </Link>  
            </div>
            <div className='my-4 mx-4'>
              <Link to="/resumescoreform">
                <button className='w-[20vw] h-[5vh]'>
                    <div className='hover:bg-black   hover:fill-white hover:text-white border-4 border-black p-4 rounded-xl flex justify-center items-center'>
                        <h1 className='mx-4 text-[1em] font-bold '>
                            Cloud Engineer
                        </h1>
                    </div>
                </button>
                </Link>  
            </div>    
        </div>
    </div>
  )
}

export default Jobs
