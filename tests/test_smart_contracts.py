import unittest
from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

class TestSmartContracts(unittest.TestCase):
    
    def setUp(self):
        self.web3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
        with open("artifacts/FlashLoanArbitrage.json") as f:
            self.contract_abi = json.load(f)["abi"]
        self.contract = self.web3.eth.contract(
            address=os.getenv("FLASHLOAN_CONTRACT"), abi=self.contract_abi
        )
    
    def test_contract_connection(self):
        """Test if the contract is correctly connected."""
        self.assertTrue(self.web3.is_connected(), "Web3 is not connected")
        self.assertIsNotNone(self.contract, "Contract instance is None")
    
    def test_execute_arbitrage_function_exists(self):
        """Test if the executeArbitrage function exists in the contract."""
        self.assertIn("executeArbitrage", dir(self.contract.functions), "executeArbitrage function not found")
    
if __name__ == "__main__":
    unittest.main()