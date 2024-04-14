import React,{useState,useEffect} from 'react'
import { useParams } from 'react-router-dom'

const Simple = () => {
    const [data,setData]=useState([])
    const [jobPositions,setJobPositions]=useState([])

    useEffect(()=>{
        fetchData()
    },[])

    const {jobTitle}=useParams();
    const jobDetailsArray=jobTitle.split("&")
   
    const fetchData=async()=>{
        const url="http://127.0.0.1:5000/resume_scanned?jobtitle="+jobDetailsArray[0]+"&techstack="+jobDetailsArray[1]
        const response=await fetch(url)
        const data=await response.json()
        setData(data)
        setJobPositions(data.jobPosition.split(","))
        alert(jobPositions)
    }

  return (
    <div className='mx-8 mt-24'>
        <h1 className='text-[2em] text-center'><span className='font-bold'>Job Position :</span> {data.jobPositionClicked}</h1>
        <h2 className='text-[2em] text-center'><span className='font-bold'>Required Tech Stack :</span> {data.techStackRequired}</h2>
        <table border>
          <tr>
            <th>Job Position</th>
            <th>Name</th>
            <th>Email</th>
            <th>Tech Stack</th>
          </tr>
          <tr>
            <td>{data.jobPosition}</td>
            <td>{data.name}</td>
            <td>{data.email}</td>
            <td>{data.techStack}</td>
          </tr>
        </table>
    </div>
  )
}

export default Simple