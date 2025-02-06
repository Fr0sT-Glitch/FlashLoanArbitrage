from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

class FlashbotsMempool:
    def __init__(self, rpc_url, private_key, flashloan_contract):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = self.web3.eth.account.from_key(private_key)
        
        with open("artifacts/FlashLoanArbitrage.json") as f:
            contract_data = json.load(f)
        
        self.contract = self.web3.eth.contract(
            address=flashloan_contract,
            abi=contract_data["abi"]
        )
    
    def send_private_tx(self, token_in, token_out, amount, relay_url):
        """Sends an arbitrage transaction privately via Flashbots to avoid MEV attacks."""
        nonce = self.web3.eth.get_transaction_count(self.account.address)
        tx = self.contract.functions.executeArbitrage(token_in, token_out, amount).build_transaction({
            "from": self.account.address,
            "gas": 5000000,
            "gasPrice": self.web3.to_wei("50", "gwei"),
            "nonce": nonce
        })
        
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.account.key)
        
        flashbots_payload = {
            "jsonrpc": "2.0",
            "method": "eth_sendPrivateTransaction",
            "params": [{"tx": self.web3.to_hex(signed_tx.rawTransaction), "preferences": {"fast": True}}],
            "id": 1
        }
        
        response = self.web3.provider.make_request("post", relay_url, json=flashbots_payload)
        print("Flashbots transaction sent:", response)
    
if __name__ == "__main__":
    flashbots = FlashbotsMempool(
        rpc_url=os.getenv("RPC_URL"),
        private_key=os.getenv("PRIVATE_KEY"),
        flashloan_contract=os.getenv("FLASHLOAN_CONTRACT")
    )
    
    relay_url = "https://relay.flashbots.net/"
    token_in = "0xTokenInAddress"
    token_out = "0xTokenOutAddress"
    amount = 1000000000000000000  # 1 token assuming 18 decimals
    
    flashbots.send_private_tx(token_in, token_out, amount, relay_url)