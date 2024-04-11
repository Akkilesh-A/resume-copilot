// import React, { useState } from 'react';
// import { useDropzone } from 'react-dropzone';

// const FileUpload = () => {
//   const [uploadedFiles, setUploadedFiles] = useState([]);
//   const { getRootProps, getInputProps } = useDropzone({
//     onDrop: (acceptedFiles) => {
//       setUploadedFiles(acceptedFiles);
//     },
//   });
//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if(uploadedFiles.length === 0){
//       alert("Please upload a file first!")
//       return
//     }
//     alert("File Uploaded Successfully!")
//     window.location.href='/adminjobsportal'
//   }
// //TO DO : Customize and Style this Drag and Drop to Upload box as you want🧑‍💻😊
//   return (
//     <form onSubmit={handleSubmit}>
//       <div className="border w-[30vw] h-[30vh] flex flex-col justify-center bg-gray-200 rounded-xl cursor-pointer text-center" {...getRootProps()}>
        
//           <input {...getInputProps()} />
//           <p className='font-semibold'>Drop it like it's hot </p>
//           <span className='text-3xl'>🥵</span>
//           <ul>
//             {uploadedFiles.map((file) => (
//               <li className='text-xs' key={file.name}>{file.name}</li>
//             ))}
//           </ul>
          
//       </div>
//       <div className='text-center flex justify-center pt-8'>
//         <button type="submit" className='hover:bg-black hover:fill-white  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold'>
//           <h1 className=''>Upload Files</h1>   
//         </button> 
//       </div>
//     </form>
//   );
// };
// export default FileUpload;

import React from 'react'

const FileUpload = () => {

  const handleSubmit = async (e) => {
    e.preventDefault();
    alert("File Uploaded Successfully!")
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" />
        <button type="submit" className='hover:bg-black hover:fill-white  hover:text-white flex justify-center items-center rounded-xl px-4 p-2 border-4 border-black font-bold'>
          <h1 className=''>Upload Files</h1>   
        </button>       
      </form>
    </div>
  )
}

export default FileUpload