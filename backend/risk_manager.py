import os
import json
from web3 import Web3

class RiskManager:
    def __init__(self, slippage_tolerance=0.005, gas_limit=3000000, gas_price_gwei=50):
        self.slippage_tolerance = slippage_tolerance  # Default 0.5%
        self.gas_limit = gas_limit
        self.gas_price = Web3.to_wei(gas_price_gwei, "gwei")
    
    def check_slippage(self, expected_price, actual_price):
        """Checks if the slippage is within the acceptable tolerance."""
        slippage = abs(expected_price - actual_price) / expected_price
        return slippage <= self.slippage_tolerance
    
    def optimize_gas(self, web3):
        """Dynamically adjust gas price based on network conditions."""
        latest_gas_price = web3.eth.gas_price
        return min(latest_gas_price, self.gas_price)
    
    def validate_trade(self, expected_price, actual_price):
        """Ensures that the trade is valid under the risk parameters."""
        if not self.check_slippage(expected_price, actual_price):
            raise ValueError("Trade rejected due to high slippage.")
        return True
    
if __name__ == "__main__":
    risk_manager = RiskManager()
    expected_price = 3000
    actual_price = 2995  # Simulating a 0.17% slippage
    
    if risk_manager.validate_trade(expected_price, actual_price):
        print("Trade approved within risk limits.")
    else:
        print("Trade rejected.")