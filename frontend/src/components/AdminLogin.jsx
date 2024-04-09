import React from 'react'

const AdminLogin = () => {
  return (
    <div className='mt-24 mx-8'>
      <div className='flex justify-center items-center mb-12'>
        <h1 className='text-[2.5em] font-extrabold'>Admin Login</h1>
      </div>
      <form >
        <div className='flex justify-around items-center mb-12'> 
            <table className='text-left'>
                <tr>
                  <th className='p-4'>User Id</th>
                  <td><input className='border-2 border-black p-2 rounded w-[20vw]' type="text" name="userId" id='userId' placeholder='User ID'  /></td>
                </tr>
                <tr>
                  <th className='p-4'>Paswword</th>
                  <td><input type='password' className='border-2 border-black p-2 rounded w-[20vw]' name="password" id='password' placeholder='password' /></td>
                </tr>
            </table>        
        </div>
        <div className='text-center flex justify-center '>
            <button type="submit" className='hover:bg-black hover:fill-white  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold'>
              <h1 className='px-4 text-xl'>Login</h1> 
            </button> 
        </div>
      </form>  
      
    </div>
  )
}

export default AdminLogin