import React from 'react'
import HomePage from './components/HomePage'
import {Routes,Route} from "react-router-dom"
import ResumeScoreForm from './components/routes/ResumeScoreForm'
import NavBar from './components/NavBar'
import Footer from './components/Footer'
import ResumeScore from './components/routes/ResumeScore'
import PostAJob from './components/routes/PostAJob'
import Jobs from './components/routes/Jobs'

function App(){
  return(
  <>
    <NavBar />
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/resumescoreform" element={<ResumeScoreForm />} />
      <Route path="/resumescore" element={<ResumeScore />} />
      <Route path="/postajob" element={<PostAJob />} />
      <Route path="/jobs" element={<Jobs />} />
    </Routes>
    <Footer />
  </>
  )
}

export default App
