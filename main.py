from fastapi import FastAPI
import os
import uvicorn
from eth_account import Account
from web3 import Web3

app = FastAPI()

RPC = os.getenv("ETH_RPC", "https://rpc.ankr.com/eth")
w3 = Web3(Web3.HTTPProvider(RPC))

users = {}

@app.get("/")
def home():
    return {"wallet": "running"}

# create wallet linked to telegram
@app.get("/telegram/create/{telegram_id}")
def create_wallet(telegram_id: str):

    if telegram_id in users:
        return users[telegram_id]

    acct = Account.create()

    users[telegram_id] = {
        "address": acct.address,
        "private_key": acct.key.hex(),
        "balance": 0
    }

    return {
        "address": acct.address
    }

# check balance
@app.get("/telegram/balance/{telegram_id}")
def balance(telegram_id: str):

    user = users.get(telegram_id)

    if not user:
        return {"error": "wallet not found"}

    return {
        "address": user["address"],
        "balance": user["balance"]
    }

# tip another telegram user
@app.get("/telegram/tip/{from_id}/{to_id}/{amount}")
def tip(from_id: str, to_id: str, amount: float):

    if from_id not in users or to_id not in users:
        return {"error": "user not found"}

    if users[from_id]["balance"] < amount:
        return {"error": "insufficient balance"}

    users[from_id]["balance"] -= amount
    users[to_id]["balance"] += amount

    return {"status": "tip sent"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
