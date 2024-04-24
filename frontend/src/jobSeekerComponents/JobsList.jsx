import React, { useState } from 'react'
import {CopyToClipboard} from 'react-copy-to-clipboard';

function AdminJobsList({jobs}){
    const [copied,setCopied]=useState(false)

    function handleClick(){
        setCopied(true)
        alert("Text Copied!")    
    }


    return (
    <div className='flex w-[30vw] flex-wrap'>
        {jobs.map((job) => {
                    return (
                        <div className='mx-4'>
                            <div className='my-4 h-[5vh] flex flex-col items-center'>
                                <div className='flex-col bg-gray-300  hover:fill-white hover:scale-110 duration-300 hover:duration-300 border-4 border-black p-4 rounded-xl flex justify-center items-center'>
                                    <h1 className='mx-4 text-[1em] font-semibold '>
                                        <span className='font-bold'>Job Position:</span> {job.jobTitle}
                                    </h1>
                                    <p>
                                        <span className='font-bold'>Tech Stack Required:</span> {job.techStack}
                                    </p>
                                </div>
                                <CopyToClipboard className="mt-4 border-4 border-black p-2 rounded-xl text-xs hover:bg-black hover:text-white" text={job.techStack} onCopy={handleClick}><button className=' '>Copy to Clipboard</button></CopyToClipboard>
                            </div>
                        </div>
                    )
                }
            )
        }   
    </div>
  )
}

export default AdminJobsList