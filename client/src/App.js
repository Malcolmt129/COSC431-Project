import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import LandingPage from './components/pages/LandingPage'
import LoginPage from './components/pages/LoginPage'
import RegisterPage from './components/pages/RegisterPage'
import ForgetPasswordPage from './components/pages/ForgetPasswordPage'
import HomePage from './components/pages/HomePage'
import './App.css'
import ApexChart from './components/pages/ApexChart'
import NavBar from "./components/NavBar"




export default function App() {
    return (
        <Router>
            <div>
                <NavBar/>
                <Routes>
                    <Route path="/login" element={ <LoginPage/> } />
                    <Route path="/register" element={ <RegisterPage/> } />
                    <Route path="/forget-password" element={ <ForgetPasswordPage/> } />
                    <Route path="/home" element={ <HomePage/> } />
                    <Route path="/apexchart" element={<ApexChart/>}/>
                    <Route exact path="/" element={ <LandingPage/> } />
                </Routes>
            </div>
        </Router>
    )
    
}



