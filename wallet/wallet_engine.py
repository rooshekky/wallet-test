from web3 import Web3
from eth_account import Account
import os

RPC=os.getenv("ETH_RPC","https://rpc.ankr.com/eth")

w3=Web3(Web3.HTTPProvider(RPC))

def create_wallet():

    acct=Account.create()

    return acct.address,acct.key.hex()


def send_eth(private_key,to,amount):

    acct=Account.from_key(private_key)

    tx={
        "to":to,
        "value":w3.to_wei(amount,"ether"),
        "gas":21000,
        "gasPrice":w3.eth.gas_price,
        "nonce":w3.eth.get_transaction_count(acct.address)
    }

    signed=acct.sign_transaction(tx)

    tx_hash=w3.eth.send_raw_transaction(signed.rawTransaction)

    return tx_hash.hex()
