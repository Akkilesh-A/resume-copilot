import {Routes,Route} from "react-router-dom"
import NavBar from './fixedComponents/NavBar'
import Footer from './fixedComponents/Footer'
import AdminJobsPortal from './components/AdminJobsPortal'
import PostAJob from './components/PostAJob'
import HomePage from "./fixedComponents/HomePage"
import ResumeScoreForm from "./employeeComponents/ResumeScoreForm"
import ResumeScore from "./employeeComponents/ResumeScore"
import JobsPortal from "./employeeComponents/JobsPortal"
import AdminLogin from "./components/AdminLogin"
import AdminRegister from "./components/AdminRegister"
import Simple from "./employeeComponents/Simple"

function App() {

  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/resumescoreform" element={<ResumeScoreForm />} />
        <Route path="/resumescore" element={<ResumeScore />} />
        <Route path="/adminjobsportal" element={<AdminJobsPortal />} />
        <Route path="/jobs" element={<JobsPortal />} />
        <Route path="/postajob" element={<PostAJob />} />
        <Route path="/adminlogin" element={<AdminLogin />} />
        <Route path="/adminregister" element={<AdminRegister />} />
        <Route path="/resumescanned" element={<Simple />} />
      </Routes>
      <Footer />
    </>
  )
}

export default App
