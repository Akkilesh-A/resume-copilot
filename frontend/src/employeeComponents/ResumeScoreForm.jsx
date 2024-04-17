import React,{useState} from 'react';
import { Link } from 'react-router-dom'

function ResumeScoreForm() {
  const [github,setGitHub]=useState("")
  const [name,setName]=useState(" ")

  return (
    <div className='mt-24 mx-8'>
      <div className='flex justify-center items-center mb-12'>
        <h1 className='text-[2.5em] font-extrabold'>Get your GitHub Stats here! 🛫</h1>
      </div>
      <form>
      <div className='flex justify-around items-center '>
        
          <table className='text-left'>
              <tr>
                <th className='p-4'>Name</th>
                <td><input className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="name" placeholder='Your Full Name' value={name} onChange={(e)=>setName(e.target.value)} /></td>
              </tr>
              <tr>
                <th className='p-4'>GitHub Username</th>
                <td><input className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="githubURL" placeholder='GitHub Profile URL' value={github} onChange={(e)=>setGitHub(e.target.value)}  /></td>
              </tr>
          </table>
              
      </div>
      <div className='text-center flex justify-center pt-8'>
        <Link to={"/githubstats/"+github+"&"+name}>
          <button className='hover:bg-black hover:fill-white  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold'>
            <h1 className='text-xl'>Fetch 🤖 </h1> 
          </button> 
        </Link>
          
      </div>
      </form>
      
    </div>
  );
}

export default ResumeScoreForm;
