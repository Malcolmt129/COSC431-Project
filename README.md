# Ethereum Strategy Testing Project COSC431-Project 

##COSC431 Group Project for simulating/graphing trading strategies on the market value of Etherum

This project is an attempt to create a webpage/software for individuals to simulate different trading strategies for various crypto-currencies. By providing a webpage for users, one can generate candle plots for any crypto (currently our app only supports Ethereum) from any point in time in hourly intervals for visual reference of its value. From here, users can pay to test different strategies using a MetaMask Wallet to simulate as if they were buying/selling on that portion of data (Currently we have only implemented one strategy: Running Average). The components of the project can be broken down into the following:

* Javascript React to create a front end webpage for users to interact with
* Python Flask to create a back-end server that grabs data from our Personal Database and Calculate our strategies
* Firebase Database that houses our pre-configured hourly interval data points to be grabbed from the backend (With future plans to automatically update itself with live data)


## Purpose 
With the rise of Crypto in current years, there have been many who have tried to cash out by making half-baked or even outright scam strategies. In most cases, it can be impossible to verify the authenticity of these strategies without trying them out yourself, forcing the individual to risk their assets for simply authenticity. We feel that transparency is important, and want to provide a service where users can better visualize these strategies while putting their authenticity to the test. 

## Usage
Our project is still in development stages, and is not running on a public site. To test it for yourself, you may clone the project and run it using the following steps:

* Open a terminal and direct yourself to server.py found withing the Server folder and run the file. (This starts up the python backend and is important for grabbing your data)

*Open another terminal and cd yourself into the client folder. From here run ```npm start``` (```npm install``` if this is your first time running the project) in the folder. This starts up the local webpage and can be accessed at http://localhost:3000

*Make sure to have a MetaMask Wallet to connect to our app and login. 

*To generate a graph, enter a start date and end date in the following format YYYY/MM/DD (for specific times, do YYYY/MM/DDTHH/mm/ss) and press generate

*After generating a candle Plot, you can press generate below the strategies table to test our strategy (For testing purposes, all transactions are done through goerli test etherum).
