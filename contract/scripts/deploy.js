const main = async () => {
    const [deployer] = await hre.ethers.getSigners();
    const accountBalance = await deployer.getBalance();
  
    console.log("Deploying contracts with account: ", deployer.address);
    console.log("Account balance: ", accountBalance.toString());
  
    const towsonAdvancedContractFactory = await hre.ethers.getContractFactory("testContract");
    const towsonAdvancedContract = await towsonAdvancedContractFactory.deploy();
    await towsonAdvancedContract.deployed();
  
    console.log("Towson Contract address: ", towsonAdvancedContract.address);
  };
  
  const runMain = async () => {
    try {
      await main();
      process.exit(0);
    } catch (error) {
      console.log(error);
      process.exit(1);
    }
  };
  
  runMain();