// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract MEVProtection {
    address private owner;
    mapping(address => bool) private authorizedExecutors;

    event MEVProtectionActivated(address indexed executor, uint256 feePaid);
    event ExecutorAuthorized(address indexed executor, bool status);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    modifier onlyAuthorized() {
        require(authorizedExecutors[msg.sender], "Not an authorized executor");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function authorizeExecutor(address executor, bool status) external onlyOwner {
        authorizedExecutors[executor] = status;
        emit ExecutorAuthorized(executor, status);
    }

    function activateProtection(uint256 fee, address token) external onlyAuthorized {
        require(fee > 0, "Fee must be greater than zero");
        require(IERC20(token).transferFrom(msg.sender, address(this), fee), "Fee transfer failed");
        emit MEVProtectionActivated(msg.sender, fee);
    }

    function withdrawFees(address token, uint256 amount) external onlyOwner {
        require(IERC20(token).transfer(owner, amount), "Withdrawal failed");
    }
}
