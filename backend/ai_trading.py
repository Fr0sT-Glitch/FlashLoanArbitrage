import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor

class AITrading:
    def __init__(self, model_path="models/arbitrage_model.pkl"):
        self.model = joblib.load(model_path)
    
    def predict_profitability(self, token_pair, order_book_data):
        """Predicts the profitability of an arbitrage opportunity."""
        features = self.extract_features(token_pair, order_book_data)
        return self.model.predict([features])[0]
    
    def extract_features(self, token_pair, order_book_data):
        """Extract relevant features from the order book data."""
        best_bid = order_book_data[token_pair]['best_bid']
        best_ask = order_book_data[token_pair]['best_ask']
        spread = best_ask - best_bid
        mid_price = (best_bid + best_ask) / 2
        return [best_bid, best_ask, spread, mid_price]
    
if __name__ == "__main__":
    ai_trader = AITrading()
    sample_order_book = {"ETH/USDT": {"best_bid": 3000, "best_ask": 3010}}
    prediction = ai_trader.predict_profitability("ETH/USDT", sample_order_book)
    print("Predicted Profitability:", prediction)