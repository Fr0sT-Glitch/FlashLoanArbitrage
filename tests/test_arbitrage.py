import unittest
from unittest.mock import patch
from start_arbitrage import ArbitrageBot
import os

class TestArbitrageExecution(unittest.TestCase):
    
    @patch("start_arbitrage.ArbitrageBot.execute_arbitrage")
    def test_execute_arbitrage(self, mock_execute):
        bot = ArbitrageBot(
            rpc_url=os.getenv("RPC_URL"),
            private_key=os.getenv("PRIVATE_KEY"),
            flashloan_contract=os.getenv("FLASHLOAN_CONTRACT")
        )
        
        mock_execute.return_value = "0xMockTransactionHash"
        tx_hash = bot.execute_arbitrage("0xTokenIn", "0xTokenOut", 1000000000000000000)
        
        self.assertEqual(tx_hash, "0xMockTransactionHash")
        mock_execute.assert_called_once()
    
if __name__ == "__main__":
    unittest.main()