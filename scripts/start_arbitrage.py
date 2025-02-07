from web3 import Web3
import json
import sys
import os
import time
from dotenv import load_dotenv
from backend.dex_scanner import DEXScanner  
from flashloan_executor import FlashloanExecutor
from risk_manager import RiskManager

load_dotenv()

class ArbitrageBot:
    def __init__(self, rpc_url, private_key, flashloan_contract):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = self.web3.eth.account.from_key(private_key)
        
        with open("artifacts/FlashLoanArbitrage.json") as f:
            contract_data = json.load(f)
        
        self.contract = self.web3.eth.contract(
            address=flashloan_contract,
            abi=contract_data["abi"]
        )
        
        self.dex_scanner = DEXScanner({
            "Uniswap": "https://api.uniswap.org/v1/price?pair={token_pair}",
            "SushiSwap": "https://api.sushiswap.org/v1/price?pair={token_pair}"
        })
        self.flashloan_executor = FlashloanExecutor(rpc_url, flashloan_contract, private_key)
        self.risk_manager = RiskManager()
    
    def execute_arbitrage(self, token_in, token_out, amount):
        prices = self.dex_scanner.get_prices(f"{token_in}/{token_out}")
        
        if not prices or len(prices) < 2:
            print("Not enough price data for arbitrage.")
            return
        
        best_bid_dex = max(prices, key=lambda dex: prices[dex]["best_bid"])
        best_ask_dex = min(prices, key=lambda dex: prices[dex]["best_ask"])
        
        if prices[best_bid_dex]["best_bid"] <= prices[best_ask_dex]["best_ask"]:
            print("No profitable arbitrage opportunity found.")
            return
        
        expected_profit = prices[best_bid_dex]["best_bid"] - prices[best_ask_dex]["best_ask"]
        if not self.risk_manager.validate_trade(prices[best_bid_dex]["best_bid"], prices[best_ask_dex]["best_ask"]):
            print("Trade rejected due to risk constraints.")
            return
        
        print(f"Executing arbitrage: Buy from {best_ask_dex}, Sell on {best_bid_dex}")
        tx_hash = self.flashloan_executor.execute_flashloan(token_in, token_out, amount)
        print(f"Arbitrage executed! Transaction Hash: {tx_hash}")
    
if __name__ == "__main__":
    bot = ArbitrageBot(
        rpc_url=os.getenv("RPC_URL"),
        private_key=os.getenv("PRIVATE_KEY"),
        flashloan_contract=os.getenv("FLASHLOAN_CONTRACT")
    )
    
    while True:
        try:
            token_in = "0xTokenInAddress"
            token_out = "0xTokenOutAddress"
            amount = 1000000000000000000  # 1 token assuming 18 decimals
            
            print("Scanning for arbitrage opportunities...")
            bot.execute_arbitrage(token_in, token_out, amount)
            
        except Exception as e:
            print("Error executing arbitrage:", e)
        
        time.sleep(60)  # Wait before the next attempt