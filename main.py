from fastapi import FastAPI
from fastapi.responses import FileResponse

from wallet.database import engine,Session
from wallet.models import User,Transaction,Base
from wallet.wallet_engine import create_wallet,send_eth

import uvicorn,os

app=FastAPI()

Base.metadata.create_all(engine)

@app.get("/")
def home():
    return {"wallet":"running"}

@app.get("/dashboard")
def dashboard():
    return FileResponse("index.html")

@app.get("/user/create/{telegram_id}")
def create_user(telegram_id:str):

    db=Session()

    user=db.query(User).filter(User.telegram_id==telegram_id).first()

    if user:
        return {"address":user.address}

    address,key=create_wallet()

    user=User(
        telegram_id=telegram_id,
        address=address,
        private_key=key
    )

    db.add(user)
    db.commit()

    return {"address":address}

@app.get("/wallet/{telegram_id}")
def wallet(telegram_id:str):

    db=Session()

    user=db.query(User).filter(User.telegram_id==telegram_id).first()

    return {
        "address":user.address,
        "balance":user.balance
    }

@app.get("/withdraw/{telegram_id}/{to}/{amount}")
def withdraw(telegram_id:str,to:str,amount:float):

    db=Session()

    user=db.query(User).filter(User.telegram_id==telegram_id).first()

    tx=send_eth(user.private_key,to,amount)

    return {"tx":tx}


if __name__=="__main__":

    port=int(os.environ.get("PORT",8000))

    uvicorn.run(app,host="0.0.0.0",port=port)
