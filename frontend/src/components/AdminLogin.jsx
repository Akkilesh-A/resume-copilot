import React,{useState} from 'react'
import {Link} from 'react-router-dom'

const AdminLogin = () => {
  const [userId, setUserId] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data={
      userId:userId,
      password:password
    }
    const url="http://localhost:5000/admin_login"
    const options={
      method:"POST",
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
        alert('Login Successful')
        setUserId('')
        setPassword('')
        window.location.href='/adminjobsportal'
    }
  }

  return (
    <div className='mt-24 mx-8'>
      <div className='flex justify-center items-center mb-12'>
        <h1 className='text-[2.5em] font-extrabold'>Admin Login</h1>
      </div>
      <form onSubmit={handleSubmit}>
        <div className='flex justify-around items-center mb-12'> 
            <table className='text-left'>
                <tr>
                  <th className='p-4'>User Id</th>
                  <td><input className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="userId" id='userId' placeholder='User ID' value={userId} onChange={(e)=>setUserId(e.target.value)} /></td>
                </tr>
                <tr>
                  <th className='p-4'>Paswword</th>
                  <td><input type='password' className='border-2 border-black p-2 rounded w-[20vw]' name="password" id='password' placeholder='password' value={password} onChange={(e)=>setPassword(e.target.value)}/></td>
                </tr>
            </table>        
        </div>
        <div className='text-center flex justify-center '>
            <button type="submit" className='hover:bg-black hover:fill-white  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold'>
              <h1 className='px-4 text-xl'>Login</h1> 
            </button> 
        </div>
      </form>  
      <div className='flex justify-center mt-16'>
        <Link to='/adminregister'>
          <button className='mx-4 hover:bg-black hover:fill-white  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 underline font-bold'>
            <h1 className='px-4 text-s'>Register</h1> 
          </button> 
        </Link>        
      </div>      
    </div>
  )
}

export default AdminLogin