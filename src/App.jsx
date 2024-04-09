import React from 'react'
import HomePage from './components/HomePage'
import {Routes,Route} from "react-router-dom"
import ResumeScoreForm from './components/routes/ResumeScoreForm'
import NavBar from './components/NavBar'
import Footer from './components/Footer'
import ResumeScore from './components/routes/ResumeScore'

function App(){
  return(
  <>
    <NavBar />
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/resumescoreform" element={<ResumeScoreForm />} />
      <Route path="/resumescore" element={<ResumeScore />} />
    </Routes>
    <Footer />
  </>
  )
}

export default App
