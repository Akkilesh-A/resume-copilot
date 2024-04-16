import React,{useState} from 'react';
import { Link } from 'react-router-dom'

function ResumeScoreForm() {
  const [github,setGitHub]=useState("")
  const [name,setName]=useState(" ")

  return (
    <div className='mt-24 mx-8'>
      <div className='flex justify-center items-center mb-12'>
        <h1 className='text-[2.5em] font-extrabold'>Get your Resume Score here!</h1>
      </div>
      <form>
      <div className='flex justify-around items-center '>
        
          <table className='text-left'>
              <tr>
                <th className='p-4'>Name</th>
                <td><input className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="name" placeholder='Your Full Name' value={name} onChange={(e)=>setName(e.target.value)} /></td>
              </tr>
              <tr>
                <th className='p-4'>GitHub Profile</th>
                <td><input className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="githubURL" placeholder='GitHub Profile URL' value={github} onChange={(e)=>setGitHub(e.target.value)}  /></td>
              </tr>
          </table>
              
      </div>
      <div className='text-center flex justify-center pt-8'>
        <Link to={"/githubstats/"+github+"&"+name}>
          <button className='hover:bg-black hover:fill-white  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold'>
            <h1 className='pr-4 text-xl'>Upload</h1> 
            <svg class="hover:fill-white" xmlns="http://www.w3.org/2000/svg" height="32" width="24" viewBox="0 0 384 512">
              <path d="M64 0C28.7 0 0 28.7 0 64V448c0 35.3 28.7 64 64 64H320c35.3 0 64-28.7 64-64V160H256c-17.7 0-32-14.3-32-32V0H64zM256 0V128H384L256 0zM216 408c0 13.3-10.7 24-24 24s-24-10.7-24-24V305.9l-31 31c-9.4 9.4-24.6 9.4-33.9 0s-9.4-24.6 0-33.9l72-72c9.4-9.4 24.6-9.4 33.9 0l72 72c9.4 9.4 9.4 24.6 0 33.9s-24.6 9.4-33.9 0l-31-31V408z"/>
            </svg>   
          </button> 
        </Link>
          
      </div>
      </form>
      
    </div>
  );
}

export default ResumeScoreForm;
