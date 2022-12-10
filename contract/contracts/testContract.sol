// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;
import "hardhat/console.sol";


contract testContract {

    // State vars
    address public owner;
    
    constructor() {
        owner = msg.sender;
        console.log("Hello World");
    }

}

//Contract Address 0x00c17254add3022469e7f9cd3AF542f0CD130801
