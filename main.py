from fastapi import FastAPI
import os
import uvicorn
from eth_account import Account

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/wallet/create")
def create_wallet():
    acct = Account.create()

    return {
        "address": acct.address,
        "private_key": acct.key.hex()
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
