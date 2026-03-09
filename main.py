from fastapi import FastAPI
import os
import uvicorn
from eth_account import Account
from web3 import Web3

app = FastAPI()

RPC = os.getenv("ETH_RPC", "https://rpc.ankr.com/eth")
w3 = Web3(Web3.HTTPProvider(RPC))

users = {}
transactions = []

@app.get("/")
def home():
    return {"wallet": "running"}

# create user + wallet
@app.get("/user/create/{username}")
def create_user(username: str):

    acct = Account.create()

    users[username] = {
        "address": acct.address,
        "private_key": acct.key.hex(),
        "balance": 0
    }

    return {
        "username": username,
        "address": acct.address
    }

# view wallet
@app.get("/wallet/{username}")
def wallet(username: str):

    user = users.get(username)

    if not user:
        return {"error": "user not found"}

    return {
        "address": user["address"],
        "balance": user["balance"]
    }

# tip between users
@app.get("/tip/{from_user}/{to_user}/{amount}")
def tip(from_user: str, to_user: str, amount: float):

    if from_user not in users or to_user not in users:
        return {"error": "user not found"}

    if users[from_user]["balance"] < amount:
        return {"error": "insufficient balance"}

    users[from_user]["balance"] -= amount
    users[to_user]["balance"] += amount

    transactions.append({
        "type": "tip",
        "from": from_user,
        "to": to_user,
        "amount": amount
    })

    return {"status": "tip sent"}

# withdraw ETH
@app.get("/withdraw/{username}/{to}/{amount}")
def withdraw(username: str, to: str, amount: float):

    user = users.get(username)

    if not user:
        return {"error": "user not found"}

    acct = Account.from_key(user["private_key"])

    tx = {
        "to": to,
        "value": w3.to_wei(amount, "ether"),
        "gas": 21000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(acct.address)
    }

    signed = acct.sign_transaction(tx)

    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

    return {"tx": tx_hash.hex()}

# transaction history
@app.get("/transactions")
def history():
    return transactions


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
