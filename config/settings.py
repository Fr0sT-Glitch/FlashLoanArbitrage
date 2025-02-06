import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Blockchain settings
    RPC_URL = os.getenv("RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "YOUR_PRIVATE_KEY")
    FLASHLOAN_CONTRACT = os.getenv("FLASHLOAN_CONTRACT", "0xFlashloanContractAddress")
    MEV_PROTECTION_CONTRACT = os.getenv("MEV_PROTECTION_CONTRACT", "0xMEVProtectionContractAddress")
    UNISWAP_ROUTER = os.getenv("UNISWAP_ROUTER", "0xUniswapRouterAddress")

    # API keys
    CHAINLINK_API_KEY = os.getenv("CHAINLINK_API_KEY", "your-chainlink-api-key")
    DEX_API_KEYS = {
        "Uniswap": os.getenv("UNISWAP_API_KEY", "your-uniswap-api-key"),
        "SushiSwap": os.getenv("SUSHISWAP_API_KEY", "your-sushiswap-api-key")
    }

    # Risk Management settings
    SLIPPAGE_TOLERANCE = float(os.getenv("SLIPPAGE_TOLERANCE", 0.005))  # 0.5%
    MAX_GAS_PRICE = int(os.getenv("MAX_GAS_PRICE", 100))  # Max gas price in gwei
    GAS_LIMIT = int(os.getenv("GAS_LIMIT", 3000000))

if __name__ == "__main__":
    print("Loaded Config:")
    print("RPC URL:", Config.RPC_URL)
    print("Flashloan Contract:", Config.FLASHLOAN_CONTRACT)
    print("Slippage Tolerance:", Config.SLIPPAGE_TOLERANCE)