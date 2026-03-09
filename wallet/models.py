from sqlalchemy import Column,Integer,String,Float
from .database import Base

class User(Base):

    __tablename__="users"

    id=Column(Integer,primary_key=True)
    telegram_id=Column(String)
    address=Column(String)
    private_key=Column(String)
    balance=Column(Float,default=0)


class Transaction(Base):

    __tablename__="transactions"

    id=Column(Integer,primary_key=True)
    user_id=Column(Integer)
    tx_hash=Column(String)
    amount=Column(Float)
    type=Column(String)
