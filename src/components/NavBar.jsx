import React from 'react'
import { Link } from 'react-router-dom'

const NavBar = () => {
  return (
    <div className='absolute top-0 left-0 right-0 z-10 my-4'>
        <div className='flex mx-8 justify-between items-center'>
            <div>
                <h1 className='font-extrabold'>Resume Copilot</h1>
            </div>
            <div>
                <ul className='flex font-semibold'>
                    <li className='mx-8'><Link to="/">Home</Link></li>
                    <li>|</li>
                    <li className='mx-8'><Link to="/resumescore">Resume Score</Link></li>
                    <li>|</li>
                    <li className='mx-8'>Jobs Post</li>
                    <li>|</li>
                    <li className='mx-8'>About</li>
                </ul>
            </div>
        </div>
        <hr className='mx-8 my-4' />
    </div>
  )
}

export default NavBar