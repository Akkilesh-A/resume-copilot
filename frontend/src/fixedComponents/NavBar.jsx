import React from 'react'
import { Link } from 'react-router-dom'

const NavBar = () => {
  return (
    <div className='absolute top-0 left-0 right-0 z-10 my-4'>
        <div className='flex mx-8 justify-between items-center'>
            <Link to="/">
                <div className='flex items-center'>
                    <img src="/favicon-32x32.png" alt="Logo" width="40px"/>
                    <h1 className='ml-3 font-extrabold'>Resume Copilot</h1>
                </div>
            </Link>
            <div>
                <ul className='flex font-semibold'>
                    <li className='mx-8'><Link to="/">Home 🏠</Link></li>
                    <li>|</li>
                    <li className='mx-8'><Link to="/resumescoreform">Resume Score 🚀</Link></li>
                    <li>|</li>
                    <li className='mx-8'><Link to="/postajob">Post a Job 📝</Link></li>
                    <li>|</li>
                    <li className='mx-8'>About 🤩</li>
                </ul>
            </div>
        </div>
        <hr className='mx-8 my-4' />
    </div>
  )
}

export default NavBar