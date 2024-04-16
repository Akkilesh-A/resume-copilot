import React,{useState,useEffect} from 'react'
import { useParams } from 'react-router-dom'

const ResumeScore = () => {
    const {gitHubDetails}=useParams();
    console.log(gitHubDetails)
    const gitHubDetailsArray = gitHubDetails ? gitHubDetails.split("&") : [];
    const github_user=gitHubDetailsArray[0]
    const user_name=gitHubDetailsArray[1]
    const git_hub_user_name_1 = "https://myreadme.vercel.app/api/embed/"+github_user+"?panels=userstatistics,toprepositories,toplanguages,commitgraph"
    const git_hub_user_name_2 ="https://github-readme-stats.vercel.app/api/top-langs?username="+github_user+"&show_icons=true&locale=en&layout=compact&theme=chartreuse-light"
  return (
    <div className='mx-8 mt-16'>
        <div className='text-[2.5em] font-bold '>
            Your GitHub Stats
        </div>
        <div className='flex flex-col'>
            <h2 className='text-[1.5em]'>Hello! {user_name}</h2>
            <div className='flex'>
                <img className="mx-4" src={git_hub_user_name_2} alt="ovi" />
                <img src={git_hub_user_name_1} alt="reimaginedreadme" />
            </div>
        </div>
        
    </div>
  )
}

export default ResumeScore