import os
import json
import sys
from web3 import Web3
from eth_account import Account

def anchor_merkle_root(merkle_root):
    # Sepolia RPC (using a public one for demonstration)
    rpc_url = "https://rpc.ankr.com/eth_sepolia"
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    private_key = os.getenv("SEPOLIA_PRIVATE_KEY")
    if not private_key:
        return {"error": "SEPOLIA_PRIVATE_KEY not found"}
    
    try:
        account = Account.from_key(private_key)
        address = account.address
        
        # Prepare a transaction to self with the Merkle Root in the data field
        # This is a common way to anchor data on-chain without a specific contract
        # The data is prefixed with a MatVerse identifier
        data_hex = "0x" + "4d56" + merkle_root # 4d56 = 'MV' in hex
        
        nonce = w3.eth.get_transaction_count(address)
        gas_price = w3.eth.gas_price
        
        tx = {
            'nonce': nonce,
            'to': address, # Sending to self
            'value': 0,
            'gas': 25000, # Standard transfer + some data
            'gasPrice': int(gas_price * 1.2), # 20% buffer
            'data': data_hex,
            'chainId': 11155111 # Sepolia Chain ID
        }
        
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        return {
            "status": "anchored",
            "network": "sepolia",
            "tx_hash": tx_hash.hex(),
            "address": address,
            "merkle_root": merkle_root,
            "explorer_url": f"https://sepolia.etherscan.io/tx/{tx_hash.hex()}"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 matverse_anchor.py <merkle_root>")
        sys.exit(1)
    
    root = sys.argv[1]
    result = anchor_merkle_root(root)
    print(json.dumps(result, indent=2))
