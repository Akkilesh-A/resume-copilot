import React,{useState} from 'react';

function PostAJob(updateCallback) {
  const [jobTitle, setJobTitle] = useState('');
  const [techStack, setTechStack] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data={
      jobTitle:jobTitle,
      techStack:techStack
    }
    const url="http://localhost:5000/create_job"
    const options={
      method:'POST',
      headers:{
        'Content-Type':'application/json'
      },
      body:JSON.stringify(data)
    }
    const response=await fetch(url,options)
    if(response.status!==201 && response.status!==200){
        const data=await response.json()
        alert(data.message)
    }
    else{
        alert('Job Posted Successfully')
        setJobTitle('')
        setTechStack('')
        window.location.href='/adminjobsportal'
        updateCallback()
    }
  }

  return (
    <div className='mt-24 mx-8'>
      <div className='flex justify-center items-center mb-12'>
        <h1 className='text-[2.5em] font-extrabold'>Create a Job Post</h1>
      </div>
      <form onSubmit={handleSubmit}>
        <div className='flex justify-around items-center mb-12'> 
            <table className='text-left'>
                <tr>
                  <th className='p-4'>Job Position</th>
                  <td><input className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="jobTitle" id='jobTitle' value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} /></td>
                </tr>
                <tr>
                  <th className='p-4'>Tech Stacks</th>
                  <td><textarea rows="5" className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="techStack" id='techStack' value={techStack} onChange={(e) => setTechStack(e.target.value)} placeholder='Enter Tech Stacks each seperated by a comma' /></td>
                </tr>
            </table>        
        </div>
        <div className='text-center flex justify-center '>
            <button type="submit" className='hover:bg-black hover:fill-white  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold'>
              <h1 className='pr-4 text-xl'>Post</h1> 
              <svg xmlns="http://www.w3.org/2000/svg" height="20" width="17.5" viewBox="0 0 448 512"><path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"/></svg>          
            </button> 
        </div>
      </form>  
      
    </div>
  );
}

export default PostAJob;

