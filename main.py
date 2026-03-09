from fastapi import FastAPI
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from eth_account import Account
from web3 import Web3
import os
import uvicorn

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///wallet.db")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

RPC = os.getenv("ETH_RPC","https://rpc.ankr.com/eth")
w3 = Web3(Web3.HTTPProvider(RPC))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String)
    address = Column(String)
    private_key = Column(String)
    balance = Column(Float, default=0)

Base.metadata.create_all(engine)

@app.get("/")
def home():
    return {"wallet":"running"}

@app.get("/dashboard")
def dashboard():
    return FileResponse("index.html")

@app.get("/user/create/{telegram_id}")
def create_user(telegram_id:str):

    db = Session()

    user = db.query(User).filter(User.telegram_id==telegram_id).first()

    if user:
        return {"address":user.address}

    acct = Account.create()

    user = User(
        telegram_id=telegram_id,
        address=acct.address,
        private_key=acct.key.hex(),
        balance=0
    )

    db.add(user)
    db.commit()

    return {"address":acct.address}

@app.get("/wallet/{telegram_id}")
def wallet(telegram_id:str):

    db = Session()
    user = db.query(User).filter(User.telegram_id==telegram_id).first()

    if not user:
        return {"error":"not found"}

    return {
        "address":user.address,
        "balance":user.balance
    }

@app.get("/withdraw/{telegram_id}/{to}/{amount}")
def withdraw(telegram_id:str,to:str,amount:float):

    db = Session()
    user = db.query(User).filter(User.telegram_id==telegram_id).first()

    acct = Account.from_key(user.private_key)

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
    port=int(os.environ.get("PORT",8000))
    uvicorn.run(app,host="0.0.0.0",port=port)
