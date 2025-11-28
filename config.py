import os
from dotenv import load_dotenv

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BSC_RPC = os.getenv("BSC_RPC", "https://bsc-dataseed.binance.org/")
CAPITAL_MAX = float(os.getenv("CAPITAL_MAX", 25))

REINVEST_MIN_USD = 1.0
GAS_LIMIT_USD = 0.20
