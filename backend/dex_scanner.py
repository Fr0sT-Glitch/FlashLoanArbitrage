import requests
import time

class DEXScanner:
    def __init__(self, dex_apis):
        self.dex_apis = dex_apis
    
    def get_prices(self, token_pair):
        """Scans multiple DEXs for the best bid and ask prices."""
        prices = {}
        for dex, api_url in self.dex_apis.items():
            try:
                response = requests.get(api_url.format(token_pair=token_pair))
                data = response.json()
                prices[dex] = {
                    "best_bid": data["best_bid"],
                    "best_ask": data["best_ask"]
                }
            except Exception as e:
                print(f"Error fetching data from {dex}: {e}")
        return prices
    
if __name__ == "__main__":
    dex_apis = {
        "Uniswap": "https://api.uniswap.org/v1/price?pair={token_pair}",
        "SushiSwap": "https://api.sushiswap.org/v1/price?pair={token_pair}"
    }
    scanner = DEXScanner(dex_apis)
    token_pair = "ETH/USDT"
    prices = scanner.get_prices(token_pair)
    print("DEX Prices:", prices)