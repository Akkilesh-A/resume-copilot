import React from 'react'
import NavBar from '../fixedComponents/NavBar'
import Footer from '../fixedComponents/Footer'
import { Link } from 'react-router-dom'

const Options = () => {
  return (
    <div>
        <NavBar />
        <div className='mx-8 flex items-center justify-around h-[100vh]'>
            <Link to="/technical">
                <button className='w-[30vw]'>
                    <div className='bg-black p-4 rounded-xl flex justify-center items-center'>
                        <h1 className='mx-4 text-[1.5em] font-semibold text-white'>
                            Technical Jobs
                        </h1>
                    </div>  
                </button>
            </Link>
            <Link to="/nontechnical">
                <button className='w-[30vw]'>
                    <div className='border-4 border-black p-4 rounded-xl flex justify-center items-center'>
                        <h1 className='mx-4 text-[1.5em] font-bold '>
                            Non Technical Jobs
                        </h1>
                    </div>
                </button>
            </Link>
        </div>
        <Footer />
    </div>
  )
}

export default Options