import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load dataset
DATA_FILE = "models/training_data.csv"
df = pd.read_csv(DATA_FILE)

# Prepare features and labels
features = ["best_bid", "best_ask", "spread", "mid_price"]
X = df[features]
y = df["profit"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Model Mean Absolute Error: {mae}")

# Save trained model
MODEL_FILE = "models/arbitrage_model.pkl"
joblib.dump(model, MODEL_FILE)
print(f"Model saved to {MODEL_FILE}")