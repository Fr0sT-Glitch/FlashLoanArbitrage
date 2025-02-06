const { ethers } = require("hardhat");
require("dotenv").config();

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);

    // Deploy FlashLoanArbitrage
    const FlashLoanArbitrage = await ethers.getContractFactory("FlashLoanArbitrage");
    const flashLoanArbitrage = await FlashLoanArbitrage.deploy(
        process.env.AAVE_LENDING_POOL,
        process.env.UNISWAP_ROUTER,
        process.env.CHAINLINK_PRICE_FEED
    );
    await flashLoanArbitrage.deployed();
    console.log("FlashLoanArbitrage deployed to:", flashLoanArbitrage.address);

    // Deploy MEVProtection
    const MEVProtection = await ethers.getContractFactory("MEVProtection");
    const mevProtection = await MEVProtection.deploy();
    await mevProtection.deployed();
    console.log("MEVProtection deployed to:", mevProtection.address);

    // Deploy ArbitrageExecutor
    const ArbitrageExecutor = await ethers.getContractFactory("ArbitrageExecutor");
    const arbitrageExecutor = await ArbitrageExecutor.deploy(process.env.UNISWAP_ROUTER);
    await arbitrageExecutor.deployed();
    console.log("ArbitrageExecutor deployed to:", arbitrageExecutor.address);
}

main().then(() => process.exit(0)).catch((error) => {
    console.error(error);
    process.exit(1);
});
