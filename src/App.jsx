import React from 'react'
import HomePage from './components/HomePage'
import {Routes,Route} from "react-router-dom"
import ResumeScore from './components/routes/ResumeScore'
import NavBar from './components/NavBar'
import Footer from './components/Footer'

function App(){
  return(
  <>
    <NavBar />
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/resumescore" element={<ResumeScore />} />
    </Routes>
    <Footer />
  </>
  )
}

export default App
