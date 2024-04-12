import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
const FileUpload = () => {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const { getRootProps, getInputProps } = useDropzone({
    onDrop: (acceptedFiles) => {
      setUploadedFiles(acceptedFiles);
    },
  });
//TO DO : Customize and Style this Drag and Drop to Upload box as you want🧑‍💻😊
  return (
    <div className="border w-[30vw] h-[30vh] flex flex-col justify-center bg-gray-200 rounded-xl cursor-pointer text-center" {...getRootProps()}>
      <input {...getInputProps()} />
      <p className='font-semibold'>Drop it like it's hot </p>
      <span className='text-3xl'>🥵</span>
      <ul>
        {uploadedFiles.map((file) => (
          <li className='text-xs' key={file.name}>{file.name}</li>
        ))}
      </ul>
    </div>
  );
};
export default FileUpload;