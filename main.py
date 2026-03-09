from fastapi import FastAPI
from fastapi.responses import FileResponse
from eth_account import Account
from web3 import Web3
import uvicorn
import os

app = FastAPI()

RPC = os.getenv("ETH_RPC","https://rpc.ankr.com/eth")
w3 = Web3(Web3.HTTPProvider(RPC))

users = {}

@app.get("/")
def home():
    return {"status":"running"}

@app.get("/dashboard")
def dashboard():
    return FileResponse("index.html")

@app.get("/user/create/{telegram_id}")
def create_user(telegram_id:str):

    if telegram_id in users:
        return users[telegram_id]

    acct = Account.create()

    users[telegram_id] = {
        "address": acct.address,
        "private_key": acct.key.hex(),
        "balance": 0
    }

    return {"address":acct.address}

@app.get("/wallet/{telegram_id}")
def wallet(telegram_id:str):

    if telegram_id not in users:
        return {"error":"user not found"}

    return users[telegram_id]

@app.get("/withdraw/{telegram_id}/{to}/{amount}")
def withdraw(telegram_id:str,to:str,amount:float):

    user = users.get(telegram_id)

    acct = Account.from_key(user["private_key"])

    tx = {
        "to":to,
        "value":w3.to_wei(amount,"ether"),
        "gas":21000,
        "gasPrice":w3.eth.gas_price,
        "nonce":w3.eth.get_transaction_count(acct.address)
    }

    signed = acct.sign_transaction(tx)

    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

    return {"tx":tx_hash.hex()}


if __name__ == "__main__":
    port = int(os.environ.get("PORT",8000))
    uvicorn.run(app,host="0.0.0.0",port=port)
