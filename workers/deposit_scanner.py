from web3 import Web3
from wallet.database import Session
from wallet.models import User,Transaction
import time,os

RPC=os.getenv("ETH_RPC","https://rpc.ankr.com/eth")

w3=Web3(Web3.HTTPProvider(RPC))

last_block=w3.eth.block_number

while True:

    block=w3.eth.block_number

    if block>last_block:

        for i in range(last_block+1,block+1):

            b=w3.eth.get_block(i,full_transactions=True)

            for tx in b.transactions:

                db=Session()

                user=db.query(User).filter(User.address==tx["to"]).first()

                if user:

                    value=w3.from_wei(tx["value"],"ether")

                    user.balance+=float(value)

                    db.add(Transaction(
                        user_id=user.id,
                        tx_hash=tx["hash"].hex(),
                        amount=float(value),
                        type="deposit"
                    ))

                    db.commit()

        last_block=block

    time.sleep(5)
