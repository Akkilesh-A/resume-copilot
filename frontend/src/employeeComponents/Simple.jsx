import React,{useState,useEffect} from 'react'

const Simple = () => {
    const [data,setData]=useState([])

    useEffect(()=>{
        fetchData()
    },[])
   
    const fetchData=async()=>{
        const url="http://127.0.0.1:5000/resume_scan"
        const response=await fetch(url)
        const data=await response.json()
        setData(data)
    }
  return (
    <div className='mx-8 mt-24'>
        <h1>Simple Component</h1>
        <p>{data.message}</p>
    </div>
  )
}

export default Simple