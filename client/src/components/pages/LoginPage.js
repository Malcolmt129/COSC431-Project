import React from 'react'
import { Link } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.css';
import { Col } from 'react-bootstrap';

import '../../App.css'

export default function LoginPage() {
    return (
        <div className="text-center m-5-auto box-center">
            <h2>Sign in to us</h2>
            <form action="/home" className='form-box-size position-relative'>
                <p className='row'>
                    <label className='col-md-3'>Username</label>
                    <input className="col-md-6"  type="text" name="first_name" required />
                </p>
                <p className='row'>
                    <label className='col-md-3'>Password</label>
                    <input className="col-md-6"   type="password" name="password" required />
                </p>
                <p className=''>
                    <button id="sub_btn" type="submit">Login</button>
                    <Link to="/forget-password"><label className="right-label position-absolute top-50 start-50 translate-middle">Forget password?</label></Link>
                    
                </p>
            </form>
            <footer>
                <p>First time? <Link to="/register">Create an account</Link>.</p>
                <p><Link to="/">Back to Homepage</Link>.</p>
            </footer>
        </div>
    )
}