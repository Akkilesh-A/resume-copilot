import React,{useState,useEffect} from 'react'
import { useParams } from 'react-router-dom'

const GitHubScore = () => {
    const {gitHubDetails}=useParams();
    console.log(gitHubDetails)
    const gitHubDetailsArray = gitHubDetails ? gitHubDetails.split("&") : [];
    const github_user=gitHubDetailsArray[0]
    const user_name=gitHubDetailsArray[1]

  return (
    <div className='mx-8 mt-24'>
        <div className=' text-center text-[2.5em] font-bold '>
            Your GitHub Stats
        </div>
        <h2 className='text-[2em] text-center mb-8'>Hello! {user_name}</h2>
        <div className='justify-center flex flex-col items-center'>
            <div className='flex flex-wrap justify-center mb-24'>
                <div className='flex flex-col justify-center items-center mb-8'>
                    <img src={"https://myreadme.vercel.app/api/embed/"+github_user+"?panels=userstatistics,toprepositories,toplanguages,commitgraph"} alt="reimaginedreadme" />
                    <p className="mt-4 font-bold">GitHub All Stats</p>
                </div>
                <div className='flex flex-col justify-center items-center mb-8 mr-24'>
                    <img src={"https://github-readme-streak-stats.herokuapp.com/?user="+github_user+"&theme=tokyonight"} alt="mystreak"/>
                    <p className="mt-4 font-bold">Longest streak stats</p>
                </div>
                <div className='flex flex-col justify-center items-center mb-8'>
                    <img className="mx-4" src={"https://github-readme-stats.vercel.app/api/top-langs?username="+github_user+"&show_icons=true&locale=en&layout=compact&theme=chartreuse-light"} alt="ovi" />
                    <p className="mt-4 font-bold">GitHub top languages</p>
                </div>
            </div>
        </div>
        <div className='justify-center flex flex-col'>
            <div className='flex'>
                
            </div>
        </div>        
    </div>
  )
}

export default GitHubScore