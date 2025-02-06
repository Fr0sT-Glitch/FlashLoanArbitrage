// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@aave/protocol-v2/contracts/interfaces/ILendingPool.sol";
import "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FlashLoanArbitrage {
    address private owner;
    ISwapRouter private uniswapRouter;
    ILendingPool private lendingPool;
    AggregatorV3Interface private priceFeed;

    event ArbitrageExecuted(address indexed token, uint256 profit);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    constructor(address _aaveLendingPool, address _uniswapRouter, address _priceFeed) {
        owner = msg.sender;
        lendingPool = ILendingPool(_aaveLendingPool);
        uniswapRouter = ISwapRouter(_uniswapRouter);
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function executeArbitrage(
        address tokenIn,
        address tokenOut,
        uint256 amount
    ) external onlyOwner {
        address[] memory assets = new address[](1);
        assets[0] = tokenIn;

        uint256[] memory amounts = new uint256[](1);
        amounts[0] = amount;

        uint256[] memory modes = new uint256[](1);
        modes[0] = 0;

        lendingPool.flashLoan(address(this), assets, amounts, modes, address(this), "", 0);
    }

    function swapOnDex(
        address tokenIn,
        address tokenOut,
        uint256 amountIn
    ) internal returns (uint256 amountOut) {
        IERC20(tokenIn).approve(address(uniswapRouter), amountIn);

        ISwapRouter.ExactInputSingleParams memory params = ISwapRouter.ExactInputSingleParams({
            tokenIn: tokenIn,
            tokenOut: tokenOut,
            fee: 3000,
            recipient: address(this),
            deadline: block.timestamp,
            amountIn: amountIn,
            amountOutMinimum: 0,
            sqrtPriceLimitX96: 0
        });

        amountOut = uniswapRouter.exactInputSingle(params);
    }
}
