// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";

contract ArbitrageExecutor {
    address private owner;
    ISwapRouter private uniswapRouter;

    event ArbitrageExecuted(address indexed tokenIn, address indexed tokenOut, uint256 profit);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    constructor(address _uniswapRouter) {
        owner = msg.sender;
        uniswapRouter = ISwapRouter(_uniswapRouter);
    }

    function executeArbitrage(
        address tokenIn,
        address tokenOut,
        uint256 amountIn
    ) external onlyOwner returns (uint256 profit) {
        uint256 initialBalance = IERC20(tokenOut).balanceOf(address(this));

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

        uint256 amountOut = uniswapRouter.exactInputSingle(params);
        profit = IERC20(tokenOut).balanceOf(address(this)) - initialBalance;

        emit ArbitrageExecuted(tokenIn, tokenOut, profit);
    }

    function withdrawProfits(address token, uint256 amount) external onlyOwner {
        require(IERC20(token).transfer(owner, amount), "Withdrawal failed");
    }
}
