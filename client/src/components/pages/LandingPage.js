import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import '../../App.css'
import BackgroundImage from '../../assets/images/chart.jpg'
import { ethers } from "ethers";


export default function LandingPage() {

    const [currentAccount, setCurrentAccount] = useState("");

    const connectWallet = async () => {
        try {
          const { ethereum } = window;
    
          if (!ethereum) {
            alert("Need an ETH wallet to connect to!");
            return;
          }
    
          // Makes request to connect to ETH account (Metamask wallet)
          const accounts = await ethereum.request({ method: "eth_requestAccounts" });
    
          console.log("Connected", accounts[0]);
    
          // Set the currAccount state within this component to know the address of the account
          setCurrentAccount(accounts[0]);
        } catch (error) {
          console.log(error)
        }
    }

    const checkIfWalletIsConnected = async () => {
        try {
          const { ethereum } = window;
    
          if (!ethereum) {
            console.log("Make sure you have an ETH wallet!");
            return;
          } else {
            console.log("We have the ethereum object", ethereum);
          }
    
          // Pulls array of accounts
          const accounts = await ethereum.request({ method: "eth_accounts" });
    
          if (accounts.length !== 0) {
            const account = accounts[0];
            console.log("Found an authorized account:", account);
            setCurrentAccount(account);
          } else {
            console.log("No authorized account found")
          }
        } catch (error) {
          console.log(error);
        }
    } 

    useEffect(() => {
        checkIfWalletIsConnected();
      }, [])


    //<Link to="/login">
    //    <button className="primary-button" id="log_btn"><span>log in</span></button>
    //</Link>

    //<Link to="/register">
    //    <button className="primary-button" id="reg_btn"><span>register </span></button>
    //</Link>

    return (
        <header style={ HeaderStyle }>
            <h1 className="main-title text-center">login / register page</h1>
            <p className="main-para text-center">Blockchain Project for COSC-431</p>
            <div className="buttons text-center box-center">
                {!currentAccount && (
                    <button onClick={connectWallet}>
                    Connect Wallet
                    </button>
                )}

                {currentAccount && (
                    <Link to="/apexchart">
                        <button className="primary-button" id="reg_btn"><span>Open Charting</span></button>
                    </Link>
                )}

            </div>
        </header>
    )
}

const HeaderStyle = {
    width: "100%",
    height: "100vh",
    background: `url(${BackgroundImage})`,
    backgroundPosition: "center",
    backgroundRepeat: "no-repeat",
    backgroundSize: "cover"
}