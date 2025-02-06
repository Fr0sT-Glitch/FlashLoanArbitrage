# Hybrid Arbitrage Bot

## Overview
This project is an arbitrage trading bot that utilizes flash loans to execute profitable trades across decentralized exchanges (DEXs). It integrates with Uniswap, Aave, and Chainlink price feeds for accurate market data.

## Features

- 🚀 **Automated Arbitrage Execution**: Monitors price discrepancies across multiple DEXs.
- 💰 **Flash Loan Integration**: Uses Aave flash loans to maximize capital efficiency.
- 🔒 **MEV Protection**: Submits private transactions via Flashbots to prevent front-running.
- 🤖 **AI-Driven Trading**: Machine learning model predicts profitable trade opportunities.
- ⚠️ **Risk Management**: Adjustable slippage tolerance and gas price optimization.

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/YourRepo/HybridArbitrageBot.git
cd HybridArbitrageBot
```

### 2. Install Dependencies

#### Backend
```sh
pip install -r requirements.txt
```

#### Frontend
```sh
cd frontend
npm install
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory and add the required configuration (See `.env.example`).

### 4. Deploy Smart Contracts
```sh
python scripts/deploy_contracts.py
```

### 5. Start the Arbitrage Bot
```sh
python scripts/start_arbitrage.py
```

## Architecture

## Running Tests
```sh
pytest tests/
```

## Deployment with Docker
```sh
docker build -t arbitrage-bot .
docker run -d --env-file .env arbitrage-bot
```

## Dashboard UI

The frontend dashboard allows monitoring arbitrage opportunities in real-time.

## License
MIT License