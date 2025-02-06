from web3 import Web3
import json
import os

class MEVProtection:
    def __init__(self, rpc_url, contract_address, private_key):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = self.web3.eth.account.from_key(private_key)
        
        with open("artifacts/MEVProtection.json") as f:
            contract_abi = json.load(f)["abi"]
        
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
    
    def activate_protection(self, fee, token):
        """Activates MEV protection by submitting a transaction to the contract."""
        nonce = self.web3.eth.get_transaction_count(self.account.address)
        tx = self.contract.functions.activateProtection(fee, token).build_transaction({
            "from": self.account.address,
            "gas": 3000000,
            "gasPrice": self.web3.to_wei("50", "gwei"),
            "nonce": nonce
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.web3.to_hex(tx_hash)
    
if __name__ == "__main__":
    mev_protector = MEVProtection(
        rpc_url=os.getenv("RPC_URL"),
        contract_address=os.getenv("MEV_PROTECTION_CONTRACT"),
        private_key=os.getenv("PRIVATE_KEY")
    )
    tx_hash = mev_protector.activate_protection(1000000000000000000, "0xTokenAddress")
    print("MEV protection activated, transaction hash:", tx_hash)