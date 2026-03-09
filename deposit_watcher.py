import time
from web3 import Web3

RPC="https://rpc.ankr.com/eth"
w3=Web3(Web3.HTTPProvider(RPC))

last_block=w3.eth.block_number

while True:

    block=w3.eth.block_number

    if block>last_block:
        print("checking deposits...")

        last_block=block

    time.sleep(10)
