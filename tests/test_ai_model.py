import unittest
import joblib
import numpy as np
from ai_trading import AITrading

class TestAIModel(unittest.TestCase):
    
    def setUp(self):
        self.ai_trader = AITrading(model_path="models/arbitrage_model.pkl")
    
    def test_model_loads(self):
        """Ensure the AI model loads correctly."""
        self.assertIsNotNone(self.ai_trader.model, "Model failed to load")
    
    def test_prediction_shape(self):
        """Test if the model returns a single prediction value."""
        sample_order_book = {"ETH/USDT": {"best_bid": 3000, "best_ask": 3010}}
        prediction = self.ai_trader.predict_profitability("ETH/USDT", sample_order_book)
        self.assertIsInstance(prediction, float, "Prediction should be a float")
    
if __name__ == "__main__":
    unittest.main()