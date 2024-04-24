import {Routes,Route} from "react-router-dom"
import NavBar from './fixedComponents/NavBar'
import AdminJobsPortal from './components/AdminJobsPortal'
import PostAJob from './components/PostAJob'
import HomePage from "./fixedComponents/HomePage"
import GitHubScore from "./jobSeekerComponents/GitHubScore"
import JobsPortal from "./jobSeekerComponents/JobsPortal"
import AdminLogin from "./components/AdminLogin"
import AdminRegister from "./components/AdminRegister"
import Simple from "./jobSeekerComponents/Simple"
import About from "./fixedComponents/About"
import GitHubStatsForm from "./jobSeekerComponents/GitHubStatsForm"
import ResumeScanner from "./jobSeekerComponents/ResumeScanner"
import ResumeScore from "./jobSeekerComponents/ResumeScore"
import MultipleResumeScanner from "./recruiterComponents/NonTechnical/NonTechnicalMultipleResumeScanner"
import BestResumes from "./recruiterComponents/Technical/TechnicalBestResumes"
import Options from "./recruiterComponents/Options"
import NonTechnicalBestResumes from "./recruiterComponents/NonTechnical/NonTechnicalBestResumes"
import TechnicalBestResumes from "./recruiterComponents/Technical/TechnicalBestResumes"
import TechnicalMultipleResumeScanner from "./recruiterComponents/Technical/TechnicalMultipleResumeScanner"
import NonTechnicalMultipleResumeScanner from "./recruiterComponents/NonTechnical/NonTechnicalMultipleResumeScanner"

function App() {

  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/githubstatsform" element={<GitHubStatsForm />} />
        <Route path="/githubstats/:gitHubDetails" element={<GitHubScore />} />
        <Route path="/adminjobsportal" element={<AdminJobsPortal />} />
        <Route path="/jobs" element={<JobsPortal />} />
        <Route path="/postajob" element={<PostAJob />} />
        <Route path="/adminlogin" element={<AdminLogin />} />
        <Route path="/adminregister" element={<AdminRegister />} />
        <Route path="/resumescanned/:jobTitle" element={<Simple />} />
        <Route path="/about" element={<About />} />
        <Route path="/resumescannerform" element={<ResumeScanner />} />
        <Route path="/resumescore" element={<ResumeScore />} />

        {/* Recruiter Paths */}
        <Route path="/options" element={<Options />} />
        <Route path="/technical" element={<TechnicalMultipleResumeScanner />} />
        <Route path="/technicalbestresumes" element={<TechnicalBestResumes />} />
        <Route path="/nontechnical" element={<NonTechnicalMultipleResumeScanner />} />
        <Route path="/nontechnicalbestresumes" element={<NonTechnicalBestResumes />} />
      </Routes>
    </>
  )
}

export default App
