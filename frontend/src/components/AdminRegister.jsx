import React,{useState} from 'react'

const AdminRegister = () => {
  const [userId, setUserId] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userId = document.getElementById('userId').value
    const password = document.getElementById('password').value
    const confirmPassword = document.getElementById('confirmPassword').value
    if(password!==confirmPassword){
      alert('Passwords do not match')
      return
    }
    if(!userId || !password){
      alert('Please fill all the fields')
      return
    }
    const data={
      userId:userId,
      password:password
    }
    const url="http://localhost:5000/admin_register"
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
      alert('Register Successful')
      setUserId('')
      setPassword('')
      window.location.href='/adminlogin'
  }
  }

  return (
    <div className='mx-4 mt-24'>
      <div className='flex justify-center items-center mb-12'>
        <h1 className='text-[2.5em] font-extrabold'>Admin Register</h1>
      </div>
      <form onSubmit={handleSubmit} >
        <div className='flex justify-around items-center mb-12'> 
            <table className='text-left'>
                <tr>
                  <th className='p-4'>User Id</th>
                  <td><input className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="userId" id='userId' value={userId} onChange={(e) => setUserId(e.target.value)} placeholder='User ID'  /></td>
                </tr>
                <tr>
                  <th className='p-4'>Password</th>
                  <td><input type='password' className='border-2 border-black p-2 rounded w-[20vw]' name="password" id='password' placeholder='Password' value={password} onChange={(e) => setPassword(e.target.value)} /></td>
                </tr>
                <tr>
                  <th className='p-4'>Confirm Password</th>
                  <td><input type='password' className='border-2 border-black p-2 rounded w-[20vw]' name="confirmPassword" id='confirmPassword' placeholder='Confirm password' value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)}/></td>
                </tr>
            </table>        
        </div>
        <div className='text-center flex justify-center '>
            <button type="submit" className='hover:bg-black hover:fill-white  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold'>
              <h1 className='px-4 text-xl'>Register</h1> 
            </button> 
        </div>
      </form>
    </div>
  )
}

export default AdminRegister