from web3 import Web3
import json
import os

class FlashloanExecutor:
    def __init__(self, rpc_url, contract_address, private_key):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = self.web3.eth.account.from_key(private_key)
        
        with open("artifacts/FlashLoanArbitrage.json") as f:
            contract_abi = json.load(f)["abi"]
        
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
    
    def execute_flashloan(self, token_in, token_out, amount):
        """Executes a flashloan-based arbitrage trade."""
        nonce = self.web3.eth.get_transaction_count(self.account.address)
        tx = self.contract.functions.executeArbitrage(token_in, token_out, amount).build_transaction({
            "from": self.account.address,
            "gas": 3000000,
            "gasPrice": self.web3.to_wei("50", "gwei"),
            "nonce": nonce
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.web3.to_hex(tx_hash)
    
if __name__ == "__main__":
    executor = FlashloanExecutor(
        rpc_url=os.getenv("RPC_URL"),
        contract_address=os.getenv("FLASHLOAN_CONTRACT"),
        private_key=os.getenv("PRIVATE_KEY")
    )
    tx_hash = executor.execute_flashloan("0xTokenIn", "0xTokenOut", 1000000000000000000)
    print("Flashloan executed, transaction hash:", tx_hash)