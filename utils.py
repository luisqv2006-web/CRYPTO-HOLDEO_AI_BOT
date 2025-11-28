from web3 import Web3

def connect_bsc(rpc):
    return Web3(Web3.HTTPProvider(rpc))

def format_usd(value):
    return f"${round(value, 2)} USD"
