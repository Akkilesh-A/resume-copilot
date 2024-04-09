import React from 'react';
import FileUpload from '../FileUpload';
import { Link } from 'react-router-dom'

function ResumeScoreForm() {
  return (
    <div className='mt-24 mx-8'>
      <div className='flex justify-center items-center mb-12'>
        <h1 className='text-[2.5em] font-extrabold'>Create a Job Post</h1>
      </div>
      <div className='flex justify-around items-center mb-12'>
        <form>
          <table className='text-left'>
              <tr>
                <th className='p-4'>Job Position</th>
                <td><input className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="jobPosition" placeholder="" /></td>
              </tr>
              <tr>
                <th className='p-4'>GitHub Profile</th>
                <td><textarea rows="5" className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="githubURL" placeholder='Enter Tech Stacks each seperated by a comma' /></td>
              </tr>
          </table>
        </form>        
      </div>
      <div className='text-center flex justify-center '>
        <Link to='/resumescore'>
          <button className='hover:bg-black hover:fill-white  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold'>
            <h1 className='pr-4 text-xl'>Post</h1> 
            <svg xmlns="http://www.w3.org/2000/svg" height="20" width="17.5" viewBox="0 0 448 512"><path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"/></svg>          </button> 
        </Link>
          
      </div>
      
    </div>
  );
}

export default ResumeScoreForm;

