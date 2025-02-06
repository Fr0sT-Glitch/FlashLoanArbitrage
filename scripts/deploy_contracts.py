from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ContractDeployer:
    def __init__(self, rpc_url, private_key):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = self.web3.eth.account.from_key(private_key)
    
    def deploy_contract(self, contract_name, constructor_args=[]):
        with open(f"artifacts/{contract_name}.json") as f:
            contract_data = json.load(f)
        
        contract = self.web3.eth.contract(
            abi=contract_data["abi"],
            bytecode=contract_data["bytecode"]
        )
        
        tx = contract.constructor(*constructor_args).build_transaction({
            "from": self.account.address,
            "gas": 5000000,
            "gasPrice": self.web3.to_wei("50", "gwei"),
            "nonce": self.web3.eth.get_transaction_count(self.account.address)
        })
        
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Deploying {contract_name}... Transaction Hash: {self.web3.to_hex(tx_hash)}")
        
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"{contract_name} deployed at: {tx_receipt.contractAddress}")
        return tx_receipt.contractAddress

if __name__ == "__main__":
    deployer = ContractDeployer(
        rpc_url=os.getenv("RPC_URL"),
        private_key=os.getenv("PRIVATE_KEY")
    )
    
    flashloan_contract = deployer.deploy_contract("FlashLoanArbitrage", [
        os.getenv("AAVE_LENDING_POOL"),
        os.getenv("UNISWAP_ROUTER"),
        os.getenv("CHAINLINK_PRICE_FEED")
    ])
    
    mev_protection_contract = deployer.deploy_contract("MEVProtection")
    arbitrage_executor_contract = deployer.deploy_contract("ArbitrageExecutor", [os.getenv("UNISWAP_ROUTER")])