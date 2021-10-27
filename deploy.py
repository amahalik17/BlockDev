from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

install_solc('0.6.0')

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile our solidity contracts

compiled_sol = compile_standard(
    {"language": "Solidity",
    "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
    "settings": {
        "outputSelection": {
            "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
        }
    },
    },
    solc_version="0.6.0",
)
#print(compiled_sol)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode to we can deploy
bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']

# get abi
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']
# print(abi)


# to connect to ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
chain_id = 1337
my_address = '0x292c748c80A32Fe55829C96764611E1ebA551e65'
private_key = os.getenv('PRIVATE_KEY')

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
#print(SimpleStorage)

# get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
#print(nonce)

# build, sign, send transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {'chainId':chain_id, 'from': my_address, 'nonce': nonce})

#print(transaction)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print('Deploying Contract...')

txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

print('Deployed! :)')

# contract address, and abi are needed
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

# calls simulate making the call and getting return value
# transacts actually make a state change
print(simple_storage.functions.retrieve().call())
print('Updating contract!')

store_transaction = simple_storage.functions.store(15).buildTransaction({
    "chainId": chain_id, "from": my_address, "nonce": nonce + 1})

signed_store_tx = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

tx_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print('Updated contract!')

print(simple_storage.functions.retrieve().call())

